# Setting up Etherpad (optional)

[Etherpad](https://etherpad.org) is is an open source collaborative text editor that can be embedded in a Matrix chat room using the [Dimension integrations manager](https://dimension.t2bot.io) or used as standalone web app

When enabled together with the Jitsi audio/video conferencing system (see [our docs on Jitsi](configuring-playbook-jitsi.md)), it will be made available as an option during the conferences.

## Prerequisites

The `etherpad.<your-domain>` DNS record must be created. See [Configuring your DNS server](configuring-dns.md) on how to set up DNS record correctly.

You may enable and configure the **Dimension integrations manager** as described in [the playbook documentation](configuring-playbook-dimension.md) to integrate etherpad with Dimension.

## Installing

[Etherpad](https://etherpad.org) installation is disabled by default. You can enable it in your configuration file (`inventory/host_vars/matrix.<your-domain>/vars.yml`):

```yaml
matrix_etherpad_enabled: true
```

## Etherpad Admin access (optional)

Etherpad comes with a admin web-UI which is disabled by default. You can enable it by setting a username and password in your configuration file (`inventory/host_vars/matrix.<your-domain>/vars.yml`):

```yaml
matrix_etherpad_admin_username: admin
matrix_etherpad_admin_password: some-password
```

The admin web-UI should then be available on: `https://dimension.<your-domain>/etherpad/admin`

## Managing / Deleting old pads

If you want to manage and remove old unused pads from Etherpad, you will first need to able Admin access as described above.

Then from the plugin manager page (`https://etherpad.<your-domain>/admin/plugins` or `https://dimension.<your-domain>/etherpad/admin/plugins`), install the `adminpads2` plugin. Once installed, you should have a "Manage pads" section in the Admin web-UI.

## Set Dimension default to the self-hosted Etherpad (optional)

If you decided to install [Dimension integration manager](configuring-playbook-dimension.md) alongside with Etherpad,
the Dimension administrator users can configure the default URL template. The Dimension configuration menu can be accessed with the sprocket icon as you begin to add a widget to a room in Element. There you will find the Etherpad Widget Configuration action beneath the _Widgets_ tab. Replace `scalar.vector.im` with your own Dimension domain.

### Removing the integrated Etherpad chat

If you wish to disable the Etherpad chat button, you can do it by appending `?showChat=false` to the end of the pad URL, or the template.
Example: `https://dimension.<your-domain>/etherpad/p/$roomId_$padName?showChat=false`

## Known issues

If your Etherpad widget fails to load, this might be due to Dimension generating a Pad name so long, the Etherpad app rejects it.
`$roomId_$padName` can end up being longer than 50 characters. You can avoid having this problem by altering the template so it only contains the three word random identifier `$padName`.
