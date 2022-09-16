# Setting up Cactus Comments (optional)

The playbook can install and configure [Cactus Comments](https://cactus.chat) for you.

Cactus Comments is a **federated comment system** built on Matrix. The role allows you to self-host the system.
It respects your privacy, and puts you in control.

See the project's [documentation](https://cactus.chat/docs/getting-started/introduction/) to learn what it
does and why it might be useful to you.


## Configuration

Add the following block to your `vars.yaml` and make sure to exchange the tokens to randomly generated values.

```yaml
#################
## Cactus Chat ##
#################

matrix_cactus_comments_enabled: true

# To allow guest comments without users needing to log in, you need to have guest registration enabled.
# To do this you need to uncomment one of the following lines (depending if you are using synapse or dentrite as a homeserver)
# If you don't know which one you use: The default is synapse ;)
# matrix_synapse_allow_guest_access: true
# matrix_dentrite_allow_guest_access
```

## Installing

After configuring the playbook, run the [installation](installing.md) command again:

```
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start
```


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
