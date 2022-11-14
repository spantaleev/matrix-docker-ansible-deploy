# Setting up the REST authentication password provider module (optional, advanced)

The playbook can install and configure [matrix-synapse-rest-auth](https://github.com/ma1uta/matrix-synapse-rest-password-provider) for you.

See that project's documentation to learn what it does and why it might be useful to you.

If you decide that you'd like to let this playbook install it for you, you need some configuration like this:

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
