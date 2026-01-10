<!--
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara
SPDX-FileCopyrightText: 2024 MDAD project contributors

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Setting up Draupnir for All/D4A (optional)

The playbook can install and configure the [Draupnir](https://github.com/the-draupnir-project/Draupnir) moderation tool for you in appservice mode.

Appservice mode can be used together with the regular [Draupnir bot](configuring-playbook-bot-draupnir.md) or independently. Details about the differences between the 2 modes are described below.

## Draupnir Appservice mode compared to Draupnir bot mode

The administrative functions for managing the appservice are alpha quality and very limited. However, the experience of using an appservice-provisioned Draupnir is on par with the experience of using Draupnir from bot mode except in the case of avatar customisation as described later on in this document.

Draupnir for all is the way to go if you need more than 1 Draupnir instance, but you don't need access to Synapse Admin features as they are not accessible through Draupnir for All (Even though the commands do show up in help).

Draupnir for all in the playbook is rate-limit-exempt automatically as its appservice configuration file does not specify any rate limits.

Normal Draupnir does come with the benefit of access to Synapse Admin features. You are also able to more easily customise your normal Draupnir than D4A as D4A even on the branch with the Avatar command (To be Upstreamed to Mainline Draupnir) that command is clunky as it requires the use of things like Element Web devtools. In normal Draupnir this is a quick operation where you login to Draupnir with a normal client and set Avatar and Display name normally.

Draupnir for all does not support external tooling like [MRU](https://mru.rory.gay) as it can't access Draupnir's user account.

## Prerequisites

### Create a main management room

The playbook does not create a management room for your Main Draupnir. You **need to create the room manually** before setting up the bot.

Note that the room must be unencrypted.

The management room has to be given an alias, and your bot has to be invited to the room.

This management room is used to control who has access to your D4A deployment. The room stores this data inside of the control room state so your bot must have sufficient powerlevel to send custom state events. This is default 50 or moderator as Element clients call this powerlevel.

> [!WARNING]
> Anyone in this room can control the bot so it is important that you only invite trusted users to this room.

## Adjusting the playbook configuration

Add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file. Make sure to replace `MANAGEMENT_ROOM_ALIAS_HERE`.

```yaml
matrix_appservice_draupnir_for_all_enabled: true

matrix_appservice_draupnir_for_all_config_adminRoom: "MANAGEMENT_ROOM_ALIAS_HERE"
```

### Extending the configuration

There are some additional things you may wish to configure about the component.

Take a look at:

- `roles/custom/matrix-appservice-draupnir-for-all/defaults/main.yml` for some variables that you can customize via your `vars.yml` file. You can override settings (even those that don't have dedicated playbook variables) using the `matrix_appservice_draupnir_for_all_configuration_extension_yaml` variable

For example, to change Draupnir's `protectAllJoinedRooms` option to `true`, add the following configuration to your `vars.yml` file:

```yaml
matrix_appservice_draupnir_for_all_configuration_extension_yaml: |
  # Your custom YAML configuration goes here.
  # This configuration extends the default starting configuration (`matrix_appservice_draupnir_for_all_configuration_yaml`).
  #
  # You can override individual variables from the default configuration, or introduce new ones.
  #
  # If you need something more special, you can take full control by
  # completely redefining `matrix_appservice_draupnir_for_all_configuration_yaml`.
  protectAllJoinedRooms: true
```

You can refer to the upstream [documentation](https://github.com/the-draupnir-project/Draupnir) for more configuration documentation.

**Notes**:

- The playbook ships a full copy of the example config that does transfer to provisioned Draupnirs in the production-bots.yaml.j2 file in the template directory of the role.

- Config extension does not affect the appservices config as this config is not extensible in current Draupnir anyway. It instead touches the config passed to the Draupnirs that your Appservice creates. So the example above (`protectAllJoinedRooms: true`) makes all provisioned Draupnirs protect all joined rooms.

## Installing

After configuring the playbook, run it with [playbook tags](playbook-tags.md) as below:

<!-- NOTE: let this conservative command run (instead of install-all) to make it clear that failure of the command means something is clearly broken. -->
```sh
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start
```

**Notes**:

- The shortcut commands with the [`just` program](just.md) are also available: `just install-all` or `just setup-all`

  `just install-all` is useful for maintaining your setup quickly ([2x-5x faster](../CHANGELOG.md#2x-5x-performance-improvements-in-playbook-runtime) than `just setup-all`) when its components remain unchanged. If you adjust your `vars.yml` to remove other components, you'd need to run `just setup-all`, or these components will still remain installed.

## Usage

If you made it through all the steps above and your main control room was joined by a user called `@draupnir-main:example.com` you have successfully installed Draupnir for All and can now start using it.

The installation of Draupnir for all in this playbook is very much Alpha quality. Usage-wise, Draupnir for all is almost identical to Draupnir bot mode.

### Granting Users the ability to use D4A

Draupnir for all includes several security measures like that it only allows users that are on its allow list to ask for a bot. To add a user to this list we have 2 primary options. Using the chat to tell Draupnir to do this for us or if you want to automatically do it by sending `m.policy.rule.user` events that target the subject you want to allow provisioning for with the `org.matrix.mjolnir.allow` recommendation. Using the chat is recommended.

The bot requires a powerlevel of 50 in the management room to control who is allowed to use the bot. The bot does currently not say anything if this is true or false. (This is considered a bug and is documented in issue [#297](https://github.com/the-draupnir-project/Draupnir/issues/297))

To allow users or whole homeservers you type /plain !admin allow `target` and target can be either a MXID or a wildcard like `@*:example.com` to allow all users on example.com to register. We use /plain to force the client to not attempt to mess with this command as it can break Wildcard commands especially.

### How to provision a D4A once you are allowed to

To provision a D4A, you need to start a chat with `@draupnir-main:example.com`. The bot will reject this invite and you will shortly get invited to the Draupnir control room for your newly provisioned Draupnir. From here its just a normal Draupnir experience.

Congratulations if you made it all the way here because you now have a fully working Draupnir for all deployment.
