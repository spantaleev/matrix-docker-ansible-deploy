# Setting up Cactus Comments (optional)

The playbook can install and configure the [Cactus Comments](https://cactus.chat) system for you.

Cactus Comments is a **federated comment system** built on Matrix. It respects your privacy, and puts you in control.

See the project's [documentation](https://cactus.chat/docs/getting-started/introduction/) to learn what it
does and why it might be useful to you.

The playbook contains 2 roles for configuring different pieces of the Cactus Comments system:

- `matrix-cactus-comments` - the backend appservice integrating with the Matrix homeserver

- `matrix-cactus-comments-client` - a static website server serving the [cactus-client](https://cactus.chat/docs/client/introduction/) static assets (`cactus.js` and `styles.css`)

You can enable whichever component you need (typically both).

## Configuration

Add the following block to your `vars.yaml` and make sure to exchange the tokens to randomly generated values.

```yaml
#################
## Cactus Chat ##
#################

# This enables the backend (appservice)
matrix_cactus_comments_enabled: true

# To allow guest comments without users needing to log in, you need to have guest registration enabled.
# To do this you need to uncomment one of the following lines (depending if you are using Synapse or Dendrite as a homeserver)
# If you don't know which one you use: The default is Synapse ;)
# matrix_synapse_allow_guest_access: true
# matrix_dendrite_allow_guest_access: true

# This enables client assets static files serving on `https://matrix.DOMAIN/cactus-comments`.
# When the backend (appservice) is enabled, this is also enabled automatically,
# but we explicitly enable it here.
matrix_cactus_comments_client_enabled: true

# Uncomment and adjust if you'd like to host the client assets at a different location.
# These variables are only make used if (`matrix_cactus_comments_client_enabled: true`)
# matrix_cactus_comments_client_hostname: "{{ matrix_server_fqn_matrix }}"
# matrix_cactus_comments_client_path_prefix: /cactus-comments
```

## Installing

After configuring the playbook, run the [installation](installing.md) command again.


## Usage

Upon starting Cactus Comments, a `bot.cactusbot` user account is created automatically.

To get started, send a `help` message to the `@bot.cactusbot:your-homeserver.com` bot to confirm it's working.
Then, register a site by typing: `register <sitename>`. You will then be invited into a moderation room.
Now you are good to go and can include the comment section on your website!

**Careful:** To really make use of self-hosting you need change a few things in comparison to the official docs!

Insert the following snippet into you page and make sure to replace `example.com` with your base domain!

```html
<script type="text/javascript" src="https://matrix.example.com/cactus-comments/cactus.js"></script>
<link rel="stylesheet" href="https://matrix.example.com/cactus-comments/style.css" type="text/css">
<div id="comment-section"></div>
<script>
initComments({
  node: document.getElementById("comment-section"),
  defaultHomeserverUrl: "https://matrix.example.com:8448",
  serverName: "example.com",
  siteName: "YourSiteName",
  commentSectionId: "1"
})
</script>
```
