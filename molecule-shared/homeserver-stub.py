# SPDX-FileCopyrightText: 2026 Slavi Pantaleev
#
# SPDX-License-Identifier: AGPL-3.0-or-later

"""A stand-in homeserver for Molecule scenarios.

Most components in this playbook talk to a homeserver while starting up and
exit if it is unreachable, so a scenario cannot get them running without one.
Standing up a real Synapse for every role would dominate the run time and drag
in Postgres, and the scenarios are not testing Synapse - they are testing that
the role's configuration reaches the component and that it starts.

So this answers the handful of endpoints components touch during startup, with
the blandest plausible response in each case. It is deliberately permissive: an
unknown path returns `{}` with a 200 rather than a 404, because the goal is to
get the component past its startup checks, not to model the Matrix spec.

What it is NOT: an authentication check, a room state machine, or anything a
scenario should assert *about*. Assert on what the role rendered and on what the
component reports about itself. If a scenario starts needing this stub to behave
like a real homeserver, that scenario has outgrown what these tests are for.
"""

import json
import os
import re
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

SERVER_NAME = os.environ.get("STUB_SERVER_NAME", "molecule.local")
PORT = int(os.environ.get("STUB_PORT", "8008"))

# Rooms reported as already joined. Components that resolve a room mapping at
# startup (matrix-alertmanager-receiver, for one) fail if the rooms they were
# configured with are missing, so a scenario passes its own room IDs in.
JOINED_ROOMS = [r for r in os.environ.get("STUB_JOINED_ROOMS", "").split(",") if r]

USER_ID = os.environ.get("STUB_USER_ID", f"@stub:{SERVER_NAME}")


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
        path = self.path.split("?", 1)[0]

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

        if path.endswith("/_matrix/client/v3/login"):
            return {
                "user_id": USER_ID,
                "access_token": "stub_access_token",
                "device_id": "STUBDEVICE",
                "home_server": SERVER_NAME,
            }

        if path.endswith("/createRoom"):
            return {"room_id": f"!stub-room:{SERVER_NAME}"}

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

        # Anything unrecognised: an empty object, so a component doing a startup
        # probe of an endpoint not listed here still gets past it.
        return {}

    def do_GET(self):
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
        # Quiet by default; STUB_VERBOSE=1 when a scenario will not start and you
        # need to see what the component is actually asking for.
        if os.environ.get("STUB_VERBOSE"):
            sys.stderr.write("stub: " + (fmt % args) + "\n")


if __name__ == "__main__":
    ThreadingHTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
