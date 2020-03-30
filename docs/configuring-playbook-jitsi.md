# Jitsi

The playbook can install the [Jitsi](https://jitsi.org/) video-conferencing platform and integrate it with [Riot](configuring-playbook-riot-web.md).

Jitsi installation is **not enabled by default**, because it's not a core component of Matrix services.

The setup done by the playbook is very similar to [docker-jitsi-meet](https://github.com/jitsi/docker-jitsi-meet).


## Prerequisites

Before installing Jitsi, make sure you've created the `jitsi.DOMAIN` DNS record. See [Configuring DNS](configuring-dns.md).

You may also need to open the following ports to your server:

- `10000/udp` - RTP media over UDP
- `4443/tcp` - RTP media fallback over TCP


## Installation

Add this to your `inventory/host_vars/matrix.DOMAIN/vars.yml` configuration:

```yaml
matrix_jitsi_enabled: true
```

Then re-run the playbook: `ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start`


## Usage

You can use the self-hosted Jitsi server through Riot, through an Integration Manager like [Dimension](docs/configuring-playbook-dimension.md) or directly at `https://jitsi.DOMAIN`.

To use it via riot-web (the one configured by the playbook at `https://riot.DOMAIN`), just start a voice or a video call in a room containing more than 2 members and that would create a Jitsi widget which utilizes your self-hosted Jitsi server.
