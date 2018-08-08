# Restoring `media_store` data files from an existing installation (optional)

Run this if you'd like to import your `media_store` files from a previous installation of Matrix Synapse.

Run this command (make sure to replace `<local-path-to-media_store>` with a path on your local machine):

	ansible-playbook -i inventory/hosts setup.yml --extra-vars='local_path_media_store=<local-path-to-media_store>' --tags=import-media-store

**Note**: `<local-path-to-media_store>` must be a file path to a `media_store` directory on your local machine (not on the server!). This directory's contents are then copied to the server.