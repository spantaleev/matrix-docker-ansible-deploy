# Upgrading the Matrix services

This playbook not only installs the various Matrix services for you, but can also upgrade them as new versions are made available.

If you want to be notified when new versions of Synapse are released, you should join the Synapse Homeowners room: [#homeowners:matrix.org](https://matrix.to/#/#homeowners:matrix.org).

To upgrade services:

- update your playbook directory (`git pull`), so you'd obtain everything new we've done

- take a look at [the changelog](../CHANGELOG.md) to see if there have been any backward-incompatible changes that you need to take care of

- download the upstream Ansible roles used by the playbook by running `make roles`

- re-run the [playbook setup](installing.md) and restart all serivces: `ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,ensure-matrix-users-created,start`

**Note**: major version upgrades to the internal PostgreSQL database are not done automatically. To upgrade it, refer to the [upgrading PostgreSQL guide](maintenance-postgres.md#upgrading-postgresql).
