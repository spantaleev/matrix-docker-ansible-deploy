# Setting up Matrix Corporal (optional, advanced)

-------------------------------------

**WARNING**: This is an advanced feature! It requires prior experience with Matrix and a specific need for using [Matrix Corporal](https://github.com/devture/matrix-corporal). If you're unsure whether you have such a need, you most likely don't.

-------------------------------------

The playbook can install and configure [matrix-corporal](https://github.com/devture/matrix-corporal) for you.

In short, it's a sort of automation and firewalling service, which is helpful if you're instaling Matrix services in a controlled corporate environment.
See that project's documentation to learn what it does and why it might be useful to you.

If you decide that you'd like to let this playbook install it for you, you'd need to also:
- (required) [set up the Shared Secret Auth password provider module](configuring-playbook-shared-secret-auth.md)
- (optional, but encouraged) [set up the REST authentication password provider module](configuring-playbook-rest-auth.md)


## Playbook configuration

You would then need some configuration like this:

```yaml
# The Shared Secret Auth password provider module is required for Corporal to work.
# See configuring-playbook-shared-secret-auth.md
matrix_synapse_ext_password_provider_shared_secret_auth_enabled: true
matrix_synapse_ext_password_provider_shared_secret_auth_shared_secret: YOUR_SHARED_SECRET_GOES_HERE

# When matrix-corporal is acting as the primary authentication provider,
# you need to set up the REST authentication password provider module
# to make Interactive User Authentication work.
# This is necessary for certain user actions (like E2EE, device management, etc).
#
# See configuring-playbook-rest-auth.md
matrix_synapse_ext_password_provider_rest_auth_enabled: true
matrix_synapse_ext_password_provider_rest_auth_endpoint: "http://matrix-corporal:41080/_matrix/corporal"

matrix_corporal_enabled: true

matrix_corporal_policy_provider_config: |
  {
    "Type": "http",
    "Uri": "https://intranet.example.com/matrix/policy",
    "AuthorizationBearerToken": "SOME_SECRET",
    "CachePath": "/var/cache/matrix-corporal/last-policy.json",
    "ReloadIntervalSeconds": 1800,
    "TimeoutMilliseconds": 300
  }

# If you also want to enable Matrix Corporal's HTTP API..
matrix_corporal_http_api_enabled: true
matrix_corporal_http_api_auth_token: "AUTH_TOKEN_HERE"

# If you need to change matrix-corporal's user id from the default (matrix-corporal).
# In any case, you need to make sure this Matrix user is created on your server.
matrix_corporal_corporal_user_id_local_part: "matrix-corporal"

# Because Corporal peridoically performs lots of user logins from the same IP,
# you may need raise Synapse's ratelimits.
# The values below are just an example. Tweak to your use-case (number of users, etc.)
matrix_synapse_rc_login:
  address:
    per_second: 50
    burst_count: 300
  account:
    per_second: 0.17
    burst_count: 3
  failed_attempts:
    per_second: 0.17
    burst_count: 3
```

Matrix Corporal operates with a specific Matrix user on your server.
By default, it's `matrix-corporal` (controllable by the `matrix_corporal_reconciliation_user_id_local_part` setting, see above).
No matter what Matrix user id you configure to run it with, make sure that:

- the Matrix Corporal user is created by [registering it](registering-users.md). Use a password you remember, as you'll need to log in from time to time to create or join rooms

- the Matrix Corporal user is joined and has Admin/Moderator-level access to any rooms you want it to manage


## Matrix Corporal files

The following local filesystem paths are mounted in the `matrix-corporal` container and can be used in your configuration (or policy):

- `/matrix/corporal/config` is mounted at `/etc/matrix-corporal` (read-only)

- `/matrix/corporal/var` is mounted at `/var/matrix-corporal` (read and write)

- `/matrix/corporal/cache` is mounted at `/var/cache/matrix-corporal` (read and write)

As an example: you can create your own configuration files in `/matrix/corporal/config` and they will appear in `/etc/matrix-corporal` in the Docker container. Your configuration (stuff in `matrix_corporal_policy_provider_config`) needs to refer to these files via the local container paths - `/etc/matrix-corporal` (read-only), `/var/matrix-corporal` (read and write), `/var/cache/matrix-corporal` (read and write).
