<!--
SPDX-FileCopyrightText: 2019 - 2025 Slavi Pantaleev
SPDX-FileCopyrightText: 2019 Eduardo Beltrame
SPDX-FileCopyrightText: 2020 - 2023 MDAD project contributors
SPDX-FileCopyrightText: 2020 Björn Marten
SPDX-FileCopyrightText: 2020 iLyas Bakouch
SPDX-FileCopyrightText: 2020 Tulir Asokan
SPDX-FileCopyrightText: 2022 Dennis Ciba
SPDX-FileCopyrightText: 2022 Kim Brose
SPDX-FileCopyrightText: 2022 Vladimir Panteleev
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Setting up Appservice Webhooks bridging (optional, removed)

🪦 The playbook used to be able to install and configure [matrix-appservice-webhooks](https://github.com/turt2live/matrix-appservice-webhooks), but no longer includes this component, as it has been deprecated since more than several years.

You may wish to use [matrix-hookshot](https://github.com/matrix-org/matrix-hookshot) instead.

## Uninstalling the bridge manually

If you still have matrix-appservice-webhooks installed on your Matrix server, the playbook can no longer help you uninstall it and you will need to do it manually. To uninstall manually, run these commands on the server:

```sh
systemctl disable --now matrix-appservice-webhooks.service

rm -rf /matrix/appservice-webhooks
```
