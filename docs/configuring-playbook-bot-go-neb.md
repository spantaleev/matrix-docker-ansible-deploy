<!--
SPDX-FileCopyrightText: 2019-2025 Slavi Pantaleev
SPDX-FileCopyrightText: 2021 Yannick Goossens
SPDX-FileCopyrightText: 2022 Dennis Ciba
SPDX-FileCopyrightText: 2022 Nikita Chernyi
SPDX-FileCopyrightText: 2023-2025 MDAD project contributors
SPDX-FileCopyrightText: 2024-2026 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Setting up Go-NEB (optional, removed)

🪦 The playbook used to be able to install and configure [Go-NEB](https://github.com/matrix-org/go-neb), but no longer includes this component as it has been discontinued.

While not a 1:1 replacement, the bot's author suggests taking a look at [matrix-hookshot](https://github.com/matrix-org/matrix-hookshot) as a replacement, which can also be [installed using this playbook](configuring-playbook-bridge-hookshot.md).

## Uninstalling Go-NEB manually

If you still have the Go-NEB component installed on your Matrix server, the playbook can no longer help you uninstall it and you will need to do it manually. To uninstall manually, run these commands on the server:

```sh
systemctl disable --now matrix-bot-go-neb.service

rm -rf /matrix/go-neb
```
