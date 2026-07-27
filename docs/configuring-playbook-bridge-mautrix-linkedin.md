<!--
SPDX-FileCopyrightText: 2026 MDAD project contributors
SPDX-FileCopyrightText: 2026 Nikita Chernyi
SPDX-FileCopyrightText: 2026 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Setting up Mautrix LinkedIn bridging (optional)

<sup>Refer the common guide for configuring mautrix bridges: [Setting up a Generic Mautrix Bridge](configuring-playbook-bridge-mautrix-bridges.md)</sup>

The playbook can install and configure [mautrix-linkedin](https://github.com/mautrix/linkedin) for you, for bridging to [LinkedIn](https://www.linkedin.com/) messaging.

See the project's [documentation](https://docs.mau.fi/bridges/go/linkedin/index.html) to learn what it does and why it might be useful to you.

>[!NOTE]
> LinkedIn keeps its messaging function behind a login wall and does not provide a usable public API, so using this bridge requires you to manually copy cookies on a web browser for logging in. Refer to [this section](#usage) below for details.

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

### Logging in

First you need to log in to LinkedIn to obtain the request which the web browser sent while signed in. Because the bridge presents itself as Chrome on Linux, you need to obtain it with **Chrome or a Chrome-based browser**.

>[!WARNING]
> LinkedIn pins the session to the exact browser that made the request, and refuses a session that arrived under a different user-agent. Therefore, if you copy the cURL from Chrome and replay it on Firefox, then the session dies right away.

You need to follow these steps to log in:

1. Open [linkedin.com](https://www.linkedin.com/) in a private/incognito window on Chrome / a Chrome-based browser
2. Sign in to LinkedIn
3. Open your browser's devtools (F12) and go to the Network tab
4. Filter for `graphql`
5. Right-click any one of those requests, then "Copy" and "Copy as cURL"
6. Paste the output into the chat with the bot and send it

The bridge's [official Authentication guide](https://docs.mau.fi/bridges/go/linkedin/authentication.html) walks the same steps with screenshots.

Once you log in, the bridge builds portal rooms for your recent conversations and carries messages both ways.

**💡 Notes:**

- The cookies are a login session, and LinkedIn can have them expired at their will. When the bridge seems to have become inactive, please re-log in by following the login steps.
- If you do not want to bother with request retrieval, you might want to take at look at [mautrix-manager](https://github.com/mautrix/manager).

## Troubleshooting

**Q. The paste went through, but the bot does not seem to be working.** — A. It is most likely because you have obtained the cURL output on other browsers than Chrome or a Chrome-based browser. LinkedIn silently throws out a session replayed under a different user-agent. Please try again with the log in steps described above on Chrome or a Chrome-based browser.

**Q. The bot worked yesterday, but does not work today. Why?** — A. It is likely because your LinkedIn cookies expired (or LinkedIn had it expired). Please send `login` to the bot, and follow the login steps described above again.

For everything else, as with all other services, you can find the logs in [systemd-journald](https://www.freedesktop.org/software/systemd/man/systemd-journald.service.html) by logging in to the server with SSH and running `journalctl -fu matrix-mautrix-linkedin`.

### Increase logging verbosity

The default logging level for this component is `warn`. If you want to increase the verbosity, add the following configuration to your `vars.yml` file and re-run the playbook:

```yaml
# Valid values: fatal, error, warn, info, debug, trace
matrix_bridge_mautrix_linkedin_logging_level: 'debug'
```
