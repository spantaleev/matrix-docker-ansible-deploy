# Setting up Appservice IRC (optional)

**Note**: bridging to [IRC](https://en.wikipedia.org/wiki/Internet_Relay_Chat) can also happen via the [Heisenbridge](configuring-playbook-bridge-heisenbridge.md) bridge supported by the playbook.

The playbook can install and configure the [matrix-appservice-irc](https://github.com/matrix-org/matrix-appservice-irc) bridge for you.

See the project's [documentation](https://github.com/matrix-org/matrix-appservice-irc/blob/master/HOWTO.md) to learn what it does and why it might be useful to you.

You'll need to use the following playbook configuration:

```yaml
matrix_appservice_irc_enabled: true

matrix_appservice_irc_ircService_servers:
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
