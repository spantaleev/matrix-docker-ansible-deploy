# Matrix (An open network for secure, decentralized communication) server setup using Ansible and Docker

## Purpose

This Ansible playbook is meant to easily let you run your own [Matrix](http://matrix.org/) homeserver.

That is, it lets you join the Matrix network with your own `@<username>:<your-domain>` identifier, all hosted on your own server.

Using this playbook, you can get the following services configured on your server:

- a [Matrix Synapse](https://github.com/matrix-org/synapse) homeserver - storing your data and managing your presence in the [Matrix](http://matrix.org/) network

- (optional) [Amazon S3](https://aws.amazon.com/s3/) storage for your Matrix Synapse's content repository (`media_store`) files using [s3fs-fuse](https://github.com/s3fs-fuse/s3fs-fuse)

- (optional default) [PostgreSQL](https://www.postgresql.org/) database for Matrix Synapse - providing better performance than the default [SQLite](https://sqlite.org/) database. Using an external PostgreSQL server [is possible](#using-an-external-postgresql-server-optional) as well

- a [STUN/TURN server](https://github.com/coturn/coturn) for WebRTC audio/video calls

- (optional default) a [Riot](https://riot.im/) web UI, which is configured to connect to your own Matrix Synapse server by default

- free [Let's Encrypt](https://letsencrypt.org/) SSL certificate, which secures the connection to the Synapse server and the Riot web UI

- (optional default) an [nginx](http://nginx.org/) web server, listening on ports 80 and 443 - standing in front of all the other services. Using your own webserver [is possible](#using-your-own-webserver-instead-of-this-playbooks-nginx-proxy-optional)

Basically, this playbook aims to get you up-and-running with all the basic necessities around Matrix, without you having to do anything else.


## What's different about this Ansible playbook?

This is similar to the [EMnify/matrix-synapse-auto-deploy](https://github.com/EMnify/matrix-synapse-auto-deploy) Ansible deployment, but:

- this one is a complete Ansible playbook (instead of just a role), so it should be **easier to run** - especially for folks not familiar with Ansible

- this one **can be re-ran many times** without causing trouble

- works on both **CentOS** (7.0+) and Debian-based distributions (**Debian** 9/Stretch+, **Ubuntu** 16.04+)

- this one keeps mostly everything in a single directory (`/matrix` by default) and **doesn't "contaminate" your server** with files all over the place

- this one **doesn't necessarily take over** ports 80 and 443. By default, it sets up nginx for you there, but you can disable that and configure your own webserver (proxy)

- this one **runs everything in Docker containers** (like [silviof/docker-matrix](https://hub.docker.com/r/silviof/docker-matrix/) and [silviof/matrix-riot-docker](https://hub.docker.com/r/silviof/matrix-riot-docker/)), so it's likely more predictable

- this one retrieves and automatically renews free [Let's Encrypt](https://letsencrypt.org/) **SSL certificates** for you

- this one optionally can store the `media_store` content repository files on [Amazon S3](https://aws.amazon.com/s3/) (but defaults to storing files on the server's filesystem)

- this one optionally **allows you to use an external PostgreSQL server** for Matrix Synapse's database (but defaults to running one in a container)

Special thanks goes to:

- [EMnify/matrix-synapse-auto-deploy](https://github.com/EMnify/matrix-synapse-auto-deploy) - for the inspiration

- [silviof/docker-matrix](https://hub.docker.com/r/silviof/docker-matrix/) - for packaging Matrix Synapse as a Docker image

- [silviof/matrix-riot-docker](https://hub.docker.com/r/silviof/matrix-riot-docker/) - for packaging Riot as a Docker image


## Prerequisites

- **CentOS** (7.0+), **Debian** (9/Stretch+) or **Ubuntu** (16.04+) server. This playbook can take over your whole server or co-exist with other services that you have there.

- the [Ansible](http://ansible.com/) program, which is used to run this playbook and configures everything for you

- properly configured DNS SRV record for `<your-domain>` (details in [Configuring DNS](#configuring-dns) below)

- `matrix.<your-domain>` domain name pointing to your new server - this is where the Matrix Synapse server will live (details in [Configuring DNS](#configuring-dns) below)

- `riot.<your-domain>` domain name pointing to your new server - this is where the Riot web UI will live (details in [Configuring DNS](#configuring-dns) below)

- some TCP/UDP ports open. This playbook configures the server's internal firewall for you. In most cases, you don't need to do anything special. But **if your server is running behind another firewall**, you'd need to open these ports: `80/tcp` (HTTP webserver), `443/tcp` (HTTPS webserver), `3478/tcp`  (STUN over TCP), `3478/udp` (STUN over UDP), `8448/tcp` (Matrix federation HTTPS webserver), `49152-49172/udp` (TURN over UDP).


## Configuring DNS

In order to use an identifier like `@<username>:<your-domain>`, you don't actually need
to install anything on the actual `<your-domain>` server.

All services created by this playbook are meant to be installed on their own server (such as `matrix.<your-domain>`).

In order to do this, you must first instruct the Matrix network of this by setting up a DNS SRV record (think of it as a "redirect").
The SRV record should look like this:
- Name: `_matrix._tcp` (use this text as-is)
- Content: `10 0 8448 matrix.<your-domain>` (replace `<your-domain>` with your own)

Once you've set up this DNS SRV record, you should create 2 other domain names (`matrix.<your-domain>` and `riot.<your-domain>`) and point both of them to your new server's IP address (DNS `A` record or `CNAME` is fine).

This playbook can then install all the services on that new server and you'll be able to join the Matrix network as `@<username>:<your-domain>`, even though everything is installed elsewhere (not on `<your-domain>`).


## Configuration

Once you have your server and you have [configured your DNS records](#configuring-dns), you can proceed with configuring this playbook, so that it knows what to install and where.

You can follow these steps:

- create a directory to hold your configuration (`mkdir inventory/matrix.<your-domain>`)

- copy the sample configuration file (`cp examples/host-vars.yml inventory/matrix.<your-domain>/vars.yml`)

- edit the configuration file (`inventory/matrix.<your-domain>/vars.yml`) to your liking. You may also take a look at `roles/matrix-server/defaults.main.yml` and see if there's something you'd like to copy over and override in your `vars.yml` configuration file.

- copy the sample inventory hosts file (`cp examples/hosts inventory/hosts`)

- edit the inventory hosts file (`inventory/hosts`) to your liking


## Amazon S3 configuration (optional)

By default, this playbook configures your server to store Matrix Synapse's content repository (`media_store`) files on the local filesystem.
If that's alright, you can skip ahead.

If you'd like to store Matrix Synapse's content repository (`media_store`) files on Amazon S3,
you can let this playbook configure [s3fs-fuse](https://github.com/s3fs-fuse/s3fs-fuse) for you.

You'll need an Amazon S3 bucket and some IAM user credentials (access key + secret key) with full write access to the bucket. Example security policy:

```
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

You then need to enable S3 support in your configuration file (`inventory/matrix.<your-domain>/vars.yml`).
It would be something like this:

```
matrix_s3_media_store_enabled: true
matrix_s3_media_store_bucket_name: "your-bucket-name"
matrix_s3_media_store_aws_access_key: "access-key-goes-here"
matrix_s3_media_store_aws_secret_key: "secret-key-goes-here"
```


## Using an external PostgreSQL server (optional)

By default, this playbook would set up a PostgreSQL database server on your machine, running in a Docker container.
If that's alright, you can skip ahead.

If you'd like to use an external PostgreSQL server that you manage, you can edit your configuration file  (`inventory/matrix.<your-domain>/vars.yml`).
It should be something like this:

```
matrix_postgres_use_external: true
matrix_postgres_connection_hostname: "your-postgres-server-hostname"
matrix_postgres_connection_username: "your-postgres-server-username"
matrix_postgres_connection_password: "your-postgres-server-password"
matrix_postgres_db_name: "your-postgres-server-database-name"
```

The database (as specified in `matrix_postgres_db_name`) must exist and be accessible with the given credentials.
It must be empty or contain a valid Matrix Synapse database. If empty, Matrix Synapse would populate it the first time it runs.


## Using your own webserver, instead of this playbook's nginx proxy (optional)

By default, this playbook installs its own nginx webserver (in a Docker container) which listens on ports 80 and 443.
If that's alright, you can skip ahead.

If you don't want this playbook's nginx webserver to take over your server's 80/443 ports like that,
and you'd like to use your own webserver (be it nginx, Apache, Varnish Cache, etc.), you can.

All it takes is editing your configuration file (`inventory/matrix.<your-domain>/vars.yml`):

```
matrix_nginx_proxy_enabled: false
```

**Note**: even if you do this, in order [to install](#installing), this playbook still expects port 80 to be available. **Please manually stop your other webserver while installing**. You can start it back again afterwards.

**If your own webserver is nginx**, you can most likely directly use the config files installed by this playbook at: `/matrix/nginx-proxy/conf.d`. Just include them in your `nginx.conf` like this: `include /matrix/nginx-proxy/conf.d/*.conf;`

**If your own webserver is not nginx**, you can still take a look at the sample files in `/matrix/nginx-proxy/conf.d`, and:

- ensure you set up (separate) vhosts that proxy for both Riot (`localhost:8765`) and Matrix Synapse (`localhost:8008`)

- ensure that the `/.well-known/acme-challenge` location for each "port=80 vhost" is an alias to the `/matrix/ssl/run/acme-challenge` directory (for automated SSL renewal to work)

- ensure that you restart/reload your webserver once in a while, so that renewed SSL certificates would take effect (once a month should be enough)


## Installing

Once you have your server and you have [configured your DNS records](#configuring-dns), you can proceed with installing.

To make use of this playbook, you should invoke the `setup.yml` playbook multiple times, with different tags.


### Configuring a server

Run this as-is to set up a server.
This doesn't start any services just yet (another step does this later - below).
Feel free to re-run this any time you think something is off with the server configuration.

	ansible-playbook -i inventory/hosts setup.yml --tags=setup-main


### Restoring an existing SQLite database (from another installation)

Run this if you'd like to import your database from a previous default installation of Matrix Synapse.
(don't forget to import your `media_store` files as well - see below).

While this playbook always sets up PostgreSQL, by default, a Matrix Synapse installation would run
using an SQLite database.

If you have such a Matrix Synapse setup and wish to migrate it here (and over to PostgreSQL), this command is for you.

Run this command (make sure to replace `<local-path-to-homeserver.db>` with a file path on your local machine):

	ansible-playbook -i inventory/hosts setup.yml --extra-vars='local_path_homeserver_db=<local-path-to-homeserver.db>' --tags=import-sqlite-db

**Note**: `<local-path-to-homeserver.db>` must be a file path to a `homeserver.db` file on your local machine (not on the server!). This file is copied to the server and imported.


### Restoring `media_store` data files from an existing installation

Run this if you'd like to import your `media_store` files from a previous installation of Matrix Synapse.

Run this command (make sure to replace `<local-path-to-media_store>` with a path on your local machine):

	ansible-playbook -i inventory/hosts setup.yml --extra-vars='local_path_media_store=<local-path-to-media_store>' --tags=import-media-store

**Note**: `<local-path-to-media_store>` must be a file path to a `media_store` directory on your local machine (not on the server!). This directory's contents are then copied to the server.


### Starting the services

Run this as-is to start all the services and to ensure they'll run on system startup later on.

	ansible-playbook -i inventory/hosts setup.yml --tags=start


### Registering a user

Run this to create a new user account on your Matrix server.

You can do it via this Ansible playbook (make sure to edit the `<your-username>` and `<your-password>` part below):

	ansible-playbook -i inventory/hosts setup.yml --extra-vars='username=<your-username> password=<your-password> admin=<yes|no>' --tags=register-user

**or** using the command-line after **SSH**-ing to your server (requires that [all services have been started](#starting-the-services)):

	/usr/local/bin/matrix-synapse-register-user <your-username> <your-password> <admin access: 0 or 1>

**Note**: `<your-username>` is just a plain username (like `john`), not your full `@<username>:<your-domain>` identifier.


## Uninstalling

**Note**: If you have some trouble with your installation configuration, you can just re-run the playbook and it will try to set things up again. You don't need to uninstall and install fresh.

However, if you've installed this on some server where you have other stuff you wish to preserve, and now want get rid of Matrix, it's enough to do these:

- ensure all Matrix services are stopped (`systemctl stop 'matrix*'`)

- delete the Matrix-related systemd .service files (`rm -f /etc/systemd/system/matrix*`) and reload systemd (`systemctl daemon-reload`)

- delete all Matrix-related cronjobs (`rm -f /etc/cron.d/matrix*'`)

- delete some helper scripts (`rm -f /usr/local/bin/matrix*`)

- delete some cached Docker images (or just delete them all: `docker rmi $(docker images -aq)`)

- uninstall Docker itself, if necessary

- delete the `/matrix` directory (`rm -rf /matrix`)


## Deficiencies

This Ansible playbook can be improved in the following ways:

- setting up automatic backups to one or more storage providers
