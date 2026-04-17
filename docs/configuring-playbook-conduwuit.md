<!--
SPDX-FileCopyrightText: 2019 Eduardo Beltrame
SPDX-FileCopyrightText: 2019-2025 Slavi Pantaleev
SPDX-FileCopyrightText: 2020 Tulir Asokan
SPDX-FileCopyrightText: 2021, 2024 MDAD project contributors
SPDX-FileCopyrightText: 2022 Dennis Ciba
SPDX-FileCopyrightText: 2022 Vladimir Panteleev
SPDX-FileCopyrightText: 2023 Justin Croonenberghs
SPDX-FileCopyrightText: 2023 Kuba Orlik
SPDX-FileCopyrightText: 2023 Pierre 'McFly' Marty
SPDX-FileCopyrightText: 2023 Samuel Meenzen
SPDX-FileCopyrightText: 2024 Fabio Bonelli
SPDX-FileCopyrightText: 2024-2026 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Configuring conduwuit (optional, removed)

🪦 The playbook used to be able to install and configure the [conduwuit](https://conduwuit.puppyirl.gay/) Matrix server, but no longer includes this component, as it's been abandoned and unmaintained.

## Uninstalling the service manually

If you still have conduwuit installed on your Matrix server, the playbook can no longer help you uninstall it and you will need to do it manually.

To uninstall the service, run the command below on the server:

```sh
systemctl disable --now matrix-conduwuit.service
```

## Migrating to Continuwuity

Since [Continuwuity](configuring-playbook-continuwuity.md) is a drop-in replacement for conduwuit, migration is possible. Please refer to [this section](./configuring-playbook-continuwuity.md#migrating-from-conduwuit) for details.

## Removing data manually

If you are not going to migrate to [Continuwuity](configuring-playbook-continuwuity.md), you can remove data by running the command on the server:

```sh
rm -rf /matrix/conduwuit
```

>[!WARNING]
> Once you removing the path, there is no going back. Your data on the homeserver (including chat history, rooms, etc.) will be deleted and not be possible to restore them. Please be certain.
