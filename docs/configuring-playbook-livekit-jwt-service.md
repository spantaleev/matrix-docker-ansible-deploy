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
