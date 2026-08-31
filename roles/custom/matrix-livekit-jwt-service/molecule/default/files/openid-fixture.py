# SPDX-FileCopyrightText: 2026 Slavi Pantaleev
#
# SPDX-License-Identifier: AGPL-3.0-or-later

"""Small HTTPS Matrix federation OpenID userinfo fixture for Molecule."""

import json
import ssl
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse


KNOWN_TOKEN = "known-openid-token"
KNOWN_SUBJECT = "@alice:matrix-openid-fixture:8443"
REQUESTS = []


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
            self.send_json(200, {"requests": REQUESTS})
            return

        if parsed.path != "/_matrix/federation/v1/openid/userinfo":
            self.send_json(404, {"errcode": "M_NOT_FOUND"})
            return

        token = parse_qs(parsed.query).get("access_token", [""])[0]
        REQUESTS.append({"path": parsed.path, "access_token": token})
        if token == KNOWN_TOKEN:
            self.send_json(200, {"sub": KNOWN_SUBJECT})
            return

        self.send_json(401, {"errcode": "M_UNAUTHORIZED", "error": "unknown token"})

    def log_message(self, message, *args):
        print("openid-fixture:", message % args, flush=True)


server = ThreadingHTTPServer(("0.0.0.0", 8443), OpenIDHandler)
tls_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
tls_context.load_cert_chain("/fixture/cert.pem", "/fixture/key.pem")
server.socket = tls_context.wrap_socket(server.socket, server_side=True)
server.serve_forever()
