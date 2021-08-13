# Storing Matrix media files on Amazon S3 (optional)

By default, this playbook configures your server to store Synapse's content repository (`media_store`) files on the local filesystem.
If that's alright, you can skip this.

If you'd like to store Synapse's content repository (`media_store`) files on Amazon S3 (or other S3-compatible service),
you can let this playbook configure [Goofys](https://github.com/kahing/goofys) for you.

Using a Goofys-backed media store works, but performance may not be ideal. If possible, try to use a region which is close to your Matrix server.

If you'd like to move your locally-stored media store data to Amazon S3 (or another S3-compatible object store), we also provide some migration instructions below.


## Amazon S3

You'll need an Amazon S3 bucket and some IAM user credentials (access key + secret key) with full write access to the bucket. Example security policy:

```json
{
	"Version": "2012-10-17",
	"Statement": [
		{
			"Sid": "Stmt1400105486000",
			"Effect": "Allow",
			"Action": [
				"s3:*"
			],
			"Resource": [
				"arn:aws:s3:::your-bucket-name",
				"arn:aws:s3:::your-bucket-name/*"
			]
		}
	]
}
```

You then need to enable S3 support in your configuration file (`inventory/host_vars/matrix.<your-domain>/vars.yml`).
It would be something like this:

```yaml
matrix_s3_media_store_enabled: true
matrix_s3_media_store_bucket_name: "your-bucket-name"
matrix_s3_media_store_aws_access_key: "access-key-goes-here"
matrix_s3_media_store_aws_secret_key: "secret-key-goes-here"
matrix_s3_media_store_region: "eu-central-1"
```


## Using other S3-compatible object stores

You can use any S3-compatible object store by **additionally** configuring these variables:

```yaml
matrix_s3_media_store_custom_endpoint_enabled: true
# Example: "https://storage.googleapis.com"
matrix_s3_media_store_custom_endpoint: "your-custom-endpoint"
```

### Backblaze B2

To use [Backblaze B2](https://www.backblaze.com/b2/cloud-storage.html):

- create a new **private** bucket through its user interface (you can call it something like `matrix-DOMAIN-media-store`)
- note the **Endpoint** for your bucket (something like `s3.us-west-002.backblazeb2.com`)
- adjust its lifecycle rules to use the following **custom** rules:
  - File Path: *empty value*
  - Days Till Hide: *empty value*
  - Days Till Delete: `1`
- go to [App Keys](https://secure.backblaze.com/app_keys.htm) and use the **Add a New Application Key** to create a new one
  - restrict it to the previously created bucket (e.g. `matrix-DOMAIN-media-store`)
  - give it *Read & Write* access

Copy the `keyID` and `applicationKey`.

You need the following *additional* playbook configuration (on top of what you see above):

```yaml
matrix_s3_media_store_bucket_name: "YOUR_BUCKET_NAME_GOES_HERE"
matrix_s3_media_store_aws_access_key: "YOUR_keyID_GOES_HERE"
matrix_s3_media_store_aws_secret_key: "YOUR_applicationKey_GOES_HERE"
matrix_s3_media_store_custom_endpoint_enabled: true
matrix_s3_media_store_custom_endpoint: "https://s3.us-west-002.backblazeb2.com" # this may be different for your bucket
```

If you have local media store files and wish to migrate to Backblaze B2 subsequently, follow our [migration guide to Backblaze B2](#migrating-to-backblaze-b2) below instead of applying this configuration as-is.


## Migrating from local filesystem storage to S3

It's a good idea to [make a complete server backup](faq.md#how-do-i-backup-the-data-on-my-server) before migrating your local media store to an S3-backed one.

Follow one of the guides below for a migration path from a locally-stored media store to one stored on S3-compatible storage:

- [Migrating to any S3-compatible storage (universal, but likely slow)](#migrating-to-any-s3-compatible-storage-universal-but-likely-slow)
- [Migrating to Backblaze B2](#migrating-to-backblaze-b2)

### Migrating to any S3-compatible storage (universal, but likely slow)

It's a good idea to [make a complete server backup](faq.md#how-do-i-backup-the-data-on-my-server) before doing this.

1. Proceed with the steps below without stopping Matrix services

2. Start by adding the base S3 configuration in your `vars.yml` file (seen above, may be different depending on the S3 provider of your choice)

3. In addition to the base configuration you see above, add this to your `vars.yml` file:

```yaml
matrix_s3_media_store_path: /matrix/s3-media-store
```

This enables S3 support, but mounts the S3 storage bucket to `/matrix/s3-media-store` without hooking it to your homeserver yet. Your homeserver will still continue using your local filesystem for its media store.

5. Run the playbook to apply the changes: `ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start`

6. Do an **initial sync of your files** by running this **on the server** (it may take a very long time):

```sh
sudo -u matrix -- rsync --size-only --ignore-existing -avr /matrix/synapse/storage/media-store/. /matrix/s3-media-store/.
```

You may need to install `rsync` manually.

7. Stop all Matrix services (`ansible-playbook -i inventory/hosts setup.yml --tags=stop`)

8. Start the S3 service by running this **on the server**: `systemctl start matrix-goofys`

9. Sync the files again by re-running the `rsync` command you see in step #6

10. Stop the S3 service by running this **on the server**: `systemctl stop matrix-goofys`

11. Get the old media store out of the way by running this command on the server:

```sh
mv /matrix/synapse/storage/media-store /matrix/synapse/storage/media-store-local-backup
```

12. Remove the `matrix_s3_media_store_path` configuration from your `vars.yml` file (undoing step #3 above)

13. Run the playbook: `ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start`

14. You're done! Verify that loading existing (old) media files works and that you can upload new ones.

15. When confident that it all works, get rid of the local media store directory: `rm -rf /matrix/synapse/storage/media-store-local-backup`


### Migrating to Backblaze B2

It's a good idea to [make a complete server backup](faq.md#how-do-i-backup-the-data-on-my-server) before doing this.

1. While all Matrix services are running, run the following command on the server:

(you need to adjust the 3 `--env` line below with your own data)

```sh
docker run -it --rm -w /work \
--env='B2_KEY_ID=YOUR_KEY_GOES_HERE' \
--env='B2_KEY_SECRET=YOUR_SECRET_GOES_HERE' \
--env='B2_BUCKET_NAME=YOUR_BUCKET_NAME_GOES_HERE' \
-v /matrix/synapse/storage/media-store/:/work \
--entrypoint=/bin/sh \
docker.io/tianon/backblaze-b2:2.1.0 \
-c 'b2 authorize-account $B2_KEY_ID $B2_KEY_SECRET > /dev/null && b2 sync /work/ b2://$B2_BUCKET_NAME'
```

This is some initial file sync, which may take a very long time.

2. Stop all Matrix services (`ansible-playbook -i inventory/hosts setup.yml --tags=stop`)

3. Run the command from step #1 again.

Doing this will sync any new files that may have been created locally in the meantime.

Now that Matrix services aren't running, we're sure to get Backblaze B2 and your local media store fully in sync.

4. Get the old media store out of the way by running this command on the server:

```sh
mv /matrix/synapse/storage/media-store /matrix/synapse/storage/media-store-local-backup
```

5. Put the [Backblaze B2 settings seen above](#backblaze-b2) in your `vars.yml` file

6. Run the playbook: `ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start`

7. You're done! Verify that loading existing (old) media files works and that you can upload new ones.

8. When confident that it all works, get rid of the local media store directory: `rm -rf /matrix/synapse/storage/media-store-local-backup`
