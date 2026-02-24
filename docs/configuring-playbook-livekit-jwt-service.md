<!--
SPDX-FileCopyrightText: 2025 Slavi Pantaleev

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Setting up LiveKit JWT Service (optional)

The playbook can install and configure [LiveKit JWT Service](https://github.com/element-hq/lk-jwt-service/) for you.

This is a helper component which is part of the [Matrix RTC stack](configuring-playbook-matrix-rtc.md) that allows [Element Call](configuring-playbook-element-call.md) to integrate with [LiveKit Server](configuring-playbook-livekit-server.md).

💡 LiveKit JWT Service is automatically installed and configured when either [Element Call](configuring-playbook-element-call.md) or the [Matrix RTC stack](configuring-playbook-matrix-rtc.md) is enabled, so you don't need to do anything extra.

Take a look at:

- `roles/custom/matrix-livekit-jwt-service/defaults/main.yml` for some variables that you can customize via your `vars.yml` file
- `roles/custom/matrix-livekit-jwt-service/templates/env.j2` for the component's default configuration.

## Using with an external nginx reverse-proxy

If you use nginx (running on a separate host or outside Docker) to reverse-proxy the LiveKit JWT Service, the location block **must include a trailing slash** after the path prefix.

The service runs on `/livekit-jwt-service` by default (set via `matrix_livekit_jwt_service_path_prefix`). nginx rewrites paths using the `proxy_pass` URI via string replacement: without the trailing slash, `location ^~ /livekit-jwt-service` combined with `proxy_pass http://BACKEND_HOST:PORT/;` replaces `/livekit-jwt-service` with `/`, turning `/livekit-jwt-service/get_token` into `//get_token` (double slash). Go's `net/http` server then issues a 301 redirect to normalize the path, which prevents Element Call from obtaining a LiveKit JWT token and causes calls to connect at the signaling level but without audio/video.

**Correct nginx configuration:**

```nginx
# Note the trailing slash in location — required to avoid the double-slash path bug
location ^~ /livekit-jwt-service/ {
    proxy_pass http://MATRIX_SERVER_HOST:8091/;
    proxy_set_header X-Forwarded-For $remote_addr;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
}
```

Similarly, when reverse-proxying the LiveKit Server's HTTP/WebSocket port:

```nginx
# Note the trailing slash in location — required for correct path rewriting
location ^~ /livekit-server/ {
    proxy_pass http://MATRIX_SERVER_HOST:7880/;
    proxy_set_header Host $host;
    proxy_set_header X-Forwarded-For $remote_addr;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_read_timeout 3600s;
    proxy_send_timeout 3600s;
}
```

The playbook's built-in Traefik reverse-proxy handles path stripping correctly using its `stripprefix` middleware, so this only affects setups using an external nginx.
