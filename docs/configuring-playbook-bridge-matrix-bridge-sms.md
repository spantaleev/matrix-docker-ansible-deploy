# Setting up matrix-sms-bridge (optional)

The playbook can install and configure [matrix-sms-bridge](https://github.com/benkuly/matrix-sms-bridge) for you.

See the project page to learn what it does and why it might be useful to you.

**The bridge uses [android-sms-gateway-server](https://github.com/RebekkaMa/android-sms-gateway-server). You need to configure it first.**

To enable the bridge just use the following
playbook configuration:


```yaml
matrix_sms_bridge_enabled: true

# (optional but recommended) a room id to a default room
matrix_sms_bridge_default_room: "" 

# (optional but recommended) configure your server location
matrix_sms_bridge_default_region: DE
matrix_sms_bridge_default_timezone: Europe/Berlin

# Settings to connect to android-sms-gateway-server
matrix_sms_bridge_provider_android_baseurl: https://192.168.24.24:9090
matrix_sms_bridge_provider_android_username: admin
matrix_sms_bridge_provider_android_password: supeSecretPassword

# (optional) if your android-sms-gateway-server uses a self signed vertificate, the bridge needs a "truststore". This can be the certificate itself.
matrix_sms_bridge_provider_android_truststore_local_path: android-sms-gateway-server.p12
matrix_sms_bridge_provider_android_truststore_password: 123

```


## Usage

Read the [user guide](https://github.com/benkuly/matrix-sms-bridge/blob/master/README.md#user-guide) to see how this bridge works.
