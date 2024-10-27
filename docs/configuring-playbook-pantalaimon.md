# Setting up Pantalaimon (E2EE aware proxy daemon) (optional)

The playbook can install and configure the [pantalaimon](https://github.com/matrix-org/pantalaimon) E2EE aware proxy daemon for you.

See the project's [documentation](https://github.com/matrix-org/pantalaimon) to learn what it does and why it might be useful to you.

This role exposes Pantalaimon's API only within the container network, so bots and clients installed on the same machine can use it. In particular the [Draupnir](configuring-playbook-bot-draupnir.md) and [Mjolnir](configuring-playbook-bot-mjolnir.md) roles (and possibly others) can use it.

## 1. Adjusting the playbook configuration

Add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file (adapt to your needs):

```yaml
matrix_pantalaimon_enabled: true
```

The default configuration should suffice. For advanced configuration, you can override the variables documented in the role's [defaults](../roles/custom/matrix-pantalaimon/defaults/main.yml).

## 2. Installing

After configuring the playbook, run the [installation](installing.md) command: `just install-all` or `just setup-all`
