# SPDX-FileCopyrightText: 2026 Slavi Pantaleev
#
# SPDX-License-Identifier: AGPL-3.0-or-later

"""Exercise local Matrix registration and report observations to verify.yml."""

import json
import secrets
import sys
from urllib.error import HTTPError
from urllib.parse import quote
from urllib.request import Request, urlopen


base_url, registration_token = sys.argv[1:]


def request(path, body=None, access_token=None):
    headers = {"Content-Type": "application/json"}
    if access_token:
        headers["Authorization"] = f"Bearer {access_token}"
    data = json.dumps(body).encode() if body is not None else None
    req = Request(base_url + path, data=data, headers=headers)
    try:
        response = urlopen(req, timeout=15)
    except HTTPError as error:
        response = error
    with response:
        return {"status": response.status, "body": json.load(response)}


# A fresh localpart lets `molecule verify` run repeatedly against the same database.
username = "alice_" + secrets.token_hex(6)
credentials = {"username": username, "password": secrets.token_urlsafe(24)}
result = {"username": username}
result["challenge"] = request("/_matrix/client/v3/register", credentials)
session = result["challenge"]["body"].get("session", "")
auth = {"type": "m.login.registration_token", "session": session}
result["bad_token"] = request(
    "/_matrix/client/v3/register",
    {**credentials, "auth": {**auth, "token": registration_token + "-invalid"}},
)
registration = request(
    "/_matrix/client/v3/register",
    {**credentials, "auth": {**auth, "token": registration_token}},
)
access_token = registration["body"].pop("access_token", None)
result["registration"] = registration
if access_token:
    result["whoami"] = request("/_matrix/client/v3/account/whoami", access_token=access_token)
    user_id = quote(registration["body"]["user_id"], safe="")
    result["profile"] = request(f"/_matrix/client/v3/profile/{user_id}/displayname")
    result["media"] = request("/_matrix/client/v1/media/config", access_token=access_token)
result["well_known"] = request("/.well-known/matrix/client")
print(json.dumps(result))
