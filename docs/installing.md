# Installing

<sup>⚡️[Quick start](README.md) | [Prerequisites](prerequisites.md) > [Configuring your DNS server](configuring-dns.md) > [Getting the playbook](getting-the-playbook.md) > [Configuring the playbook](configuring-playbook.md) > Installing </sup>

If you've [configured your DNS](configuring-dns.md) and have [configured the playbook](configuring-playbook.md), you can start the installation procedure.

## Update Ansible roles

Before installing, you need to update the Ansible roles in this playbook by running `just roles`.

`just roles` is a shortcut (a `roles` target defined in [`justfile`](../justfile) and executed by the [`just`](https://github.com/casey/just) utility) which ultimately runs [agru](https://github.com/etkecc/agru) or [ansible-galaxy](https://docs.ansible.com/ansible/latest/cli/ansible-galaxy.html) (depending on what is available in your system) to download Ansible roles. If you don't have `just`, you can also manually run the `roles` commands seen in the `justfile`.

There's another shortcut (`just update`) which updates the playbook (`git pull`) and updates roles (`just roles`) at the same time.

## Install Matrix server and services

The Ansible playbook's tasks are tagged, so that certain parts of the Ansible playbook can be run without running all other tasks.

The general command syntax for installation (and also maintenance) is: `ansible-playbook -i inventory/hosts setup.yml --tags=COMMA_SEPARATED_TAGS_GO_HERE`. It is recommended to get yourself familiar with the [playbook tags](playbook-tags.md) before proceeding.

If you **don't** use SSH keys for authentication, but rather a regular password, you may need to add `--ask-pass` to the all Ansible commands.

If you **do** use SSH keys for authentication, **and** use a non-root user to *become* root (sudo), you may need to add `-K` (`--ask-become-pass`) to all Ansible commands.

There 2 ways to start the installation process - depending on whether you're [Installing a brand new server (without importing data)](#installing-a-brand-new-server-without-importing-data) or [Installing a server into which you'll import old data](#installing-a-server-into-which-youll-import-old-data).

### Installing a brand new server (without importing data)

If this is **a brand new** Matrix server and you **won't be importing old data into it**, run all these tags:

```sh
ansible-playbook -i inventory/hosts setup.yml --tags=install-all,ensure-matrix-users-created,start
```

This will do a full installation and start all Matrix services.

**Note**: if the command does not work as expected, make sure that you have properly installed and configured software required to run the playbook, as described on [Prerequisites](prerequisites.md).

### Installing a server into which you'll import old data

If you will be importing data into your newly created Matrix server, install it, but **do not** start its services just yet. Starting its services or messing with its database now will affect your data import later on.

To do the installation **without** starting services, run `ansible-playbook` with the `install-all` tag only:

```sh
ansible-playbook -i inventory/hosts setup.yml --tags=install-all
```

**Note**: do not run the just "recipe" `just install-all` instead, because it automatically starts services at the end of execution.

When this command completes, services won't be running yet.

You can now:

- [Importing an existing SQLite database (from another Synapse installation)](importing-synapse-sqlite.md) (optional)

- [Importing an existing Postgres database (from another installation)](importing-postgres.md) (optional)

- [Importing `media_store` data files from an existing Synapse installation](importing-synapse-media-store.md) (optional)

.. and then proceed to starting all services:

```sh
ansible-playbook -i inventory/hosts setup.yml --tags=start
```

## Finalize the installation

Now that services are running, you need to **finalize the installation process** (required for federation to work!) by [Configuring Service Discovery via .well-known](configuring-well-known.md).

If you need the base domain (`example.com`) for anything else such as hosting a website, you have to configure it manually, following the procedure described on the linked documentation.

However, if you do not need the base domain for anything else, the easiest way of configuring it is to [serve the base domain](configuring-playbook-base-domain-serving.md) from the integrated web server. It will enable you to use a Matrix user identifier like `@<username>:example.com` while hosting services on a subdomain like `matrix.example.com`.

To configure Service Discovery in this way, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
matrix_static_files_container_labels_base_domain_enabled: true
```

After configuring the playbook, run the [installation](installing.md) command:

```sh
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start
```

## Things to do next

After finilizing the installation, you can:

- [check if services work](maintenance-checking-services.md)
- or [create your first Matrix user account](registering-users.md)
- or [set up additional services](configuring-playbook.md#other-configuration-options) (bridges to other chat networks, bots, etc.)
- or learn how to [upgrade services when new versions are released](maintenance-upgrading-services.md)
- or learn how to [maintain your server](faq.md#maintenance)
- or join some Matrix rooms:
  * via the *Explore rooms* feature in Element Web or some other clients, or by discovering them using this [matrix-static list](https://view.matrix.org). **Note**: joining large rooms may overload small servers.
  * or come say Hi in our support room - [#matrix-docker-ansible-deploy:devture.com](https://matrix.to/#/#matrix-docker-ansible-deploy:devture.com). You might learn something or get to help someone else new to Matrix hosting.
- or help make this playbook better by contributing (code, documentation, or [coffee/beer](https://liberapay.com/s.pantaleev/donate))

### Maintaining your setup in the future

Feel free to **re-run the setup command any time** you think something is off with the server configuration. Ansible will take your configuration and update your server to match. To update the playbook and the Ansible roles in the playbook, simply run `just roles`.

Note that if you remove components from `vars.yml`, or if we switch some component from being installed by default to not being installed by default anymore, you'd need to run the setup command with `--tags=setup-all` instead of `--tags=install-all`. See [this page on the playbook tags](playbook-tags.md) for more information.

A way to invoke these `ansible-playbook` commands with less typing in the future is to use [just](https://github.com/casey/just) to run the "recipe": `just install-all` or `just setup-all`. See [our `justfile`](../justfile) for more information.
