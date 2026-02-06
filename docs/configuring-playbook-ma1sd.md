<!--
SPDX-FileCopyrightText: 2018-2025 Slavi Pantaleev
SPDX-FileCopyrightText: 2019 Eduardo Beltrame
SPDX-FileCopyrightText: 2019 Noah Fleischmann
SPDX-FileCopyrightText: 2019-2022, 2024 MDAD project contributors
SPDX-FileCopyrightText: 2020 Hugues Morisset
SPDX-FileCopyrightText: 2020 Marcel Partap
SPDX-FileCopyrightText: 2020 Tulir Asokan
SPDX-FileCopyrightText: 2020, 2023 Justin Croonenberghs
SPDX-FileCopyrightText: 2022 Dennis Ciba
SPDX-FileCopyrightText: 2022 Vladimir Panteleev
SPDX-FileCopyrightText: 2023 Kuba Orlik
SPDX-FileCopyrightText: 2023 Pierre 'McFly' Marty
SPDX-FileCopyrightText: 2023 Samuel Meenzen
SPDX-FileCopyrightText: 2024 Fabio Bonelli
SPDX-FileCopyrightText: 2024-2026 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Setting up ma1sd Identity Server (optional, removed)

🪦 The playbook used to be able to install and configure the [ma1sd](https://github.com/ma1uta/ma1sd) Identity Server, but no longer includes this component, as it has been unmaintained for a long time.

Please note that some of the functions can be achieved with other components. For example, if you wish to implement LDAP integration, you might as well check out [the LDAP provider module for Synapse](./configuring-playbook-ldap-auth.md) instead.

## Uninstalling the component manually

If you still have the ma1sd Identity Server installed on your Matrix server, the playbook can no longer help you uninstall it and you will need to do it manually. To uninstall manually, run these commands on the server:

```sh
systemctl disable --now matrix-ma1sd.service

rm -rf /matrix/ma1sd

/matrix/postgres/bin/cli-non-interactive 'DROP DATABASE matrix_ma1sd;'
```
