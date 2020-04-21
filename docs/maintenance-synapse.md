# Synapse maintenance

This document shows you how to perform various maintenance tasks related to the Synapse chat server.

Table of contents:

- [Purging unused data with synapse-janitor](#purging-unused-data-with-synapse-janitor), for when you wish to delete unused data from the Synapse database

- [Purging old data with the Purge History API](#purging-old-data-with-the-purge-history-api), for when you wish to delete in-use (but old) data from the Synapse database

- [Synapse maintenance](#synapse-maintenance)
	- [Purging unused data with synapse-janitor](#purging-unused-data-with-synapse-janitor)
		- [Vacuuming Postgres](#vacuuming-postgres)
	- [Purging old data with the Purge History API](#purging-old-data-with-the-purge-history-api)
	- [Compressing state with rust-synapse-compress-state](#compressing-state-with-rust-synapse-compress-state)


## Purging unused data with synapse-janitor

**NOTE**: There are [reports](https://github.com/spantaleev/matrix-docker-ansible-deploy/issues/465) that **synapse-janitor is dangerous to use and causes database corruption**. You may wish to refrain from using it.

When you **leave** and **forget** a room, Synapse can clean up its data, but currently doesn't.
This **unused and unreachable data** remains in your database forever.

There are external tools (like [synapse-janitor](https://github.com/xwiki-labs/synapse_scripts)), which are meant to solve this problem.

To ask the playbook to run synapse-janitor, execute:

```bash
ansible-playbook -i inventory/hosts setup.yml --tags=run-postgres-synapse-janitor,start
```

**Note**: this will automatically stop Synapse temporarily and restart it later.


### Vacuuming Postgres

Running synapse-janitor potentially deletes a lot of data from the Postgres database.
However, disk space only ever gets released after a [`FULL` Postgres `VACUUM`](./maintenance-postgres.md#vacuuming-postgresql).

It's easiest if you ask the playbook to run both synapse-janitor and a `VACUUM FULL` in one call:

```bash
ansible-playbook -i inventory/hosts setup.yml --tags=run-postgres-synapse-janitor,run-postgres-vacuum,start
```

**Note**: this will automatically stop Synapse temporarily and restart it later. You'll also need plenty of available disk space in your Postgres data directory (usually `/matrix/postgres/data`).


## Purging old data with the Purge History API

If [purging unused and unreachable data](#purging-unused-data-with-synapse-janitor) is not enough for you, you can start deleting in-use (but old) data.

**This is destructive** (especially for non-federated rooms), because it means **people will no longer have access to history past a certain point**.

Synapse provides a [Purge History API](https://github.com/matrix-org/synapse/blob/master/docs/admin_api/purge_history_api.rst) that you can use to purge on a per-room basis.

To make use of this API, **you'll need an admin access token** first. You can find your access token in the setting of some clients (like riot-web).
Alternatively, you can log in and obtain a new access token like this:

```
curl \
--data '{"identifier": {"type": "m.id.user", "user": "YOUR_MATRIX_USERNAME" }, "password": "YOUR_MATRIX_PASSWORD", "type": "m.login.password", "device_id": "Synapse-Purge-History-API"}' \
https://matrix.DOMAIN/_matrix/client/r0/login
```

Follow the [Purge History API](https://github.com/matrix-org/synapse/blob/master/docs/admin_api/purge_history_api.rst) documentation page for the actual purging instructions.

Don't forget that disk space only ever gets released after a [`FULL` Postgres `VACUUM`](./maintenance-postgres.md#vacuuming-postgresql) - something the playbook can help you with.


## Compressing state with rust-synapse-compress-state

[rust-synapse-compress-state](https://github.com/matrix-org/rust-synapse-compress-state) can be used to optimize some `_state` tables used by Synapse.

Unfortunately, at this time the playbook can't help you run this **experimental tool**.

Since it's also experimental, you may wish to stay away from it, or at least [make Postgres backups](./maintenance-postgres.md#backing-up-postgresql) first.
