# Importing an existing Postgres database from another installation (optional)

Run this if you'd like to import your database from a previous installation.
(don't forget to import your Synapse `media_store` files as well - see [the importing-synape-media-store guide](importing-synapse-media-store.md)).


## Prerequisites

For this to work, **the database name in Postgres must match** what this playbook uses.
This playbook uses a Postgres database name of `homeserver` by default (controlled by the `matrix_postgres_db_name` variable).
If your database name differs, be sure to change `matrix_postgres_db_name` to your desired name and to re-run the playbook before proceeding.

The playbook supports importing Postgres dump files in **text** (e.g. `pg_dump > dump.sql`) or **gzipped** formats (e.g. `pg_dump | gzip -c > dump.sql.gz`).

Importing multiple databases (as dumped by `pg_dumpall`) is also supported.

Before doing the actual import, **you need to upload your Postgres dump file to the server** (any path is okay).


## Importing

To import, run this command (make sure to replace `<server-path-to-postgres-dump.sql>` with a file path on your server):

	ansible-playbook -i inventory/hosts setup.yml --extra-vars='server_path_postgres_dump=<server-path-to-postgres-dump.sql>' --tags=import-postgres

**Note**: `<server-path-to-postgres-dump.sql>` must be a file path to a Postgres dump file on the server (not on your local machine!).

## Troubleshooting

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
$ grep "ALTER TABLE" homeserver.sql"
ALTER TABLE public.access_tokens OWNER TO synapse_user;
ALTER TABLE public.account_data OWNER TO synapse_user;
ALTER TABLE public.account_data_max_stream_id OWNER TO synapse_user;
ALTER TABLE public.account_validity OWNER TO synapse_user;
ALTER TABLE public.application_services_state OWNER TO synapse_user;
...
```

It can be worked around by changing the username to `synapse`, for example by using `sed`:

```Shell
$ sed -i "s/synapse_user/synapse/g" homeserver.sql"
```

This uses sed to perform an 'in-place' (`-i`) replacement globally (`/g`), searching for `synapse user` and replacing with `synapse` (`s/synapse_user/synapse`). If your database username was different, change `synapse_user` to that username instead.

Note that if the previous import failed with an error it may have made changes which are incompatible with re-running the import task right away; if you do so it may fail with an error such as:

```
ERROR:  relation \"access_tokens\" already exists
```

In this case you can use the command suggested in the import task to clear the database before retrying the import:

```Shell
# systemctl stop matrix-postgres
# rm -rf /matrix/postgres/data/*
# systemctl start matrix-postgres
```

Once the database is clear and the ownership of the tables has been fixed in the SQL file, the import task should succeed.
