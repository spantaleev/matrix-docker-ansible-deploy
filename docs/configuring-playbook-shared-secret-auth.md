# Setting up the Shared Secret Auth password provider module (optional, advanced)

The playbook can install and configure [matrix-synapse-shared-secret-auth](https://github.com/devture/matrix-synapse-shared-secret-auth) for you.

See that project's documentation to learn what it does and why it might be useful to you.

If you decide that you'd like to let this playbook install it for you, you need some configuration like this:

```yaml
matrix_synapse_ext_password_provider_shared_secret_auth_enabled: true
matrix_synapse_ext_password_provider_shared_secret_auth_shared_secret: YOUR_SHARED_SECRET_GOES_HERE
```