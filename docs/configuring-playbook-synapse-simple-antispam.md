<!--
SPDX-FileCopyrightText: 2019 Slavi Pantaleev
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Setting up Synapse Simple Antispam (optional, advanced)

The playbook can install and configure [synapse-simple-antispam](https://github.com/t2bot/synapse-simple-antispam) for you.

It lets you fight invite-spam by automatically blocking invitations from a list of servers specified by you (blacklisting).

See the project's [documentation](https://github.com/t2bot/synapse-simple-antispam/blob/master/README.md) to learn what it does and why it might be useful to you.

## Adjusting the playbook configuration

Add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file (adapt to your needs):

```yaml
matrix_synapse_ext_spam_checker_synapse_simple_antispam_enabled: true

matrix_synapse_ext_spam_checker_synapse_simple_antispam_config_blocked_homeservers:
- example.com
- example.net
```

## Installing

After configuring the playbook, run it with [playbook tags](playbook-tags.md) as below:

<!-- NOTE: let this conservative command run (instead of install-all) to make it clear that failure of the command means something is clearly broken. -->
```sh
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start
```

The shortcut commands with the [`just` program](just.md) are also available: `just install-all` or `just setup-all`

`just install-all` is useful for maintaining your setup quickly ([2x-5x faster](../CHANGELOG.md#2x-5x-performance-improvements-in-playbook-runtime) than `just setup-all`) when its components remain unchanged. If you adjust your `vars.yml` to remove other components, you'd need to run `just setup-all`, or these components will still remain installed. Note these shortcuts run the `ensure-matrix-users-created` tag too.
