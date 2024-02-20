# Setting up Synapse Auto Invite Accept (optional)

The playbook can install and configure [synapse-auto-invite-accept](https://github.com/matrix-org/synapse-auto-accept-invite) for you.

See that project's [documentation](https://github.com/matrix-org/synapse-auto-accept-invite) to learn what it does and why it might be useful to you.
In short, it automatically accepts room invites. You can specify that only 1:1 room invites are auto-accepted. Defaults to false if not specified.

If you decide that you'd like to let this playbook install it for you, you need a configuration like this:

```yaml
matrix_synapse_ext_synapse_auto_accept_invite_enabled: true

matrix_synapse_ext_synapse_auto_accept_invite_only_one_to_one: true
```