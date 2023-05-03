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


## Customizing templates

[Templates](https://github.com/matrix-org/synapse/blob/develop/docs/templates.md) are used by Synapse for showing **certain web pages** handled by the server, as well as for **email notifications**.

This playbook allows you to customize the default templates (see the [`synapse/res/templates` directory](https://github.com/matrix-org/synapse/tree/develop/synapse/res/templates)).

If template customization is enabled, the playbook will build a custom container image based on the official one.

Your custom templates need to live in a public or private git repository. This repository will be cloned during Synapse image customization (during the playbook run).

To enable template customizations, use a configuration (`inventory/host_vars/matrix.DOMAIN/vars.yml`) like this:

```yaml
# If you'd like to ensure that the customized image is built each time the playbook runs, enable this.
# Otherwise, the customized image will only be rebuilt whenever the Synapse version changes (once every ~2 weeks).
# matrix_synapse_docker_image_customized_build_nocache: true

matrix_synapse_container_image_customizations_templates_enabled: true

# Our templates live in a templates/ directory within the repository.
# If they're at the root path, delete this line.
matrix_synapse_container_image_customizations_templates_in_container_template_files_relative_path: templates

matrix_synapse_container_image_customizations_templates_git_repository_url: git@github.com:organization/repository.git
matrix_synapse_container_image_customizations_templates_git_repository_branch: main

matrix_synapse_container_image_customizations_templates_git_repository_keyscan_enabled: true
matrix_synapse_container_image_customizations_templates_git_repository_keyscan_hostname: github.com

# If your git repository is public, do not define the private key (remove the variable).
matrix_synapse_container_image_customizations_templates_git_repository_ssh_private_key: |
  -----BEGIN OPENSSH PRIVATE KEY-----
  ....
  -----END OPENSSH PRIVATE KEY-----
```

As mentioned in Synapse's Templates documentation, Synapse will fall back to its own templates if a template is not found in that directory.
Due to this, it's recommended to only store and maintain template files in your repository if you need to make custom changes. Other files (which you don't need to change), should not be duplicated, so that you don't need to worry about getting out-of-sync with the original Synapse templates.


## Monitoring Synapse Metrics with Prometheus and Grafana

This playbook allows you to enable Synapse metrics, which can provide insight into the performance and activity of Synapse.

To enable Synapse metrics see [`configuring-playbook-prometheus-grafana.md`](./configuring-playbook-prometheus-grafana.md)
