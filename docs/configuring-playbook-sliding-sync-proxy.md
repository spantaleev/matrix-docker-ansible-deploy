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

# Setting up the Sliding Sync proxy (optional, removed)

🪦 The playbook used to be able to install and configure the [sliding-sync](https://github.com/matrix-org/sliding-sync) proxy, but no longer includes this component, as it's been replaced with a different method (called Simplified Sliding Sync) integrated to newer homeservers by default (**Conduit** homeserver from version `0.6.0` or **Synapse** from version `1.114`).

## Uninstalling the proxy manually

If you still have the Sliding Sync proxy installed on your Matrix server, the playbook can no longer help you uninstall it and you will need to do it manually. To uninstall manually, run these commands on the server:

```sh
systemctl disable --now matrix-sliding-sync.service

rm -rf /matrix/sliding-sync

/matrix/postgres/bin/cli-non-interactive -c 'DROP DATABASE matrix_sliding_sync;'
```
