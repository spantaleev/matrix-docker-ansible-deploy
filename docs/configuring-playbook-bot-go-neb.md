<!--
SPDX-FileCopyrightText: 2021 - 2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2021 Yannick Goossens
SPDX-FileCopyrightText: 2022 Dennis Ciba
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara
SPDX-FileCopyrightText: 2025 MDAD project contributors

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Setting up Go-NEB (optional, unmaintained)

**Note**: [Go-NEB](https://github.com/matrix-org/go-neb) is now an archived (**unmaintained**) project. We recommend not bothering with installing it. While not a 1:1 replacement, the bridge's author suggests taking a look at [matrix-hookshot](https://github.com/matrix-org/matrix-hookshot) as a replacement, which can also be [installed using this playbook](configuring-playbook-bridge-hookshot.md). Consider using that bot instead of this one.

The playbook can install and configure [Go-NEB](https://github.com/matrix-org/go-neb) for you.

Go-NEB is a Matrix bot written in Go. It is the successor to Matrix-NEB, the original Matrix bot written in Python.

See the project's [documentation](https://github.com/matrix-org/go-neb/blob/master/README.md) to learn what it does and why it might be useful to you.

## Prerequisites

### Register the bot account

The playbook does not automatically create users for you. You **need to register the bot user manually** before setting up the bot.

Generate a strong password for the bot. You can create one with a command like `pwgen -s 64 1`.

You can use the playbook to [register a new user](registering-users.md):

```sh
ansible-playbook -i inventory/hosts setup.yml --extra-vars='username=bot.go-neb password=PASSWORD_FOR_THE_BOT admin=no' --tags=register-user
```

### Obtain an access token

The bot requires an access token to be able to connect to your homeserver. Refer to the documentation on [how to obtain an access token](obtaining-access-tokens.md).

> [!WARNING]
> Access tokens are sensitive information. Do not include them in any bug reports, messages, or logs. Do not share the access token with anyone.

## Adjusting DNS records

By default, this playbook installs Go-NEB on the `goneb.` subdomain (`goneb.example.com`) and requires you to create a CNAME record for `goneb`, which targets `matrix.example.com`.

When setting, replace `example.com` with your own.

## Adjusting the playbook configuration

To enable the bot, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file. Make sure to replace `ACCESS_TOKEN_FOR_GONEB_HERE` and `ACCESS_TOKEN_FOR_ANOTHER_GONEB_HERE` with the ones created [above](#obtain-an-access-token).

```yaml
matrix_bot_go_neb_enabled: true

# You need at least 1 client.
# Use the access token you obtained in the step above.
matrix_bot_go_neb_clients:
  - UserID: "@goneb:{{ matrix_domain }}"
    AccessToken: "ACCESS_TOKEN_FOR_GONEB_HERE"
    DeviceID: "DEVICE1"
    HomeserverURL: "{{ matrix_addons_homeserver_client_api_url }}"
    Sync: true
    AutoJoinRooms: true
    DisplayName: "Go-NEB!"
    AcceptVerificationFromUsers: [":{{ matrix_domain }}"]

  - UserID: "@another_goneb:{{ matrix_domain }}"
    AccessToken: "ACCESS_TOKEN_FOR_ANOTHER_GONEB_HERE"
    DeviceID: "DEVICE2"
    HomeserverURL: "{{ matrix_addons_homeserver_client_api_url }}"
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
    UserID: "@alice:{{ matrix_domain }}" # This needs to be the username of the person that's allowed to use the !github commands
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

# Obtain a key via https://api.imgur.com/oauth2/addclient
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
          rooms: ["!qporfwt:{{ matrix_domain }}"]
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
      ClientUserID: "@alice:{{ matrix_domain }}" # needs to be an authenticated user so Go-NEB can create webhooks. Check the UserID field in the github_realm in matrix_bot_go_neb_sessions.
      Rooms:
        "!qporfwt:example.com":
          Repos:
            "element-hq/synapse":
              Events: ["push", "issues"]
            "matrix-org/dendron":
              Events: ["pull_request"]
        "!aaabaa:example.com":
          Repos:
            "element-hq/synapse":
              Events: ["push", "issues"]
            "matrix-org/dendron":
              Events: ["pull_request"]

  - ID: "slackapi_service"
    Type: "slackapi"
    UserID: "@slackapi:{{ matrix_domain }}"
    Config:
      Hooks:
        "hook1":
          RoomID: "!qporfwt:example.com"
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
        "!qporfwt:example.com":
          text_template: "{% raw %}{{range .Alerts -}} [{{ .Status }}] {{index .Labels \"alertname\" }}: {{index .Annotations \"description\"}} {{ end -}}{% endraw %}"
          html_template: "{% raw %}{{range .Alerts -}}  {{ $severity := index .Labels \"severity\" }}    {{ if eq .Status \"firing\" }}      {{ if eq $severity \"critical\"}}        <font color='red'><b>[FIRING - CRITICAL]</b></font>      {{ else if eq $severity \"warning\"}}        <font color='orange'><b>[FIRING - WARNING]</b></font>      {{ else }}        <b>[FIRING - {{ $severity }}]</b>      {{ end }}    {{ else }}      <font color='green'><b>[RESOLVED]</b></font>    {{ end }}  {{ index .Labels \"alertname\"}} : {{ index .Annotations \"description\"}}   <a href=\"{{ .GeneratorURL }}\">source</a><br/>{{end -}}{% endraw %}"
          msg_type: "m.text"  # Must be either `m.text` or `m.notice`
```

### Adjusting the Go-NEB URL (optional)

By tweaking the `matrix_bot_go_neb_hostname` and `matrix_bot_go_neb_path_prefix` variables, you can easily make the service available at a **different hostname and/or path** than the default one.

Example additional configuration for your `vars.yml` file:

```yaml
# Switch to the domain used for Matrix services (`matrix.example.com`),
# so we won't need to add additional DNS records for Go-NEB.
matrix_bot_go_neb_hostname: "{{ matrix_server_fqn_matrix }}"

# Expose under the /go-neb subpath
matrix_bot_go_neb_path_prefix: /go-neb
```

After changing the domain, **you may need to adjust your DNS** records to point the Go-NEB domain to the Matrix server.

If you've decided to reuse the `matrix.` domain, you won't need to do any extra DNS configuration.

### Extending the configuration

There are some additional things you may wish to configure about the bot.

Take a look at:

- `roles/custom/matrix-bot-go-neb/defaults/main.yml` for some variables that you can customize via your `vars.yml` file
- `roles/custom/matrix-bot-go-neb/templates/config.yaml.j2` for the bot's default configuration. You can override settings (even those that don't have dedicated playbook variables) using the `matrix_bot_go_neb_configuration_extension_yaml` variable

## Installing

After configuring the playbook and potentially [adjusting your DNS records](#adjusting-dns-records), run the playbook with [playbook tags](playbook-tags.md) as below:

<!-- NOTE: let this conservative command run (instead of install-all) to make it clear that failure of the command means something is clearly broken. -->
```sh
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start
```

The shortcut commands with the [`just` program](just.md) are also available: `just install-all` or `just setup-all`

`just install-all` is useful for maintaining your setup quickly ([2x-5x faster](../CHANGELOG.md#2x-5x-performance-improvements-in-playbook-runtime) than `just setup-all`) when its components remain unchanged. If you adjust your `vars.yml` to remove other components, you'd need to run `just setup-all`, or these components will still remain installed. Note these shortcuts run the `ensure-matrix-users-created` tag too.

## Usage

To use the bot, invite it to any existing Matrix room (`/invite @bot.go-neb:example.com` where `example.com` is your base domain, not the `matrix.` domain). Make sure you are granted with the sufficient permission if you are not the room owner.

Basic usage is like this: `!echo hi` or `!imgur puppies` or `!giphy matrix`

If you enabled the github_cmd service, send `!github help` to the bot in the room to see the available commands.

You can also refer to the upstream [Documentation](https://github.com/matrix-org/go-neb).

## Troubleshooting

As with all other services, you can find the logs in [systemd-journald](https://www.freedesktop.org/software/systemd/man/systemd-journald.service.html) by logging in to the server with SSH and running `journalctl -fu matrix-bot-go-neb`.
