# Setting up Matrix User Verification Service (optional)

The playbook can install and configure [Matrix User Verification Service](https://github.com/matrix-org/matrix-user-verification-service) (hereafter: UVS) for you.

See the project's [documentation](https://github.com/matrix-org/matrix-user-verification-service/blob/master/README.md) to learn what it does and why it might be useful to you.

Currently, the main purpose of this role is to allow Jitsi to authenticate Matrix users and check if they are authorized to join a conference. If the Jitsi server is also configured by this playbook, all plugging of variables and secrets is handled in `group_vars/matrix_servers`.

## What does it do?

UVS can be used to verify two claims:

* (A) Whether a given OpenID token is valid for a given server and
* (B) whether a user is member of a given room and the corresponding PowerLevel

Verifying an OpenID token ID done by finding the corresponding Homeserver via `/.well-known/matrix/server` for the given domain. The configured `matrix_user_verification_service_uvs_homeserver_url` does **not** factor into this. By default, this playbook only checks against `matrix_server_fqn_matrix`. Therefore, the request will be made against the public `openid` API for `matrix_server_fqn_matrix`.

Verifying RoomMembership and PowerLevel is done against `matrix_user_verification_service_uvs_homeserver_url` which is by default done via the docker network. UVS will verify the validity of the token beforehand though.

## Prerequisites

### Open Matrix Federation port

Enabling the UVS service will automatically reconfigure your Synapse homeserver to expose the `openid` API endpoints on the Matrix Federation port (usually `8448`), even if [federation](configuring-playbook-federation.md) is disabled. If you enable the component, make sure that the port is accessible.

### Install Matrix services

UVS can only be installed after Matrix services are installed and running. If you're just installing Matrix services for the first time, please continue with the [Configuration](configuring-playbook.md) / [Installation](installing.md) and come back here later.

### Register a dedicated Matrix user (optional, recommended)

We recommend that you create a dedicated Matrix user for uvs (`uvs` is a good username). **Because UVS requires an access token as an admin user, that user needs to be an admin.**

Generate a strong password for the user. You can create one with a command like `pwgen -s 64 1`.

You can use the playbook to [register a new user](registering-users.md):

```sh
ansible-playbook -i inventory/hosts setup.yml --extra-vars='username=uvs password=PASSWORD_FOR_THE_USER admin=yes' --tags=register-user
```

### Obtain an access token

UVS requires an access token as an admin user to verify RoomMembership and PowerLevel against `matrix_user_verification_service_uvs_homeserver_url`. Refer to the documentation on [how to obtain an access token](obtaining-access-tokens.md).

⚠️ **Warning**: Access tokens are sensitive information. Do not include them in any bug reports, messages, or logs. Do not share the access token with anyone.

## Adjusting the playbook configuration

To enable UVS, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file. Make sure to replace `ACCESS_TOKEN_HERE` with the one created [above](#obtain-an-access-token).

```yaml
matrix_user_verification_service_enabled: true

matrix_user_verification_service_uvs_access_token: "ACCESS_TOKEN_HERE"
```

Check the role's [defaults/main.yml](../roles/custom/matrix-user-verification-service/defaults/main.yml) for the full list of variables that you could override. Note that all the plugging happening in `group_vars/matrix_servers`.

In the default configuration, the UVS Server is only reachable via the docker network, which is fine if e.g. Jitsi is also running in a container on the host. However, it is possible to expose UVS via setting `matrix_user_verification_service_container_http_host_bind_port`.

### Custom Auth Token (optional)

It is possible to set an API Auth Token to restrict access to the UVS. If this is enabled, anyone making a request to UVS must provide it via the header "Authorization: Bearer TOKEN"

By default, the token will be derived from `matrix_homeserver_generic_secret_key` in `group_vars/matrix_servers`.

To set your own Token, add the following configuration to your `vars.yml` file:

```yaml
matrix_user_verification_service_uvs_auth_token: "TOKEN"
```

In case Jitsi is also managed by this playbook and 'matrix' authentication in Jitsi is enabled, this collection will automatically configure Jitsi to use the configured auth token.

### Disable Auth (optional)

Authorization is enabled by default. To disable it, add the following configuration to your `vars.yml` file:

```yaml
matrix_user_verification_service_uvs_require_auth: false
```

### Federation (optional)

In theory (however currently untested), UVS can handle federation. To enable it, add the following configuration to your `vars.yml` file:

```yaml
matrix_user_verification_service_uvs_pin_openid_verify_server_name: false
```

This will instruct UVS to verify the OpenID token against any domain given in a request. Homeserver discovery is done via '.well-known/matrix/server' of the given domain.

### Controlling the logging level (optional)

To specify the logging level, add the following configuration to your `vars.yml` file:

```yaml
UVS_LOG_LEVEL: info
```

Replace `info` with one of the choices (they can be checked [here](https://github.com/winstonjs/winston#logging-levels)) to control the verbosity of the logs generated.

If you have issues with a service, and are requesting support, the higher levels of logging will generally be more helpful.

## Installing

After configuring the playbook, run it with [playbook tags](playbook-tags.md) as below:

<!-- NOTE: let this conservative command run (instead of install-all) to make it clear that failure of the command means something is clearly broken. -->
```sh
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start
```

The shortcut commands with the [`just` program](just.md) are also available: `just install-service matrix-user-verification-service` or `just setup-all`

`just install-service matrix-user-verification-service` is useful for maintaining your setup quickly when its components remain unchanged. If you adjust your `vars.yml` to remove other components, you'd need to run `just setup-all`, or these components will still remain installed. Note `just setup-all` runs the `ensure-matrix-users-created` tag too.

## Troubleshooting

### TLS Certificate Checking

If the Matrix Homeserver does not provide a valid TLS certificate, UVS will fail with the following error message:

> message: 'No response received: [object Object]',

This also applies to self-signed and let's encrypt staging certificates.

To disable certificate validation altogether (INSECURE! Not suitable for production use!) set: `NODE_TLS_REJECT_UNAUTHORIZED=0`

Alternatively, it is possible to inject your own CA certificates into the container by mounting a PEM file with additional trusted CAs into the container and pointing the `NODE_EXTRA_CA_CERTS` environment variable to it.
