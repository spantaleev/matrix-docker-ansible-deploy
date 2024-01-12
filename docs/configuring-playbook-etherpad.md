# Setting up Etherpad (optional)

[Etherpad](https://etherpad.org) is an open source collaborative text editor that can be embedded in a Matrix chat room using the [Dimension integrations manager](https://dimension.t2bot.io) or used as standalone web app.

When enabled together with the Jitsi audio/video conferencing system (see [our docs on Jitsi](configuring-playbook-jitsi.md)), it will be made available as an option during the conferences.


## Decide on a domain and path

By default, Etherpad is configured to use its own dedicated domain (`etherpad.DOMAIN`) and requires you to [adjust your DNS records](#adjusting-dns-records).

You can override the domain and path like this:

```yaml
# Switch to the domain used for Matrix services (`matrix.DOMAIN`),
# so we won't need to add additional DNS records for Etherpad.
etherpad_hostname: "{{ matrix_server_fqn_matrix }}"

# Expose under the /etherpad subpath
etherpad_path_prefix: /etherpad
```


## Adjusting DNS records

Once you've decided on the domain and path, **you may need to adjust your DNS** records to point the Etherpad domain to the Matrix server.

If you've decided to reuse the `matrix.` domain, you won't need to do any extra DNS configuration.


## Installing

[Etherpad](https://etherpad.org) installation is disabled by default. You can enable it in your configuration file (`inventory/host_vars/matrix.<your-domain>/vars.yml`):

```yaml
etherpad_enabled: true

# Uncomment below to enable the admin web UI
# etherpad_admin_username: admin
# etherpad_admin_password: some-password
```

Then, [run the installation process](installing.md) again (e.g. `just install-all`).


## Usage

The Etherpad UI should be available at `https://etherpad.<your-domain>`, while the admin UI (if enabled) should then be available at `https://etherpad.<your-domain>/admin`.

If you've [decided on another hostname or path-prefix](#decide-on-a-domain-and-path) (e.g. `https://matrix.DOMAIN/etherpad`), adjust these URLs accordingly before usage.


### Managing / Deleting old pads

If you want to manage and remove old unused pads from Etherpad, you will first need to able Admin access as described above.

Then from the plugin manager page (`https://etherpad.<your-domain>/admin/plugins`, install the `adminpads2` plugin. Once installed, you should have a "Manage pads" section in the Admin web-UI.


### How to use Etherpad widgets without an Integration Manager (like Dimension)

This is how it works in Element, it might work quite similar with other clients:

To integrate a standalone etherpad in a room, create your pad by visiting `https://etherpad.DOMAIN`. When the pad opens, copy the URL and send a command like this to the room: `/addwidget URL`. You will then find your integrated Etherpad within the right sidebar in the `Widgets` section.


### Set Dimension default to the self-hosted Etherpad (optional)

If you decided to install [Dimension integration manager](configuring-playbook-dimension.md) alongside Etherpad, the Dimension administrator users can configure the default URL template.
The Dimension configuration menu can be accessed with the sprocket icon as you begin to add a widget to a room in Element. There you will find the Etherpad Widget Configuration action beneath the _Widgets_ tab.


#### Removing the integrated Etherpad chat

If you wish to disable the Etherpad chat button, you can do it by appending `?showChat=false` to the end of the pad URL, or the template.

Example: `https://etherpad.<your-domain>/p/$roomId_$padName?showChat=false`


## Known issues

If your Etherpad widget fails to load, this might be due to Dimension generating a Pad name so long, the Etherpad app rejects it.
`$roomId_$padName` can end up being longer than 50 characters. You can avoid having this problem by altering the template so it only contains the three word random identifier `$padName`.
