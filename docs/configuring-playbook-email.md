# Adjusting email-sending settings (optional)

By default, this playbook sets up an [Exim](https://www.exim.org/) email server through which all Matrix services send emails.

The email server would attempt to deliver emails directly to their final destination. This may or may not work, depending on your domain configuration (SPF settings, etc.)

By default, emails are sent from `matrix@matrix.example.com`, as specified by the `exim_relay_sender_address` playbook variable.

⚠️ **Warning**: On some cloud providers (Google Cloud, etc.), [port 25 is always blocked](https://cloud.google.com/compute/docs/tutorials/sending-mail/), so sending email directly from your server is not possible. You will need to [relay email through another SMTP server](#relaying-email-through-another-smtp-server).

💡 To improve deliverability, we recommend [relaying email through another SMTP server](#relaying-email-through-another-smtp-server) anyway.

## Firewall settings

No matter whether you send email directly (the default) or you relay email through another host (see how below), you'll probably need to allow outgoing traffic for TCP ports 25/587 (depending on configuration).

## Relaying email through another SMTP server

If you'd like to relay email through another SMTP server, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file (adapt to your needs):

```yaml
exim_relay_sender_address: "another.sender@example.com"
exim_relay_relay_use: true
exim_relay_relay_host_name: "mail.example.com"
exim_relay_relay_host_port: 587
exim_relay_relay_auth: true
exim_relay_relay_auth_username: "another.sender@example.com"
exim_relay_relay_auth_password: "some-password"
```

**Note**: only the secure submission protocol (using `STARTTLS`, usually on port `587`) is supported. **SMTPS** (encrypted SMTP, usually on port `465`) **is not supported**.

### Configuations for sending emails using Sendgrid

An easy and free SMTP service to set up is [Sendgrid](https://sendgrid.com/), the free tier allows for up to 100 emails per day to be sent. In the settings below you can provide any email for `exim_relay_sender_address`.

The only other thing you need to change is the `exim_relay_relay_auth_password`, which you can generate at https://app.sendgrid.com/settings/api_keys. The API key password looks something like `SG.955oW1mLSfwds7i9Yd6IA5Q.q8GTaB8q9kGDzasegdG6u95fQ-6zkdwrPP8bOeuI`.

Note that the `exim_relay_relay_auth_username` is literally the string `apikey`, it's always the same for Sendgrid.

```yaml
exim_relay_sender_address: "arbitrary@email.com"
exim_relay_relay_use: true
exim_relay_relay_host_name: "smtp.sendgrid.net"
exim_relay_relay_host_port: 587
exim_relay_relay_auth: true
exim_relay_relay_auth_username: "apikey"
exim_relay_relay_auth_password: "<your api key password>"
```

## Troubleshooting

If you're having trouble with email not being delivered, it may be useful to inspect the mailer logs: `journalctl -f -u matrix-exim-relay`.
