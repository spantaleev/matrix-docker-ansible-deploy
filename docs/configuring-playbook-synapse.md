# Configuring Synapse (optional)

By default, this playbook configures the [Synapse](https://github.com/matrix-org/synapse) Matrix server, so that it works for the general case.
If that's enough for you, you can skip this document.

The playbook provides lots of customization variables you could use to change Synapse's settings.

Their defaults are defined in [`roles/custom/matrix-synapse/defaults/main.yml`](../roles/custom/matrix-synapse/defaults/main.yml) and they ultimately end up in the generated `/matrix/synapse/config/homeserver.yaml` file (on the server). This file is generated from the [`roles/custom/matrix-synapse/templates/synapse/homeserver.yaml.j2`](../roles/custom/matrix-synapse/templates/synapse/homeserver.yaml.j2) template.

**If there's an existing variable** which controls a setting you wish to change, you can simply define that variable in your configuration file (`inventory/host_vars/matrix.<your-domain>/vars.yml`) and [re-run the playbook](installing.md) to apply the changes.

Alternatively, **if there is no pre-defined variable** for a Synapse setting you wish to change:

- you can either **request a variable to be created** (or you can submit such a contribution yourself). Keep in mind that it's **probably not a good idea** to create variables for each one of Synapse's various settings that rarely get used.

- or, you can **extend and override the default configuration** ([`homeserver.yaml.j2`](../roles/custom/matrix-synapse/templates/synapse/homeserver.yaml.j2)) by making use of the `matrix_synapse_configuration_extension_yaml` variable. You can find information about this in [`roles/custom/matrix-synapse/defaults/main.yml`](../roles/custom/matrix-synapse/defaults/main.yml).

- or, if extending the configuration is still not powerful enough for your needs, you can **override the configuration completely** using `matrix_synapse_configuration` (or `matrix_synapse_configuration_yaml`). You can find information about this in [`roles/custom/matrix-synapse/defaults/main.yml`](../roles/custom/matrix-synapse/defaults/main.yml).


## Load balancing with workers

To have Synapse gracefully handle thousands of users, worker support should be enabled. It factors out some homeserver tasks and spreads the load of incoming client and server-to-server traffic between multiple processes. More information can be found in the [official Synapse workers documentation](https://github.com/matrix-org/synapse/blob/master/docs/workers.md).

To enable Synapse worker support, update your `inventory/host_vars/matrix.DOMAIN/vars.yml` file:

```yaml
matrix_synapse_workers_enabled: true
```

We support a few configuration presets (`matrix_synapse_workers_preset: one-of-each` being the default configuration):
- `little-federation-helper` - a very minimal worker configuration to improve federation performance
- `one-of-each` - one worker of each supported type

If you'd like more customization power, you can start with one of the presets and tweak various `matrix_synapse_workers_*_count` variables manually.

If you increase worker counts too much, you may need to increase the maximum number of Postgres connections too (example):

```yaml
devture_postgres_process_extra_arguments: [
  "-c 'max_connections=200'"
]
```

**NOTE**: Disabling `matrix-nginx-proxy` (`matrix_nginx_proxy_enabled: false`) (that is, [using your own other webserver](configuring-playbook-own-webserver.md) when running a Synapse worker setup is likely to cause various troubles (see [this issue](https://github.com/spantaleev/matrix-docker-ansible-deploy/issues/2090)).

In case any problems occur, make sure to have a look at the [list of synapse issues about workers](https://github.com/matrix-org/synapse/issues?q=workers+in%3Atitle) and your `journalctl --unit 'matrix-*'`.


## Synapse Admin

Certain Synapse administration tasks (managing users and rooms, etc.) can be performed via a web user-interace, if you install [Synapse Admin](configuring-playbook-synapse-admin.md).


## Synapse + OpenID Connect for Single-Sign-On

If you'd like to use OpenID Connect authentication with Synapse, you'll need some additional reverse-proxy configuration (see [our nginx reverse-proxy doc page](configuring-playbook-nginx.md#synapse-openid-connect-for-single-sign-on)).

This example configuration is for [keycloak](https://www.keycloak.org/), an opensource Identity Provider maintained by Red Hat.

For more detailed documentation on available options and how to setup keycloak, see the [Synapse documentation on OpenID Connect with keycloak](https://github.com/matrix-org/synapse/blob/develop/docs/openid.md#keycloak).

In case you encounter errors regarding the parsing of the variables, you can try to add `{% raw %}` and `{% endraw %}` blocks around them. For example ;

```
matrix_synapse_configuration_extension_yaml: |
  oidc_providers:
    - idp_id: keycloak
      idp_name: "My KeyCloak server"
      issuer: "https://url.ix/auth/realms/{realm_name}"
      client_id: "matrix"
      client_secret: "{{ vault_synapse_keycloak }}"
      scopes: ["openid", "profile"]
      user_mapping_provider:
        config:
          localpart_template: "{% raw %}{{ user.preferred_username }}{% endraw %}"
          display_name_template: "{% raw %}{{ user.name }}{% endraw %}"
          email_template: "{% raw %}{{ user.email }}{% endraw %}"
      allow_existing_users: true # Optional
      backchannel_logout_enabled: true # Optional
```

