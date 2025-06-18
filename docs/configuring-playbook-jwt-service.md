<!--
SPDX-FileCopyrightText: 2024 wjbeckett
SPDX-FileCopyrightText: 2024 Slavi Pantaleev

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Setting up JWT Service (optional)

The playbook can install and configure [LiveKit JWT Service](https://github.com/element-hq/lk-jwt-service) for you.

LK-JWT-Service is currently used for a single reason: generate JWT tokens with a given identity for a given room, so that users can use them to authenticate against LiveKit SFU.

See the project's [documentation](https://github.com/element-hq/lk-jwt-service/) to learn more.

## Decide on a domain and path

By default, JWT Service is configured to be served:

- on the Matrix domain (`matrix.example.com`), configurable via `matrix_livekit_jwt_service_hostname`
- under a `/livekit-jwt-service` path prefix, configurable via `matrix_livekit_jwt_service_path_prefix`

This makes it easy to set it up, **without** having to adjust your DNS records manually.

## Adjusting DNS records

If you've changed the default hostname, **you may need to adjust your DNS** records accordingly to point to the correct server.

## Adjusting the playbook configuration

Add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
matrix_livekit_jwt_service_enabled: true
```

## Installing

After configuring the playbook and potentially [adjusting your DNS records](#adjusting-dns-records), run the [installation](installing.md) command: `just install-all` or `just setup-all`

## Usage

Once installed, a new `org.matrix.msc4143.rtc_foci` section is added to the Element Web client to point to your JWT service URL (e.g., `https://matrix.example.com/livekit-jwt-service`).

## Additional Information

Refer to the LiveKit JWT-Service documentation for more details on configuring and using JWT Service.
