<!--
SPDX-FileCopyrightText: 2018 - 2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2019 Eduardo Beltrame
SPDX-FileCopyrightText: 2020 - 2025 MDAD project contributors
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Adjusting email-sending settings (optional)

By default, this playbook sets up an [Exim](https://www.exim.org/) email server through which all Matrix services send emails.

By default, emails are sent from `matrix@matrix.example.com`, as specified by the `exim_relay_sender_address` playbook variable.

The Ansible role for exim-relay is developed and maintained by [the MASH (mother-of-all-self-hosting) project](https://github.com/mother-of-all-self-hosting/ansible-role-exim-relay). For details about configuring exim-relay, you can check them via:
- 🌐 [the role's documentation at the MASH project](https://github.com/mother-of-all-self-hosting/ansible-role-exim-relay/blob/main/docs/configuring-exim-relay.md) online
- 📁 `roles/galaxy/exim_relay/docs/configuring-exim-relay.md` locally, if you have [fetched the Ansible roles](installing.md#update-ansible-roles)

## Firewall settings

No matter whether you send email directly (the default) or you relay email through another host (see how below), you'll probably need to allow outgoing traffic for TCP ports 25/587 (depending on configuration).

## Adjusting the playbook configuration

### Relaying email through another SMTP server (optional)

By default, exim-relay attempts to deliver emails directly. This may or may not work, depending on your domain configuration (SPF settings, etc.)

**On some cloud providers such as Google Cloud, [port 25 is always blocked](https://cloud.google.com/compute/docs/tutorials/sending-mail/), so sending email directly from your server is not possible.** In this case, you will need to relay email through another SMTP server.

For details about configuration, refer [this section](https://github.com/mother-of-all-self-hosting/ansible-role-exim-relay/blob/main/docs/configuring-exim-relay.md#relaying-email-through-another-smtp-server) on the role's document.

💡 To improve deliverability, we recommend relaying email through another SMTP server anyway.

## Troubleshooting

See [this section](https://github.com/mother-of-all-self-hosting/ansible-role-exim-relay/blob/main/docs/configuring-exim-relay.md#troubleshooting) on the role's documentation for details.
