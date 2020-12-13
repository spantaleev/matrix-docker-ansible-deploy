# Importing `media_store` data files from an existing Synapse installation (optional)

Run this if you'd like to import your `media_store` files from a previous installation of Synapse.


## Prerequisites

Before doing the actual data restore, **you need to upload your media store directory to the server** (any path is okay).

If you are [Storing Matrix media files on Amazon S3](configuring-playbook-s3.md) (optional), restoring with this tool is not possible right now.
As an alternative, you can perform a manual restore using the [AWS CLI tool](https://aws.amazon.com/cli/) (e.g. `aws s3 sync /path/to/server/media_store/. s3://name-of-bucket/`)

**Note for Mac users**: Due to case-sensitivity issues on certain Mac filesystems (HFS or HFS+), filename corruption may occur if you copy a `media_store` directory to your Mac. If you're transferring a `media_store` directory between 2 servers, make sure you do it directly (from server to server with a tool such as [rsync](https://rsync.samba.org/)), and not by downloading the files to your Mac.


## Importing

Run this command (make sure to replace `<server-path-to-media_store>` with a path on your server):

	ansible-playbook -i inventory/hosts setup.yml --extra-vars='server_path_media_store=<server-path-to-media_store>' --tags=import-synapse-media-store

**Note**: `<server-path-to-media_store>` must be a file path to a `media_store` directory on the server (not on your local machine!).
