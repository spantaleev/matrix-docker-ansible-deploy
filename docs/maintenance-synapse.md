# Synapse maintenance

This document shows you how to perform various maintenance tasks related to the Synapse chat server.

Table of contents:

- [Purging old data with the Purge History API](#purging-old-data-with-the-purge-history-api), for when you wish to delete in-use (but old) data from the Synapse database

- [Synapse maintenance](#synapse-maintenance)
	- [Purging old data with the Purge History API](#purging-old-data-with-the-purge-history-api)
	- [Compressing state with rust-synapse-compress-state](#compressing-state-with-rust-synapse-compress-state)
	- [Browse and manipulate the database](#browse-and-manipulate-the-database)

- [Browse and manipulate the database](#browse-and-manipulate-the-database), for when you really need to take matters into your own hands


## Purging old data with the Purge History API

You can use the **Purge History API** to delete in-use (but old) data.

**This is destructive** (especially for non-federated rooms), because it means **people will no longer have access to history past a certain point**.

Synapse's [Purge History API](https://github.com/matrix-org/synapse/blob/master/docs/admin_api/purge_history_api.rst) can be used to purge on a per-room basis.

To make use of this API, **you'll need an admin access token** first. You can find your access token in the setting of some clients (like Element).
Alternatively, you can log in and obtain a new access token like this:

```
curl \
--data '{"identifier": {"type": "m.id.user", "user": "YOUR_MATRIX_USERNAME" }, "password": "YOUR_MATRIX_PASSWORD", "type": "m.login.password", "device_id": "Synapse-Purge-History-API"}' \
https://matrix.DOMAIN/_matrix/client/r0/login
```

Follow the [Purge History API](https://github.com/matrix-org/synapse/blob/master/docs/admin_api/purge_history_api.rst) documentation page for the actual purging instructions.

After deleting data, you may wish to run a [`FULL` Postgres `VACUUM`](./maintenance-postgres.md#vacuuming-postgresql).


## Compressing state with rust-synapse-compress-state

[rust-synapse-compress-state](https://github.com/matrix-org/rust-synapse-compress-state) can be used to optimize some `_state` tables used by Synapse.

This tool should be safe to use (even when Synapse is running), but it's always a good idea to [make Postgres backups](./maintenance-postgres.md#backing-up-postgresql) first.

To ask the playbook to run rust-synapse-compress-state, execute:

```
ansible-playbook -i inventory/hosts setup.yml --tags=rust-synapse-compress-state
```

By default, all rooms with more than `100000` state group rows will be compressed.
If you need to adjust this, pass: `--extra-vars='matrix_synapse_rust_synapse_compress_state_min_state_groups_required=SOME_NUMBER_HERE'` to the command above.

After state compression, you may wish to run a [`FULL` Postgres `VACUUM`](./maintenance-postgres.md#vacuuming-postgresql).


## Browse and manipulate the database

When the [matrix admin API](https://github.com/matrix-org/synapse/tree/master/docs/admin_api) and the other tools do not provide a more convenient way, having a look at synapse's postgresql database can satisfy a lot of admins' needs.
First, set up an SSH tunnel to your matrix server (skip if it is your local machine):

```
# you may replace 1799 with an arbitrary port unbound on both machines
ssh -L 1799:localhost:1799 matrix.DOMAIN
```

Then start up an ephemeral [adminer](https://www.adminer.org/) container on the Matrix server, connecting it to the `matrix` network and linking the postgresql container:

```
docker run --rm --publish 1799:8080 --link matrix-postgres --net matrix adminer
```

You should then be able to browse the adminer database administration GUI at http://localhost:1799/ after entering your DB credentials (found in the `host_vars` or on the server in `{{matrix_synapse_config_dir_path}}/homeserver.yaml` under `database.args`)

⚠️ Be **very careful** with this, there is **no undo** for impromptu DB operations.
