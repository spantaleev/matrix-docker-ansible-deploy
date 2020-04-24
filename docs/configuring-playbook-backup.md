# Setting up Matrix Synapse backups (optional)

This playbook installs a weekly cron backup.

## Variable Table 

| Variables | Default | Example |
|-----------|---------|---------|
| matrix_backup_enabled | false | True |
| matrix_backup_bucket | "" | "s3//bucketname/prefix/" |
| matrix_backup_bucket_endpoint | "" | "https://nyc3.digitaloceanspaces.com" |
| matrix_backup_bucket_awscli_docker_image_latest | "amazon/aws-cli:2.0.10" | "amazon/aws-cli:latest" |
| matrix_backup_bucket_key_id | "" | "AKIAQIOAVK3Q4HMXL272" |
| matrix_backup_bucket_key_secret | "" | "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" |
| matrix_backup_rsync_target | "" | ?? |
| matrix_backup_cron_day | "*/7" (Weekly) | "*/2" Biweekly |


## Method 1: Rsync 

??

## Method 2: S3 Compatible object store

Setup: S3 compatible buckets

### S3 compatible services https://en.wikipedia.org/wiki/Amazon_S3#S3_API_and_competing_services

| Service Provider | Costs | Compatibility | Endpoint |
|------------------|-------|---------------|----------|
| AWS  S3 | https://aws.amazon.com/s3/pricing/ | N/A | N/A |
| Digital Ocean Spaces | https://www.digitalocean.com/pricing/#Storage | https://developers.digitalocean.com/documentation/spaces/ | `https://<region>.digitaloceanspaces.com` |
| Azure Blob | https://azure.microsoft.com/en-us/pricing/details/storage/blobs/ | https://cloudblogs.microsoft.com/opensource/2017/11/09/s3cmd-amazon-s3-compatible-apps-azure-storage/  | Requires minio |
| Blackblaze B2 | https://www.backblaze.com/b2/cloud-storage-pricing.html | https://www.backblaze.com/b2/docs/s3_compatible_api.html | `https://s3.<region>.backblazeb2.com/` |
| Google Cloud Storage | https://cloud.google.com/storage/pricing | https://cloud.google.com/storage/docs/interoperability | `https://storage.googleapis.com` |
| Wasbi | https://wasabi.com/s3-compatible-cloud-storage/ | https://wasabi-support.zendesk.com/hc/en-us/articles/115001910791-How-do-I-use-AWS-CLI-with-Wasabi- | `https://s3.wasabisys.com` |
| IBM Cloud Object Storage | https://cloud.ibm.com/catalog/services/cloud-object-storage | https://cloud.ibm.com/docs/cloud-object-storage?topic=cloud-object-storage-aws-cli | `s3.<region>.cloud-object-storage.appdomain.cloud` |
| Linode Object Storage | https://www.linode.com/pricing/#row--storage | https://www.linode.com/docs/platform/object-storage/bucket-versioning/ | `http://<region>.linodeobjects.com` |
| Dream Hosts | https://www.dreamhost.com/cloud/storage/ | https://help.dreamhost.com/hc/en-us/articles/360022654971-AWS-CLI-commands-to-manage-your-DreamObjects-data | https://objects-us-east-1.dream.io |

### Preparation

Select a S3 compatible provider. 
Create S3 Bucket
Create a specialized IAM users with the permissions recorded below. For users who deployed their postgres instance on an AWS EC2, you can create attachable IAM roles instead for password less S3 access.




Backup-acl.json
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor1",
            "Effect": "Allow",
            "Action": "s3:ListBucket",
            "Resource": "arn:aws:s3:::<your-bucket>",
            "Condition": {
                "ForAnyValue:IpAddress": {
                    "aws:SourceIp": [
                        "<Restrict-IP>"
                    ]
                }
            }
        },
        {
            "Sid": "VisualEditor3",
            "Effect": "Allow",
            "Action": [
                "s3:PutObject",
                "s3:AbortMultipartUpload"
            ],
            "Resource": [
                "arn:aws:s3:::<your-bucket>/matrix/*",
                "arn:aws:s3:::<your-bucket>/matrix"
            ],
            "Condition": {
                "IpAddress": {
                    "aws:SourceIp": "<Restrict-IP>"
                }
            }
        }
    ]
}
```

Restore-acl.json
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor1",
            "Effect": "Allow",
            "Action": "s3:ListBucket",
            "Resource": "arn:aws:s3:::<your-bucket>",
            "Condition": {
                "ForAnyValue:IpAddress": {
                    "aws:SourceIp": [
                        "<Restrict-IP>"
                    ]
                }
            }
        },
        {
            "Sid": "VisualEditor3",
            "Effect": "Allow",
            "Action": [
                "s3:PutObject",
                "s3:GetObject",
                "s3:AbortMultipartUpload"
            ],
            "Resource": [
                "arn:aws:s3:::<your-bucket>/matrix/*",
                "arn:aws:s3:::<your-bucket>/matrix"
            ],
            "Condition": {
                "IpAddress": {
                    "aws:SourceIp": "<Restrict-IP>"
                }
            }
        }
    ]
}
```

### Deploy Matrix S3 Backup
#### Using AWS IAM Role
Set `matrix_backup_enabled` and `matrix_backup_bucket`.
#### Using AWS IAM User
Set  `matrix_backup_enabled`, `matrix_backup_bucket`, `matrix_backup_bucket_key_id`, and `matrix_backup_bucket_key_secret`

#### S3 Compatible Services
Set  `matrix_backup_enabled`, `matrix_backup_bucket`, `matrix_backup_bucket_key_id`, `matrix_backup_bucket_key_secret`, and `matrix_backup_bucket_endpoint`

#### Run
```bash
ansible-playbook -i inventory/hosts setup.yml --tags=setup-matrix-backup,start
```