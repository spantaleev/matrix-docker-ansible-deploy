# SPDX-FileCopyrightText: 2026 Slavi Pantaleev
#
# SPDX-License-Identifier: AGPL-3.0-or-later

"""A stand-in homeserver for Molecule scenarios.

Most components talk to a homeserver while starting up and exit if it is unreachable,
so a scenario cannot get them running without one. A real Synapse for every role would
dominate the run time and drag in Postgres, and the scenarios are not testing Synapse.

This answers the handful of endpoints components touch during startup, with the blandest
plausible response in each case. Deliberately permissive: an unknown path returns `{}` with
a 200 rather than a 404, because the goal is to get the component past its startup checks.

What it is NOT: an authentication check, a room state machine, or anything a scenario should
assert *about*. Assert on what the role rendered and what the component reports about itself.
Scenarios may supply a small static room-state fixture when startup requires it, but the stub
does not model state changes.
"""

import json
import os
import re
import sys
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, unquote, urlparse

SERVER_NAME = os.environ.get("STUB_SERVER_NAME", "molecule.local")
PORT = int(os.environ.get("STUB_PORT", "8008"))

# Rooms reported as already joined. Components that resolve a room mapping at startup
# (matrix-alertmanager-receiver, for one) fail if the rooms they were configured with
# are missing, so a scenario passes its own room IDs in.
JOINED_ROOMS = [r for r in os.environ.get("STUB_JOINED_ROOMS", "").split(",") if r]

USER_ID = os.environ.get("STUB_USER_ID", f"@stub:{SERVER_NAME}")
ROOM_STATE = json.loads(os.environ.get("STUB_ROOM_STATE", "[]"))

# Longest a /sync call is held open. Long-polling clients ask for a 30s timeout and
# immediately ask again when the call returns, so answering instantly spins them into a hot
# loop that eats the test machine. Honouring the requested timeout, capped here, keeps an
# idle bot idle.
SYNC_MAX_HOLD_SECONDS = 30


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def _send(self, payload, status=200):
        body = json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _route(self):
        parsed = urlparse(self.path)
        path = parsed.path

        # A client that syncs (every bot here does) needs a `next_batch` back or
        # the response will not deserialize, and it needs the call to block for
        # the timeout it asked for or it will hammer this stub. Nothing is ever
        # reported: an idle bot is what a scenario wants.
        if path.endswith("/sync"):
            requested_ms = parse_qs(parsed.query).get("timeout", ["0"])[0]
            try:
                hold = min(int(requested_ms) / 1000.0, SYNC_MAX_HOLD_SECONDS)
            except ValueError:
                hold = 0
            if hold > 0:
                time.sleep(hold)
            return {"next_batch": "molecule-stub-batch"}

        # Before the generic `/upload` below: this one is the end-to-end
        # encryption key upload, and the client insists on the key counts.
        if path.endswith("/keys/upload"):
            return {"one_time_key_counts": {}}

        # Media. A bot that sets its own avatar asks for the upload limits first
        # and refuses to proceed without them, then uploads and expects an MXC
        # URI back.
        if path.endswith("/media/config") or path.endswith("/media/v3/config"):
            return {"m.upload.size": 10485760}

        if path.endswith("/upload"):
            return {"content_uri": f"mxc://{SERVER_NAME}/molecule-stub-media"}

        # Sync filters are uploaded before the first sync and referenced by id.
        if path.endswith("/filter"):
            return {"filter_id": "molecule-stub-filter"}

        if path.endswith("/joined_rooms"):
            return {"joined_rooms": JOINED_ROOMS}

        if path.endswith("/whoami"):
            return {"user_id": USER_ID, "device_id": "STUBDEVICE"}

        if path.endswith("/versions"):
            return {
                "versions": ["v1.1", "v1.2", "v1.3", "v1.4", "v1.5", "v1.6"],
                "unstable_features": {},
            }

        if path.endswith("/capabilities"):
            return {"capabilities": {}}

        # Where bots authenticating with a username and password log in, rather than as an
        # appservice with a token. Matched loosely on purpose, because clients differ on the
        # API version prefix, and a login falling through to the catch-all `{}` below looks
        # to the client like bad credentials.
        if path.endswith("/login"):
            return {
                "user_id": USER_ID,
                "access_token": "stub_access_token",
                "device_id": "STUBDEVICE",
                "home_server": SERVER_NAME,
            }

        if path.endswith("/createRoom"):
            return {"room_id": f"!stub-room:{SERVER_NAME}"}

        join_match = re.search(r"/join/([^/]+)$", path)
        if join_match:
            return {"room_id": unquote(join_match.group(1))}

        if re.search(r"/rooms/[^/]+/join$", path) or path.endswith("/join"):
            return {"room_id": f"!stub-room:{SERVER_NAME}"}

        if "/send/" in path or "/state/" in path:
            return {"event_id": f"$stub-event:{SERVER_NAME}"}

        if path.endswith("/register"):
            return {
                "user_id": USER_ID,
                "access_token": "stub_access_token",
                "device_id": "STUBDEVICE",
                "home_server": SERVER_NAME,
            }

        if path.endswith("/profile") or "/profile/" in path:
            return {"displayname": "stub"}

        if path.startswith("/_matrix/key/"):
            return {"server_name": SERVER_NAME, "verify_keys": {}, "old_verify_keys": {}}

        if path.startswith("/.well-known/matrix/client"):
            return {"m.homeserver": {"base_url": f"http://{SERVER_NAME}:{PORT}"}}

        if path.startswith("/.well-known/matrix/server"):
            return {"m.server": f"{SERVER_NAME}:{PORT}"}

        if path.endswith("/health") or path.endswith("/_matrix/federation/v1/version"):
            return {"server": {"name": "molecule-stub", "version": "0"}}

        # Anything unrecognised: an empty object, so a component probing an endpoint
        # not listed here still gets past it.
        return {}

    def do_GET(self):
        path = urlparse(self.path).path

        if ROOM_STATE:
            if re.search(r"/rooms/[^/]+/state$", path):
                self._send(ROOM_STATE)
                return

            if "/account_data/" in path or re.search(
                r"/rooms/[^/]+/state/[^/]+(?:/[^/]+)?$", path
            ):
                self._send(
                    {
                        "errcode": "M_NOT_FOUND",
                        "error": "Molecule stub state not found",
                    },
                    status=404,
                )
                return

        self._send(self._route())

    def do_POST(self):
        length = int(self.headers.get("Content-Length") or 0)
        if length:
            self.rfile.read(length)
        self._send(self._route())

    def do_PUT(self):
        self.do_POST()

    def do_DELETE(self):
        self._send({})

    def log_message(self, fmt, *args):
        # Quiet by default. STUB_VERBOSE=1 when a scenario will not start and you need
        # to see what the component is actually asking for.
        if os.environ.get("STUB_VERBOSE"):
            sys.stderr.write("stub: " + (fmt % args) + "\n")


if __name__ == "__main__":
    ThreadingHTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
