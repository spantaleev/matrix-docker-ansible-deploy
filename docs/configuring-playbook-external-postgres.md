# Using an external PostgreSQL server (optional)

By default, this playbook would set up a PostgreSQL database server on your machine, running in a Docker container.
If that's alright, you can skip this.

If you'd like to use an external PostgreSQL server that you manage, you can edit your configuration file  (`inventory/matrix.<your-domain>/vars.yml`).
It should be something like this:

```yaml
matrix_postgres_use_external: true
matrix_postgres_connection_hostname: "your-postgres-server-hostname"
matrix_postgres_connection_username: "your-postgres-server-username"
matrix_postgres_connection_password: "your-postgres-server-password"
matrix_postgres_db_name: "your-postgres-server-database-name"
```

The database (as specified in `matrix_postgres_db_name`) must exist and be accessible with the given credentials.
It must be empty or contain a valid Matrix Synapse database. If empty, Matrix Synapse would populate it the first time it runs.

**Note**: the external server that you specify in `matrix_postgres_connection_hostname` must be accessible from within the container `matrix-synapse` Docker container (and possibly others). This means that it either needs to be a publicly accessible hostname or that it's a hostname on the same Docker network where all containers installed by this playbook run (a network called `matrix` by default). Using a local PostgreSQL instance on the host (running on the same machine, but not in a contianer) is not possible.