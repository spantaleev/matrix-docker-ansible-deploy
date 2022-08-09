# Setting up ntfy (optional)

The playbook can install and configure the [ntfy](https://ntfy.sh/) push notifications server for you.

Using the [UnifiedPush](https://unifiedpush.org) standard, ntfy enables self-hosted (Google-free) push notifications from Matrix (and other) servers to UnifiedPush-compatible matrix compatible client apps running on Android and other devices.

This role is intended to support UnifiedPush notifications for use with the Matrix and Matrix-related services that this playbook installs. This role is not intended to support all of ntfy's other features.

**Note**: In contrast to push notifications using Google's FCM or Apple's APNs, the use of UnifiedPush allows each end-user to choose the push notification server that they prefer.  As a consequence, deploying this ntfy server does not by itself ensure any particular user or device or client app will use it.


## Adjusting the playbook configuration

Add the following configuration to your `inventory/host_vars/matrix.DOMAIN/vars.yml` file (adapt to your needs):

```yaml
# Enabling it is the only required setting
matrix_ntfy_enabled: true

# Some other options
matrix_server_fqn_ntfy: "ntfy.{{ matrix_domain }}"
matrix_ntfy_configuration_extension_yaml: |
  log_level: DEBUG
```

For a more complete list of variables that you could override, see `roles/matrix-ntfy/defaults/main.yml`.

For a complete list of ntfy config options that you could put in `matrix_ntfy_configuration_extension_yaml`, see the [ntfy config documentation](https://ntfy.sh/docs/config/#config-options).


## Installing

Don't forget to add `ntfy.<your-domain>` to DNS as described in [Configuring DNS](configuring-dns.md) before running the playbook.

After configuring the playbook, run the [installation](installing.md) command again:

```
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start
```


## Usage

To make use of your ntfy installation, on Android for example, you need two things:

* the `ntfy` app
* a UnifiedPush-compatible matrix app

You need to install the `ntfy` app on each device on which you want to receive push notifications through your ntfy server. The `ntfy` app will provide UnifiedPush notifications to any number of UnifiedPush-compatible messaging apps installed on the same device.

### Setting up the `ntfy` Android app

1. Install the [ntfy Android app](https://ntfy.sh/docs/subscribe/phone/) from F-droid or Google Play.
2. In its Settings -> `General: Default server`, enter your ntfy server URL, such as `https://ntfy.DOMAIN`.
3. In its Settings -> `Advanced: Connection protocol`, choose `WebSockets`.

That is all you need to do in the ntfy app. It has many other features, but for our purposes you can ignore them. In particular you do not need to follow any instructions about subscribing to a notification topic as UnifiedPush will do that automatically.

### Setting up a UnifiedPush-compatible matrix app

Install any UnifiedPush-enabled matrix app on that same device. The matrix app will learn from the `ntfy` app that you have configured UnifiedPush on this device, and then it will tell your matrix server to use it.

Steps needed for specific matrix apps:

* FluffyChat-android:
  - Should auto-detect and use it. No manual settings.

* SchildiChat-android:
  1. enable `Settings` -> `Notifications` -> `UnifiedPush: Force custom push gateway`.
  2. choose `Settings` -> `Notifications` -> `UnifiedPush: Re-register push distributor`. *(For info, a more complex alternative to achieve the same is: delete the relevant unifiedpush registration in `ntfy` app, force-close SchildiChat, re-open it.)*
  3. verify `Settings` -> `Notifications` -> `UnifiedPush: Notification targets` as described below in the "Troubleshooting" section.

* Element-android v1.4.26+:
  - [not yet documented; should auto-detect and use it?]

If the matrix app asks, "Choose a distributor: FCM Fallback or ntfy", then choose "ntfy".

If the matrix app doesn't seem to pick it up, try restarting it and try the Troubleshooting section below.


## Troubleshooting

First check that the matrix client app you are using supports UnifiedPush. There may well be different variants of the app.

Set the ntfy server's log level to 'DEBUG', as shown in the example settings above, and watch the server's logs with `sudo journalctl -fu matrix-ntfy`.

To check if UnifiedPush is correctly configured on the client device, look at "Settings -> Notifications -> Notification Targets" in Element-Android or SchildiChat, or "Settings -> Notifications -> Devices" in FluffyChat. There should be one entry for each matrix client app that has enabled push notifications, and when that client is using UnifiedPush you should see a URL that begins with your ntfy server's URL.

In the "Notification Targets" screen in Element-Android or SchildiChat, two relevant URLs are shown, "push\_key" and "Url", and both should begin with your ntfy server's URL. If "push\_key" shows your server but "Url" shows an external server such as `up.schildi.chat` then push notifications will still work but are being routed through that external server before they reach your ntfy server. To rectify that, in SchildiChat (at least around version 1.4.20.sc55) you must enable the `Force custom push gateway` setting as described in the "Usage" section above.

If it is not working, useful tools are "Settings -> Notifications -> Re-register push distributor" and "Settings -> Notifications -> Troubleshoot Notifications" in SchildiChat (possibly also Element-Android). In particular the "Endpoint/FCM" step of that troubleshooter should display your ntfy server's URL that it has discovered from the ntfy client app.

The simple [UnifiedPush troubleshooting](https://unifiedpush.org/users/troubleshooting/) app [UP-Example](https://f-droid.org/en/packages/org.unifiedpush.example/) can be used to manually test UnifiedPush registration and operation on an Android device.
