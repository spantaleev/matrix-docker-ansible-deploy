# Setting up the REST authentication password provider module (optional, advanced)

The playbook can install and configure [matrix-synapse-rest-auth](https://github.com/ma1uta/matrix-synapse-rest-password-provider) for you.

See the project's [documentation](https://github.com/ma1uta/matrix-synapse-rest-password-provider/blob/master/README.md) to learn what it does and why it might be useful to you.

## Adjusting the playbook configuration

Add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file (adapt to your needs):

```yaml
matrix_synapse_ext_password_provider_rest_auth_enabled: true
matrix_synapse_ext_password_provider_rest_auth_endpoint: "http://matrix-ma1sd:8090"
matrix_synapse_ext_password_provider_rest_auth_registration_enforce_lowercase: false
matrix_synapse_ext_password_provider_rest_auth_registration_profile_name_autofill: true
matrix_synapse_ext_password_provider_rest_auth_login_profile_name_autofill: false
```

## Authenticating only using a password provider

If you wish for users to **authenticate only against configured password providers** (like this one), **without consulting Synapse's local database**, feel free to disable it:

```yaml
matrix_synapse_password_config_localdb_enabled: false
```

## Installing

After configuring the playbook, run it with [playbook tags](playbook-tags.md) as below:

<!-- NOTE: let this conservative command run (instead of install-all) to make it clear that failure of the command means something is clearly broken. -->
```sh
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start
```

The shortcut commands with the [`just` program](just.md) are also available: `just install-all` or `just setup-all`

`just install-all` is useful for maintaining your setup quickly ([2x-5x faster](../CHANGELOG.md#2x-5x-performance-improvements-in-playbook-runtime) than `just setup-all`) when its components remain unchanged. If you adjust your `vars.yml` to remove other components, you'd need to run `just setup-all`, or these components will still remain installed. Note these shortcuts run the `ensure-matrix-users-created` tag too.
