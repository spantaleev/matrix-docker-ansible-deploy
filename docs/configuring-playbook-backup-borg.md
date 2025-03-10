<!--
SPDX-FileCopyrightText: 2022 - 2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2022 - 2025 Nikita Chernyi
SPDX-FileCopyrightText: 2022 Julian-Samuel Gebühr
SPDX-FileCopyrightText: 2022 MDAD project contributors
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Setting up BorgBackup (optional)

The playbook can install and configure [BorgBackup](https://www.borgbackup.org/) (short: Borg) with [borgmatic](https://torsion.org/borgmatic/) for you.

BorgBackup is a deduplicating backup program with optional compression and encryption. That means your daily incremental backups can be stored in a fraction of the space and is safe whether you store it at home or on a cloud service.

The [Ansible role for BorgBackup](https://github.com/mother-of-all-self-hosting/ansible-role-backup_borg) is developed and maintained by [the MASH (mother-of-all-self-hosting) project](https://github.com/mother-of-all-self-hosting). For details about configuring BorgBackup, you can check them via:
- 🌐 [the role's documentation at the MASH project](https://github.com/mother-of-all-self-hosting/ansible-role-backup_borg/blob/main/docs/configuring-backup-borg.md) online
- 📁 `roles/galaxy/backup_borg/docs/configuring-backup-borg.md` locally, if you have [fetched the Ansible roles](installing.md#update-ansible-roles)
