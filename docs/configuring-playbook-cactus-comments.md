# Setting up Cactus Comments (optional)

The playbook can install and configure the [Cactus Comments](https://cactus.chat) system for you.

Cactus Comments is a **federated comment system** built on Matrix. It respects your privacy, and puts you in control.

See the project's [documentation](https://cactus.chat/docs/getting-started/introduction/) to learn what it does and why it might be useful to you.

The playbook contains 2 roles for configuring different pieces of the Cactus Comments system:

- `matrix-cactus-comments` - the backend appservice integrating with the Matrix homeserver

- `matrix-cactus-comments-client` - a static website server serving the [cactus-client](https://cactus.chat/docs/client/introduction/) static assets (`cactus.js` and `styles.css`)

You can enable whichever component you need (typically both).

## Configuration

Add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

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

# Uncomment and adjust this part if you'd like to host the client assets at a different location.
# These variables are only make used if (`matrix_cactus_comments_client_enabled: true`)
# matrix_cactus_comments_client_hostname: "{{ matrix_server_fqn_matrix }}"
# matrix_cactus_comments_client_path_prefix: /cactus-comments
```

## Installing

After configuring the playbook, run the [installation](installing.md) command: `just install-all` or `just setup-all`

## Usage

Upon starting Cactus Comments, a `bot.cactusbot` user account is created automatically.

To get started, send a `help` message to the `@bot.cactusbot:example.com` bot to confirm it's working.

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
