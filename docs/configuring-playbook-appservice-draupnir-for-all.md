# Setting up Draupnir for All/D4A (optional)

The playbook can install and configure the [Draupnir](https://github.com/the-draupnir-project/Draupnir) moderation tool for you in appservice mode.

Appservice mode can be used together with the regular [Draupnir bot](configuring-playbook-bot-draupnir.md) or independently.

D4A compared to Draupnir Normal. 

Draupnir for all is the way to go if you need more than 1 Draupnir but you don't need access to Synapse Admin features as they are not accessible thru Draupnir for All (Even tho the commands do show up in help). 

Draupnir for all in the playbook is rate limit exempt automatically as its part of the appservice configuration file if the appservice is rate limited or not. 

Normal Draupnir does come with the benefit of access to Synapse Admin features. You are also able to more easily customise your normal Draupnir than D4A as D4A even on the branch with the Avatar command (To be Upstreamed to Mainline Draupnir) that command is clunky as it requires the use of things like Element devtools. In normal draupnir this is a quick operation where you login to Draupnir with a normal client and set Avatar and Display name normally. 

Draupnir for all does also not support external tooling like [MRU](https://mru.rory.gay) as it cant access Draupnirs user account like is needed to use it. 

Last downside of Draupnir for all is the state of the Admin side of the user experience being Alpha quality. This flaw is not in regular Draupnir and is mostly not in the provisioned Draupnirs either.

## 1. Create a main management room.

The playbook does not create a management room for your Main Draupnir. This task you have to do on your own. 

The management room has to be given an alias and be public when you are setting up the bot for the first time as the bot does not differentiate between invites
and invites to the management room. 

This management room is used to control who has access to your D4A deployment. The room stores this data inside of the control room state so your bot must have sufficient powerlevel to send custom state events. This is default 50 or moderator as Element calls this powerlevel.

As noted in the Draupnir install instructions the control room is sensitive. The following is said about the control room in the Draupnir install instructions. 
>Anyone in this room can control the bot so it is important that you only invite trusted users to this room. The room must be unencrypted since the playbook does not support installing Pantalaimon yet.

## 2. Give your main management room an alias.

Give the room from step 1 an alias. This alias can be anything you want and its recommended for increased security during the setup phase of the bot that you make this alias be a random string. You can give your room a secondary human readable alias when it has been locked down after setup phase.

## 3. Adjusting the playbook configuration.

Add the following configuration to your `inventory/host_vars/matrix.DOMAIN/vars.yml` file (adapt to your needs):

You must replace `ALIAS_FROM_STEP_2_GOES_HERE` with the alias you created in step 2.

```yaml
matrix_appservice_draupnir_for_all_enabled: true

matrix_appservice_draupnir_for_all_master_control_room_alias: "ALIAS_FROM_STEP_2_GOES_HERE"
```

## 4. Installing

After configuring the playbook, run the [installation](installing.md) command:

```
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start
```

# Using Draupnir For All

If you made it thru all the steps above and your main control room was joined by a user called `@draupnir-main:matrix-homeserver-domain` you have succesfully installed Draupnir for All and can now start using it. 

This side of Draupnir for all is very much Alpha quality in the user experience it should be noted. Draupnir for all on the end user side is almost identical to Draupnir normal mode. 

## 1. Granting Users the ability to use D4A

Draupnir for all includes several security measures like that it only allows users that are on its allow list to ask for a bot. To add a user to this list we have 2 primary options. Using the chat to tell Draupnir to do this for us or manually sending the state event via either curl or devtools in Element. 

If you want to give individual users access grants the recommended way is via the chat. To use the chat to tell Draupnir to do things you need to ping it in a specific way. Clients like Element and nheko will do this correctly by default because they send `<a href=\"https://matrix.to/#/@example:example.com\">Example</a>:` when you try to mention a user. Draupnir expects this format and will NOT respond to anything else in the main control room. As mentioned earlier D4A is Alpha in its user experience for the main control room.

The command is `<a href=\"https://matrix.to/#/@example:example.com\">Example</a>: allow mxid`

If you want to allow all users on your homeserver you instead send a `m.policy.rule.user` event with the contents being `{"entity": "@*:matrix-homeserver-domain", "recommendation": "org.matrix.mjolnir.allow"}` and a `state_key` that is `_*:matrix-homeserver-domain`.

Using curl you can send this via `curl --request PUT --url 'https://homeserver_url/_matrix/client/v3/rooms/management_room_room_ID/state/m.policy.rule.user/_*:matrix-homeserver-domain' --header 'Authorization: Bearer ACCESS_TOKEN_HERE' --header 'Content-Type: application/json' --data '{"entity": "@*:matrix-homeserver-domain", "recommendation": "org.matrix.mjolnir.allow"}'`

## 2. How to provision a D4A once you are allowed to.

Open a DM with @draupnir-main:matrix-homeserver-domain and if using Element send a message into this DM to finalise creating it. The bot will reject this invite and you will shortly get invited to the Draupnir control room for your newly provisioned Draupnir. From here its just a normal Draupnir experience. 

Congratulations if you made it all the way here because you now have a fully working Draupnir for all deployment.

## Configuration of D4A

You can refer to the upstream [documentation](https://github.com/the-draupnir-project/Draupnir) for more configuration documentation. Please note that the playbook ships a full copy of the example config that does transfer to provisioned draupnirs in the production-bots.yaml.j2 file in the template directory of the role.

Please note that Config extension does not affect the appservices config as this config is not extensible in current Draupnir anyways. Config extension instead touches the config passed to the Draupnirs that your Appservice creates. So for example below makes all provisioned Draupnirs protect all joined rooms.

You can configure additional options by adding the `matrix_appservice_draupnir_for_all_extension_yaml` variable to your `inventory/host_vars/matrix.DOMAIN/vars.yml` file.

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