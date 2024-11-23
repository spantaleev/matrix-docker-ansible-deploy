# Upgrading the Matrix services

This playbook not only installs the various Matrix services for you, but can also upgrade them as new versions are made available.

While this playbook helps you to set up Matrix services and maintain them, it will **not** automatically run the maintenance task for you. You will need to update the playbook and re-run it **manually**.

The upstream projects, which this playbook makes use of, occasionally if not often suffer from security vulnerabilities (for example, see [here](https://github.com/element-hq/element-web/security) for known ones on Element Web).

Since it is unsafe to keep outdated services running on the server connected to the internet, please consider to update the playbook and re-run it periodically, in order to keep the services up-to-date.

The developers of this playbook strive to maintain the playbook updated, so that you can re-run the playbook to address such vulnerabilities. It is **your responsibility** to keep your server and the services on it up-to-date.

If you want to be notified when new versions of Synapse are released, you should join the Synapse Homeowners room: [#homeowners:matrix.org](https://matrix.to/#/#homeowners:matrix.org).

## Steps to upgrade the Matrix services

Before updating the playbook and the Ansible roles in the playbook, take a look at [the changelog](../CHANGELOG.md) to see if there have been any backward-incompatible changes that you need to take care of.

If it looks good to you, go to the `matrix-docker-ansible-deploy` directory, then:

- update your playbook directory and all upstream Ansible roles (defined in the `requirements.yml` file) using:

  - either: `just update`
  - or: a combination of `git pull` and `just roles` (or `make roles` if you have `make` program on your computer instead of `just`)

  `just update` and `just roles` are shortcuts (their targets are defined in [`justfile`](../justfile) and executed by the [`just`](https://github.com/casey/just) utility) which ultimately run [agru](https://github.com/etkecc/agru) or [ansible-galaxy](https://docs.ansible.com/ansible/latest/cli/ansible-galaxy.html) (depending on what is available in your system) to download Ansible roles, after upgrading the playbook (in case of `just update`).

  If you don't have either `just` tool or `make` program, you can run the `ansible-galaxy` tool directly: `rm -rf roles/galaxy; ansible-galaxy install -r requirements.yml -p roles/galaxy/ --force`

- re-run the [playbook setup](installing.md#maintaining-your-setup-in-the-future) and restart all services:

  ```sh
  ansible-playbook -i inventory/hosts setup.yml --tags=install-all,start
  ```

Note that if you remove components from `vars.yml`, or if we switch some component from being installed by default to not being installed by default anymore, you'd need to run the setup command with `--tags=setup-all` instead of `--tags=install-all`. See [this page on the playbook tags](playbook-tags.md) for more information.

A way to invoke these `ansible-playbook` commands with less typing is to use [just](https://github.com/casey/just) to run the "recipe": `just install-all` or `just setup-all`. See [our `justfile`](../justfile) for more information. If you don't have `just`, you can also manually run the commands seen in the `justfile`.

**Note**: major version upgrades to the internal PostgreSQL database are not done automatically. To upgrade it, refer to the [upgrading PostgreSQL guide](maintenance-postgres.md#upgrading-postgresql).
