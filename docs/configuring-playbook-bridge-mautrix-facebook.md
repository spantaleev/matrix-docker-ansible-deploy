<!--
SPDX-FileCopyrightText: 2019 - 2025 Slavi Pantaleev
SPDX-FileCopyrightText: 2019 Eduardo Beltrame
SPDX-FileCopyrightText: 2019 Hugues Morisset
SPDX-FileCopyrightText: 2020 Tulir Asokan
SPDX-FileCopyrightText: 2021 - 2022 MDAD project contributors
SPDX-FileCopyrightText: 2021 Aaron Raimist
SPDX-FileCopyrightText: 2022 Dennis Ciba
SPDX-FileCopyrightText: 2022 László Várady
SPDX-FileCopyrightText: 2022 Vladimir Panteleev
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Setting up Mautrix Facebook bridging (optional, removed)

🪦 The playbook used to be able to install and configure [mautrix-facebook](https://github.com/mautrix/facebook), but no longer includes this component, as it has been deprecated in favor of the [mautrix-meta](https://github.com/mautrix/meta) Messenger/Instagram bridge.

The mautrix-meta bridge can be [installed using this playbook](configuring-playbook-bridge-mautrix-meta-messenger.md).

## Uninstalling the bridge manually

If you still have the bridge installed on your Matrix server, the playbook can no longer help you uninstall it and you will need to do it manually. To uninstall manually, run these commands on the server:

```sh
systemctl disable --now matrix-mautrix-facebook.service

rm -rf /matrix/mautrix-facebook

/matrix/postgres/bin/cli-non-interactive 'DROP DATABASE matrix_mautrix_facebook;'
```
