<!--
SPDX-FileCopyrightText: 2025 - 2026 Slavi Pantaleev

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Setting up LiveKit JWT Service (optional)

The playbook can install and configure [LiveKit JWT Service](https://github.com/element-hq/lk-jwt-service/) for you.

This is a helper component which is part of the [Matrix RTC stack](configuring-playbook-matrix-rtc.md) that allows [Element Call](configuring-playbook-element-call.md) to integrate with [LiveKit Server](configuring-playbook-livekit-server.md).

💡 LiveKit JWT Service is automatically installed and configured when either [Element Call](configuring-playbook-element-call.md) or the [Matrix RTC stack](configuring-playbook-matrix-rtc.md) is enabled, so you don't need to do anything extra.

Take a look at:

- `roles/custom/matrix-livekit-jwt-service/defaults/main.yml` for some variables that you can customize via your `vars.yml` file
- `roles/custom/matrix-livekit-jwt-service/templates/env.j2` for the component's default configuration.

## Stable MatrixRTC transport (Synapse only)

When [Synapse](configuring-playbook-synapse.md) is your homeserver, the playbook also registers LiveKit JWT Service as a Synapse application service. This enables the stable MatrixRTC LiveKit transport (`m.livekit`): clients request call tokens through your homeserver, which forwards these requests to LiveKit JWT Service.

Synapse advertises both the stable transport and the deprecated `livekit` one, so older clients can keep talking to LiveKit JWT Service directly.

The application service covers all local users (non-exclusively). LiveKit JWT Service uses it to check that callers are joined to the room, and to manage delayed leave events on their behalf. Running as an application service also changes the existing endpoints: users who aren't joined to the room no longer get tokens, as long as `matrix_livekit_jwt_service_environment_variable_livekit_full_access_homeservers_list` only contains your own homeserver.

If you install services selectively (e.g. `just install-service synapse`), run a full installation (`just install-all` or `just setup-all`) the first time, so that both Synapse and LiveKit JWT Service pick up the registration.

Standalone mode is deprecated upstream and will be removed in a future release; no removal version or date has been announced. Keep the application service enabled on Synapse. Other supported homeservers currently use standalone mode because they do not support the required application-service integration; migrating to Synapse enables the supported transport. Older clients can continue using the legacy endpoints while the application service is enabled.

## Federated calls and trusted homeservers

Since LiveKit JWT Service 0.7.0, only users from homeservers listed in `matrix_livekit_jwt_service_environment_variable_livekit_full_access_homeservers_list` may publish audio, video, or screen shares on your SFU. The list defaults to your `matrix_domain`. Other federated users receive media here and publish on their own homeserver's SFU, using clients with multi-SFU support. See [upstream's explanation](https://github.com/element-hq/lk-jwt-service/issues/238#issuecomment-5709655222).

Current Element Call supports this in its `compatibility` mode using the existing JWT endpoint. Older clients, clients configured to use a single SFU, and callers without their own SFU may join but be unable to publish media.

With the [stable transport](#stable-matrixrtc-transport-synapse-only), your own users get full access. Remote users remain receive-only by default in this playbook. To let users of a trusted homeserver publish through federated token requests, add its Matrix server name to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
matrix_livekit_jwt_service_environment_variable_livekit_remote_can_publish_homeservers_list_custom:
  - example.org
```

Use `'*'` in this list to allow publishing from all remote homeservers, as recommended by MatrixRTC and enabled by default upstream since 0.10.0. The playbook keeps the previous receive-only default to avoid silently expanding publishing permissions. Room membership is verified for every relayed request. Even receive-only users can trigger SFU room creation through this transport, provided the membership checks pass.

The `matrix_livekit_jwt_service_environment_variable_livekit_full_access_homeservers_list_custom` setting only affects the legacy endpoints. Allowing multiple homeservers or `'*'` there is deprecated upstream, with no removal version or date announced. Remove those entries and use the stable transport with the remote publishing list above instead. Unlike the stable transport, legacy full access for multiple homeservers permits publishing and room creation without a room-membership check.

## Participant metadata and data publishing

LiveKit JWT Service disables participants' ability to update their own name, metadata and attributes by default. If your clients require that permission, enable it explicitly:

```yaml
matrix_livekit_jwt_service_environment_variables_extension: |
  LIVEKIT_CAN_UPDATE_OWN_METADATA=true
```

Data publishing follows the media publishing permission: receive-only participants cannot publish data either.
