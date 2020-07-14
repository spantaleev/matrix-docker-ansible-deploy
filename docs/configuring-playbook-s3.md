# Storing Matrix media files on Amazon S3 (optional)

By default, this playbook configures your server to store Synapse's content repository (`media_store`) files on the local filesystem.
If that's alright, you can skip this.

If you'd like to store Synapse's content repository (`media_store`) files on Amazon S3 (or other S3-compatible service),
you can let this playbook configure [Goofys](https://github.com/kahing/goofys) for you.

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
