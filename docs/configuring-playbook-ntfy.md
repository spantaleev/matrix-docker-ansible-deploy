# Setting up the ntfy push notifications server (optional)

The playbook can install and configure the [ntfy](https://ntfy.sh/) push notifications server for you.

Using the [UnifiedPush](https://unifiedpush.org) standard, ntfy enables self-hosted (Google-free) push notifications from Matrix (and other) servers to UnifiedPush-compatible Matrix compatible client apps running on Android and other devices.

This role is intended to support UnifiedPush notifications for use with the Matrix and Matrix-related services that this playbook installs. This role is not intended to support all of ntfy's other features.

**Note**: In contrast to push notifications using Google's FCM or Apple's APNs, the use of UnifiedPush allows each end-user to choose the push notification server that they prefer.  As a consequence, deploying this ntfy server does not by itself ensure any particular user or device or client app will use it.

## Adjusting the playbook configuration

To enable ntfy, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
# Enabling it is the only required setting
ntfy_enabled: true

# Uncomment to enable the ntfy web app (disabled by default)
# ntfy_web_root: app  # defaults to "disable"

# Uncomment and change to inject additional configuration options.
# ntfy_configuration_extension_yaml: |
#   log_level: DEBUG
```

For a more complete list of variables that you could override, see the [`defaults/main.yml` file](https://github.com/mother-of-all-self-hosting/ansible-role-ntfy/blob/main/defaults/main.yml) of the ntfy Ansible role.

For a complete list of ntfy config options that you could put in `ntfy_configuration_extension_yaml`, see the [ntfy config documentation](https://ntfy.sh/docs/config/#config-options).

### Adjusting the ntfy URL

By default, this playbook installs ntfy on the `ntfy.` subdomain (`ntfy.example.com`) and requires you to [adjust your DNS records](#adjusting-dns-records).

By tweaking the `ntfy_hostname` variable, you can easily make the service available at a **different hostname** than the default one.

Example additional configuration for your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
# Change the default hostname
ntfy_hostname: push.example.com
```

## Adjusting DNS records

Once you've decided on the domain, **you may need to adjust your DNS** records to point the ntfy domain to the Matrix server.

By default, you will need to create a CNAME record for `ntfy`. See [Configuring DNS](configuring-dns.md) for details about DNS changes.

## Installing

After configuring the playbook and potentially [adjusting your DNS records](#adjusting-dns-records), run the playbook with [playbook tags](playbook-tags.md) as below:

<!-- NOTE: let this conservative command run (instead of install-all) to make it clear that failure of the command means something is clearly broken. -->
```sh
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start
```

The shortcut commands with the [`just` program](just.md) are also available: `just install-all` or `just setup-all`

`just install-all` is useful for maintaining your setup quickly ([2x-5x faster](../CHANGELOG.md#2x-5x-performance-improvements-in-playbook-runtime) than `just setup-all`) when its components remain unchanged. If you adjust your `vars.yml` to remove other components, you'd need to run `just setup-all`, or these components will still remain installed. Note these shortcuts run the `ensure-matrix-users-created` tag too.

## Usage

To make use of your ntfy installation, on Android for example, you need two things:

* the `ntfy` app
* a UnifiedPush-compatible Matrix app

You need to install the `ntfy` app on each device on which you want to receive push notifications through your ntfy server. The `ntfy` app will provide UnifiedPush notifications to any number of UnifiedPush-compatible messaging apps installed on the same device.

### Setting up the `ntfy` Android app

1. Install the [ntfy Android app](https://ntfy.sh/docs/subscribe/phone/) from F-droid or Google Play.
2. In its Settings -> `General: Default server`, enter your ntfy server URL, such as `https://ntfy.example.com`.
3. In its Settings -> `Advanced: Connection protocol`, choose `WebSockets`.

That is all you need to do in the ntfy app. It has many other features, but for our purposes you can ignore them. In particular you do not need to follow any instructions about subscribing to a notification topic as UnifiedPush will do that automatically.

### Setting up a UnifiedPush-compatible Matrix app

Install any UnifiedPush-enabled Matrix app on that same device. The Matrix app will learn from the `ntfy` app that you have configured UnifiedPush on this device, and then it will tell your Matrix server to use it.

Steps needed for specific Matrix apps:

* FluffyChat-android:
  - Should auto-detect and use it. No manual settings.

* SchildiChat-android:
  1. enable `Settings` -> `Notifications` -> `UnifiedPush: Force custom push gateway`.
  2. choose `Settings` -> `Notifications` -> `UnifiedPush: Re-register push distributor`. *(For info, a more complex alternative to achieve the same is: delete the relevant unifiedpush registration in `ntfy` app, force-close SchildiChat, re-open it.)*
  3. verify `Settings` -> `Notifications` -> `UnifiedPush: Notification targets` as described below in the "Troubleshooting" section.

* Element-android v1.4.26+:
  1. choose `Settings` -> `Notifications` -> `Notification method` -> `ntfy`
  2. verify `Settings` -> `Troubleshoot` -> `Troubleshoot notification settings`

If the Matrix app asks, "Choose a distributor: FCM Fallback or ntfy", then choose "ntfy".

If the Matrix app doesn't seem to pick it up, try restarting it and try the Troubleshooting section below.

### Web App

ntfy also has a web app to subscribe to and push to topics from the browser. This may be helpful to further troubleshoot UnifiedPush problems or to use ntfy for other purposes. The web app only runs in the browser locally (after downloading the JavaScript).

The web app is disabled in this playbook by default as the expectation is that most users won't use it. You can either use the [official hosted one](https://ntfy.sh/app) (it supports using other public reachable ntfy instances) or host it yourself by setting `ntfy_web_root: "app"` and re-running Ansible.

## Troubleshooting

First check that the Matrix client app you are using supports UnifiedPush. There may well be different variants of the app.

Set the ntfy server's log level to 'DEBUG', as shown in the example settings above, and watch the server's logs with `sudo journalctl -fu matrix-ntfy`.

To check if UnifiedPush is correctly configured on the client device, look at "Settings -> Notifications -> Notification Targets" in Element Android or SchildiChat Android, or "Settings -> Notifications -> Devices" in FluffyChat. There should be one entry for each Matrix client app that has enabled push notifications, and when that client is using UnifiedPush you should see a URL that begins with your ntfy server's URL.

In the "Notification Targets" screen in Element Android or SchildiChat Android, two relevant URLs are shown, "push\_key" and "Url", and both should begin with your ntfy server's URL. If "push\_key" shows your server but "Url" shows an external server such as `up.schildi.chat` then push notifications will still work but are being routed through that external server before they reach your ntfy server. To rectify that, in SchildiChat (at least around version 1.4.20.sc55) you must enable the `Force custom push gateway` setting as described in the "Usage" section above.

If it is not working, useful tools are "Settings -> Notifications -> Re-register push distributor" and "Settings -> Notifications -> Troubleshoot Notifications" in SchildiChat Android (possibly also Element Android). In particular the "Endpoint/FCM" step of that troubleshooter should display your ntfy server's URL that it has discovered from the ntfy client app.

The simple [UnifiedPush troubleshooting](https://unifiedpush.org/users/troubleshooting/) app [UP-Example](https://f-droid.org/en/packages/org.unifiedpush.example/) can be used to manually test UnifiedPush registration and operation on an Android device.
