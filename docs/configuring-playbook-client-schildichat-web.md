<!--
SPDX-FileCopyrightText: 2019 Edgars Voroboks
SPDX-FileCopyrightText: 2019 Eduardo Beltrame
SPDX-FileCopyrightText: 2019-2025 MDAD project contributors
SPDX-FileCopyrightText: 2019-2025 Slavi Pantaleev
SPDX-FileCopyrightText: 2020 Chris van Dijk
SPDX-FileCopyrightText: 2020 Tulir Asokan
SPDX-FileCopyrightText: 2020 jens quade
SPDX-FileCopyrightText: 2022 Dennis Ciba
SPDX-FileCopyrightText: 2022 Kim Brose
SPDX-FileCopyrightText: 2022 Travis Ralston
SPDX-FileCopyrightText: 2022 Vladimir Panteleev
SPDX-FileCopyrightText: 2022 Yan Minagawa
SPDX-FileCopyrightText: 2023 Nikita Chernyi
SPDX-FileCopyrightText: 2024-2026 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Setting up SchildiChat Web (optional, removed)

🪦 The playbook used to be able to install and configure the [SchildiChat Web](https://github.com/SchildiChat/schildichat-desktop) Matrix client, but no longer includes this component, as it has been unmaintained.

## Uninstalling the component manually

If you still have the client installed on your Matrix server, the playbook can no longer help you uninstall it and you will need to do it manually. To uninstall manually, run these commands on the server:

```sh
systemctl disable --now matrix-client-schildichat.service

rm -rf /matrix/client-schildichat
```
