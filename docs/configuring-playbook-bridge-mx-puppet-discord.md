<!--
SPDX-FileCopyrightText: 2019 - 2025 Slavi Pantaleev
SPDX-FileCopyrightText: 2019 Eduardo Beltrame
SPDX-FileCopyrightText: 2020 Hugues Morisset
SPDX-FileCopyrightText: 2020 Tulir Asokan
SPDX-FileCopyrightText: 2021 - 2022 MDAD project contributors
SPDX-FileCopyrightText: 2022 Dennis Ciba
SPDX-FileCopyrightText: 2022 MDAD project contributors
SPDX-FileCopyrightText: 2022 Vladimir Panteleev
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Setting up MX Puppet Discord bridging (optional, removed)

🪦 The playbook used to be able to install and configure [mx-puppet-discord](https://gitlab.com/mx-puppet/discord/mx-puppet-discord), but no longer includes this component, as it has been unmaintained for a long time.

You may wish to use the [Mautrix Discord bridge](https://github.com/mautrix/discord) instead.

## Uninstalling the bridge manually

If you still have the MX Puppet Discord bridge installed on your Matrix server, the playbook can no longer help you uninstall it and you will need to do it manually. To uninstall manually, run these commands on the server:

```sh
systemctl disable --now matrix-mx-puppet-discord.service

rm -rf /matrix/mx-puppet-discord

/matrix/postgres/bin/cli-non-interactive 'DROP DATABASE matrix_mx_puppet_discord;'
```
