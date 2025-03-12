<!--
SPDX-FileCopyrightText: 2024 wjbeckett
SPDX-FileCopyrightText: 2024 - 2025 Slavi Pantaleev

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Setting up Element Call (optional)

The playbook can install and configure [Element Call](https://github.com/element-hq/element-call) for you.

Element Call is a native Matrix video conferencing application developed by [Element](https://element.io), designed for secure, scalable, privacy-respecting, and decentralized video and voice calls over the Matrix protocol. Built on MatrixRTC ([MSC4143](https://github.com/matrix-org/matrix-spec-proposals/pull/4143)), it utilizes [MSC4195](https://github.com/hughns/matrix-spec-proposals/blob/hughns/matrixrtc-livekit/proposals/4195-matrixrtc-livekit.md) with [LiveKit](configuring-playbook-livekit-server.md) as its backend.

See the project's [documentation](https://github.com/element-hq/element-call) to learn more.

> [!WARNING]
>  Because Element Call [requires](https://github.com/element-hq/element-call/blob/93ae2aed9841e0b066d515c56bd4c122d2b591b2/docs/self-hosting.md#a-matrix-homeserver) a few experimental features in the Matrix protocol, it's <strong>very likely that it only works with the Synapse homeserver</strong>.

## Decide on a domain and path

By default, Element Call is configured to be served on the `call.element.DOMAIN` domain.

If you'd like to run Element Call on another hostname or path, use the `matrix_element_call_hostname` variable. A `matrix_element_call_path_prefix` variable is also available to set a path prefix for the Element Call service, but Element Call does not support running under a sub-path yet.

## Adjusting DNS records

If you've changed the default hostname, **you may need to adjust your DNS** records accordingly to point to the correct server.

Ensure that the following DNS names have a public IP/FQDN:
- `call.element.example.com`
- `livekit.example.com`

## Adjusting firewall rules

All services are exposed via HTTP/HTTPS as per usual, ports for which you've already opened as described in the [prerequisites](prerequisites.md) document.

In addition to that, you'll also need to open ports required by LiveKit Server as described in its own [Adjusting firewall rules](configuring-playbook-livekit-server.md#adjusting-firewall-rules) section.

## Adjusting the playbook configuration

Add the following configuration to your `inventory/host_vars/matrix.DOMAIN/vars.yml` file:

```yaml
matrix_element_call_enabled: true
```

💡 Enabling Element Call will automatically:

- enable the [LiveKit JWT Service](configuring-playbook-livekit-jwt-service.md) and [Livekit Server](configuring-playbook-livekit-server.md) services

- enable a few experimental features in Synapse that Element Call [requires](https://github.com/element-hq/element-call/blob/93ae2aed9841e0b066d515c56bd4c122d2b591b2/docs/self-hosting.md#a-matrix-homeserver)

## Installing

After configuring the playbook and potentially [adjusting your DNS records](#adjusting-dns-records) and [adjusting firewall rules](#adjusting-firewall-rules), run the [installation](installing.md) command: `just install-all` or `just setup-all`

## Usage

Once installed, Element Call integrates seamlessly with Matrix clients like [Element Web](configuring-playbook-client-element-web.md).