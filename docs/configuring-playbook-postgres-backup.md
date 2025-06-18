<!--
SPDX-FileCopyrightText: 2021 - 2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2021 foxcris
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Setting up Postgres backup (optional)

The playbook can install and configure [docker-postgres-backup-local](https://github.com/prodrigestivill/docker-postgres-backup-local) for you.

The [Ansible role for docker-postgres-backup-local](https://github.com/mother-of-all-self-hosting/ansible-role-postgres-backup) is developed and maintained by [the MASH (mother-of-all-self-hosting) project](https://github.com/mother-of-all-self-hosting). For details about configuring docker-postgres-backup-local, you can check them via:
- 🌐 [the role's documentation at the MASH project](https://github.com/mother-of-all-self-hosting/ansible-role-postgres-backup/blob/main/docs/configuring-postgres-backup.md) online
- 📁 `roles/galaxy/postgres_backup/docs/configuring-postgres-backup.md` locally, if you have [fetched the Ansible roles](installing.md#update-ansible-roles)

**Note**: for a more complete backup solution (one that includes not only Postgres, but also other configuration/data files), you may wish to look into [BorgBackup](configuring-playbook-backup-borg.md) instead.
