# Matrix (An open network for secure, decentralized communication) server setup using Ansible and Docker

## Purpose

This Ansible playbook is meant to easily let you run your own [Matrix](http://matrix.org/) homeserver.

That is, it lets you join the Matrix network with your own `@<username>:<your-domain>` identifier, all hosted on your own server.

Using this playbook, you can get the following services configured on your server:

- a [Matrix Synapse](https://github.com/matrix-org/synapse) homeserver - storing your data and managing your presence in the [Matrix](http://matrix.org/) network

- (optional) [Amazon S3](https://aws.amazon.com/s3/) storage for your Matrix Synapse's content repository (`media_store`) files using [Goofys](https://github.com/kahing/goofys)

- (optional default) [PostgreSQL](https://www.postgresql.org/) database for Matrix Synapse. [Using an external PostgreSQL server](configuring-playbook-external-postgres.md) is also possible.

- a [coturn](https://github.com/coturn/coturn) STUN/TURN server for WebRTC audio/video calls

- free [Let's Encrypt](https://letsencrypt.org/) SSL certificate, which secures the connection to the Synapse server and the Riot web UI

- (optional default) a [Riot](https://riot.im/) web UI, which is configured to connect to your own Matrix Synapse server by default

- (optional default) an [mxisd](https://github.com/kamax-io/mxisd) Matrix Identity server

- (optional default) a [Postfix](http://www.postfix.org/) mail server, through which all Matrix services send outgoing email (can be configured to relay through another SMTP server)

- (optional default) an [nginx](http://nginx.org/) web server, listening on ports 80 and 443 - standing in front of all the other services. Using your own webserver [is possible](#using-your-own-webserver-instead-of-this-playbooks-nginx-proxy-optional)

- (optional) the [matrix-synapse-rest-auth](https://github.com/kamax-io/matrix-synapse-rest-auth) REST authentication password provider module

Basically, this playbook aims to get you up-and-running with all the basic necessities around Matrix, without you having to do anything else.


## What's different about this Ansible playbook?

This is similar to the [EMnify/matrix-synapse-auto-deploy](https://github.com/EMnify/matrix-synapse-auto-deploy) Ansible deployment, but:

- this one is a complete Ansible playbook (instead of just a role), so it's **easier to run** - especially for folks not familiar with Ansible

- this one installs and hooks together **a lot more Matrix-related services** for you (see above)

- this one **can be re-ran many times** without causing trouble

- works on both **CentOS** (7.0+) and Debian-based distributions (**Debian** 9/Stretch+, **Ubuntu** 16.04+)

- this one installs everything in a single directory (`/matrix` by default) and **doesn't "contaminate" your server** with files all over the place

- this one **doesn't necessarily take over** ports 80 and 443. By default, it sets up nginx for you there, but you can also [use your own webserver](docs/configuring-playbook-own-webserver.md)

- this one **runs everything in Docker containers**, so it's likely more predictable and less fragile (see [Docker images used by this playbook](#docker-images-used-by-this-playbook))

- this one retrieves and automatically renews free [Let's Encrypt](https://letsencrypt.org/) **SSL certificates** for you

- this one optionally can store the `media_store` content repository files on [Amazon S3](https://aws.amazon.com/s3/) (but defaults to storing files on the server's filesystem)

- this one optionally **allows you to use an external PostgreSQL server** for Matrix Synapse's database (but defaults to running one in a container)


## Installation

To configure and install Matrix on your own server, follow the [README in the docs/ directory](docs/README.md).


## Changes

This playbook evolves over time, sometimes with backward-incompatible changes.

When updating the playbook, refer to [the changelog](CHANGELOG.md) to catch up with what's new.


## Docker images used by this playbook

This playbook sets up your server using the following Docker images:

- [matrixdotorg/synapse](https://hub.docker.com/r/matrixdotorg/synapse/) - the official [Matrix Synapse](https://github.com/matrix-org/synapse) server

- [instrumentisto/coturn](https://hub.docker.com/r/instrumentisto/coturn/) - the [Coturn](https://github.com/coturn/coturn) STUN/TURN server

- [avhost/docker-matrix-riot](https://hub.docker.com/r/avhost/docker-matrix-riot/) - the [Riot.im](https://about.riot.im/) web client (optional)

- [kamax/mxisd](https://hub.docker.com/r/kamax/mxisd/) - the [mxisd](https://github.com/kamax-io/mxisd) Matrix Identity server (optional)

- [postgres](https://hub.docker.com/_/postgres/) - the [Postgres](https://www.postgresql.org/) database server (optional)

- [cloudproto/goofys](https://hub.docker.com/r/cloudproto/goofys/) - the [Goofys](https://github.com/kahing/goofys) Amazon [S3](https://aws.amazon.com/s3/) file-system-mounting program (optional)

- [panubo/postfix](https://hub.docker.com/r/panubo/postfix/) - the [Postfix](http://www.postfix.org/) email server (optional)

- [nginx](https://hub.docker.com/_/nginx/) - the [nginx](http://nginx.org/) web server (optional)


## Deficiencies

This Ansible playbook can be improved in the following ways:

- setting up automatic backups to one or more storage providers


## Support

Matrix room: [#matrix-docker-ansible-deploy:devture.com](https://matrix.to/#/#matrix-docker-ansible-deploy:devture.com)

Github issues: [spantaleev/matrix-docker-ansible-deploy/issues](https://github.com/spantaleev/matrix-docker-ansible-deploy/issues)
