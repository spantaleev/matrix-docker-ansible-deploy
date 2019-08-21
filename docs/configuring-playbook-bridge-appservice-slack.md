# Setting up Appservice Slack (optional)

The playbook can install and configure [matrix-appservice-slack](https://github.com/matrix-org/matrix-appservice-slack) for you.

See the project's [documentation](https://github.com/matrix-org/matrix-appservice-slack/blob/master/README.md) to learn what it does and why it might be useful to you.

Setup Instructions:

loosely based on [this](https://github.com/matrix-org/matrix-appservice-slack#Setup)

1. Create a new Matrix room to act as the administration control room. Note its internal room ID. This can
be done in Riot by making a message, opening the options for that message and choosing "view source". The
room ID will be displayed near the top.
2. Enable the bridge with the following configuration in your `vars.yml` file:

```yaml
matrix_appservice_slack_enabled: true
matrix_appservice_slack_control_room_id: "Your matrix admin room id"
```

3. If you've already installed Matrix services using the playbook before, you'll need to re-run it (`--tags=setup-all,start`). If not, proceed with [configuring other playbook services](configuring-playbook.md) and then with [Installing](installing.md). Get back to this guide once ready.
4. Invite the bridge bot user into the admin room:

```
    /invite @slackbot:MY.DOMAIN
```

Note that the bot's domain is your server's domain **without the `matrix.` prefix.**

5. Create a new Slack App [here](https://api.slack.com/apps).

    Name the app & select the team/workspace this app will belong to.

    Click on bot users and add a new bot user. We will use this account to bridge the the rooms.

6. Click on Event Subscriptions and enable them and use the request url `https://matrix.DOMAIN/appservice-slack`. Then add the following events and save:

     Bot User Events:

    - team_domain_change
    - message.channels
    - message.groups (if you want to bridge private channels)
    - reaction_added
    - reaction_removed

7. Click on OAuth & Permissions and add the following scopes:

    - chat:write:bot
    - users:read
    - reactions:write

    If you want to bridge files, also add the following:

    - files:write:user

    Note: In order to make Slack files visible to matrix users, this bridge will make Slack files visible to anyone with the url (including files in private channels). This is different than the current behavior in Slack, which only allows authenticated access to media posted in private channels. See MSC701 for details.

8. Click on Install App and Install App to Workspace. Note the access tokens shown. You will need the Bot User OAuth Access Token and if you want to bridge files, the OAuth Access Token whenever you link a room.

9. For each channel you would like to bridge, perform the following steps:

    * Create a Matrix room in the usual manner for your client. Take a note of its Matrix room ID - it will look something like !aBcDeF:example.com.

    * Invite the bot user to both the Slack and Matrix channels you would like to bridge using `/invite @slackbot` for slack and `/invite @slackbot:MY.DOMAIN` for matrix.

    * Determine the "channel ID" that Slack uses to identify the channel, which can be found in the url https://XXX.slack.com/messages/<channel id>/.

    * Issue a link command in the administration control room with these collected values as arguments:

        with file bridging:
    ```
        link --channel_id CHANNELID --room !the-matrix:room.id --slack_bot_token xoxb-xxxxxxxxxx-xxxxxxxxxxxxxxxxxxxx --slack_user_token xoxp-xxxxxxxx-xxxxxxxxx-xxxxxxxx-xxxxxxxx
    ```
        without file bridging:
    ```
        link --channel_id CHANNELID --room !the-matrix:room.id --slack_bot_token xoxb-xxxxxxxxxx-xxxxxxxxxxxxxxxxxxxx
    ```
        These arguments can be shortened to single-letter forms:
    ```
        link -I CHANNELID -R !the-matrix:room.id -t xoxb-xxxxxxxxxx-xxxxxxxxxxxxxxxxxxxx
    ```

Other configuration options are available via the `matrix_appservice_slack_configuration_extension_yaml` variable.
