# Setting up the Shared Secret Auth password provider module (optional, advanced)

The playbook can install and configure [matrix-synapse-shared-secret-auth](https://github.com/devture/matrix-synapse-shared-secret-auth) for you.

See that project's documentation to learn what it does and why it might be useful to you.

## Adjusting the playbook configuration

Add the following configuration to your `inventory/host_vars/matrix.DOMAIN/vars.yml` file:

```yaml
matrix_synapse_ext_password_provider_shared_secret_auth_enabled: true
matrix_synapse_ext_password_provider_shared_secret_auth_shared_secret: YOUR_SHARED_SECRET_GOES_HERE
```

You can generate a strong shared secret with a command like this: `pwgen -s 64 1`


## Authenticating only using a password provider

If you wish for users to **authenticate only against configured password providers** (like this one), **without consulting Synapse's local database**, feel free to disable it:

```yaml
matrix_synapse_password_config_localdb_enabled: false
```

## Installing

After configuring the playbook, run the [installation](installing.md) command: `just install-all` or `just setup-all`
