<!--
SPDX-FileCopyrightText: 2026 MDAD project contributors
SPDX-FileCopyrightText: 2026 Nikita Chernyi

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Setting up Mautrix LinkedIn bridging (optional)

<sup>Refer the common guide for configuring mautrix bridges: [Setting up a Generic Mautrix Bridge](configuring-playbook-bridge-mautrix-bridges.md)</sup>

The playbook can install and configure [mautrix-linkedin](https://github.com/mautrix/linkedin) for you, for bridging to [LinkedIn](https://www.linkedin.com/) messaging.

LinkedIn keeps its messaging behind a login wall with no usable public API, so this bridge does it the undignified way: it borrows your own browser's LinkedIn session, cookies copied out by hand. It works, it carries messages both ways, and it is held together with tape and good intentions. The login is clumsier than any QR-code bridge you have set up, and LinkedIn drops the session whenever it pleases. Go in expecting to redo it now and then, and you will be fine.

See the project's [documentation](https://docs.mau.fi/bridges/go/linkedin/index.html) to learn what it does and why it might be useful to you.

## Prerequisite (optional)

### Enable Appservice Double Puppet

If you want to set up [Double Puppeting](https://docs.mau.fi/bridges/general/double-puppeting.html) (hint: you most likely do) for this bridge automatically, you need to have enabled [Appservice Double Puppet](configuring-playbook-appservice-double-puppet.md) for this playbook.

See [this section](configuring-playbook-bridge-mautrix-bridges.md#set-up-double-puppeting-optional) on the [common guide for configuring mautrix bridges](configuring-playbook-bridge-mautrix-bridges.md) for details about setting up Double Puppeting.

## Adjusting the playbook configuration

To enable the bridge, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
matrix_bridge_mautrix_linkedin_enabled: true
```

If you previously ran the older, now-defunct `beeper-linkedin` bridge on this host, turn it off before you turn this one on. Both bridges claim the same `@linkedinbot` username and `@linkedin_*` user range as exclusive appservice namespaces, and two appservices brawling over one namespace means Synapse routes those users at random and one bridge can quietly act as the other's puppets. The playbook refuses to run with both enabled and says so to your face. Set `matrix_bridge_beeper_linkedin_enabled: false` and re-run the playbook first: its uninstall path pulls the old registration out of the way, and then this bridge comes up clean.

### Extending the configuration

There are some additional things you may wish to configure about the bridge.

<!-- NOTE: relay mode is not supported for this bridge -->
See [this section](configuring-playbook-bridge-mautrix-bridges.md#extending-the-configuration) on the [common guide for configuring mautrix bridges](configuring-playbook-bridge-mautrix-bridges.md) for details about variables that you can customize and the bridge's default configuration, including [bridge permissions](configuring-playbook-bridge-mautrix-bridges.md#configure-bridge-permissions-optional), [encryption support](configuring-playbook-bridge-mautrix-bridges.md#enable-encryption-optional), [bot's username](configuring-playbook-bridge-mautrix-bridges.md#set-the-bots-username-optional), etc.

## Installing

After configuring the playbook, run it with [playbook tags](playbook-tags.md) as below:

<!-- NOTE: let this conservative command run (instead of install-all) to make it clear that failure of the command means something is clearly broken. -->
```sh
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start
```

The shortcut commands with the [`just` program](just.md) are also available: `just install-all` or `just setup-all`

`just install-all` is useful for maintaining your setup quickly ([2x-5x faster](../CHANGELOG.md#2x-5x-performance-improvements-in-playbook-runtime) than `just setup-all`) when its components remain unchanged. If you adjust your `vars.yml` to remove other components, you'd need to run `just setup-all`, or these components will still remain installed. Note these shortcuts run the `ensure-matrix-users-created` tag too.

## Usage

Start a chat with `@linkedinbot:example.com` (where `example.com` is your base domain, the bare one without the `matrix.` prefix) and send `login`.

**Before you open devtools, read this, because it is where almost everyone gets stuck.** LinkedIn pins the session to the exact browser that made the request. Copy the cURL from Chrome, replay it from Firefox, and the session dies on the spot: no error, no "invalid login", just silence and a bot that stares back while you spend an hour wondering what you broke. You broke nothing; LinkedIn simply refused a session that arrived under the wrong user-agent. The bridge presents itself as Chrome on Linux, so grab your request from Chrome, or from a browser that lies about itself in exactly the same way. [mautrix-manager](https://github.com/mautrix/manager) does the whole grab with the right user-agent, if you would rather never think about any of this.

With the landmine flagged, here is the login itself. LinkedIn has no QR code, no OAuth, and no dignity, so you log in by handing the bot a request your own browser already made while signed in:

1. Open [linkedin.com](https://www.linkedin.com/) in a private/incognito window and sign in.
2. Open your browser's devtools (F12) and go to the Network tab.
3. Filter for `graphql`.
4. Right-click any one of those requests, then "Copy" and "Copy as cURL".
5. Paste that whole wall of text into the chat with the bot.

The bridge's [official Authentication guide](https://docs.mau.fi/bridges/go/linkedin/authentication.html) walks the same steps with screenshots. Once you log in, the bridge builds portal rooms for your recent conversations and carries messages both ways. Those cookies are a login session, and LinkedIn expires them whenever the mood strikes, days or weeks, no warning. When the bridge goes quiet, send `login` and run the devtools dance again. Nothing is broken, that is just how cookie auth ages.

## Troubleshooting

**The paste went through and the bot just sat there?** You grabbed the cURL in Firefox, Safari, or Edge, did you not, and that is the single most common reason anyone lands on this page. LinkedIn silently throws out a session replayed under a different user-agent. Redo the copy in Chrome, or match the bridge's user-agent, and try again.

**Worked yesterday, dead today?** Your LinkedIn cookies expired, which they do on LinkedIn's own whims, because a Fortune 500 company apparently treats session auth like a weekend hobby project. Send `login` to the bot and run the devtools dance one more time.

For everything else, as with all other services, you can find the logs in [systemd-journald](https://www.freedesktop.org/software/systemd/man/systemd-journald.service.html) by logging in to the server with SSH and running `journalctl -fu matrix-mautrix-linkedin`.

### Increase logging verbosity

The default logging level for this component is `warn`. If you want to increase the verbosity, add the following configuration to your `vars.yml` file and re-run the playbook:

```yaml
# Valid values: fatal, error, warn, info, debug, trace
matrix_bridge_mautrix_linkedin_logging_level: 'debug'
```
