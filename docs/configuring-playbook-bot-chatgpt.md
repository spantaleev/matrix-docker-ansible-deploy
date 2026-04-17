<!--
SPDX-FileCopyrightText: 2019 - 2025 Slavi Pantaleev
SPDX-FileCopyrightText: 2022 Dennis Ciba
SPDX-FileCopyrightText: 2022 Nikita Chernyi
SPDX-FileCopyrightText: 2023 - 2024 MDAD project contributors
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Setting up matrix-chatgpt-bot (optional, removed)

🪦 The playbook used to be able to install and configure [matrix-chatgpt-bot](https://github.com/matrixgpt/matrix-chatgpt-bot), but no longer includes this component.

While not a 1:1 replacement, the bot's author suggests taking a look at [baibot](https://github.com/etkecc/baibot) as a replacement, which can also be [installed using this playbook](configuring-playbook-bot-baibot.md).

## Uninstalling matrix-chatgpt-bot manually

If you still have the matrix-chatgpt-bot component installed on your Matrix server, the playbook can no longer help you uninstall it and you will need to do it manually. To uninstall manually, run these commands on the server:

```sh
systemctl disable --now matrix-bot-chatgpt.service

rm -rf /matrix/chatgpt
```
