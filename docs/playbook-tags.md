# Playbook tags

The Ansible playbook's tasks are tagged, so that certain parts of the Ansible playbook can be run without running all other tasks.

The general command syntax is: `ansible-playbook -i inventory/hosts setup.yml --tags=COMMA_SEPARATED_TAGS_GO_HERE`

Here are some playbook tags that you should be familiar with:

- `setup-all` - runs all setup tasks (installation and uninstallation) for all components, but does not start/restart services

- `install-all` - like `setup-all`, but skips uninstallation tasks. Useful for maintaining your setup quickly when its components remain unchanged. If you adjust your `vars.yml` to remove components, you'd need to run `setup-all` though, or these components will still remain installed

- `setup-SERVICE` (e.g. `setup-postmoogle`) - runs the setup tasks only for a given role, but does not start/restart services. You can discover these additional tags in each role (`roles/**/tasks/main.yml`). Running per-component setup tasks is **not recommended**, as components sometimes depend on each other and running just the setup tasks for a given component may not be enough. For example, setting up the [mautrix-telegram bridge](configuring-playbook-bridge-mautrix-telegram.md), in addition to the `setup-mautrix-telegram` tag, requires database changes (the `setup-postgres` tag) as well as reverse-proxy changes (the `setup-nginx-proxy` tag).

- `install-SERVICE` (e.g. `install-postmoogle`) - like `setup-SERVICE`, but skips uninstallation tasks. See `install-all` above for additional information.

- `start` - starts all systemd services and makes them start automatically in the future

- `stop` - stops all systemd services

- `ensure-matrix-users-created` - a special tag which ensures that all special users needed by the playbook (for bots, etc.) are created

**Notes**:
- `setup-*` tags and `install-*` tags **do not start services** automatically, because you may wish to do things before starting services, such as importing a database dump, restoring data from another server, etc.
- Please be careful not to confuse the playbook tags with the `just` shortcut commands ("recipes"). For details about `just` commands, see: [Running `just` commands](just.md)
