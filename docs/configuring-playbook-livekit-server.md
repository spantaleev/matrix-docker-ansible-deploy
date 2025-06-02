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

## Limitations

For some reason, LiveKit Server's TURN ports (`3479/udp` and `5350/tcp`) are not reachable over IPv6 regardless of whether you've [enabled IPv6](./configuring-ipv6.md) for your server.

It seems like LiveKit Server intentionally only listens on `udp4` and `tcp4` as seen [here](https://github.com/livekit/livekit/blob/154b4d26b769c68a03c096124094b97bf61a996f/pkg/service/turn.go#L128) and [here](https://github.com/livekit/livekit/blob/154b4d26b769c68a03c096124094b97bf61a996f/pkg/service/turn.go#L92).
