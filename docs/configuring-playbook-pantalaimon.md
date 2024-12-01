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

After configuring the playbook, run it with [playbook tags](playbook-tags.md) as below:

<!-- NOTE: let this conservative command run (instead of install-all) to make it clear that failure of the command means something is clearly broken. -->
```sh
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start
```

The shortcut commands with `just` program are also available: `just run-tags install-all,start` or `just run-tags setup-all,start`

`just run-tags install-all,start` is useful for maintaining your setup quickly when its components remain unchanged. If you adjust your `vars.yml` to remove other components, you'd need to run `just run-tags setup-all,start`, or these components will still remain installed. For more information about `just` shortcuts, take a look at this page: [Running `just` commands](just.md)
