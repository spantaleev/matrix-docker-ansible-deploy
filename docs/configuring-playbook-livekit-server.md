<!--
SPDX-FileCopyrightText: 2024 wjbeckett
SPDX-FileCopyrightText: 2024 - 2025 Slavi Pantaleev

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Setting up LiveKit Server (optional)

The playbook can install and configure [LiveKit Server](https://github.com/livekit/livekit) for you.

LiveKit Server is an open source project that provides scalable, multi-user conferencing based on WebRTC. It's designed to provide everything you need to build real-time video audio data capabilities in your applications.

💡 LiveKit Server is automatically installed and configured when either [Element Call](configuring-playbook-element-call.md) or the [Matrix RTC stack](configuring-playbook-matrix-rtc.md) is enabled, so you don't need to do anything extra.

The [Ansible role for LiveKit Server](https://github.com/mother-of-all-self-hosting/ansible-role-livekit-server) is developed and maintained by [the MASH (mother-of-all-self-hosting) project](https://github.com/mother-of-all-self-hosting). For details about configuring LiveKit Server, you can check them via:
- 🌐 [the role's documentation at the MASH project](https://github.com/mother-of-all-self-hosting/ansible-role-livekit-server/blob/main/docs/configuring-livekit-server.md) online
- 📁 `roles/galaxy/livekit-server/docs/configuring-livekit-server.md` locally, if you have [fetched the Ansible roles](installing.md#update-ansible-roles)

## Adjusting firewall rules

To ensure LiveKit Server functions correctly, the following firewall rules and port forwarding settings are required:

- `7881/tcp`: ICE/TCP

- `7882/udp`: ICE/UDP Mux

- `3479/udp`: TURN/UDP. Also see the [Limitations](#limitations) section below.

- `5350/tcp`: TURN/TCP. Also see the [Limitations](#limitations) section below.

💡 The suggestions above are inspired by the upstream [Ports and Firewall](https://docs.livekit.io/home/self-hosting/ports-firewall/) documentation based on how LiveKit is configured in the playbook. If you've using custom configuration for the LiveKit Server role, you may need to adjust the firewall rules accordingly.

## TURN TLS handling

When `matrix_playbook_reverse_proxy_type` is `playbook-managed-traefik` (which is the default for this playbook), TURN over TCP is terminated by Traefik and forwarded to LiveKit with `turn.external_tls = true`. In this playbook default, this mode is enabled automatically when SSL is enabled and TURN is enabled.

- The playbook installs a dedicated Traefik TCP entrypoint for TURN (`matrix-livekit-turn`) by default and binds it to `tcp/5350`.
- `livekit_server_config_turn_external_tls` is automatically enabled for this setup.
- Because Traefik handles TLS, LiveKit no longer needs certificate-file paths for TURN in this mode.

To opt out and keep TURN TLS termination in LiveKit itself, set:

```yml
livekit_server_config_turn_external_tls: false
```

In this playbook, certificate paths are managed automatically via `group_vars/matrix_servers` when certificate dumping is enabled.

If your setup uses `other-traefik-container` or [another reverse-proxy](./configuring-playbook-own-webserver.md), behavior is unchanged by default and still relies on certificates being available inside the container as before.

Deployments using `other-traefik-container` can opt into the same Traefik-terminated mode there, by setting:

```yml
livekit_server_config_turn_external_tls: true
livekit_server_container_labels_turn_traefik_enabled: true
livekit_server_container_labels_turn_traefik_entrypoints: "<your-livekit-turn-traffic-entrypoint>"
```

and configuring their own Traefik TCP entrypoint dedicated to LiveKit TURN traffic.

## Limitations

LiveKit Server's TURN listener behavior depends on where TLS is terminated:

- Direct LiveKit TURN listeners (`livekit_server_config_turn_external_tls: false`) still use IPv4-only sockets for `3479/udp` and `5350/tcp`, so IPv6 connectivity to these endpoints is not possible.
- With [TURN TLS handling](#turn-tls-handling) (`livekit_server_config_turn_external_tls: true`), the playbook's dedicated `matrix-livekit-turn` TCP entrypoint can still listen on both IPv4 and IPv6. Traefik then forwards TURN/TCP to LiveKit.

It appears that LiveKit Server intentionally only listens on `udp4` and `tcp4` in direct mode, as seen [here](https://github.com/livekit/livekit/blob/154b4d26b769c68a03c096124094b97bf61a996f/pkg/service/turn.go#L128) and [here](https://github.com/livekit/livekit/blob/154b4d26b769c68a03c096124094b97bf61a996f/pkg/service/turn.go#L92).
