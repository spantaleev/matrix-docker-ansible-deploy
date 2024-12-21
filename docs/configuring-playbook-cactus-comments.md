# Setting up Cactus Comments (optional)

The playbook can install and configure the [Cactus Comments](https://cactus.chat) system for you.

Cactus Comments is a **federated comment system** built on Matrix. It respects your privacy, and puts you in control.

See the project's [documentation](https://cactus.chat/docs/getting-started/introduction/) to learn what it does and why it might be useful to you.

The playbook contains 2 roles for configuring different pieces of the Cactus Comments system:

- `matrix-cactus-comments` - the backend appservice integrating with the Matrix homeserver

- `matrix-cactus-comments-client` - a static website server serving the [cactus-client](https://cactus.chat/docs/client/introduction/) static assets (`cactus.js` and `styles.css`)

You can enable whichever component you need (typically both).

## Configuration

To enable Cactus Comments, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
#################
## Cactus Comments ##
#################

# This enables the backend (appservice)
matrix_cactus_comments_enabled: true

# To allow guest comments without users needing to log in, you need to have guest registration enabled.
# To do this you need to uncomment one of the following lines (depending if you are using Synapse or Dendrite as a homeserver)
# If you don't know which one you use: The default is Synapse ;)
# matrix_synapse_allow_guest_access: true
# matrix_dendrite_allow_guest_access: true

# This enables client assets static files serving on `https://matrix.example.com/cactus-comments`.
# When the backend (appservice) is enabled, this is also enabled automatically,
# but we explicitly enable it here.
matrix_cactus_comments_client_enabled: true
```

### Adjusting the Cactus Comments' client URL

By default, this playbook installs Cactus Comments' client on the `matrix.` subdomain, at the `/cactus-comments` path (https://matrix.example.com/cactus-comments). This makes it easy to install it, because it **doesn't require additional DNS records to be set up**. If that's okay, you can skip this section.

By tweaking the `matrix_cactus_comments_client_hostname` and `matrix_cactus_comments_client_path_prefix` variables, you can easily make the service available at a **different hostname and/or path** than the default one.

Example additional configuration for your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
# Change the default hostname and path prefix to host the client assets at a different location
# These variables are used only if (`matrix_cactus_comments_client_enabled: true`)
matrix_cactus_comments_client_hostname: cactus.example.com
matrix_cactus_comments_client_path_prefix: /
```

## Adjusting DNS records

If you've changed the default hostname, **you may need to adjust your DNS** records to point the Cactus Comments' client domain to the Matrix server.

See [Configuring DNS](configuring-dns.md) for details about DNS changes.

If you've decided to use the default hostname, you won't need to do any extra DNS configuration.

## Installing

After configuring the playbook and potentially [adjusting your DNS records](#adjusting-dns-records), run the playbook with [playbook tags](playbook-tags.md) as below:

<!-- NOTE: let this conservative command run (instead of install-all) to make it clear that failure of the command means something is clearly broken. -->
```sh
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,ensure-matrix-users-created,start
```

**Notes**:

- The `ensure-matrix-users-created` playbook tag makes the playbook automatically create the bot's user account.

- The shortcut commands with the [`just` program](just.md) are also available: `just install-all` or `just setup-all`

  `just install-all` is useful for maintaining your setup quickly ([2x-5x faster](../CHANGELOG.md#2x-5x-performance-improvements-in-playbook-runtime) than `just setup-all`) when its components remain unchanged. If you adjust your `vars.yml` to remove other components, you'd need to run `just setup-all`, or these components will still remain installed.

## Usage

Upon starting Cactus Comments, a `bot.cactusbot` user account is created automatically.

To get started, send `help` to the `@bot.cactusbot:example.com` bot to confirm it's working.

Then, register a site by sending `register <YourSiteName>` (where `<YourSiteName>` is a unique identifier you choose. It does not have to match your domain). You will then be invited into a moderation room.

Now you are good to go and can embed the comment section on your website!

## Embed Cactus Comments

The official [documentation](https://cactus.chat/docs/getting-started/quick-start/) provides a useful guide to embed Cactus Comments on your website.

After including the JavaScript and CSS asset files, insert a `<div>` where you'd like to display the comment section:

````html
<div id="comment-section"></div>
````

Then, you need to initialize the comment section. Make sure to replace `example.com` with your base domain and `<YourSiteName>` with the one that has been registered above:

```html
<script>
initComments({
  node: document.getElementById("comment-section"),
  defaultHomeserverUrl: "https://matrix.example.com:8448",
  serverName: "example.com",
  siteName: "<YourSiteName>",
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
