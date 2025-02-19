<!--
SPDX-FileCopyrightText: 2018 - 2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2019 Eduardo Beltrame
SPDX-FileCopyrightText: 2020 - 2025 MDAD project contributors
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Adjusting email-sending settings (optional)

By default, this playbook sets up an [Exim](https://www.exim.org/) email server through which all Matrix services send emails.

The email server would attempt to deliver emails directly to their final destination. This may or may not work, depending on your domain configuration (SPF settings, etc.)

By default, emails are sent from `matrix@matrix.example.com`, as specified by the `exim_relay_sender_address` playbook variable.

> [!WARNING]
> On some cloud providers (Google Cloud, etc.), [port 25 is always blocked](https://cloud.google.com/compute/docs/tutorials/sending-mail/), so sending email directly from your server is not possible. You will need to [relay email through another SMTP server](#relaying-email-through-another-smtp-server).

💡 To improve deliverability, we recommend [relaying email through another SMTP server](#relaying-email-through-another-smtp-server) anyway.

The Ansible role for exim-relay is developed and maintained by [the MASH (mother-of-all-self-hosting) project](https://github.com/mother-of-all-self-hosting/ansible-role-exim-relay). For details about configuring exim-relay, you can check them via:
- 🌐 [the role's documentation at the MASH project](https://github.com/mother-of-all-self-hosting/ansible-role-exim-relay/blob/main/docs/configuring-exim-relay.md) online
- 📁 `roles/galaxy/exim_relay/docs/configuring-exim-relay.md` locally, if you have [fetched the Ansible roles](installing.md#update-ansible-roles)

## Firewall settings

No matter whether you send email directly (the default) or you relay email through another host (see how below), you'll probably need to allow outgoing traffic for TCP ports 25/587 (depending on configuration).

## Adjusting the playbook configuration

### Relaying email through another SMTP server

If you'd like to relay email through another SMTP server, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file (adapt to your needs):

```yaml
exim_relay_sender_address: "another.sender@example.com"
exim_relay_relay_use: true
exim_relay_relay_host_name: "mail.example.com"
exim_relay_relay_host_port: 587
exim_relay_relay_auth: true
exim_relay_relay_auth_username: "another.sender@example.com"
exim_relay_relay_auth_password: "PASSWORD_FOR_THE_RELAY_HERE"
```

**Note**: only the secure submission protocol (using `STARTTLS`, usually on port `587`) is supported. **SMTPS** (encrypted SMTP, usually on port `465`) **is not supported**.

### Sending emails using Sendgrid

An easy and free SMTP service to set up is [Sendgrid](https://sendgrid.com/). Its free tier allows for up to 100 emails per day to be sent.

To set it up, add the following configuration to your `vars.yml` file (adapt to your needs):

```yaml
exim_relay_sender_address: "example@example.org"
exim_relay_relay_use: true
exim_relay_relay_host_name: "smtp.sendgrid.net"
exim_relay_relay_host_port: 587
exim_relay_relay_auth: true

# This needs to be literally the string "apikey". It is always the same for Sendgrid.
exim_relay_relay_auth_username: "apikey"

# You can generate the API key password at this URL: https://app.sendgrid.com/settings/api_keys
# The password looks something like `SG.955oW1mLSfwds7i9Yd6IA5Q.q8GTaB8q9kGDzasegdG6u95fQ-6zkdwrPP8bOeuI`.
exim_relay_relay_auth_password: "YOUR_API_KEY_PASSWORD_HERE"
```

## Troubleshooting

If you're having trouble with email not being delivered, it may be useful to inspect the mailer logs.

To do so, log in to the server with SSH and run `journalctl -f -u matrix-exim-relay`.
