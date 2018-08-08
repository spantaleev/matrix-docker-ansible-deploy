# Importing an existing SQLite database from another installation (optional)

Run this if you'd like to import your database from a previous default installation of Matrix Synapse.
(don't forget to import your `media_store` files as well - see below).

While this playbook always sets up PostgreSQL, by default a Matrix Synapse installation would run
using an SQLite database.

If you have such a Matrix Synapse setup and wish to migrate it here (and over to PostgreSQL), this command is for you.

Run this command (make sure to replace `<local-path-to-homeserver.db>` with a file path on your local machine):

	ansible-playbook -i inventory/hosts setup.yml --extra-vars='local_path_homeserver_db=<local-path-to-homeserver.db>' --tags=import-sqlite-db

**Note**: `<local-path-to-homeserver.db>` must be a file path to a `homeserver.db` file on your local machine (not on the server!). This file is copied to the server and imported.