<!--
SPDX-FileCopyrightText: 2019 - 2025 Slavi Pantaleev
SPDX-FileCopyrightText: 2022 Dennis Ciba
SPDX-FileCopyrightText: 2022 Nikita Chernyi
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara
SPDX-FileCopyrightText: 2024 MDAD project contributors

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Setting up Email2Matrix (optional, removed)

🪦 The playbook used to be able to install and configure [Email2Matrix](https://github.com/devture/email2matrix), but no longer includes this component.

For a long time now, it been replaced by the much better and more maintained [Postmoogle](https://github.com/etkecc/postmoogle) bridge, which can also be [installed using this playbook](configuring-playbook-bridge-postmoogle.md).


## Uninstalling Email2Matrix manually

If you still have the Email2Matrix component installed on your Matrix server, the playbook can no longer help you uninstall it and you will need to do it manually. To uninstall manually, run these commands on the server:

```sh
systemctl disable --now matrix-email2matrix.service

rm -rf /matrix/email2matrix
```
