<!--
SPDX-FileCopyrightText: 2022 - 2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2022 Julian Foad
SPDX-FileCopyrightText: 2022 MDAD project contributors
SPDX-FileCopyrightText: 2023 Felix Stupp
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Setting up the ntfy push notifications server (optional)

The playbook can install and configure the [ntfy](https://ntfy.sh/) push notifications server for you.

Using the [UnifiedPush](https://unifiedpush.org) standard, ntfy enables self-hosted (Google-free) push notifications from Matrix (and other) servers to UnifiedPush-compatible Matrix compatible client apps running on Android and other devices.

See the project's [documentation](https://docs.ntfy.sh/) to learn what it does and why it might be useful to you.

**Notes**:
- To make use of your ntfy installation, you need to install [the `ntfy` app](https://docs.ntfy.sh/subscribe/phone/) on your device and configuring your UnifiedPush-compatible Matrix client. **Otherwise your device will not receive push notifications from the ntfy server.** Refer [this section](#usage) for details.
- This playbook focuses on setting up a ntfy server for getting it send UnifiedPush notifications to Matrix-related services that this playbook installs, while the installed server will be available for other non-Matrix apps as well like [Tusky](https://tusky.app/) and [DAVx⁵](https://www.davx5.com/). This playbook does not intend to support all of ntfy's features.

The [Ansible role for ntfy](https://github.com/mother-of-all-self-hosting/ansible-role-ntfy) is developed and maintained by [the MASH (mother-of-all-self-hosting) project](https://github.com/mother-of-all-self-hosting). For details about configuring ntfy, you can check them via:
- 🌐 [the role's documentation at the MASH project](https://github.com/mother-of-all-self-hosting/ansible-role-ntfy/blob/main/docs/configuring-ntfy.md) online
- 📁 `roles/galaxy/ntfy/docs/configuring-ntfy.md` locally, if you have [fetched the Ansible roles](installing.md#update-ansible-roles)

## Adjusting DNS records

By default, this playbook installs ntfy on the `ntfy.` subdomain (`ntfy.example.com`) and requires you to create a CNAME record for `ntfy`, which targets `matrix.example.com`.

When setting, replace `example.com` with your own.

## Adjusting the playbook configuration

To enable ntfy, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
########################################################################
#                                                                      #
# ntfy                                                                 #
#                                                                      #
########################################################################

ntfy_enabled: true

########################################################################
#                                                                      #
# /ntfy                                                                #
#                                                                      #
########################################################################
```

As the most of the necessary settings for the role have been taken care of by the playbook, you can enable ntfy on your Matrix server with this minimum configuration.

See the role's documentation for details about configuring ntfy per your preference (such as [setting access control with authentication](https://github.com/mother-of-all-self-hosting/ansible-role-ntfy/blob/main/docs/configuring-ntfy.md#enable-access-control-with-authentication-optional)).

### Adjusting the ntfy URL (optional)

By tweaking the `ntfy_hostname` variable, you can easily make the service available at a **different hostname** than the default one.

Example additional configuration for your `vars.yml` file:

```yaml
# Change the default hostname
ntfy_hostname: push.example.com
```

After changing the domain, **you may need to adjust your DNS** records to point the ntfy domain to the Matrix server.

### Enable web app (optional)

ntfy also has a web app to subscribe to and push to topics from the browser. This may be helpful to troubleshoot notification issues or to use ntfy for other purposes than getting ntfy send UnifiedPush notifications to your Matrix-related services.

To enable the web app, add the following configuration to your `vars.yml` file:

```yaml
ntfy_web_root: app
```

See [the official documentation](https://docs.ntfy.sh/subscribe/web/) for details about how to use it.

## Installing

After configuring the playbook and potentially [adjusting your DNS records](#adjusting-dns-records), run the playbook with [playbook tags](playbook-tags.md) as below:

<!-- NOTE: let this conservative command run (instead of install-all) to make it clear that failure of the command means something is clearly broken. -->
```sh
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start
```

The shortcut commands with the [`just` program](just.md) are also available: `just install-all` or `just setup-all`

`just install-all` is useful for maintaining your setup quickly ([2x-5x faster](../CHANGELOG.md#2x-5x-performance-improvements-in-playbook-runtime) than `just setup-all`) when its components remain unchanged. If you adjust your `vars.yml` to remove other components, you'd need to run `just setup-all`, or these components will still remain installed. Note these shortcuts run the `ensure-matrix-users-created` tag too.

## Usage

Unlike push notifications using Google's FCM or Apple's APNs, each end-user can choose the UnifiedPush-enabled push notification server that one prefer. This means that deploying a ntfy server does not ensure any particular user, device or Matrix client will use it.

To receive push notifications from your ntfy server, you need to set up these two applications on your device:

* [the `ntfy` app](https://docs.ntfy.sh/subscribe/phone/)
* a UnifiedPush-compatible Matrix client

For details about installing and configuring the `ntfy` app, take a look at [this section](https://github.com/mother-of-all-self-hosting/ansible-role-ntfy/blob/main/docs/configuring-ntfy.md#setting-up-the-ntfy-android-app) on the role's documentation.

**Note**: on the app you do not need to subscribe to a notification topic by yourself, as UnifiedPush will do that automatically.

### Setting up a UnifiedPush-compatible Matrix client

After installing the `ntfy` app, install any UnifiedPush-enabled Matrix client on that same device. The Matrix client will learn from the `ntfy` app that you have configured UnifiedPush on this device, and then it will tell your Matrix server to use it.

Steps needed for specific Matrix clients:

* FluffyChat-android: this should auto-detect and use the app. No manual settings required.

* SchildiChat-android:
  1. enable `Settings` -> `Notifications` -> `UnifiedPush: Force custom push gateway`.
  2. choose `Settings` -> `Notifications` -> `UnifiedPush: Re-register push distributor`. *(For info, a more complex alternative to achieve the same is: delete the relevant unifiedpush registration in `ntfy` app, force-close SchildiChat, re-open it.)*
  3. verify `Settings` -> `Notifications` -> `UnifiedPush: Notification targets` as described below in the "Troubleshooting" section.

* Element-android v1.4.26+:
  1. choose `Settings` -> `Notifications` -> `Notification method` -> `ntfy`
  2. verify `Settings` -> `Troubleshoot` -> `Troubleshoot notification settings`

If the Matrix client asks, "Choose a distributor: FCM Fallback or ntfy", then choose "ntfy".

If the Matrix client doesn't seem to pick it up, try restarting it and try the Troubleshooting section below.

## Troubleshooting

### Check the Matrix client

First, make sure that the Matrix client you are using supports UnifiedPush. There may well be different variants of the app.

To check if UnifiedPush is correctly configured on the client device, look at "Settings -> Notifications -> Notification Targets" in Element Android or SchildiChat Android, or "Settings -> Notifications -> Devices" in FluffyChat. There should be one entry for each Matrix client that has enabled push notifications, and when that client is using UnifiedPush you should see a URL that begins with your ntfy server's URL.

In the "Notification Targets" screen in Element Android or SchildiChat Android, two relevant URLs are shown, "push\_key" and "Url", and both should begin with your ntfy server's URL. If "push\_key" shows your server but "Url" shows an external server such as `up.schildi.chat` then push notifications will still work but are being routed through that external server before they reach your ntfy server. To rectify that, in SchildiChat (at least around version 1.4.20.sc55) you must enable the `Force custom push gateway` setting as described in the "Usage" section above.

If it is not working, useful tools are "Settings -> Notifications -> Re-register push distributor" and "Settings -> Notifications -> Troubleshoot Notifications" in SchildiChat Android (possibly also Element Android). In particular the "Endpoint/FCM" step of that troubleshooter should display your ntfy server's URL that it has discovered from the ntfy client app.

The simple [UnifiedPush troubleshooting](https://unifiedpush.org/users/troubleshooting/) app [UP-Example](https://f-droid.org/en/packages/org.unifiedpush.example/) can be used to manually test UnifiedPush registration and operation on an Android device.

### Check the service's logs

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-etherpad/blob/main/docs/configuring-etherpad.md#check-the-service-s-logs) on the role's documentation for details.
