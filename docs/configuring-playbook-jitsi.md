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

# Run `bash inventory/scripts/jitsi-generate-passwords.sh` to generate these passwords,
# or define your own strong passwords manually.
matrix_jitsi_jicofo_component_secret: ""
matrix_jitsi_jicofo_auth_password: ""
matrix_jitsi_jvb_auth_password: ""
matrix_jitsi_jibri_recorder_password: ""
matrix_jitsi_jibri_xmpp_password: ""
```


## (Optional) configure internal Jitsi authentication and guests mode

By default the Jitsi Meet instance does not require any kind of login and is open to use for anyone without registration.

If you're fine with such an open Jitsi instance, please skip to [Apply changes](#apply-changes).

If you would like to control who is allowed to open meetings on your new Jitsi instance, then please follow this step to enable Jitsi's `internal` authentication and guests mode. With this optional configuration, all meeting rooms have to be opened by at least one registered user, after that guests are free to join. If a registered host is not present yet, guests are put on hold into a waiting room.

Add these two lines to your `inventory/host_vars/matrix.DOMAIN/vars.yml` configuration:

```yaml
matrix_jitsi_enable_auth: true
matrix_jitsi_enable_guests: true
```

## Apply changes

Then re-run the playbook: `ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start`

## Required if configuring Jitsi with its internal authentication: register new users

Until this gets integrated into the playbook, we need to register new users / meeting hosts for Jitsi manually.
Please SSH into your matrix host machine and execute the following command targeting the `matrix-jitsi-prosody` container:

```bash
docker exec matrix-jitsi-prosody prosodyctl --config /config/prosody.cfg.lua register <USERNAME> matrix-jitsi-web <PASSWORD>
```

Run this command for each user you would like to create, replacing `<USERNAME>` and `<PASSWORD>` accordingly. After you've finished, please exit the host.

**If you get an error** like this: "Error: Account creation/modification not supported.", it's likely that you had previously installed Jitsi without auth/guest support. In such a case, you should look into [Rebuilding your Jitsi installation](#rebuilding-your-jitsi-installation).


## Usage

You can use the self-hosted Jitsi server through Riot, through an Integration Manager like [Dimension](docs/configuring-playbook-dimension.md) or directly at `https://jitsi.DOMAIN`.

To use it via riot-web (the one configured by the playbook at `https://riot.DOMAIN`), just start a voice or a video call in a room containing more than 2 members and that would create a Jitsi widget which utilizes your self-hosted Jitsi server.


## Troubleshooting

### Rebuilding your Jitsi installation

**If you ever run into any trouble** or **if you change configuration (`matrix_jitsi_*` variables) too much**, we urge you to rebuild your Jitsi setup.

We normally don't require such manual intervention for other services, but Jitsi services generate a lot of configuration files on their own.

These files are not all managed by Ansible (at least not yet), so you may sometimes need to delete them all and start fresh.

To rebuild your Jitsi configuration:

- SSH into the server and do this:
  - stop all Jitsi services (`systemctl stop matrix-jitsi-*`).
  - remove all Jitsi configuration & data (`rm -rf /matrix/jitsi`)
- ask Ansible to set up Jitsi anew and restart services (`ansible-playbook -i inventory/hosts setup.yml --tags=setup-jitsi,start`)
