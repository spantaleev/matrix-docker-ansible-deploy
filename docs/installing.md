# Installing

If you've [configured your DNS](configuring-dns.md) and have [configured the playbook](configuring-playbook.md), you can start the installation procedure.

**Before installing** and each time you update the playbook in the future, you will need to update the Ansible roles in this playbook by running `make roles`. `make roles` is a shortcut (a `roles` target defined in [`Makefile`](Makefile) and executed by the [`make`](https://www.gnu.org/software/make/) utility) which ultimately runs [ansible-galaxy](https://docs.ansible.com/ansible/latest/cli/ansible-galaxy.html) to download Ansible roles. If you don't have `make`, you can also manually run the `roles` commands seen in the `Makefile`.


## Playbook tags introduction

The Ansible playbook's tasks are tagged, so that certain parts of the Ansible playbook can be run without running all other tasks.

The general command syntax is: `ansible-playbook -i inventory/hosts setup.yml --tags=COMMA_SEPARATED_TAGS_GO_HERE`

Here are some playbook tags that you should be familiar with:

- `setup-all` - runs all setup tasks (installation and uninstallation) for all components, but does not start/restart services

- `install-all` - like `setup-all`, but skips uninstallation tasks. Useful for maintaining your setup quickly when its components remain unchanged. If you adjust your `vars.yml` to remove components, you'd need to run `setup-all` though, or these components will still remain installed

- `setup-SERVICE` (e.g. `setup-bot-postmoogle`) - runs the setup tasks only for a given role, but does not start/restart services. You can discover these additional tags in each role (`roles/*/main.yml`). Running per-component setup tasks is **not recommended**, as components sometimes depend on each other and running just the setup tasks for a given component may not be enough. For example, setting up the [mautrix-telegram bridge](configuring-playbook-bridge-mautrix-telegram.md), in addition to the `setup-mautrix-telegram` tag, requires database changes (the `setup-postgres` tag) as well as reverse-proxy changes (the `setup-nginx-proxy` tag).

- `install-SERVICE` (e.g. `install-bot-postmoogle`) - like `setup-SERVICE`, but skips uninstallation tasks. See `install-all` above for additional information.

- `start` - starts all systemd services and makes them start automatically in the future

- `stop` - stops all systemd services

- `ensure-matrix-users-created` - a special tag which ensures that all special users needed by the playbook (for bots, etc.) are created

`setup-*` tags and `install-*` tags **do not start services** automatically, because you may wish to do things before starting services, such as importing a database dump, restoring data from another server, etc.


## 1. Installing Matrix

If you **don't** use SSH keys for authentication, but rather a regular password, you may need to add `--ask-pass` to the all Ansible commands

If you **do** use SSH keys for authentication, **and** use a non-root user to *become* root (sudo), you may need to add `-K` (`--ask-become-pass`) to all Ansible commands

There 2 ways to start the installation process - depending on whether you're [Installing a brand new server (without importing data)](#installing-a-brand-new-server-without-importing-data) or [Installing a server into which you'll import old data](#installing-a-server-into-which-youll-import-old-data).


### Installing a brand new server (without importing data)

If this is **a brand new** Matrix server and you **won't be importing old data into it**, run all these tags:

```sh
ansible-playbook -i inventory/hosts setup.yml --tags=install-all,ensure-matrix-users-created,start
```

This will do a full installation and start all Matrix services.

Proceed to [Maintaining your setup in the future](#2-maintaining-your-setup-in-the-future) and [Finalize the installation](#3-finalize-the-installation)


### Installing a server into which you'll import old data

If you will be importing data into your newly created Matrix server, install it, but **do not** start its services just yet.
Starting its services or messing with its database now will affect your data import later on.

To do the installation **without** starting services, run only the `setup-all` tag:

```sh
ansible-playbook -i inventory/hosts setup.yml --tags=install-all
```

When this command completes, services won't be running yet.

You can now:

- [Importing an existing SQLite database (from another Synapse installation)](importing-synapse-sqlite.md) (optional)

- [Importing an existing Postgres database (from another installation)](importing-postgres.md) (optional)

- [Importing `media_store` data files from an existing Synapse installation](importing-synapse-media-store.md) (optional)

.. and then proceed to starting all services:

```sh
ansible-playbook -i inventory/hosts setup.yml --tags=start
```

Proceed to [Maintaining your setup in the future](#2-maintaining-your-setup-in-the-future) and [Finalize the installation](#3-finalize-the-installation)


## 2. Maintaining your setup in the future

Feel free to **re-run the setup command any time** you think something is off with the server configuration. Ansible will take your configuration and update your server to match.

Note that if you remove components from `vars.yml`, or if we switch some component from being installed by default to not being installed by default anymore, you'd need to run the setup command with `--tags=setup-all` instead of `--tags=install-all`. See [Playbook tags introduction](#playbook-tags-introduction)


## 3. Finalize the installation

Now that services are running, you need to **finalize the installation process** (required for federation to work!) by [Configuring Service Discovery via .well-known](configuring-well-known.md).


## 4. Things to do next

After you have started the services and **finalized the installation process** (required for federation to work!) by [Configuring Service Discovery via .well-known](configuring-well-known.md), you can:

- [check if services work](maintenance-checking-services.md)
- or [create your first Matrix user account](registering-users.md)
- or [set up additional services](configuring-playbook.md#other-configuration-options) (bridges to other chat networks, bots, etc.)
- or learn how to [upgrade services when new versions are released](maintenance-upgrading-services.md)
- or learn how to [maintain your server](faq.md#maintenance)
- or join some Matrix rooms:
  * via the *Explore rooms* feature in Element or some other client, or by discovering them using this [matrix-static list](https://view.matrix.org). Note: joining large rooms may overload small servers.
  * or come say Hi in our support room - [#matrix-docker-ansible-deploy:devture.com](https://matrix.to/#/#matrix-docker-ansible-deploy:devture.com). You might learn something or get to help someone else new to Matrix hosting.
- or help make this playbook better by contributing (code, documentation, or [coffee/beer](https://liberapay.com/s.pantaleev/donate))
