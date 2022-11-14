# TURN server

The playbook installs a [Coturn](https://github.com/coturn/coturn) TURN server by default, so that clients can make audio/video calls even from [NAT](https://en.wikipedia.org/wiki/Network_address_translation)-ed networks.

By default, the Synapse chat server is configured, so that it points to the Coturn TURN server installed by the playbook.


## Disabling Coturn

If, for some reason, you'd like to prevent the playbook from installing Coturn, you can use the following configuration:

```yaml
matrix_coturn_enabled: false
```

In that case, Synapse would not point to any Coturn servers and audio/video call functionality may fail.


## Using your own external Coturn server

If you'd like to use another TURN server (be it Coturn or some other one), you can configure the playbook like this:

```yaml
# Disable integrated Coturn server
matrix_coturn_enabled: false

# Point Synapse to your other Coturn server
matrix_synapse_turn_uris:
- turns:HOSTNAME_OR_IP?transport=udp
- turns:HOSTNAME_OR_IP?transport=tcp
- turn:HOSTNAME_OR_IP?transport=udp
- turn:HOSTNAME_OR_IP?transport=tcp
```

If you have or want to enable [Jitsi](configuring-playbook-jitsi.md), you might want to enable the TURN server there too.
If you do not do it, Jitsi will fall back to an upstream service.

```yaml
matrix_jitsi_web_stun_servers:
- stun:HOSTNAME_OR_IP:PORT
```
You can put multiple host/port combinations if you like.
