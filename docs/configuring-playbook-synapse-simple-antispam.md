# Setting up Synapse Simple Antispam (optional, advanced)

The playbook can install and configure [synapse-simple-antispam](https://github.com/t2bot/synapse-simple-antispam) for you.

It lets you fight invite-spam by automatically blocking invitiations from a list of servers specified by you (blacklisting).

See the project's [documentation](https://github.com/t2bot/synapse-simple-antispam/blob/master/README.md) to learn what it does and why it might be useful to you.

## Adjusting the playbook configuration

Add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file (adapt to your needs):

```yaml
matrix_synapse_ext_spam_checker_synapse_simple_antispam_enabled: true

matrix_synapse_ext_spam_checker_synapse_simple_antispam_config_blocked_homeservers:
- example.com
- example.net
```
