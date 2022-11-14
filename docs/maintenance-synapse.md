# Synapse maintenance

This document shows you how to perform various maintenance tasks related to the Synapse chat server.

Table of contents:

- [Purging old data with the Purge History API](#purging-old-data-with-the-purge-history-api), for when you wish to delete in-use (but old) data from the Synapse database

- [Compressing state with rust-synapse-compress-state](#compressing-state-with-rust-synapse-compress-state)

- [Browse and manipulate the database](#browse-and-manipulate-the-database), for when you really need to take matters into your own hands

- [Make Synapse faster](#make-synapse-faster)

## Purging old data with the Purge History API

You can use the **[Purge History API](https://github.com/matrix-org/synapse/blob/master/docs/admin_api/purge_history_api.md)** to delete old messages on a per-room basis. **This is destructive** (especially for non-federated rooms), because it means **people will no longer have access to history past a certain point**.

To make use of this API, **you'll need an admin access token** first. Refer to the documentation on [how to obtain an access token](obtaining-access-tokens.md).

Synapse's Admin API is not exposed to the internet by default. To expose it you will need to add `matrix_nginx_proxy_proxy_matrix_client_api_forwarded_location_synapse_admin_api_enabled: true` to your `vars.yml` file.

Follow the [Purge History API](https://github.com/matrix-org/synapse/blob/master/docs/admin_api/purge_history_api.md) documentation page for the actual purging instructions.

After deleting data, you may wish to run a [`FULL` Postgres `VACUUM`](./maintenance-postgres.md#vacuuming-postgresql).


## Compressing state with rust-synapse-compress-state

[rust-synapse-compress-state](https://github.com/matrix-org/rust-synapse-compress-state) can be used to optimize some `_state` tables used by Synapse. If your server participates in large rooms this is the most effective way to reduce the size of your database.

This tool should be safe to use (even when Synapse is running), but it's always a good idea to [make Postgres backups](./maintenance-postgres.md#backing-up-postgresql) first.

To ask the playbook to run rust-synapse-compress-state, execute:

```
ansible-playbook -i inventory/hosts setup.yml --tags=rust-synapse-compress-state
```

By default, all rooms with more than `100000` state group rows will be compressed.
If you need to adjust this, pass: `--extra-vars='matrix_synapse_rust_synapse_compress_state_min_state_groups_required=SOME_NUMBER_HERE'` to the command above.

After state compression, you may wish to run a [`FULL` Postgres `VACUUM`](./maintenance-postgres.md#vacuuming-postgresql).


## Browse and manipulate the database

When the [Synapse Admin API](https://github.com/matrix-org/synapse/tree/master/docs/admin_api) and the other tools do not provide a more convenient way, having a look at synapse's postgresql database can satisfy a lot of admins' needs.

Editing the database manually is not recommended or supported by the Synapse developers. If you are going to do so you should [make a database backup](./maintenance-postgres.md#backing-up-postgresql).

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

## Make Synapse faster

Synapse's presence feature which tracks which users are online and which are offline can use a lot of processing power. You can disable presence by adding `matrix_synapse_presence_enabled: false` to your `vars.yml` file.

Tuning Synapse's cache factor can help reduce RAM usage. [See the upstream documentation](https://github.com/matrix-org/synapse#help-synapse-is-slow-and-eats-all-my-ram-cpu) for more information on what value to set the cache factor to. Use the variable `matrix_synapse_caches_global_factor` to set the cache factor.

Tuning your PostgreSQL database will also make Synapse run significantly faster. See [maintenance-postgres.md##tuning-postgresql](maintenance-postgres.md##tuning-postgresql).

See also [How do I optimize this setup for a low-power server?](faq.md#how-do-i-optimize-this-setup-for-a-low-power-server).
