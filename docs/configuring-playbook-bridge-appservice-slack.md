<!--
SPDX-FileCopyrightText: 2019 Edgars Voroboks
SPDX-FileCopyrightText: 2019 Eduardo Beltrame
SPDX-FileCopyrightText: 2019-2025 MDAD project contributors
SPDX-FileCopyrightText: 2019-2025 Slavi Pantaleev
SPDX-FileCopyrightText: 2020 Chris van Dijk
SPDX-FileCopyrightText: 2020 Tulir Asokan
SPDX-FileCopyrightText: 2020 Udo Rader
SPDX-FileCopyrightText: 2020 jens quade
SPDX-FileCopyrightText: 2021 Joel Bennett
SPDX-FileCopyrightText: 2022 Dennis Ciba
SPDX-FileCopyrightText: 2022 Kim Brose
SPDX-FileCopyrightText: 2022 Travis Ralston
SPDX-FileCopyrightText: 2022 Vladimir Panteleev
SPDX-FileCopyrightText: 2022 Yan Minagawa
SPDX-FileCopyrightText: 2024 Fabio Bonelli
SPDX-FileCopyrightText: 2024-2026 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Setting up Appservice Slack bridging (optional, removed)

🪦 The playbook used to be able to install and configure [matrix-appservice-slack](https://github.com/matrix-org/matrix-appservice-slack), but no longer includes this component, as it had been unavailable for new installation since 2024, and was finally abandoned because the public Matrix.org Slack bridge has been decommissioned on January 14th, 2026.

**Note**: Bridging to [Slack](https://slack.com) can also happen via the [mautrix-slack](configuring-playbook-bridge-mautrix-slack.md) bridge supported by the playbook.

## Uninstalling the component manually

If you still have matrix-appservice-slack installed on your Matrix server, the playbook can no longer help you uninstall it and you will need to do it manually. To uninstall manually, run these commands on the server:

```sh
systemctl disable --now matrix-appservice-slack.service

rm -rf /matrix/appservice-slack

/matrix/postgres/bin/cli-non-interactive -c 'DROP DATABASE matrix_appservice_slack;'
```
