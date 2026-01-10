<!--
SPDX-FileCopyrightText: 2018 - 2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Using an external PostgreSQL server (optional)

By default, this playbook would set up a PostgreSQL database server on your machine, running in a Docker container. If that's okay, you can skip this document.

**Note**: using **an external Postgres server is currently [not very seamless](https://github.com/spantaleev/matrix-docker-ansible-deploy/issues/1682#issuecomment-1061461683) when it comes to enabling various other playbook services** — you will need to create a new database/credentials for each service and to point each service to its corresponding database using custom `vars.yml` configuration. **For the best experience with the playbook, stick to using the integrated Postgres server**.

If you'd like to use an external Postgres server that you manage, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file (adapt to your needs):

```yaml
postgres_enabled: false

# Rewire Synapse to use your external Postgres server
matrix_synapse_database_host: "your-postgres-server-hostname"
matrix_synapse_database_user: "your-postgres-server-username"
matrix_synapse_database_password: "your-postgres-server-password"
matrix_synapse_database_database: "your-postgres-server-database-name"

# Rewire any other service (each `matrix-*` role) you may wish to use to use your external Postgres server.
# Each service expects to have its own dedicated database on the Postgres server
# and uses its own variable names (see `roles/custom/matrix-*/defaults/main.yml`) for configuring Postgres connectivity.
```

The database (as specified in `matrix_synapse_database_database`) must exist and be accessible with the given credentials. It must be empty or contain a valid Synapse database. If empty, Synapse would populate it the first time it runs.

**Note**: the external server that you specify in `matrix_synapse_database_host` must be accessible from within the `matrix-synapse` Docker container (and possibly other containers too). This means that it either needs to be a publicly accessible hostname or that it's a hostname on the same Docker network where all containers installed by this playbook run (a network called `matrix` by default). Using a local PostgreSQL instance on the host (running on the same machine, but not in a container) is not possible.

The connection to your external Postgres server **will not be SSL encrypted**, as [we don't support that yet](https://github.com/spantaleev/matrix-docker-ansible-deploy/issues/89).
