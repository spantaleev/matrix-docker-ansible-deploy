# Setting up matrix-sms-bridge (optional)

The playbook can install and configure
[matrix-sms-bridge](https://github.com/benkuly/matrix-sms-bridge) for you.

See the project page to learn what it does and why it might be useful to you.

First you need to ensure, that the bridge has unix read and write rights to your modem. On debian based distributions there is nothing to do. On others distributions you either add a group `dialout` to your host and assign it to your modem or you give the matrix user or group access to your modem.

To enable the bridge just use the following
playbook configuration:


```yaml
matrix_sms_bridge_enabled: true
matrix_sms_bridge_gammu_modem: "/dev/serial/by-id/myDeviceId"
# generate a secret passwort e.g. with pwgen -s 64 1
matrix_sms_bridge_database_password: ""
# (optional) a room id to a default room
matrix_sms_bridge_default_room: "" 
# (optional) gammu reset frequencies (see https://wammu.eu/docs/manual/smsd/config.html#option-ResetFrequency)
matrix_sms_bridge_gammu_reset_frequency: 3600
matrix_sms_bridge_gammu_hard_reset_frequency: 0
# (optional) group with unix read and write rights to modem
matrix_sms_bridge_modem_group: 'dialout'
```


## Usage

Read the [user guide](https://github.com/benkuly/matrix-sms-bridge/blob/master/README.md#user-guide) to see how this bridge works.
