# Adjusting TURN server configuration (optional, advanced)

The playbook installs a [Coturn](https://github.com/coturn/coturn) TURN server by default, so that clients can make audio/video calls even from [NAT](https://en.wikipedia.org/wiki/Network_address_translation)-ed networks.

By default, the Synapse chat server is configured, so that it points to the Coturn TURN server installed by the playbook.

## Disabling Coturn

If, for some reason, you'd like to prevent the playbook from installing Coturn, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

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

## Changing the authentication mechanism

The playbook uses the [`auth-secret` authentication method](https://github.com/coturn/coturn/blob/873cabd6a2e5edd7e9cc5662cac3ffe47fe87a8e/README.turnserver#L186-L199) by default, but you may switch to the [`lt-cred-mech` method](https://github.com/coturn/coturn/blob/873cabd6a2e5edd7e9cc5662cac3ffe47fe87a8e/README.turnserver#L178) which [some report](https://github.com/spantaleev/matrix-docker-ansible-deploy/issues/3191) to be working better.

To do so, add this override to your configuration:

```yaml
matrix_coturn_authentication_method: lt-cred-mech
```

Regardless of the selected authentication method, the playbook generates secrets automatically and passes them to the homeserver and Coturn.

If you're using [Jitsi](./configuring-playbook-jitsi.md), note that switching to `lt-cred-mech` will remove the integration between Jitsi and your own Coturn server, because Jitsi only seems to support the `auth-secret` authentication method.

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

If you have or want to enable [Jitsi](configuring-playbook-jitsi.md), you might want to enable the TURN server there too. If you do not do it, Jitsi will fall back to an upstream service.

```yaml
jitsi_web_stun_servers:
- stun:HOSTNAME_OR_IP:PORT
```
You can put multiple host/port combinations if you like.

## Further variables and configuration options
To see all the available configuration options, check roles/custom/matrix-coturn/defaults/main.yml
