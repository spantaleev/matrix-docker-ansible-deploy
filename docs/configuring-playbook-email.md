<!--
SPDX-FileCopyrightText: 2018 - 2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2019 Eduardo Beltrame
SPDX-FileCopyrightText: 2020 - 2025 MDAD project contributors
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Adjusting email-sending settings (optional)

By default, this playbook sets up an [Exim](https://www.exim.org/) relay SMTP mailer service (powered by [exim-relay](https://github.com/devture/exim-relay) and the [ansible-role-exim-relay](https://github.com/mother-of-all-self-hosting/ansible-role-exim-relay) Ansible role), through which all Matrix services send emails.

**With the default setting, exim-relay attempts to deliver emails directly with the address `matrix@matrix.example.com`**, as specified by the `exim_relay_sender_address` playbook variable. See below if you want to configure the playbook to relay email through another SMTP server.

The [Ansible role for exim-relay](https://github.com/mother-of-all-self-hosting/ansible-role-exim-relay) is developed and maintained by [the MASH (mother-of-all-self-hosting) project](https://github.com/mother-of-all-self-hosting). For details about configuring exim-relay, you can check them via:
- 🌐 [the role's documentation at the MASH project](https://github.com/mother-of-all-self-hosting/ansible-role-exim-relay/blob/main/docs/configuring-exim-relay.md) online
- 📁 `roles/galaxy/exim_relay/docs/configuring-exim-relay.md` locally, if you have [fetched the Ansible roles](installing.md#update-ansible-roles)

## Firewall settings

No matter whether you send email directly (the default) or you relay email through another host, you'll probably need to allow outgoing traffic for TCP ports 25/587 (depending on configuration).

Docker automatically opens these ports in the server's firewall, so you likely don't need to do anything. If you use another firewall in front of the server, you may need to adjust it.

## Adjusting the playbook configuration

### Enable DKIM authentication to improve deliverability (optional)

By default, exim-relay attempts to deliver emails directly. This may or may not work, depending on your domain configuration.

To improve email deliverability, you can configure authentication methods such as DKIM (DomainKeys Identified Mail), SPF, and DMARC for your domain. Without setting any of these authentication methods, your outgoing email is most likely to be quarantined as spam at recipient's mail servers.

For details about configuring DKIM, refer [this section](https://github.com/mother-of-all-self-hosting/ansible-role-exim-relay/blob/main/docs/configuring-exim-relay.md#enable-dkim-support-optional) on the role's documentation.

💡 If you cannot enable DKIM, SPF, or DMARC on your domain for some reason, we recommend relaying email through another SMTP server.

### Relaying email through another SMTP server (optional)

**On some cloud providers such as Google Cloud, [port 25 is always blocked](https://cloud.google.com/compute/docs/tutorials/sending-mail/), so sending email directly from your server is not possible.** In this case, you will need to relay email through another SMTP server.

For details about configuration, refer [this section](https://github.com/mother-of-all-self-hosting/ansible-role-exim-relay/blob/main/docs/configuring-exim-relay.md#relaying-email-through-another-smtp-server) on the role's document.

### Disable mail service (optional)

For a low-power server you might probably want to disable exim-relay. To do so, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
exim_relay_enabled: false
```

Note that disabling exim-relay will stop email-notifications and other similar functions from working.

See [this entry on the FAQ](faq.md#how-do-i-optimize-this-setup-for-a-low-power-server) for other possible optimizations for a low-power server.

## Installing

After configuring the playbook, run it with [playbook tags](playbook-tags.md) as below:

<!-- NOTE: let this conservative command run (instead of install-all) to make it clear that failure of the command means something is clearly broken. -->
```sh
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start
```

The shortcut commands with the [`just` program](just.md) are also available: `just install-all` or `just setup-all`

`just install-all` is useful for maintaining your setup quickly ([2x-5x faster](../CHANGELOG.md#2x-5x-performance-improvements-in-playbook-runtime) than `just setup-all`) when its components remain unchanged. If you adjust your `vars.yml` to remove other components, you'd need to run `just setup-all`, or these components will still remain installed. Note these shortcuts run the `ensure-matrix-users-created` tag too.

## Troubleshooting

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-exim-relay/blob/main/docs/configuring-exim-relay.md#troubleshooting) on the role's documentation for details.
