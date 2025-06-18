<!--
SPDX-FileCopyrightText: 2018 - 2023 Slavi Pantaleev
SPDX-FileCopyrightText: 2023 Michael Hollister
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Storing Synapse media files on Amazon S3 or another compatible Object Storage (optional)

By default, this playbook configures your server to store Synapse's content repository (`media_store`) files on the local filesystem. If that's okay, you can skip this document.

As an alternative to storing media files on the local filesystem, you can store them on [Amazon S3](https://aws.amazon.com/s3/) or another S3-compatible object store.

You can do this either by sticking to Synapse's media repository and making that use S3 (read below for this method), or by switching to an external media storage implementation like [matrix-media-repo](configuring-playbook-matrix-media-repo.md).

First, [choose an Object Storage provider](#choosing-an-object-storage-provider).

Then, [create the S3 bucket](#bucket-creation-and-security-configuration).

Finally, [set up S3 storage for Synapse](#setting-up) (with [Goofys](configuring-playbook-s3-goofys.md), [synapse-s3-storage-provider](configuring-playbook-synapse-s3-storage-provider.md), or use s3 datastore with the [matrix-media-repo](https://docs.t2bot.io/matrix-media-repo/configuration/s3-datastore.html)).

## Choosing an Object Storage provider

You can create [Amazon S3](https://aws.amazon.com/s3/) or another S3-compatible object storage like [Backblaze B2](https://www.backblaze.com/b2/cloud-storage.html), [Wasabi](https://wasabi.com), [Digital Ocean Spaces](https://www.digitalocean.com/products/spaces), [Storj](https://storj.io), etc.

Amazon S3 and Backblaze B2 are pay-as-you with no minimum charges for storing too little data. Note that Backblaze egress is free, but for only certain users for up to 3x the amount of data stored. Beyond that you will pay $0.01/GB of egress.

Wasabi has a minimum charge of 1TB if you're storing less than 1TB, which becomes expensive if you need to store less data than that. Likewise, Digital Ocean Spaces has also a minimum charge of 250GB ($5/month as of 2022-10). Though Storj does not set minimum amount of data to be stored, it also charges $5 minimum monthly usage fee since July 1, 2025, if your monthly usage (storage, bandwidth, and segments) totals less than $5.

Here are some of the important aspects of choosing the right provider:

- if a provider is a company you like and trust (or dislike less than the others)
- if a provider implements end-to-end encryption of your data
- if a provider has a data region close to your Matrix server (if it's farther away, high latency may cause slowdowns)
- if a provider's infrastructure such as data center is centralized or distributed
- if a provider's price model is transparent (whether it includes hidden costs like minimum charge, minimum storage term, etc.)
- if a provider has free or cheap egress fee (in case you need to get the data out often, for some reason) — likely not too important for the common use-case

## Bucket creation and Security Configuration

Now that you've [chosen an Object Storage provider](#choosing-an-object-storage-provider), you need to create a storage bucket.

How you do this varies from provider to provider, with Amazon S3 being the most complicated due to its vast number of services and complicated security policies.

Below, we provider some guides for common providers. If you don't see yours, look at the others for inspiration or read some guides online about how to create a bucket. Feel free to contribute to this documentation with an update!

## Amazon S3

You'll need an Amazon S3 bucket and some IAM user credentials (access key + secret key) with full write access to the bucket. Example IAM security policy:

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

**Note**: This policy needs to be attached to an IAM user created from the **Security Credentials** menu. This is not a **Bucket Policy**.

## Backblaze B2

To use [Backblaze B2](https://www.backblaze.com/b2/cloud-storage.html) you first need to sign up.

You [can't easily change which region (US, Europe) your Backblaze account stores files in](https://old.reddit.com/r/backblaze/comments/hi1v90/make_the_choice_for_the_b2_data_center_region/), so make sure to carefully choose the region when signing up (hint: it's a hard to see dropdown below the username/password fields in the signup form).

After logging in to Backblaze:

- create a new **private** bucket through its user interface (you can call it something like `matrix-example-media-store`)
- note the **Endpoint** for your bucket (something like `s3.us-west-002.backblazeb2.com`).
- adjust its Lifecycle Rules to: Keep only the last version of the file
- go to [App Keys](https://secure.backblaze.com/app_keys.htm) and use the **Add a New Application Key** to create a new one
  - restrict it to the previously created bucket (e.g. `matrix-example-media-store`)
  - give it *Read & Write* access

The `keyID` value is your **Access Key** and `applicationKey` is your **Secret Key**.

For configuring [Goofys](configuring-playbook-s3-goofys.md) or [s3-synapse-storage-provider](configuring-playbook-synapse-s3-storage-provider.md) you will need:

- **Endpoint URL** — this is the  **Endpoint** value you saw above, but prefixed with `https://`
- **Region** — use the value you see in the Endpoint (e.g. `us-west-002`)
- **Storage Class** — use `STANDARD`. Backblaze B2 does not have different storage classes, so it doesn't make sense to use any other value.

## Other providers

For other S3-compatible providers, you most likely just need to create an S3 bucket and get some credentials (access key and secret key) for accessing the bucket in a read/write manner. You may not need to configure security policies, etc.

For details about setting up a bucket at Storj, please see the instruction [here](https://storj.dev/dcs/getting-started) to get started.

## Setting up

To set up Synapse to store files in S3, follow the instructions for the method of your choice:

- using [synapse-s3-storage-provider](configuring-playbook-synapse-s3-storage-provider.md) (recommended)
- using [Goofys to mount the S3 store to the local filesystem](configuring-playbook-s3-goofys.md)
- using [matrix-media-repo](configuring-playbook-matrix-media-repo.md)
