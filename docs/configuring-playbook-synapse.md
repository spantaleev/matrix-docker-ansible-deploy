# Configuring Synapse (optional)

By default, this playbook configures the [Synapse](https://github.com/matrix-org/synapse) Matrix server, so that it works for the general case.
If that's enough for you, you can skip this document.

The playbook provides lots of customization variables you could use to change Synapse's settings.

Their defaults are defined in [`roles/matrix-synapse/defaults/main.yml`](../roles/matrix-synapse/defaults/main.yml) and they ultimately end up in the generated `/matrix/synapse/config/homeserver.yaml` file (on the server). This file is generated from the [`roles/matrix-synapse/templates/synapse/homeserver.yaml.j2`](../roles/matrix-synapse/templates/synapse/homeserver.yaml.j2) template.

**If there's an existing variable** which controls a setting you wish to change, you can simply define that variable in your configuration file (`inventory/host_vars/matrix.<your-domain>/vars.yml`) and [re-run the playbook](installing.md) to apply the changes.

Alternatively, **if there is no pre-defined variable** for a Synapse setting you wish to change:

- you can either **request a variable to be created** (or you can submit such a contribution yourself). Keep in mind that it's **probably not a good idea** to create variables for each one of Synapse's various settings that rarely get used.

- or, you can **extend and override the default configuration** ([`homeserver.yaml.j2`](../roles/matrix-synapse/templates/synapse/homeserver.yaml.j2)) by making use of the `matrix_synapse_configuration_extension_yaml` variable. You can find information about this in [`roles/matrix-synapse/defaults/main.yml`](../roles/matrix-synapse/defaults/main.yml).

- or, if extending the configuration is still not powerful enough for your needs, you can **override the configuration completely** using `matrix_synapse_configuration` (or `matrix_synapse_configuration_yaml`). You can find information about this in [`roles/matrix-synapse/defaults/main.yml`](../roles/matrix-synapse/defaults/main.yml).


## Load balancing with workers
To have synapse gracefully handle thousands of users, worker support should be enabled. It factors out some homeserver tasks and spreads the load of incoming client and server-to-server traffic between multiple processes. More information can be found at https://github.com/matrix-org/synapse/blob/master/docs/workers.md (which, coincidentally, also is the file which an awk script extracts the endpoint URLs from when running with tag `setup-synapse`).

To enable synapse worker support, set

```yaml
matrix_synapse_workers_enabled: true
```

in your `inventory/host_vars/matrix.DOMAIN/vars.yml` file.
There, you can also override the default `matrix_synapse_workers_enabled_list` from [`roles/matrix-synapse/defaults/main.yml`](../roles/matrix-synapse/defaults/main.yml).

If you are not using the inbuilt nginx proxy container but an instance managed by yourself, you are currently on your own as the template needs yet to be adapted to better support this use case.

In case any problems occur, make sure to have a look at the [list of synapse issues about workers](https://github.com/matrix-org/synapse/issues?q=workers+in%3Atitle) and your `journalctl --unit 'matrix-*'`.


## Synapse Admin

Certain Synapse administration tasks (managing users and rooms, etc.) can be performed via a web user-interace, if you install [Synapse Admin](configuring-playbook-synapse-admin.md).
