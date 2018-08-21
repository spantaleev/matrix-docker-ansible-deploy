# Setting up Matrix Corporal

The playbook can install and configure [matrix-corporal](https://github.com/devture/matrix-corporal) for you.

See that project's documentation to learn what it does and why it might be useful to you.

If you decide that you'd like to let this playbook install it for you, you'd need to also [set up the Shared Secret Auth password provider module](configuring-playbook-shared-secret-auth.md).

You would then need some configuration like this:

```yaml
matrix_corporal_enabled: true

matrix_corporal_policy_provider_config: |
  {
    "Type": "http",
    "Uri": "https://intranet.example.com/matrix/policy",
    "AuthorizationBearerToken": "SOME_SECRET",
    "CachePath": "/var/cache/matrix-corporal/last-policy.json",
    "ReloadIntervalSeconds": 1800
  }

# If you also want to enable Matrix Corporal's HTTP API..
matrix_corporal_http_api_enabled: true
matrix_corporal_http_api_auth_token: "AUTH_TOKEN_HERE"

# If you need to change the reconciliator user's id from the default (matrix-corporal)..
matrix_corporal_reconciliation_user_id_local_part: "matrix-corporal"
```

The following local filesystem paths are mounted in the `matrix-corporal` container and can be used in your configuration (or policy):

- `/matrix/corporal/config` is mounted at `/etc/matrix-corporal` (read-only)

- `/matrix/corporal/var` is mounted at `/var/matrix-corporal` (read and write)

- `/matrix/corporal/cache` is mounted at `/var/cache/matrix-corporal` (read and write)
