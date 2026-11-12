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

Standalone operation is [deprecated upstream](https://github.com/element-hq/lk-jwt-service/blob/v0.10.0/README.md#-when-to-use), with removal planned for a future version and no announced date. Synapse deployments already use the application service by default. Remove any `matrix_livekit_jwt_service_appservice_enabled: false` override and run a full installation to migrate. Other homeservers need support for MSC4502 and MSC4512 before they can migrate.

For temporary compatibility with a deployment that cannot yet use the application service:

```yaml
matrix_livekit_jwt_service_appservice_enabled: false
```

## Federated calls and trusted homeservers

With the stable transport, your own users may publish audio, video, and screen shares. Remote users receive media here and publish on their own SFU by default, using clients with multi-SFU support. The playbook explicitly preserves this policy; upstream otherwise allows all remote homeservers to publish.

To allow users of a trusted remote homeserver to publish here through the stable transport, add the following to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
matrix_livekit_jwt_service_environment_variable_livekit_remote_can_publish_homeservers_list_custom:
  - example.org
```

Use `['*']` to allow all remote homeservers. Room membership is checked for every relayed request. This setting controls publishing only: joined remote subscribers can also trigger room creation. See [upstream's publishing policy](https://github.com/element-hq/lk-jwt-service/blob/v0.10.0/README.md#-publishing-from-other-homeservers).

### Legacy clients

For clients using the deprecated `livekit` transport, publishing and room creation are controlled by `matrix_livekit_jwt_service_environment_variable_livekit_full_access_homeservers_list`, which defaults to your `matrix_domain`. Older clients, clients using a single SFU, and callers without their own SFU may join but be unable to publish media.

Fronting multiple homeservers with this legacy list (including `'*'`) is deprecated upstream, with no announced removal date. Existing `matrix_livekit_jwt_service_environment_variable_livekit_full_access_homeservers_list_custom` settings still work for legacy clients, but disable the legacy endpoints' room membership checks when they add other homeservers. Migrate clients to the stable transport and configure remote publishing with the setting above. Once clients have migrated, remove the additional legacy homeservers so that the list contains only your own homeserver.

## Participant metadata

Issued tokens disable participant edits to their own name, metadata, and attributes by default. If a client requires this permission, explicitly enable upstream's `LIVEKIT_CAN_UPDATE_OWN_METADATA` through `matrix_livekit_jwt_service_environment_variables_extension` (merge this with any existing extension):

```yaml
matrix_livekit_jwt_service_environment_variables_extension: |
  LIVEKIT_CAN_UPDATE_OWN_METADATA=true
```
