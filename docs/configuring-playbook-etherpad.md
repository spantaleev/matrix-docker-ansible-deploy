# Setting up Etherpad (optional)

[Etherpad](https://etherpad.org) is is an open source collaborative text editor that can be embedded in a Matrix chat room using the [Dimension integrations manager](https://dimension.t2bot.io) or used as standalone web app.

When enabled together with the Jitsi audio/video conferencing system (see [our docs on Jitsi](configuring-playbook-jitsi.md)), it will be made available as an option during the conferences.


## Prerequisites

Etherpad can be installed in 2 modes:

- (default) `standalone` mode (`matrix_etherpad_mode: standalone`) - Etherpad will be hosted on `etherpad.<your-domain>` (`matrix_server_fqn_etherpad`), so the DNS record for this domian must be created. See [Configuring your DNS server](configuring-dns.md) on how to set up the `etherpad` DNS record correctly

- `dimension` mode (`matrix_etherpad_mode: dimension`) - Etherpad will be hosted on `dimension.<your-domain>/etherpad` (`matrix_server_fqn_dimension`). This requires that you **first** configure the **Dimension integrations manager** as described in [the playbook documentation](configuring-playbook-dimension.md)

We recomend that you go with the default (`standalone`) mode, which makes Etherpad independent and allows it to be used with or without Dimension.


## Installing

[Etherpad](https://etherpad.org) installation is disabled by default. You can enable it in your configuration file (`inventory/host_vars/matrix.<your-domain>/vars.yml`):

```yaml
matrix_etherpad_enabled: true

# Uncomment below if you'd like to install Etherpad on the Dimension domain (not recommended)
# matrix_etherpad_mode: dimension

# Uncomment below to enable the admin web UI
# matrix_etherpad_admin_username: admin
# matrix_etherpad_admin_password: some-password
```

If enabled, the admin web-UI should then be available on `https://etherpad.<your-domain>/admin` (or `https://dimension.<your-domain>/etherpad/admin`, if `matrix_etherpad_mode: dimension`)


## Managing / Deleting old pads

If you want to manage and remove old unused pads from Etherpad, you will first need to able Admin access as described above.

Then from the plugin manager page (`https://etherpad.<your-domain>/admin/plugins` or `https://dimension.<your-domain>/etherpad/admin/plugins`), install the `adminpads2` plugin. Once installed, you should have a "Manage pads" section in the Admin web-UI.


## How to use Etherpad widgets without an Integration Manager (like Dimension)

This is how it works in Element, it might work quite similar with other clients:

To integrate a standalone etherpad in a room, create your pad by visiting `https://etherpad.DOMAIN`. When the pad opens, copy the URL and send a command like this to the room: `/addwidget URL`. You will then find your integrated Etherpad within the right sidebar in the `Widgets` section.


## Set Dimension default to the self-hosted Etherpad (optional)

If you decided to install [Dimension integration manager](configuring-playbook-dimension.md) alongside Etherpad, the Dimension administrator users can configure the default URL template.
The Dimension configuration menu can be accessed with the sprocket icon as you begin to add a widget to a room in Element. There you will find the Etherpad Widget Configuration action beneath the _Widgets_ tab.


### Removing the integrated Etherpad chat

If you wish to disable the Etherpad chat button, you can do it by appending `?showChat=false` to the end of the pad URL, or the template. Examples:
- `https://etherpad.<your-domain>/p/$roomId_$padName?showChat=false` (for the default - `matrix_etherpad_mode: standalone`)

- `https://dimension.<your-domain>/etherpad/p/$roomId_$padName?showChat=false` (for `matrix_etherpad_mode: dimension`)


### Known issues

If your Etherpad widget fails to load, this might be due to Dimension generating a Pad name so long, the Etherpad app rejects it.
`$roomId_$padName` can end up being longer than 50 characters. You can avoid having this problem by altering the template so it only contains the three word random identifier `$padName`.
