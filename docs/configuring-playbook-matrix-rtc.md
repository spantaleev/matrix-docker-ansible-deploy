<!--
SPDX-FileCopyrightText: 2024 wjbeckett
SPDX-FileCopyrightText: 2024 - 2025 Slavi Pantaleev

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Setting up the Matrix RTC stack (optional)

The playbook can install and configure the Matrix RTC (Real-Time Communication) stack.

The Matrix RTC stack is a set of supporting components ([LiveKit Server](configuring-playbook-livekit-server.md) and [LiveKit JWT Service](configuring-playbook-livekit-jwt-service.md)) that allow the new [Element Call](configuring-playbook-element-call.md) audio/video calls to function.

💡 If you only plan on doing audio/video calls via Matrix client (which typically embed the Element Call frontend UI within them), you only need to install the Matrix RTC stack and don't necessarily need to install [Element Call](configuring-playbook-element-call.md). See the [Decide between Element Call vs just the Matrix RTC stack](configuring-playbook-element-call.md#decide-between-element-call-vs-just-the-matrix-rtc-stack) section of the [Element Call documentation](configuring-playbook-element-call.md) for more details.

## Prerequisites

- A [Synapse](configuring-playbook-synapse.md) homeserver (see the warning below)
- Various experimental features for the Synapse homeserver which Element Call [requires](https://github.com/element-hq/element-call/blob/93ae2aed9841e0b066d515c56bd4c122d2b591b2/docs/self-hosting.md#a-matrix-homeserver) (automatically done when Element Call is enabled)
- A [LiveKit Server](configuring-playbook-livekit-server.md) (automatically installed when [Element Call or the Matrix RTC stack is enabled](#decide-between-element-call-vs-just-the-matrix-rtc-stack))
- The [LiveKit JWT Service](configuring-playbook-livekit-jwt-service.md) (automatically installed when [Element Call or the Matrix RTC stack is enabled](#decide-between-element-call-vs-just-the-matrix-rtc-stack))
- A client compatible with Element Call. As of 2025-03-15, that's just [Element Web](configuring-playbook-client-element-web.md) and the Element X mobile clients (iOS and Android).

> [!WARNING]
>  Because Element Call [requires](https://github.com/element-hq/element-call/blob/93ae2aed9841e0b066d515c56bd4c122d2b591b2/docs/self-hosting.md#a-matrix-homeserver) a few experimental features in the Matrix protocol, it's **very likely that it only works with the Synapse homeserver**.

## Adjusting the playbook configuration

Add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
# Enable the Matrix RTC stack.
# This provides all supporting services for Element Call, without the Element Call frontend.
matrix_rtc_enabled: true
```

## Adjusting firewall rules

In addition to the HTTP/HTTPS ports (which you've already exposed as per the [prerequisites](prerequisites.md) document), you'll also need to open ports required by [LiveKit Server](configuring-playbook-livekit-server.md) as described in its own [Adjusting firewall rules](configuring-playbook-livekit-server.md#adjusting-firewall-rules) section.

## Installing

After configuring the playbook and potentially [adjusting your DNS records](#adjusting-dns-records) and [adjusting firewall rules](#adjusting-firewall-rules), run the playbook with [playbook tags](playbook-tags.md) as below:

<!-- NOTE: let this conservative command run (instead of install-all) to make it clear that failure of the command means something is clearly broken. -->
```sh
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start
```

The shortcut commands with the [`just` program](just.md) are also available: `just install-all` or `just setup-all`

`just install-all` is useful for maintaining your setup quickly ([2x-5x faster](../CHANGELOG.md#2x-5x-performance-improvements-in-playbook-runtime) than `just setup-all`) when its components remain unchanged. If you adjust your `vars.yml` to remove other components, you'd need to run `just setup-all`, or these components will still remain installed. Note these shortcuts run the `ensure-matrix-users-created` tag too.

## Usage

Once installed, Matrix clients which support Element Call (like [Element Web](configuring-playbook-client-element-web.md) and Element X on mobile (iOS and Android)) will automatically use the Matrix RTC stack.

These clients typically embed the Element Call frontend UI within them, so installing [Element Call](configuring-playbook-element-call.md) is only necessary if you'd like to use it standalone - directly via a browser.
