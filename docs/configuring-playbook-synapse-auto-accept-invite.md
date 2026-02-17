<!--
SPDX-FileCopyrightText: 2019 Eduardo Beltrame
SPDX-FileCopyrightText: 2019-2025 Slavi Pantaleev
SPDX-FileCopyrightText: 2020 Tulir Asokan
SPDX-FileCopyrightText: 2021, 2024 MDAD project contributors
SPDX-FileCopyrightText: 2022 Dennis Ciba
SPDX-FileCopyrightText: 2022 Vladimir Panteleev
SPDX-FileCopyrightText: 2023 Justin Croonenberghs
SPDX-FileCopyrightText: 2023 Kuba Orlik
SPDX-FileCopyrightText: 2023 Pierre 'McFly' Marty
SPDX-FileCopyrightText: 2023 Samuel Meenzen
SPDX-FileCopyrightText: 2024 Fabio Bonelli
SPDX-FileCopyrightText: 2024-2026 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Setting up Synapse Auto Invite Accept (optional, removed)

🪦 The playbook used to be able to install and configure [synapse-auto-invite-accept](https://github.com/matrix-org/synapse-auto-accept-invite), but no longer includes this component, as the same functionality [has been integrated](https://github.com/element-hq/synapse/pull/17147) to Synapse since [v1.109.0](https://github.com/element-hq/synapse/releases/tag/v1.109.0).

## Native alternative

Here's example configuration for using the **native** Synapse feature:

```yaml
matrix_synapse_auto_accept_invites_enabled: true

# Default settings below. Uncomment and adjust this part if necessary.
# matrix_synapse_auto_accept_invites_only_for_direct_messages: false
# matrix_synapse_auto_accept_invites_only_from_local_users: false

# If workers are enabled, you may delegate usage to a specific worker.
# matrix_synapse_auto_accept_invites_worker_to_run_on: 'matrix-synapse-worker-generic-0'
```
