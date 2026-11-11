# SPDX-FileCopyrightText: 2026 Slavi Pantaleev
#
# SPDX-License-Identifier: AGPL-3.0-or-later

"""Small HTTPS Matrix fixture for Molecule.

It serves the federation OpenID userinfo endpoint and, playing the homeserver of the
application service mode, the MSC4502 room membership endpoint.
"""

import json
import os
import ssl
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, unquote, urlparse


KNOWN_TOKENS = {
    "known-openid-token": "@alice:matrix-openid-fixture:8443",
    "full-access-openid-token": "@bob:full-access.molecule.local:8443",
}
REQUESTS = []
IS_JOINED_REQUESTS = []

AS_TOKEN = os.environ["MOLECULE_AS_TOKEN"]
IS_JOINED_PREFIX = "/_matrix/client/unstable/io.element.msc4502/rooms/"
JOINED_MEMBERS = {
    "!call-room:molecule.local": {"@carol:homeserver.molecule.local"},
}


class OpenIDHandler(BaseHTTPRequestHandler):
    def send_json(self, status, document):
        body = json.dumps(document, separators=(",", ":")).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):  # noqa: N802 - BaseHTTPRequestHandler API
        parsed = urlparse(self.path)
        if parsed.path == "/_molecule/requests":
            self.send_json(200, {"requests": REQUESTS, "is_joined_requests": IS_JOINED_REQUESTS})
            return

        if parsed.path.startswith(IS_JOINED_PREFIX) and parsed.path.endswith("/is_joined"):
            room_id = unquote(parsed.path[len(IS_JOINED_PREFIX):-len("/is_joined")])
            mxid = parse_qs(parsed.query).get("mxid", [""])[0]
            authorized = self.headers.get("Authorization", "") == "Bearer " + AS_TOKEN
            IS_JOINED_REQUESTS.append({"room_id": room_id, "mxid": mxid, "authorized": authorized})
            if not authorized:
                self.send_json(401, {"errcode": "M_UNKNOWN_TOKEN"})
                return
            self.send_json(200, {"joined": mxid in JOINED_MEMBERS.get(room_id, set())})
            return

        if parsed.path != "/_matrix/federation/v1/openid/userinfo":
            self.send_json(404, {"errcode": "M_NOT_FOUND"})
            return

        token = parse_qs(parsed.query).get("access_token", [""])[0]
        REQUESTS.append({"path": parsed.path, "access_token": token})
        if token in KNOWN_TOKENS:
            self.send_json(200, {"sub": KNOWN_TOKENS[token]})
            return

        self.send_json(401, {"errcode": "M_UNAUTHORIZED", "error": "unknown token"})

    def log_message(self, message, *args):
        print("openid-fixture:", message % args, flush=True)


server = ThreadingHTTPServer(("0.0.0.0", 8443), OpenIDHandler)
tls_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
tls_context.load_cert_chain("/fixture/cert.pem", "/fixture/key.pem")
server.socket = tls_context.wrap_socket(server.socket, server_side=True)
server.serve_forever()
