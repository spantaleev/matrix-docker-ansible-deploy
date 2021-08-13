# Importing an existing SQLite database from another Synapse installation (optional)

Run this if you'd like to import your database from a previous default installation of Synapse.
(don't forget to import your `media_store` files as well - see [the importing-synapse-media-store guide](importing-synapse-media-store.md)).

While this playbook always sets up PostgreSQL, by default a Synapse installation would run
using an SQLite database.

If you have such a Synapse setup and wish to migrate it here (and over to PostgreSQL), this command is for you.


## Prerequisites

Before doing the actual import, **you need to upload your SQLite database file to the server** (any path is okay).


## Importing

Run this command (make sure to replace `<server-path-to-homeserver.db>` with a file path on your server):

	ansible-playbook -i inventory/hosts setup.yml --extra-vars='server_path_homeserver_db=<server-path-to-homeserver.db>' --tags=import-synapse-sqlite-db

**Notes**:

- `<server-path-to-homeserver.db>` must be a file path to a `homeserver.db` **file on the server** (not on your local machine!).
- if the SQLite database is from an older version of Synapse, the **importing procedure may run migrations on it to bring it up to date**. That is, your SQLite database file may get modified and become unusable with your older Synapse version. Keeping a copy of the original is probably wise.
