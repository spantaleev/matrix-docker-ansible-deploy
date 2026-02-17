<!--
SPDX-FileCopyrightText: 2024 MDAD project contributors
SPDX-FileCopyrightText: 2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2024 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Setting up Synapse Auto Invite Accept (optional)

The playbook can install and configure [synapse-auto-invite-accept](https://github.com/matrix-org/synapse-auto-accept-invite) for you.

In short, it automatically accepts room invites. You can specify that only 1:1 room invites are auto-accepted. Defaults to false if not specified.

See the project's [documentation](https://github.com/matrix-org/synapse-auto-accept-invite/blob/main/README.md) to learn what it does and why it might be useful to you.

**Note**: Synapse [v1.109.0](https://github.com/element-hq/synapse/releases/tag/v1.109.0), the same feature [has been merged](https://github.com/element-hq/synapse/pull/17147) into Synapse (see the [Native alternative](#native-alternative) section below). You'd better use the native feature, instead of the [synapse-auto-invite-accept](https://github.com/matrix-org/synapse-auto-accept-invite) 3rd party module.

## Native alternative

Since Synapse [v1.109.0](https://github.com/element-hq/synapse/releases/tag/v1.109.0), the functionality provided by the [synapse-auto-invite-accept](https://github.com/matrix-org/synapse-auto-accept-invite) 3rd party module [has been made](https://github.com/element-hq/synapse/pull/17147) part of Synapse.

Here's example configuration for using the **native** Synapse feature:

```yaml
matrix_synapse_auto_accept_invites_enabled: true

# Default settings below. Uncomment and adjust this part if necessary.
# matrix_synapse_auto_accept_invites_only_for_direct_messages: false
# matrix_synapse_auto_accept_invites_only_from_local_users: false

# If workers are enabled, you may delegate usage to a specific worker.
# matrix_synapse_auto_accept_invites_worker_to_run_on: 'matrix-synapse-worker-generic-0'
```
