# Setting up Etherpad (optional)

[Etherpad](https://etherpad.org) is is an open source collaborative text editor that can be embedded in a Matrix chat room using the [Dimension integrations manager](https://dimension.t2bot.io)

When enabled together with the Jitsi audio/video conferencing system (see [our docs on Jitsi](configuring-playbook-jitsi.md)), it will be made available as an option during the conferences.

## Prerequisites

For the self-hosted Etherpad instance to be available to your users, you must first enable and configure the **Dimension integrations manager** as described in [the playbook documentation](configuring-playbook-dimension.md)

## Installing

[Etherpad](https://etherpad.org) installation is disabled by default. You can enable it in your configuration file (`inventory/host_vars/matrix.<your-domain>/vars.yml`):

```yaml
matrix_etherpad_enabled: true
```

## Set Dimension default to the self-hosted Etherpad

The Dimension administrator users can configure the default URL template. The Dimension configuration menu can be accessed with the sprocket icon as you begin to add a widget to a room in Element. There you will find the Etherpad Widget Configuration action beneath the _Widgets_ tab. Replace `scalar.vector.im` with your own Dimension domain.

### Removing the integrated Etherpad chat

If you wish to disable the Etherpad chat button, you can do it by appending `?showChat=false` to the end of the pad URL, or the template.
Example: `https://dimension.<your-domain>/etherpad/p/$roomId_$padName?showChat=false`

## Known issues

If your Etherpad widget fails to load, this might be due to Dimension generating a Pad name so long, the Etherpad app rejects it.
`$roomId_$padName` can end up being longer than 50 characters. You can avoid having this problem by altering the template so it only contains the three word random identifier `$padName`.
