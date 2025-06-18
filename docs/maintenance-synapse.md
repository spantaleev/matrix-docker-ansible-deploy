<!--
SPDX-FileCopyrightText: 2019 - 2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2020 Marcel Partap
SPDX-FileCopyrightText: 2021 - 2024 MDAD project contributors
SPDX-FileCopyrightText: 2021 Aaron Raimist
SPDX-FileCopyrightText: 2022 Dennis Ciba
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Synapse maintenance

This document shows you how to perform various maintenance tasks related to the Synapse chat server.

Table of contents:
- [Purging old data with the Purge History API](#purging-old-data-with-the-purge-history-api), for when you wish to delete in-use (but old) data from the Synapse database
- [Compressing state with rust-synapse-compress-state](#compressing-state-with-rust-synapse-compress-state)
- [Browse and manipulate the database](#browse-and-manipulate-the-database), for when you really need to take matters into your own hands
- [Make Synapse faster](#make-synapse-faster)

💡 See this page for details about configuring Synapse: [Configuring Synapse](configuring-playbook-synapse.md)

## Purging old data with the Purge History API

You can use the **[Purge History API](https://github.com/element-hq/synapse/blob/master/docs/admin_api/purge_history_api.md)** to delete old messages on a per-room basis. **This is destructive** (especially for non-federated rooms), because it means **people will no longer have access to history past a certain point**.

To make use of this Synapse Admin API, **you'll need an admin access token** first. Refer to the documentation on [how to obtain an access token](obtaining-access-tokens.md).

> [!WARNING]
> Access tokens are sensitive information. Do not include them in any bug reports, messages, or logs. Do not share the access token with anyone.

Synapse's Admin API is not exposed to the internet by default, following [official Synapse reverse-proxying recommendations](https://github.com/element-hq/synapse/blob/master/docs/reverse_proxy.md#synapse-administration-endpoints). To expose it you will need to add `matrix_synapse_container_labels_public_client_synapse_admin_api_enabled: true` to your `vars.yml` file.

Follow the [Purge History API](https://github.com/element-hq/synapse/blob/master/docs/admin_api/purge_history_api.md) documentation page for the actual purging instructions.

After deleting data, you may wish to run a [`FULL` Postgres `VACUUM`](./maintenance-postgres.md#vacuuming-postgresql).

## Compressing state with rust-synapse-compress-state

[rust-synapse-compress-state](https://github.com/matrix-org/rust-synapse-compress-state) can be used to optimize some `_state` tables used by Synapse. If your server participates in large rooms this is the most effective way to reduce the size of your database.

**Note**: besides running the `rust-synapse-compress-state` tool manually, you can also enable its `synapse-auto-compressor` tool by [Setting up synapse-auto-compressor](configuring-playbook-synapse-auto-compressor.md). The automatic tool will run on a schedule every day and you won't have to compress state manually ever again.

`rust-synapse-compress-state` should be safe to use (even when Synapse is running), but it's always a good idea to [make Postgres backups](./maintenance-postgres.md#backing-up-postgresql) first.

To ask the playbook to run rust-synapse-compress-state, execute:

```sh
ansible-playbook -i inventory/hosts setup.yml --tags=rust-synapse-compress-state
```

The shortcut command with `just` program is also available: `just run-tags rust-synapse-compress-state`

By default, all rooms with more than `100000` state group rows will be compressed. If you need to adjust this, pass: `--extra-vars='matrix_synapse_rust_synapse_compress_state_min_state_groups_required=SOME_NUMBER_HERE'` to the command above.

After state compression, you may wish to run a [`FULL` Postgres `VACUUM`](./maintenance-postgres.md#vacuuming-postgresql).

## Browse and manipulate the database

When the [Synapse Admin API](https://github.com/element-hq/synapse/tree/master/docs/admin_api) and the other tools do not provide a more convenient way, having a look at synapse's postgresql database can satisfy a lot of admins' needs.

Editing the database manually is not recommended or supported by the Synapse developers. If you are going to do so you should [make a database backup](./maintenance-postgres.md#backing-up-postgresql).

First, set up an SSH tunnel to your Matrix server (skip if it is your local machine):

```sh
# you may replace 1799 with an arbitrary port unbound on both machines
ssh -L 1799:localhost:1799 matrix.example.com
```

Then start up an ephemeral [adminer](https://www.adminer.org/) container on the Matrix server, connecting it to the `matrix` network and linking the postgresql container:

```sh
docker run --rm --publish 1799:8080 --link matrix-postgres --net matrix adminer
```

You should then be able to browse the adminer database administration GUI at http://localhost:1799/ after entering your DB credentials (found in the `host_vars` or on the server in `{{matrix_synapse_config_dir_path}}/homeserver.yaml` under `database.args`)

⚠️️ Be **very careful** with this, there is **no undo** for impromptu DB operations.

## Make Synapse faster

Synapse's presence feature which tracks which users are online and which are offline can use a lot of processing power. You can disable presence by adding `matrix_synapse_presence_enabled: false` to your `vars.yml` file.

If you have enough compute resources (CPU & RAM), you can make Synapse better use of them by [enabling load-balancing with workers](configuring-playbook-synapse.md#load-balancing-with-workers).

[Tuning your PostgreSQL database](maintenance-postgres.md#tuning-postgresql) could also improve Synapse performance. The playbook tunes the integrated Postgres database automatically, but based on your needs you may wish to adjust tuning variables manually. If you're using an [external Postgres database](configuring-playbook-external-postgres.md), you will also need to tune Postgres manually.

### Tuning caches and cache autotuning

Tuning Synapse's cache factor is useful for performance increases but also as part of controlling Synapse's memory use. Use the variable `matrix_synapse_caches_global_factor` to set the cache factor as part of this process.

**The playbook defaults the global cache factor to a large value** (e.g. `10`). A smaller value (e.g. `0.5`) will decrease the amount used for caches, but will [not necessarily decrease RAM usage as a whole](https://github.com/matrix-org/synapse/issues/3939).

Tuning the cache factor is useful only to a limited degree (as its crude to do in isolation) and therefore users who are tuning their cache factor should likely look into tuning autotune variables as well (see below).

Cache autotuning is **enabled by default** and controlled via the following variables:

- `matrix_synapse_cache_autotuning_max_cache_memory_usage` — defaults to 1/8 of total RAM with a cap of 2GB; values are specified in bytes
- `matrix_synapse_cache_autotuning_target_cache_memory_usage` — defaults to 1/16 of total RAM with a cap of 1GB; values are specified in bytes
- `matrix_synapse_cache_autotuning_min_cache_ttl` — defaults to `30s`

You can **learn more about cache-autotuning and the global cache factor settings** in the [Synapse's documentation on caches and associated values](https://matrix-org.github.io/synapse/latest/usage/configuration/config_documentation.html#caches-and-associated-values).

To **disable cache auto-tuning**, unset all values:

```yaml
matrix_synapse_cache_autotuning_max_cache_memory_usage: ''
matrix_synapse_cache_autotuning_target_cache_memory_usage: ''
matrix_synapse_cache_autotuning_min_cache_ttl: ''
```

Users who wish to lower Synapse's RAM footprint should look into lowering the global cache factor and tweaking the autotune variables (or disabling auto-tuning). If your cache factor is too low for a given auto tune setting your caches will not reach autotune thresholds and autotune won't be able to do its job. Therefore, when auto-tuning is enabled (which it is by default), it's recommended to have your cache factor be large.

See also [How do I optimize this setup for a low-power server?](faq.md#how-do-i-optimize-this-setup-for-a-low-power-server).
