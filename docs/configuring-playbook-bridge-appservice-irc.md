# Setting up Appservice IRC (optional)

The playbook can install and configure [matrix-appservice-irc](https://github.com/TeDomum/matrix-appservice-irc) for you.

See the project's [documentation](https://github.com/TeDomum/matrix-appservice-irc/blob/master/HOWTO.md) to learn what it does and why it might be useful to you.

You'll need to use the following playbook configuration:

```yaml
matrix_appservice_irc_enabled: true
matrix_appservice_irc_configuration_extension_yaml: |
  # Your custom YAML configuration for Appservice IRC servers goes here.
  # This configuration extends the default starting configuration (`matrix_appservice_irc_configuration_yaml`).
  #
  # You can override individual variables from the default configuration, or introduce new ones.
  #
  # If you need something more special, you can take full control by
  # completely redefining `matrix_appservice_irc_configuration_yaml`.
  # 
  # For a full example configuration with comments, see `roles/matrix-synapse/defaults/main.yml`
  #
  # A simple example configuration extension follows:
  #
  ircService:
    databaseUri: "nedb:///data" # does not typically need modification
    passwordEncryptionKeyPath: "/data/passkey.pem" # does not typically need modification
    matrixHandler:
      eventCacheSize: 4096
    servers:
      irc.example.com:
        name: "ExampleNet"
        port: 6697
        ssl: true
        sasl: false
        allowExpiredCerts: false
        sendConnectionMessages: true
        botConfig:
          enabled: true
          nick: "MatrixBot"
          joinChannelsIfNoUsers: true
        privateMessages:
          enabled: true
          federate: true
        dynamicChannels:
          enabled: true
          createAlias: true
          published: true
          joinRule: public
          groupId: +myircnetwork:localhost
          federate: true
          aliasTemplate: "#irc_$CHANNEL"
        membershipLists:
          enabled: false
          floodDelayMs: 10000
          global:
            ircToMatrix:
              initial: false
              incremental: false
            matrixToIrc:
              initial: false
              incremental: false
        matrixClients:
          userTemplate: "@irc_$NICK"
          displayName: "$NICK (IRC)"
          joinAttempts: -1
        ircClients:
          nickTemplate: "$DISPLAY[m]"
          allowNickChanges: true
          maxClients: 30
          idleTimeout: 10800
          reconnectIntervalMs: 5000
          concurrentReconnectLimit: 50
          lineLimit: 3
```

You then need to start a chat with `@irc_bot:YOUR_DOMAIN` (where `YOUR_DOMAIN` is your base domain, not the `matrix.` domain).
