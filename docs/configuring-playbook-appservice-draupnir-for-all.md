# Setting up Draupnir for All/D4A (optional)

The playbook can install and configure the [Draupnir](https://github.com/the-draupnir-project/Draupnir) moderation tool for you in appservice mode.

Appservice mode can be used together with the regular [Draupnir bot](configuring-playbook-bot-draupnir.md) or independently. Details about the differences between the 2 modes are described below.


## Draupnir Appservice mode compared to Draupnir bot mode

The administrative functions for managing the appservice are alpha quality and very limited. However, the experience of using an appservice-provisioned Draupnir is on par with the experience of using Draupnir from bot mode except in the case of avatar customisation as described later on in this document.

Draupnir for all is the way to go if you need more than 1 Draupnir instance, but you don't need access to Synapse Admin features as they are not accessible through Draupnir for All (Even though the commands do show up in help).

Draupnir for all in the playbook is rate-limit-exempt automatically as its appservice configuration file does not specify any rate limits.

Normal Draupnir does come with the benefit of access to Synapse Admin features. You are also able to more easily customise your normal Draupnir than D4A as D4A even on the branch with the Avatar command (To be Upstreamed to Mainline Draupnir) that command is clunky as it requires the use of things like Element devtools. In normal draupnir this is a quick operation where you login to Draupnir with a normal client and set Avatar and Display name normally.

Draupnir for all does not support external tooling like [MRU](https://mru.rory.gay) as it can't access Draupnir's user account.


## Installation

### 1. Create a main management room.

The playbook does not create a management room for your Main Draupnir. This task you have to do on your own.

The management room has to be given an alias and be public when you are setting up the bot for the first time as the bot does not differentiate between invites
and invites to the management room.

This management room is used to control who has access to your D4A deployment. The room stores this data inside of the control room state so your bot must have sufficient powerlevel to send custom state events. This is default 50 or moderator as Element calls this powerlevel.

As noted in the Draupnir install instructions the control room is sensitive. The following is said about the control room in the Draupnir install instructions.
>Anyone in this room can control the bot so it is important that you only invite trusted users to this room. The room must be unencrypted since the playbook does not support installing Pantalaimon yet.

### 2. Give your main management room an alias.

Give the room from step 1 an alias. This alias can be anything you want and its recommended for increased security during the setup phase of the bot that you make this alias be a random string. You can give your room a secondary human readable alias when it has been locked down after setup phase.

### 3. Adjusting the playbook configuration.

Add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file (adapt to your needs):

You must replace `ALIAS_FROM_STEP_2_GOES_HERE` with the alias you created in step 2.

```yaml
matrix_appservice_draupnir_for_all_enabled: true

matrix_appservice_draupnir_for_all_master_control_room_alias: "ALIAS_FROM_STEP_2_GOES_HERE"
```

### 4. Installing

After configuring the playbook, run the [installation](installing.md) command:

```
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start
```


## Usage

If you made it through all the steps above and your main control room was joined by a user called `@draupnir-main:example.com` you have succesfully installed Draupnir for All and can now start using it.

The installation of Draupnir for all in this playbook is very much Alpha quality. Usage-wise, Draupnir for allis almost identical to Draupnir bot mode.

### 1. Granting Users the ability to use D4A

Draupnir for all includes several security measures like that it only allows users that are on its allow list to ask for a bot. To add a user to this list we have 2 primary options. Using the chat to tell Draupnir to do this for us or if you want to automatically do it by sending `m.policy.rule.user` events that target the subject you want to allow provisioning for with the `org.matrix.mjolnir.allow` recomendation. Using the chat is recomended.

The bot requires a powerlevel of 50 in the management room to control who is allowed to use the bot. The bot does currently not say anything if this is true or false. (This is considered a bug and is documented in issue [#297](https://github.com/the-draupnir-project/Draupnir/issues/297))

To allow users or whole homeservers you type /plain @draupnir-main:example.com allow `target` and target can be either a MXID or a wildcard like `@*:example.com` to allow all users on example.com to register. We use /plain to force the client to not attempt to mess with this command as it can break Wildcard commands especially.

### 2. How to provision a D4A once you are allowed to.

Open a DM with @draupnir-main:example.com and if using Element send a message into this DM to finalise creating it. The bot will reject this invite and you will shortly get invited to the Draupnir control room for your newly provisioned Draupnir. From here its just a normal Draupnir experience.

Congratulations if you made it all the way here because you now have a fully working Draupnir for all deployment.

### Configuration of D4A

You can refer to the upstream [documentation](https://github.com/the-draupnir-project/Draupnir) for more configuration documentation. Please note that the playbook ships a full copy of the example config that does transfer to provisioned draupnirs in the production-bots.yaml.j2 file in the template directory of the role.

Please note that Config extension does not affect the appservices config as this config is not extensible in current Draupnir anyways. Config extension instead touches the config passed to the Draupnirs that your Appservice creates. So for example below makes all provisioned Draupnirs protect all joined rooms.

You can configure additional options by adding the `matrix_appservice_draupnir_for_all_extension_yaml` variable to your `inventory/host_vars/matrix.example.com/vars.yml` file.

For example to change draupnir's `protectAllJoinedRooms` option to `true` you would add the following to your `vars.yml` file.

```yaml
matrix_appservice_draupnir_for_all_extension_yaml: |
  # Your custom YAML configuration goes here.
  # This configuration extends the default starting configuration (`matrix_appservice_draupnir_for_all_yaml`).
  #
  # You can override individual variables from the default configuration, or introduce new ones.
  #
  # If you need something more special, you can take full control by
  # completely redefining `matrix_appservice_draupnir_for_all_yaml`.
  protectAllJoinedRooms: true
```
