# Importing an existing Postgres database from another installation (optional)

Run this if you'd like to import your database from a previous installation.
(don't forget to import your Synapse `media_store` files as well - see [the importing-synape-media-store guide](importing-synapse-media-store.md)).


## Prerequisites

For this to work, **the database name in Postgres must match** what this playbook uses.
This playbook uses a Postgres database name of `synapse` by default (controlled by the `matrix_synapse_database_database` variable).
If your database name differs, be sure to change `matrix_synapse_database_database` to your desired name and to re-run the playbook before proceeding.

The playbook supports importing Postgres dump files in **text** (e.g. `pg_dump > dump.sql`) or **gzipped** formats (e.g. `pg_dump | gzip -c > dump.sql.gz`).

Importing multiple databases (as dumped by `pg_dumpall`) is also supported.
But the migration might be a good moment, to "reset" a not properly working bridge. Be aware, that it might affect all users (new link to bridge, new rooms, ...)

Before doing the actual import, **you need to upload your Postgres dump file to the server** (any path is okay).


## Importing

To import, run this command (make sure to replace `<server-path-to-postgres-dump.sql>` with a file path on your server):

```sh
ansible-playbook -i inventory/hosts setup.yml \
--extra-vars='server_path_postgres_dump=<server-path-to-postgres-dump.sql> postgres_default_import_database=matrix' \
--tags=import-postgres
```

**Notes**:

- `<server-path-to-postgres-dump.sql>` must be a file path to a Postgres dump file on the server (not on your local machine!)
- `postgres_default_import_database` defaults to `matrix`, which is useful for importing multiple databases (for dumps made with `pg_dumpall`). If you're importing a single database (e.g. `synapse`), consider changing `postgres_default_import_database` accordingly


## Troubleshooting

### Table Ownership
A table ownership issue can occur if you are importing from a Synapse installation which was both:

 - migrated from SQLite to Postgres, and
 - used a username other than 'synapse'

In this case you may run into the following error during the import task:

```
"ERROR:  role \"synapse_user\" does not exist"
```

where `synapse_user` is the database username from the previous Synapse installation.

This can be verified by examining the dump for ALTER TABLE statements which set OWNER TO that username:

```Shell
$ grep "ALTER TABLE" homeserver.sql
ALTER TABLE public.access_tokens OWNER TO synapse_user;
ALTER TABLE public.account_data OWNER TO synapse_user;
ALTER TABLE public.account_data_max_stream_id OWNER TO synapse_user;
ALTER TABLE public.account_validity OWNER TO synapse_user;
ALTER TABLE public.application_services_state OWNER TO synapse_user;
...
```

It can be worked around by changing the username to `synapse`, for example by using `sed`:

```Shell
$ sed -i "s/OWNER TO synapse_user;/OWNER TO synapse;/g" homeserver.sql
```

This uses sed to perform an 'in-place' (`-i`) replacement globally (`/g`), searching for `synapse_user` and replacing with `synapse` (`s/synapse_user/synapse`). If your database username was different, change `synapse_user` to that username instead. Expand search/replace statement as shown in example above, in case of old user name like `matrix` - replacing `matrix` only would... well - you can imagine.

Note that if the previous import failed with an error it may have made changes which are incompatible with re-running the import task right away; if you do so it may fail with an error such as:

```
ERROR:  relation \"access_tokens\" already exists
```

### Repeat import

In this case you can use the command suggested in the import task to clear the database before retrying the import:

```Shell
# systemctl stop matrix-postgres
# rm -rf /matrix/postgres/data/*
# systemctl start matrix-postgres
```

Now on your local machine run `ansible-playbook -i inventory/hosts setup.yml --tags=setup-postgres` to prepare the database roles etc.

If not, you probably get this error. `synapse` is the correct table owner, but the role is missing in database.
```
"ERROR:  role synapse does not exist"
```

Once the database is clear and the ownership of the tables has been fixed in the SQL file, the import task should succeed.
Check, if `--dbname` is set to `synapse` (not `matrix`) and replace paths (or even better, copy this line from your terminal)

```
/usr/bin/env docker run --rm --name matrix-postgres-import --log-driver=none --user=998:1001 --cap-drop=ALL --network=matrix --env-file=/matrix/postgres/env-postgres-psql --mount type=bind,src=/migration/synapse_dump.sql,dst=/synapse_dump.sql,ro --entrypoint=/bin/sh docker.io/postgres:15.0-alpine -c "cat /synapse_dump.sql | grep -vE '^(CREATE|ALTER) ROLE (matrix)(;| WITH)' | grep -vE '^CREATE DATABASE (matrix)\s' | psql -v ON_ERROR_STOP=1 -h matrix-postgres --dbname=synapse"
```

### Hints

To open psql terminal run `/matrix/postgres/bin/cli`
