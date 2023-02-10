# Setting up Matrix User Verification Service (optional)

**[Matrix User Verification Service](https://github.com/matrix-org/matrix-user-verification-service) (hereafter: UVS) can only be installed after Matrix services are installed and running.**
If you're just installing Matrix services for the first time, please continue with the [Configuration](configuring-playbook.md) / [Installation](installing.md) flow and come back here later.

Currently, the main purpose of this role is to allow Jitsi to authenticate matrix users and check if they are authorized to join a conference. Please refer to the documentation of the [Matrix User Verification Service](https://github.com/matrix-org/matrix-user-verification-service) to understand how it works.

**Note**: enabling Matrix User Verification Service, means that the `openid` API endpoints will be exposed on the Matrix Federation port (usually `8448`), even if [federation](configuring-playbook-federation.md) is disabled.

If the Jitsi server is also configured by this playbook, all plugging of variables and secrets is handled in `group_vars/matrix_servers`.

__Some general concepts of UVS may be helpful to understand the rest, so here they are:__

UVS can be used to verify two claims: 

* (A) Whether a given OpenID token is valid for a given server and
* (B) whether a user is member of a given room and the corresponding PowerLevel

Verifying an OpenID token id done by finding the corresponding Homeserver via  '.well-known/matrix/server' for the given domain.
The configured `matrix_user_verification_service_uvs_homeserver_url` does **not** factor into this.
By default, this playbook only checks against `matrix_server_fqn_matrix`.
Therefore, the request will be made against the public openid API for `matrix_server_fqn_matrix`.

Verifying RoomMembership and PowerLevel is done against `matrix_user_verification_service_uvs_homeserver_url` which is by default done via the docker network.
UVS will verify the validity of the token beforehand though.

## Prerequisites

In order to use UVS, an admin token for the configured homeserver must be supplied. For now this means configuring Synapse and creating the token before installing UVS.

## Enable

[Matrix User Verification Service](https://github.com/matrix-org/matrix-user-verification-service) installation is disabled by default.
You can enable it in your configuration file (`inventory/host_vars/matrix.<your-domain>/vars.yml`):

```yaml
matrix_user_verification_service_enabled: true
```

## Configuration

The only required configuration variable is `matrix_user_verification_service_uvs_access_token` (see below).

For a list of all configuration options see the role defaults [`roles/matrix-user-verification-service/defaults/main.yml`](../roles/custom/matrix-user-verification-service/defaults/main.yml).
But be aware of all the plugging happening in `group_vars/matrix_servers`.

In the default configuration, the UVS Server is only reachable via the docker network, which is fine if e.g. Jitsi is also running in a container on the host.
However, it is possible to expose UVS via setting `matrix_user_verification_service_container_http_host_bind_port`.

### Access token

The Synapse Access Token is used to verify RoomMembership and PowerLevel against `matrix_user_verification_service_uvs_homeserver_url`.

We recommend that you create a dedicated Matrix user for uvs (`uvs` is a good username).
Follow our [Registering users](registering-users.md) guide to register a user with administration privileges.

You are required to specify an access token (belonging to this new user) for UVS to work.
To get an access token for the UVS user, you can follow the documentation on [how to do obtain an access token](obtaining-access-tokens.md).

**Access tokens are sensitive information. Do not include them in any bug reports, messages, or logs. Do not share the access token with anyone.**

```yaml
matrix_user_verification_service_uvs_access_token: "YOUR ACCESS TOKEN HERE"
```

### (Optional) Custom Auth Token

It is possible to set an API Auth Token to restrict access to the UVS. If this is enabled, anyone making a request to UVS must provide it via the header "Authorization: Bearer TOKEN"

By default, the token will be derived from `matrix_homeserver_generic_secret_key` in `group_vars/matrix_servers`.
To set your own Token, simply put the following in your host_vars.

```yaml
matrix_user_verification_service_uvs_auth_token: "TOKEN"
```

In case Jitsi is also managed by this playbook and 'matrix' authentication in Jitsi is enabled, this collection will automatically configure Jitsi to use the configured auth token.

###  (Optional) Disable Auth
Authorization is enabled by default. To disable set

```yaml
matrix_user_verification_service_uvs_require_auth: false
```

in your host_vars.

### (Optional) Federation

In theory (however currently untested), UVS can handle federation. Simply set:

```yaml
matrix_user_verification_service_uvs_pin_openid_verify_server_name: false
```

in your host_vars.

This will instruct UVS to verify the OpenID token against any domain given in a request. 
Homeserver discovery is done via '.well-known/matrix/server' of the given domain.

## Installation

After these variables have been set, please run the following command to re-run setup and to restart UVS:

```
ansible-playbook -i inventory/hosts setup.yml --tags=setup-matrix-user-verification-service,start
```

## Logging

The configuration variable `UVS_LOG_LEVEL` can be set to: 
- warning
- info
- debug

## TLS Certificate Checking
If the matrix Homeserver does not provide a valid TLS certificate, UVS will fail with the following error message:

> message: 'No response received: [object Object]',

This also applies to self-signed and let's encrypt staging certificates.

To disable certificate validation altogether (INSECURE! Not suitable for production use!) set: `NODE_TLS_REJECT_UNAUTHORIZED=0`

Alternatively, it is possible to inject your own CA certificates into the container by mounting a PEM file with additional trusted CAs into the container and pointing the `NODE_EXTRA_CA_CERTS` environment variable to it.
