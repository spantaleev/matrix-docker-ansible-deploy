<!--
SPDX-FileCopyrightText: 2019 - 2025 Slavi Pantaleev
SPDX-FileCopyrightText: 2019 Eduardo Beltrame
SPDX-FileCopyrightText: 2021 MDAD project contributors
SPDX-FileCopyrightText: 2022 Dennis Ciba
SPDX-FileCopyrightText: 2022 Vladimir Panteleev
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Setting up Go Skype Bridge bridging (optional, removed)

🪦 The playbook used to be able to install and configure [go-skype-bridge](https://github.com/kelaresg/go-skype-bridge), but no longer includes this component, as Skype has been discontinued since May 2025.

## Uninstalling the bridge manually

If you still have the Go Skype bridge installed on your Matrix server, the playbook can no longer help you uninstall it and you will need to do it manually. To uninstall manually, run these commands on the server:

```sh
systemctl disable --now matrix-go-skype-bridge.service

rm -rf /matrix/go-skype-bridge

/matrix/postgres/bin/cli-non-interactive 'DROP DATABASE matrix_go_skype_bridge;'
```
