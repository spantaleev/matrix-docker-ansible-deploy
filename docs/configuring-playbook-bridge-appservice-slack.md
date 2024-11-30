# Setting up Appservice Slack bridging (optional)

**Notes**:
- Bridging to [Slack](https://slack.com) can also happen via the [mx-puppet-slack](configuring-playbook-bridge-mx-puppet-slack.md) and [mautrix-slack](configuring-playbook-bridge-mautrix-slack.md) bridges supported by the playbook.
- Currently (as of November, 2024) **this component is not available for new installation unless you have already created a classic Slack application** (which the bridge makes use of in order to enable bridging between Slack and Matrix), because the creation of classic Slack applications has been discontinued since June 4 2024. The author of the bridge claims [here](https://github.com/matrix-org/matrix-appservice-slack/issues/789#issuecomment-2172947787) that he plans to support the modern Slack application and until then "the best (and only) option for new installations is to use the webhook bridging".

The playbook can install and configure [matrix-appservice-slack](https://github.com/matrix-org/matrix-appservice-slack) for you.

See the project's [documentation](https://github.com/matrix-org/matrix-appservice-slack/blob/master/README.md) to learn what it does and why it might be useful to you.

## Prerequisites

### Create a Classic Slack App

First, you need to create a Classic Slack App [here](https://api.slack.com/apps?new_classic_app=1).

Name the app "matrixbot" (or anything else you'll remember). Select the team/workspace this app will belong to. Click on bot users and add a new bot user. We will use this account to bridge the the rooms.

Then, click on Event Subscriptions and enable them and use the request url: `https://matrix.example.com/appservice-slack`.

Add the following events as `Bot User Events` and save:

- team_domain_change
- message.channels
- message.groups (if you want to bridge private channels)
- reaction_added
- reaction_removed

Next, click on "OAuth & Permissions" and add the following scopes:

- chat:write:bot
- users:read
- reactions:write
- files:write:user (if you want to bridge files)

**Note**: In order to make Slack files visible to Matrix users, this bridge will make Slack files visible to anyone with the url (including files in private channels). This is different than the current behavior in Slack, which only allows authenticated access to media posted in private channels. See MSC701 for details.

Click on "Install App" and "Install App to Workspace". Note the access tokens shown. You will need the Bot User OAuth Access Token and if you want to bridge files, the OAuth Access Token whenever you link a room.

### Create an administration control room on Matrix

Create a new Matrix room to act as the administration control room.

Note its internal room ID. This can be done in Element Web by sending a message, opening the options for that message and choosing "view source". The room ID will be displayed near the top.

## Adjusting the playbook configuration

To enable the bridge, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
matrix_appservice_slack_enabled: true
matrix_appservice_slack_control_room_id: "Your Matrix admin room ID"

# Uncomment to enable puppeting (optional, but recommended)
# matrix_appservice_slack_puppeting_enabled: true
# matrix_appservice_slack_puppeting_slackapp_client_id: "Your Classic Slack App Client ID"
# matrix_appservice_slack_puppeting_slackapp_client_secret: "Your Classic Slack App Client Secret"

# Uncomment to enable Team Sync (optional)
# See https://matrix-appservice-slack.readthedocs.io/en/latest/team_sync/
# matrix_appservice_slack_team_sync_enabled: true
```

Other configuration options are available via the `matrix_appservice_slack_configuration_extension_yaml` variable.

## Installing

After configuring the playbook, run it with [playbook tags](playbook-tags.md) as below:

<!-- NOTE: let this conservative command run (instead of install-all) to make it clear that failure of the command means something is clearly broken. -->
```sh
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,ensure-matrix-users-created,start
```

**Notes**:

- The `ensure-matrix-users-created` playbook tag makes the playbook automatically create the bot's user account.

- The shortcut commands with `just` program are also available: `just install-all` or `just setup-all`

  `just install-all` is useful for maintaining your setup quickly when its components remain unchanged. If you adjust your `vars.yml` to remove other components, you'd need to run `just setup-all`, or these components will still remain installed. For more information about `just` shortcuts, take a look at this page: [Running `just` commands](just.md)

## Usage

Send `/invite @slackbot:example.com` to invite the bridge bot user into the admin room.

If Team Sync is not enabled, for each channel you would like to bridge, perform the following steps:

- Create a Matrix room in the usual manner for your client. Take a note of its Matrix room ID - it will look something like `!qporfwt:example.com`.
- Invite the bot user to both the Slack and Matrix channels you would like to bridge using `/invite @matrixbot` for Slack and `/invite @slackbot:example.com` for Matrix.
- Determine the "channel ID" that Slack uses to identify the channel. You can see it when you open a given Slack channel in a browser. The URL reads like this: `https://app.slack.com/client/XXX/<the channel ID>/details/`.
- Issue a link command in the administration control room with these collected values as arguments:

    with file bridging:

    ```
    link --channel_id CHANNELID --room !qporfwt:example.com --slack_bot_token xoxb-xxxxxxxxxx-xxxxxxxxxxxxxxxxxxxx --slack_user_token xoxp-xxxxxxxx-xxxxxxxxx-xxxxxxxx-xxxxxxxx
    ```

    without file bridging:

    ```
    link --channel_id CHANNELID --room !qporfwt:example.com --slack_bot_token xoxb-xxxxxxxxxx-xxxxxxxxxxxxxxxxxxxx
    ```

    These arguments can be shortened to single-letter forms:

    ```
    link -I CHANNELID -R !qporfwt:example.com -t xoxb-xxxxxxxxxx-xxxxxxxxxxxxxxxxxxxx
    ```

### Unlinking

Channels can be unlinked again by sending this:

```
unlink --room !qporfwt:example.com
```

Unlinking doesn't only disconnect the bridge, but also makes the slackbot leave the bridged Matrix room. So in case you want to re-link later, don't forget to re-invite the slackbot into this room again.

## Troubleshooting

As always, check the logs: `journalctl -fu matrix-appservice-slack`

### Linking: "Room is now pending-name"

This typically means that you haven't used the correct Slack channel ID. Unlink the room and recheck 'Determine the "channel ID"' from above.

### Messages work from Matrix to Slack, but not the other way around

Check you logs, if they say something like

`WARN SlackEventHandler Ignoring message from unrecognised Slack channel ID : %s (%s) <the channel ID> <some other ID>`

then unlink your room, reinvite the bot and re-link it again. This may particularly hit you, if you tried to unsuccessfully link your room multiple times without unlinking it after each failed attempt.
