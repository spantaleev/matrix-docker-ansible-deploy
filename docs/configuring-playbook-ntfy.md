<!--
SPDX-FileCopyrightText: 2022 - 2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2022 - 2024 Nikita Chernyi
SPDX-FileCopyrightText: 2022 Julian Foad
SPDX-FileCopyrightText: 2022 MDAD project contributors
SPDX-FileCopyrightText: 2023 Felix Stupp
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Setting up the ntfy push notifications server (optional)

The playbook can install and configure the [ntfy](https://ntfy.sh/) (pronounced "notify") push notifications server for you.

ntfy lets you send push notifications to your phone or desktop via scripts from any computer, using simple HTTP PUT or POST requests. It makes it possible to send/receive notifications, without relying on servers owned and controlled by third parties.

With the [UnifiedPush](https://unifiedpush.org) standard, ntfy also enables self-hosted push notifications from Matrix (and other) servers to UnifiedPush-compatible Matrix client apps running on Android devices.

See the project's [documentation](https://docs.ntfy.sh/) to learn what ntfy does and why it might be useful to you.

The [Ansible role for ntfy](https://github.com/mother-of-all-self-hosting/ansible-role-ntfy) is developed and maintained by [the MASH (mother-of-all-self-hosting) project](https://github.com/mother-of-all-self-hosting). For details about configuring ntfy, you can check them via:
- 🌐 [the role's documentation at the MASH project](https://github.com/mother-of-all-self-hosting/ansible-role-ntfy/blob/main/docs/configuring-ntfy.md) online
- 📁 `roles/galaxy/ntfy/docs/configuring-ntfy.md` locally, if you have [fetched the Ansible roles](installing.md#update-ansible-roles)

**Note**: this playbook focuses on setting up a ntfy server for getting it send push notifications with UnifiedPush to Matrix-related services that this playbook installs, while the installed server will be available for other non-Matrix apps like [Tusky](https://tusky.app/) and [DAVx⁵](https://www.davx5.com/) as well. This playbook does not intend to support all of ntfy's features. If you want to use them as well, refer the role's documentation for details to configure them by yourself.

### Improve push notification's privacy with ntfy

By default, push notifications received on Matrix apps on Android/iOS act merely as "wake-up calls" for the application, which contain only event IDs, and do not transmit actual message payload such as text message data.

While your messages remain private even without ntfy, it makes it possible to improve privacy and sovereignty of your Matrix installation, offering greater control over your data, by avoiding routing these "application wake-up calls" through Google or Apple servers and having them pass through the self-hosted ntfy instance on your Matrix server.

### How ntfy works with UnifiedPush

⚠️ [UnifiedPush does not work on iOS.](https://unifiedpush.org/users/faq/#will-unifiedpush-ever-work-on-ios)

ntfy implements UnifiedPush, the standard which makes it possible to send and receive push notifications without using Google's Firebase Cloud Messaging (FCM) service.

Working as a **Push Server**, a ntfy server can forward messages via [the ntfy Android app](https://docs.ntfy.sh/subscribe/phone/) as a **Distributor** to a UnifiedPush-compatible Matrix client such as Element Android and FluffyChat Android (see [here](https://unifiedpush.org/users/distributors/#definitions) for the definition of the Push Server and the Distributor).

Note that UnifiedPush-compatible applications must be able to communicate with the ntfy Android app which works as the Distributor on the same device, in order to receive push notifications from the Push Server.

As the ntfy Android app functions as the Distributor, you do not have to install something else on your device, besides a UnifiedPush-compatible Matrix client.

## Adjusting DNS records

By default, this playbook installs ntfy on the `ntfy.` subdomain (`ntfy.example.com`) and requires you to create a CNAME record for `ntfy`, which targets `matrix.example.com`.

When setting, replace `example.com` with your own.

## Adjusting the playbook configuration

To enable a ntfy server, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

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

As the most of the necessary settings for the role have been taken care of by the playbook, you can enable the ntfy server on your Matrix server with this minimum configuration.

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

The ntfy server can be accessed via its web app where you can subscribe to and push to "topics" from the browser. The web app may be helpful to troubleshoot notification issues or to use ntfy for other purposes than getting ntfy send UnifiedPush notifications to your Matrix-related services.

**Note**: subscribing to a topic is not necessary for using the nfty server as the Push Server for UnifiedPush.

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

To receive push notifications with UnifiedPush from the ntfy server, you need to **install [the ntfy Android app](https://docs.ntfy.sh/subscribe/phone/)** which works as the Distributor, **log in to the account on the ntfy app** if you have enabled the access control, and then **configure a UnifiedPush-compatible Matrix client**. After setting up the ntfy Android app, the Matrix client listens to it, and push notifications are "distributed" from it.

For details about installing and configuring the ntfy Android app, take a look at [this section](https://github.com/mother-of-all-self-hosting/ansible-role-ntfy/blob/main/docs/configuring-ntfy.md#install-the-ntfy-androidios-app) on the role's documentation.

⚠️ Though the ntfy app is available for iOS ([App Store](https://apps.apple.com/us/app/ntfy/id1625396347); the app's source code can be retrieved from [here](https://github.com/binwiederhier/ntfy-ios)), **any Matrix clients for iOS currently do not support ntfy** due to [technical limitations of the iOS platform](https://github.com/binwiederhier/ntfy-ios/blob/main/docs/TECHNICAL_LIMITATIONS.md). If you develop your own Matrix client app for iOS, you may need to use the [Sygnal](configuring-playbook-sygnal.md) push gateway service to deliver push notifications to it.

### Setting up a UnifiedPush-compatible Matrix client

Having configured the ntfy Android app, you can configure a UnifiedPush-compatible Matrix client on the same device.

Steps needed for specific Matrix clients:

* FluffyChat-Android: this should auto-detect and use the app. No manual settings required.

* SchildiChat-Android:
  1. enable `Settings` -> `Notifications` -> `UnifiedPush: Force custom push gateway`.
  2. choose `Settings` -> `Notifications` -> `UnifiedPush: Re-register push distributor`. *(For info, a more complex alternative to achieve the same is: delete the relevant unifiedpush registration in the ntfy Android app, force-close SchildiChat, re-open it.)*
  3. verify `Settings` -> `Notifications` -> `UnifiedPush: Notification targets` as described below in the "Troubleshooting" section.

* Element-Android v1.4.26+:
  1. choose `Settings` -> `Notifications` -> `Notification method` -> `ntfy`
  2. verify `Settings` -> `Troubleshoot` -> `Troubleshoot notification settings`

If the Matrix client asks, "Choose a distributor: FCM Fallback or ntfy", then choose "ntfy".

If the Matrix client doesn't seem to pick it up, try restarting it and try the Troubleshooting section below.

## Troubleshooting

The simple [UnifiedPush troubleshooting](https://unifiedpush.org/users/troubleshooting/) app [UP-Example](https://f-droid.org/en/packages/org.unifiedpush.example/) can be used to manually test UnifiedPush registration and operation on an Android device.

### Check the Matrix client

Make sure that the Matrix client you are using supports UnifiedPush. There may well be different variants of the app.

To check if UnifiedPush is correctly configured on the client device, look at "Settings -> Notifications -> Notification Targets" in Element Android or SchildiChat Android, or "Settings -> Notifications -> Devices" in FluffyChat. There should be one entry for each Matrix client that has enabled push notifications, and when that client is using UnifiedPush you should see a URL that begins with your ntfy server's URL.

In the "Notification Targets" screen in Element Android or SchildiChat Android, two relevant URLs are shown, "push\_key" and "Url", and both should begin with your ntfy server's URL. If "push\_key" shows your server but "Url" shows an external server such as `up.schildi.chat` then push notifications will still work but are being routed through that external server before they reach your ntfy server. To rectify that, in SchildiChat (at least around version 1.4.20.sc55) you must enable the `Force custom push gateway` setting as described in the "Usage" section above.

If it is not working, useful tools are "Settings -> Notifications -> Re-register push distributor" and "Settings -> Notifications -> Troubleshoot Notifications" in SchildiChat Android (possibly also Element Android). In particular the "Endpoint/FCM" step of that troubleshooter should display your ntfy server's URL that it has discovered from the ntfy client app.

### Check the service's logs

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-ntfy/blob/main/docs/configuring-ntfy.md#check-the-services-logs) on the role's documentation for details.
