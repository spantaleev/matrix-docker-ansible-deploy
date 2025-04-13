<!--
SPDX-FileCopyrightText: 2022 - 2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2022 Julian-Samuel Gebühr
SPDX-FileCopyrightText: 2023 MDAD project contributors
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Setting up Cactus Comments (optional)

The playbook can install and configure the [Cactus Comments](https://cactus.chat) system for you.

Cactus Comments is a **federated comment system** built on Matrix. It respects your privacy, and puts you in control.

See the project's [documentation](https://cactus.chat/docs/getting-started/introduction/) to learn what it does and why it might be useful to you.

The playbook contains 2 roles for configuring different pieces of the Cactus Comments system:

- `matrix-cactus-comments` — the backend appservice integrating with the Matrix homeserver

- `matrix-cactus-comments-client` — a static website server serving the [cactus-client](https://cactus.chat/docs/client/introduction/) static assets (`cactus.js` and `styles.css`)

You can enable whichever component you need (typically both).

## Adjusting DNS records (optional)

By default, this playbook installs Cactus Comments' client on the `matrix.` subdomain, at the `/cactus-comments` path (https://matrix.example.com/cactus-comments). This makes it easy to install it, because it **doesn't require additional DNS records to be set up**. If that's okay, you can skip this section.

If you wish to adjust it, see the section [below](#adjusting-the-cactus-comments-client-url-optional) for details about DNS configuration.

## Adjusting the playbook configuration

To enable Cactus Comments, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
# This enables the backend (appservice)
matrix_cactus_comments_enabled: true

# This enables client assets static files serving on `https://matrix.example.com/cactus-comments`.
# When the backend (appservice) is enabled, this is also enabled automatically, but we explicitly enable it here.
matrix_cactus_comments_client_enabled: true

# Uncomment and adjust this part if you'd like to use a username different than the default
# matrix_cactus_comments_user_id: "bot.cactusbot"

# To allow guest comments without users needing to log in, you need to have guest registration enabled.
# To do this you need to uncomment one of the following lines (depending if you are using Synapse or Dendrite as a homeserver)
# If you don't know which one you use: The default is Synapse ;)
# matrix_synapse_allow_guest_access: true
# matrix_dendrite_allow_guest_access: true
```

### Adjusting the Cactus Comments' client URL (optional)

By tweaking the `matrix_cactus_comments_client_hostname` and `matrix_cactus_comments_client_path_prefix` variables, you can easily make the service available at a **different hostname and/or path** than the default one.

Example additional configuration for your `vars.yml` file:

```yaml
# Change the default hostname and path prefix to host the client assets at a different location
# These variables are used only if (`matrix_cactus_comments_client_enabled: true`)
matrix_cactus_comments_client_hostname: cactus.example.com
matrix_cactus_comments_client_path_prefix: /
```

If you've changed the default hostname, you may need to create a CNAME record for the Cactus Comments' client domain (`cactus.example.com`), which targets `matrix.example.com`.

When setting, replace `example.com` with your own.

### Extending the configuration

There are some additional things you may wish to configure about the components.

For `matrix-cactus-comments`, take a look at:

- `roles/custom/matrix-cactus-comments/defaults/main.yml` for some variables that you can customize via your `vars.yml` file

For `matrix-cactus-comments-client`, take a look at:

- `roles/custom/matrix-cactus-comments-client/defaults/main.yml` for some variables that you can customize via your `vars.yml` file

## Installing

After configuring the playbook and potentially [adjusting your DNS records](#adjusting-dns-records), run the playbook with [playbook tags](playbook-tags.md) as below:

<!-- NOTE: let this conservative command run (instead of install-all) to make it clear that failure of the command means something is clearly broken. -->
```sh
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start
```

The shortcut commands with the [`just` program](just.md) are also available: `just install-all` or `just setup-all`

`just install-all` is useful for maintaining your setup quickly ([2x-5x faster](../CHANGELOG.md#2x-5x-performance-improvements-in-playbook-runtime) than `just setup-all`) when its components remain unchanged. If you adjust your `vars.yml` to remove other components, you'd need to run `just setup-all`, or these components will still remain installed. Note these shortcuts run the `ensure-matrix-users-created` tag too.

## Usage

To use the component, you need to start a chat with `@bot.cactusbot:example.com` (where `example.com` is your base domain, not the `matrix.` domain).

Then, register a site by sending `register YOUR_SITE_NAME_HERE` (where `YOUR_SITE_NAME_HERE` is a unique identifier you choose. It does not have to match your domain). You will then be invited into a moderation room.

Now you are good to go and can embed the comment section on your website!

## Embed Cactus Comments

The official [documentation](https://cactus.chat/docs/getting-started/quick-start/) provides a useful guide to embed Cactus Comments on your website.

After including the JavaScript and CSS asset files, insert a `<div>` where you'd like to display the comment section:

````html
<div id="comment-section"></div>
````

Then, you need to initialize the comment section. Make sure to replace `example.com` with your base domain and `YOUR_SITE_NAME_HERE` with the one that has been registered above:

```html
<script>
initComments({
  node: document.getElementById("comment-section"),
  defaultHomeserverUrl: "https://matrix.example.com:8448",
  serverName: "example.com",
  siteName: "YOUR_SITE_NAME_HERE",
  commentSectionId: "1"
})
</script>
```

### Adjust the domain name for self-hosting

To have the assets served from your homeserver (not from `cactus.chat`), you need to adjust the domain name on the official documentation.

Make sure to replace `example.com` with your base domain before you include the following lines, instead of the one provided by the official documentation:

```html
<script type="text/javascript" src="https://matrix.example.com/cactus-comments/cactus.js"></script>
<link rel="stylesheet" href="https://matrix.example.com/cactus-comments/style.css" type="text/css">
```

**Note**: if the `matrix_cactus_comments_client_hostname` and `matrix_cactus_comments_client_path_prefix` variables are tweaked, you would need to adjust the URLs of the assets accordingly.

## Troubleshooting

As with all other services, you can find the logs in [systemd-journald](https://www.freedesktop.org/software/systemd/man/systemd-journald.service.html) by logging in to the server with SSH and running `journalctl -fu matrix-cactus-comments` for the backend appservice or `journalctl -fu matrix-cactus-comments-client` for the server serving the client assets, respectively.

### Increase logging verbosity

It is possible to increase logging verbosity for `matrix-cactus-comments-client`. The default logging level for this component is `error`. If you want to increase the verbosity, add the following configuration to your `vars.yml` file and re-run the playbook:

```yaml
# Controls the SERVER_LOG_LEVEL environment variable.
# See: https://static-web-server.net/configuration/environment-variables/
# Valid values: error, warn, info, debug, trace
matrix_cactus_comments_client_environment_variable_server_log_level: debug
```
