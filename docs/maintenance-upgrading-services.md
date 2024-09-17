# Upgrading the Matrix services

This playbook not only installs the various Matrix services for you, but can also upgrade them as new versions are made available.

If you want to be notified when new versions of Synapse are released, you should join the Synapse Homeowners room: [#homeowners:matrix.org](https://matrix.to/#/#homeowners:matrix.org).

To upgrade services:

- update your playbook directory and all upstream Ansible roles (defined in the `requirements.yml` file) using:

  - either: `just update`
  - or: a combination of `git pull` and `just roles` (or `make roles`)

- take a look at [the changelog](../CHANGELOG.md) to see if there have been any backward-incompatible changes that you need to take care of

- re-run the [playbook setup](installing.md) and restart all services: `just install-all` or `just setup-all`

**Note**: major version upgrades to the internal PostgreSQL database are not done automatically. To upgrade it, refer to the [upgrading PostgreSQL guide](maintenance-postgres.md#upgrading-postgresql).
