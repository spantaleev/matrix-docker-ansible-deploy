# Setting up the Shared Secret Auth password provider module (optional, advanced)

The playbook can install and configure [matrix-synapse-shared-secret-auth](https://github.com/devture/matrix-synapse-shared-secret-auth) for you.

See that project's documentation to learn what it does and why it might be useful to you.

## Adjusting the playbook configuration

Add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
matrix_synapse_ext_password_provider_shared_secret_auth_enabled: true

# Generate a strong shared secret here. Consider generating it with `pwgen -s 64 1`
matrix_synapse_ext_password_provider_shared_secret_auth_shared_secret: YOUR_SHARED_SECRET_GOES_HERE
```

## Authenticating only using a password provider

If you wish for users to **authenticate only against configured password providers** (like this one), **without consulting Synapse's local database**, feel free to disable it:

```yaml
matrix_synapse_password_config_localdb_enabled: false
```

## Installing

After configuring the playbook, run the [installation](installing.md) command:

<!-- NOTE: let this conservative command run (instead of install-all) to make it clear that failure of the command means something is clearly broken. -->
```sh
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,ensure-matrix-users-created,start
```

The shortcut commands with `just` program are also available: `just install-all` or `just setup-all`.

`just install-all` is useful for maintaining your setup quickly when its components remain unchanged. If you adjust your `vars.yml` to remove other components, you'd need to run `just setup-all`, or these components will still remain installed. For more information about `just` shortcuts, take a look at this page: [Running `just` commands](just.md)
