# Setting up MX Puppet GroupMe (optional)

The playbook can install and configure
[mx-puppet-groupme](https://gitlab.com/robintown/mx-puppet-groupme) for you.

See the project page to learn what it does and why it might be useful to you.

To enable the [GroupMe](https://groupme.com/) bridge just use the following
playbook configuration:


```yaml
matrix_mx_puppet_groupme_enabled: true
matrix_mx_puppet_groupme_client_id: ""
matrix_mx_puppet_groupme_client_secret: ""
```


## Usage

Once the bot is enabled you need to start a chat with `GroupMe Puppet Bridge` with
the handle `@_groupmepuppet_bot:YOUR_DOMAIN` (where `YOUR_DOMAIN` is your base
domain, not the `matrix.` domain).

One authentication method is available.

To link your GroupMe account, go to [dev.groupme.com](https://dev.groupme.com/), sign in, and select "Access Token" from the top menu. Copy the token and message the bridge with:

```
link <access token>
```

Once logged in, send `listrooms` to the bot user to list the available rooms.

Clicking rooms in the list will result in you receiving an invitation to the
bridged room.

Also send `help` to the bot to see the commands available.
