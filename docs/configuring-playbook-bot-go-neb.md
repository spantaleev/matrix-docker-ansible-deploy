# Setting up Go-NEB (optional)

The playbook can install and configure [Go-NEB](https://github.com/matrix-org/go-neb) for you.

Go-NEB is a Matrix bot written in Go. It is the successor to Matrix-NEB, the original Matrix bot written in Python.

See the project's [documentation](https://github.com/matrix-org/go-neb) to learn what it does and why it might be useful to you.


## Registering the bot user

The playbook does not automatically create users for you. The bot requires at least 1 access token to be able to connect to your homeserver.

You **need to register the bot user manually** before setting up the bot.

Choose a strong password for the bot. You can generate a good password with a command like this: `pwgen -s 64 1`.

You can use the playbook to [register a new user](registering-users.md):

```
ansible-playbook -i inventory/hosts setup.yml --extra-vars='username=bot.go-neb password=PASSWORD_FOR_THE_BOT admin=no' --tags=register-user
```


## Getting an access token

If you use curl, you can get an access token like this:

```
curl -X POST --header 'Content-Type: application/json' -d '{
    "identifier": { "type": "m.id.user", "user": "bot.go-neb" },
    "password": "a strong password",
    "type": "m.login.password"
}' 'https://matrix.YOURDOMAIN/_matrix/client/r0/login'
```

Alternatively, you can use a full-featured client (such as Element) to log in and get the access token from there (note: don't log out from the client as that will invalidate the token), but doing so might lead to decryption problems. That warning comes from [here](https://github.com/matrix-org/go-neb#quick-start).


## Adjusting the playbook configuration

Add the following configuration to your `inventory/host_vars/matrix.DOMAIN/vars.yml` file (adapt to your needs):

```yaml
matrix_bot_go_neb_enabled: true

# You need at least 1 client.
# Use the access token you obtained in the step above.
matrix_bot_go_neb_clients:
  - UserID: "@goneb:{{ matrix_domain }}"
    AccessToken: "MDASDASJDIASDJASDAFGFRGER"
    DeviceID: "DEVICE1"
    HomeserverURL: "{{ matrix_homeserver_container_url }}"
    Sync: true
    AutoJoinRooms: true
    DisplayName: "Go-NEB!"
    AcceptVerificationFromUsers: [":{{ matrix_domain }}"]

  - UserID: "@another_goneb:{{ matrix_domain }}"
    AccessToken: "MDASDASJDIASDJASDAFGFRGER"
    DeviceID: "DEVICE2"
    HomeserverURL: "{{ matrix_homeserver_container_url }}"
    Sync: false
    AutoJoinRooms: false
    DisplayName: "Go-NEB!"
    AcceptVerificationFromUsers: ["^@admin:{{ matrix_domain }}"]

# Optional, for use with the github_cmd, github_webhooks or jira services
matrix_bot_go_neb_realms:
  - ID: "github_realm"
    Type: "github"
    Config: {} # No need for client ID or Secret as Go-NEB isn't generating OAuth URLs

# Optional. The list of *authenticated* sessions which Go-NEB is aware of.
matrix_bot_go_neb_sessions:
  - SessionID: "your_github_session"
    RealmID: "github_realm"
    UserID: "@YOUR_USER_ID:{{ matrix_domain }}" # This needs to be the username of the person that's allowed to use the !github commands
    Config:
      # Populate these fields by generating a "Personal Access Token" on github.com
      AccessToken: "YOUR_GITHUB_ACCESS_TOKEN"
      Scopes: "admin:org_hook,admin:repo_hook,repo,user"

# The list of services which Go-NEB is aware of.
# Delete or modify this list as appropriate.
# See the docs for /configureService for the full list of options:
# https://matrix-org.github.io/go-neb/pkg/github.com/matrix-org/go-neb/api/index.html#ConfigureServiceRequest
# You need at least 1 service.
matrix_bot_go_neb_services:
  - ID: "echo_service"
    Type: "echo"
    UserID: "@goneb:{{ matrix_domain }}"
    Config: {}

# Can be obtained from https://developers.giphy.com/dashboard/
  - ID: "giphy_service"
    Type: "giphy"
    UserID: "@goneb:{{ matrix_domain }}" # requires a Syncing client
    Config:
      api_key: "qwg4672vsuyfsfe"
      use_downsized: false

# This service has been dead for over a year :/
  - ID: "guggy_service"
    Type: "guggy"
    UserID: "@goneb:{{ matrix_domain }}" # requires a Syncing client
    Config:
      api_key: "2356saaqfhgfe"

# API Key via https://developers.google.com/custom-search/v1/introduction
# CX via http://www.google.com/cse/manage/all
# https://stackoverflow.com/questions/6562125/getting-a-cx-id-for-custom-search-google-api-python
# 'Search the entire web' and 'Image search' enabled for best results
  - ID: "google_service"
    Type: "google"
    UserID: "@goneb:{{ matrix_domain }}" # requires a Syncing client
    Config:
      api_key: "AIzaSyA4FD39m9"
      cx: "AIASDFWSRRtrtr"

# Get a key via https://api.imgur.com/oauth2/addclient
# Select "oauth2 without callback url"
  - ID: "imgur_service"
    Type: "imgur"
    UserID: "@imgur:{{ matrix_domain }}" # requires a Syncing client
    Config:
      client_id: "AIzaSyA4FD39m9"
      client_secret: "somesecret"

  - ID: "wikipedia_service"
    Type: "wikipedia"
    UserID: "@goneb:{{ matrix_domain }}" # requires a Syncing client
    Config:

  - ID: "rss_service"
    Type: "rssbot"
    UserID: "@another_goneb:{{ matrix_domain }}"
    Config:
      feeds:
        "http://lorem-rss.herokuapp.com/feed?unit=second&interval=60":
          rooms: ["!qmElAGdFYCHoCJuaNt:{{ matrix_domain }}"]
          must_include:
            author:
              - author1
            description:
              - lorem
              - ipsum
          must_not_include:
            title:
              - Lorem
              - Ipsum

  - ID: "github_cmd_service"
    Type: "github"
    UserID: "@goneb:{{ matrix_domain }}" # requires a Syncing client
    Config:
      RealmID: "github_realm"

    # Make sure your BASE_URL can be accessed by Github!
  - ID: "github_webhook_service"
    Type: "github-webhook"
    UserID: "@another_goneb:{{ matrix_domain }}"
    Config:
      RealmID: "github_realm"
      ClientUserID: "@YOUR_USER_ID:{{ matrix_domain }}" # needs to be an authenticated user so Go-NEB can create webhooks. Check the UserID field in the github_realm in matrix_bot_go_neb_sessions.
      Rooms:
        "!someroom:id":
          Repos:
            "matrix-org/synapse":
              Events: ["push", "issues"]
            "matrix-org/dendron":
              Events: ["pull_request"]
        "!anotherroom:id":
          Repos:
            "matrix-org/synapse":
              Events: ["push", "issues"]
            "matrix-org/dendron":
              Events: ["pull_request"]

  - ID: "slackapi_service"
    Type: "slackapi"
    UserID: "@slackapi:{{ matrix_domain }}"
    Config:
      Hooks:
        "hook1":
          RoomID: "!someroom:id"
          MessageType: "m.text" # default is m.text

  - ID: "alertmanager_service"
    Type: "alertmanager"
    UserID: "@alertmanager:{{ matrix_domain }}"
    Config:
      # This is for information purposes only. It should point to Go-NEB path as follows:
      # `/services/hooks/<base64 encoded service ID>`
      # Where in this case "service ID" is "alertmanager_service"
      # Make sure your BASE_URL can be accessed by the Alertmanager instance!
      webhook_url: "http://localhost/services/hooks/YWxlcnRtYW5hZ2VyX3NlcnZpY2U"
      # Each room will get the notification with the alert rendered with the given template
      rooms:
        "!someroomid:domain.tld":
          text_template: "{{range .Alerts -}} [{{ .Status }}] {{index .Labels \"alertname\" }}: {{index .Annotations \"description\"}} {{ end -}}"
          html_template: "{{range .Alerts -}}  {{ $severity := index .Labels \"severity\" }}    {{ if eq .Status \"firing\" }}      {{ if eq $severity \"critical\"}}        <font color='red'><b>[FIRING - CRITICAL]</b></font>      {{ else if eq $severity \"warning\"}}        <font color='orange'><b>[FIRING - WARNING]</b></font>      {{ else }}        <b>[FIRING - {{ $severity }}]</b>      {{ end }}    {{ else }}      <font color='green'><b>[RESOLVED]</b></font>    {{ end }}  {{ index .Labels \"alertname\"}} : {{ index .Annotations \"description\"}}   <a href=\"{{ .GeneratorURL }}\">source</a><br/>{{end -}}"
          msg_type: "m.text"  # Must be either `m.text` or `m.notice`
```


## Installing

Don't forget to add `goneb.<your-domain>` to DNS as described in [Configuring DNS](configuring-dns.md) before running the playbook.

After configuring the playbook, run the [installation](installing.md) command again:

```
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start
```


## Usage

To use the bot, invite it to any existing Matrix room (`/invite @whatever_you_chose:DOMAIN` where `YOUR_DOMAIN` is your base domain, not the `matrix.` domain, make sure you have permission from the room owner if that's not you).

Basic usage is like this: `!echo hi` or `!imgur puppies` or `!giphy matrix`

If you enabled the github_cmd service you can get the supported commands via `!github help`

You can also refer to the upstream [Documentation](https://github.com/matrix-org/go-neb).
