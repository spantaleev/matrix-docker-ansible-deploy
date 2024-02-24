# Setting up Synapse Auto Invite Accept (optional)

The playbook can install and configure [synapse-auto-invite-accept](https://github.com/matrix-org/synapse-auto-accept-invite) for you.

See that project's [documentation](https://github.com/matrix-org/synapse-auto-accept-invite) to learn what it does and why it might be useful to you.
In short, it automatically accepts room invites. You can specify that only 1:1 room invites are auto-accepted. Defaults to false if not specified.

If you decide that you'd like to let this playbook install it for you, you need a configuration like this:

```yaml
matrix_synapse_ext_synapse_auto_accept_invite_enabled: true

matrix_synapse_ext_synapse_auto_accept_invite_accept_invites_only_direct_messages: true
```

## Synapse worker deployments

In a [workerized Synapse deployment](https://github.com/spantaleev/matrix-docker-ansible-deploy/blob/c9a842147e09647c355799ca024d65a5de66b099/docs/configuring-playbook-synapse.md#load-balancing-with-workers) it is possible to run this module on a worker to reduce the load on the main process (Default is 'null'). For example add this to your configuration:

```yaml
matrix_synapse_ext_synapse_auto_accept_invite_worker_to_run_on: 'matrix-synapse-worker-generic-0'
```

There might be an [issue with federation](https://github.com/matrix-org/synapse-auto-accept-invite/issues/18).