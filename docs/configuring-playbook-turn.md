# TURN server

The playbook installs a [Coturn](https://github.com/coturn/coturn) TURN server by default, so that clients can make audio/video calls even from [NAT](https://en.wikipedia.org/wiki/Network_address_translation)-ed networks.

By default, the Synapse chat server is configured, so that it points to the Coturn TURN server installed by the playbook.


## Disabling Coturn

If, for some reason, you'd like to prevent the playbook from installing Coturn, you can use the following configuration:

```yaml
matrix_coturn_enabled: false
```

In that case, Synapse would not point to any Coturn servers and audio/video call functionality may fail.

## Manually defining your public IP

In the `hosts` file we explicitly ask for your server's external IP address when defining `ansible_host`, because the same value is used for configuring Coturn.

If you'd rather use a local IP for `ansible_host`, make sure to set up `matrix_coturn_turn_external_ip_address` replacing `YOUR_PUBLIC_IP` with the pubic IP used by the server.

```yaml
matrix_coturn_turn_external_ip_address: "YOUR_PUBLIC_IP"
```

If you'd like to rely on external IP address auto-detection (not recommended unless you need it), set `matrix_coturn_turn_external_ip_address` to an empty value. The playbook will automatically contact an [EchoIP](https://github.com/mpolden/echoip)-compatible service (`https://ifconfig.co/json` by default) to determine your server's IP address. This API endpoint is configurable via the `matrix_coturn_turn_external_ip_address_auto_detection_echoip_service_url` variable.

If your server has multiple external IP addresses, the Coturn role offers a different variable for specifying them:

```yaml
# Note: matrix_coturn_turn_external_ip_addresses is different than matrix_coturn_turn_external_ip_address
matrix_coturn_turn_external_ip_addresses: ['1.2.3.4', '4.5.6.7']
```

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
jitsi_web_stun_servers:
- stun:HOSTNAME_OR_IP:PORT
```
You can put multiple host/port combinations if you like.

## Further variables and configuration options
To see all the available configuration options, check roles/custom/matrix-coturn/defaults/main.yml
