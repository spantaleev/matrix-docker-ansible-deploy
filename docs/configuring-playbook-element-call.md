<!--
SPDX-FileCopyrightText: 2024 wjbeckett
SPDX-FileCopyrightText: 2024 - 2025 Slavi Pantaleev

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Setting up Element Call (optional)

The playbook can install and configure [Element Call](https://github.com/element-hq/element-call) and its supporting components that are part of the [Matrix RTC stack](configuring-playbook-matrix-rtc.md).

Element Call is a native Matrix video conferencing application developed by [Element](https://element.io), designed for secure, scalable, privacy-respecting, and decentralized video and voice calls over the Matrix protocol. Built on MatrixRTC ([MSC4143](https://github.com/matrix-org/matrix-spec-proposals/pull/4143)), it utilizes [MSC4195](https://github.com/hughns/matrix-spec-proposals/blob/hughns/matrixrtc-livekit/proposals/4195-matrixrtc-livekit.md) with [LiveKit Server](configuring-playbook-livekit-server.md) as its backend.

See the project's [documentation](https://github.com/element-hq/element-call) to learn more.

## Prerequisites

- A [Synapse](configuring-playbook-synapse.md) homeserver (see the warning below)
- The [Matrix RTC (Real-Time Communication) stack](configuring-playbook-matrix-rtc.md) (automatically done when Element Call is enabled)
- A client compatible with Element Call. As of 2025-03-15, that's just [Element Web](configuring-playbook-client-element-web.md) and the Element X mobile clients (iOS and Android).
- (Optional) Guest accounts being enabled for your Matrix server, if you'd like guests to be able to use Element Call. See [Allowing guests to use Element Call](#allowing-guests-to-use-element-call-optional)

> [!WARNING]
>  Because Element Call [requires](https://github.com/element-hq/element-call/blob/93ae2aed9841e0b066d515c56bd4c122d2b591b2/docs/self-hosting.md#a-matrix-homeserver) a few experimental features in the Matrix protocol, it's **very likely that it only works with the Synapse homeserver**.

## Decide between Element Call vs just the Matrix RTC stack

All clients that can currently use Element Call (Element Web and Element X on mobile) already embed the Element Call frontend within them.
These **clients will use their own embedded Element Call frontend**, so **self-hosting the Element Call frontend by the playbook is largely unnecessary**.

💡 A reason you may wish to continue installing the Element Call frontend (despite Matrix clients not making use of it), is if you need to use it standalone - directly via a browser (without a Matrix client). Note that unless you [allow guest accounts to use Element Call](#allowing-guests-to-use-element-call-optional), you will still need a Matrix user account **on the same homeserver** to be able to use Element Call.

The playbook makes a distinction between enabling Element Call (`matrix_element_call_enabled`) and enabling the Matrix RTC Stack (`matrix_rtc_enabled`). Enabling Element Call automatically enables the Matrix RTC stack. Because installing the Element Call frontend is now unnecessary, **we recommend only installing the Matrix RTC stack, without the Element Call frontend**.

| Description / Variable | Element Call frontend | [LiveKit Server](configuring-playbook-livekit-server.md) | [LiveKit JWT Service](configuring-playbook-livekit-jwt-service.md) |
|------------------------|-----------------------|----------------|---------------------|
| Description | Static website that provides the Element Call UI (but often embedded by clients) | Scalable, multi-user conferencing solution based on WebRTC | A helper component that allows Element Call to integrate with LiveKit Server |
| Required for Element Call to function | No | Yes | Yes |
| `matrix_element_call_enabled` | ✅ Installed | ✅ Installed | ✅ Installed |
| `matrix_rtc_enabled` | ❌ Not Installed, but usually unnecessary | ✅ Installed | ✅ Installed |

All documentation below assumes that you've decided to install Element Call and not just the Matrix RTC stack.

## Decide on a domain and path

By default, the Element Call frontend is configured to be served on the `call.element.example.com` domain.

If you'd like to run Element Call on another hostname, see the [Adjusting the Element Call URL](#adjusting-the-element-call-url-optional) section below.

## Adjusting DNS records

By default, this playbook installs Element Call on the `call.element.` subdomain (`call.element.example.com`) and requires you to create a `CNAME` record for `call.element`, which targets `matrix.example.com`.

When setting these values, replace `example.com` with your own.

All dependency services for Element Call ([LiveKit Server](configuring-playbook-livekit-server.md) and [Livekit JWT Service](configuring-playbook-livekit-jwt-service.md)) are installed and configured automatically by the playbook. By default, these services are installed on subpaths on the `matrix.` domain (e.g. `/livekit-server`, `/livekit-jwt-service`), so no DNS record adjustments are required for them.

## Adjusting firewall rules

In addition to the HTTP/HTTPS ports (which you've already exposed as per the [prerequisites](prerequisites.md) document), you'll also need to open ports required by [LiveKit Server](configuring-playbook-livekit-server.md) as described in its own [Adjusting firewall rules](configuring-playbook-livekit-server.md#adjusting-firewall-rules) section.

## Adjusting the playbook configuration

Add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
# Enable the Element Call frontend UI to allow standalone use of Element Call.
# Enabling this also auto-enables the Matrix RTC stack.
matrix_element_call_enabled: true
```

### Adjusting the Element Call URL (optional)

By tweaking the `matrix_element_call_hostname` variable, you can easily make the service available at a **different hostname** than the default one.

Example additional configuration for your `vars.yml` file:

```yaml
matrix_element_call_hostname: element-call.example.com
```

> [!WARNING]
> A `matrix_element_call_path_prefix` variable is also available and mean to let you configure a path prefix for the Element Call service, but [Element Call does not support running under a sub-path yet](https://github.com/element-hq/element-call/issues/3084).

### Allowing guests to use Element Call (optional)

By default, Element Call can only be used by people having accounts on your Matrix server.

If you'd like guests to be able to use Element Call as well, you need to enable guest accounts support for your homeserver.

> [!WARNING]
> Enabling guest accounts means that your homeserver's user database may get polluted with guest account signups (potentially made by bots).
> Guest accounts should be limited in what (damage) they can do to your server and the rest of the Matrix ecosystem, but it's better to not enable them unless necessary.

For [Synapse](configuring-playbook-synapse.md) (the default homeserver implementation), the configuration is like this:

```yml
matrix_synapse_allow_guest_access: true
```

For [Dendrite](configuring-playbook-dendrite.md), the configuration is like this:

```yml
matrix_dendrite_guests_disabled: false
```

## Installing

After configuring the playbook and potentially [adjusting your DNS records](#adjusting-dns-records) and [adjusting firewall rules](#adjusting-firewall-rules), run the playbook with [playbook tags](playbook-tags.md) as below:

<!-- NOTE: let this conservative command run (instead of install-all) to make it clear that failure of the command means something is clearly broken. -->
```sh
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start
```

The shortcut commands with the [`just` program](just.md) are also available: `just install-all` or `just setup-all`

`just install-all` is useful for maintaining your setup quickly ([2x-5x faster](../CHANGELOG.md#2x-5x-performance-improvements-in-playbook-runtime) than `just setup-all`) when its components remain unchanged. If you adjust your `vars.yml` to remove other components, you'd need to run `just setup-all`, or these components will still remain installed. Note these shortcuts run the `ensure-matrix-users-created` tag too.

## Usage

Once installed, Element Call integrates seamlessly with Matrix clients like [Element Web](configuring-playbook-client-element-web.md) and Element X on mobile (iOS and Android).
