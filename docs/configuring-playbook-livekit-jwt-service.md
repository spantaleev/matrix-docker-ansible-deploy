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

To keep using only the deprecated transport, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
matrix_livekit_jwt_service_appservice_enabled: false
```

## Federated calls and trusted homeservers

Since LiveKit JWT Service 0.7.0, only users from homeservers listed in `matrix_livekit_jwt_service_environment_variable_livekit_full_access_homeservers_list` may publish audio, video, or screen shares on your SFU. The list defaults to your `matrix_domain`. Other federated users receive media here and publish on their own homeserver's SFU, using clients with multi-SFU support. See [upstream's explanation](https://github.com/element-hq/lk-jwt-service/issues/238#issuecomment-5709655222).

Current Element Call supports this in its `compatibility` mode using the existing JWT endpoint. Older clients, clients configured to use a single SFU, and callers without their own SFU may join but be unable to publish media.

With the [stable transport](#stable-matrixrtc-transport-synapse-only), requests arrive through your homeserver: your own users get full access. Remote users receive media here by default. To allow joined users from another trusted homeserver to publish on your SFU, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
matrix_livekit_jwt_service_environment_variable_livekit_remote_can_publish_homeservers_list_custom:
  - example.org
```

Use `'*'` to allow all joined remote users to publish. Room membership is checked for every relayed request, including subscribers. Any joined user can cause an SFU room to be created. The playbook keeps remote publishing opt-in; upstream otherwise enables it for everyone by default.

Keep `matrix_livekit_jwt_service_environment_variable_livekit_full_access_homeservers_list` limited to your own homeserver. Fronting multiple homeservers through this legacy setting (including `'*'`) is deprecated upstream. If you previously added other homeservers there, migrate clients to the stable transport and move the trusted server names to the remote-can-publish list above, then remove the old list overrides. This enables room membership checks for legacy requests too. Remote homeservers need their own MatrixRTC integration to relay requests; changing the list alone does not migrate older clients.

Standalone operation is also deprecated. Synapse installations use application-service mode by default. If you disabled it, remove that override when your clients are ready. Other homeserver implementations still need standalone mode until they support the application-service integration. Upstream has announced removal in a future version without a date or version number; plan that migration before upgrading to a release that removes it. See the [upstream deprecation notices](https://github.com/element-hq/lk-jwt-service/tree/v0.10.0#readme).

To temporarily retain the previous behavior while updating clients or arranging SFU access:

```yaml
matrix_livekit_jwt_service_version: 0.6.0
matrix_livekit_jwt_service_container_healthcheck_enabled: false
matrix_livekit_jwt_service_appservice_enabled: false
```

Remove these overrides when ready to upgrade. Version 0.6.0 cannot run as an application service, which disables the [stable transport](#stable-matrixrtc-transport-synapse-only). The healthcheck must remain disabled on 0.6.0 because it is broken in that image.

## Participant metadata permissions

Issued tokens deny participants permission to update their own name, metadata and attributes, following the upstream default since 0.10.0. If your clients need that permission, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
matrix_livekit_jwt_service_environment_variable_livekit_can_update_own_metadata: true
```

Data publishing follows media publishing permissions.
