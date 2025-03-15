<!--
SPDX-FileCopyrightText: 2024 wjbeckett
SPDX-FileCopyrightText: 2024 - 2025 Slavi Pantaleev

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Setting up LiveKit Server (optional)

The playbook can install and configure [LiveKit Server](https://github.com/livekit/livekit) for you.

LiveKit Server is an open source project that provides scalable, multi-user conferencing based on WebRTC. It's designed to provide everything you need to build real-time video audio data capabilities in your applications.

💡 LiveKit Server is automatically installed and configured when [Element Call](configuring-playbook-element-call.md) is enabled, so you don't need to do anything extra.

The [Ansible role for LiveKit Server](https://github.com/mother-of-all-self-hosting/ansible-role-livekit-server) is developed and maintained by [the MASH (mother-of-all-self-hosting) project](https://github.com/mother-of-all-self-hosting). For details about configuring LiveKit Server, you can check them via:
- 🌐 [the role's documentation at the MASH project](https://github.com/mother-of-all-self-hosting/ansible-role-livekit-server/blob/main/docs/configuring-livekit-server.md) online
- 📁 `roles/galaxy/livekit-server/docs/configuring-livekit-server.md` locally, if you have [fetched the Ansible roles](installing.md#update-ansible-roles)

## Adjusting firewall rules

To ensure LiveKit Server functions correctly, the following firewall rules and port forwarding settings are required:

- `7881/tcp`: ICE/TCP

- `7882/udp`: ICE/UDP Mux

💡 The suggestions above are inspired by the upstream [Ports and Firewall](https://docs.livekit.io/home/self-hosting/ports-firewall/) documentation based on how LiveKit is configured in the playbook. If you've using custom configuration for the LiveKit Server role, you may need to adjust the firewall rules accordingly.
