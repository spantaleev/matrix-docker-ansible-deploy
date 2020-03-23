# Jitsi

The playbook can install the [Jitsi](https://jitsi.org/) video-conferencing platform and integrate it with [Riot](configuring-playbook-riot-web.md).

Jitsi installation is **not enabled by default**, because it's not a core component of Matrix services.

The setup done by the playbook is very similar to [docker-jitsi-meet](https://github.com/jitsi/docker-jitsi-meet).


## Prerequisites

Before installing Jitsi, make sure you've created the `jitsi.DOMAIN` DNS record. See [Configuring DNS](configuring-dns.md).

You may also need to open the following ports to your server:

- `udp/10000` - RTP media over UDP
- `tcp/4443` - RTP media fallback over TCP


## Installation

Add this to your `inventory/host_vars/matrix.DOMAIN/vars.yml` configuration:

```yaml
matrix_jitsi_enabled: true

# We only need this temporarily - until Jitsi integration in riot-web is finalized.
# Remove this line in the future, to switch back to a stable riot-web version.
matrix_riot_web_docker_image: "vectorim/riot-web:develop"
```

Then re-run the playbook: `ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start`

.. and fully reload your riot-web page (at `riot.DOMAIN`).

Starting a video-conference in a room with more than 2 members should then create a Jitsi widget which utilizes your self-hosted Jitsi server.


**NOTE**: the playbook currently configures the Jitsi JVB component to use Google's STUN servers even in cases where our own [Coturn TURN server](configuring-playbook-turn.md) is enabled (it is by default). This is because JVB fails to discover its own external IP correctly when pointed to our own Coturn server. The failure happens because JVB reaches Coturn via the localnetwork and discovers a local Docker IP address instead of the public one, leading to a non-working service.
