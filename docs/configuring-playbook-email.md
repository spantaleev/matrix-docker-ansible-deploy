# Adjusting email-sending settings (optional)

By default, this playbook sets up an [Exim](https://www.exim.org/) email server through which all Matrix services send emails.

The email server would attempt to deliver emails directly to their final destination.
This may or may not work, depending on your domain configuration (SPF settings, etc.)

By default, emails are sent from `matrix@<your-domain-name>` (as specified by the `matrix_mailer_sender_address` playbook variable).

**Note**: If you are using a Google Cloud instance, [port 25 is always blocked](https://cloud.google.com/compute/docs/tutorials/sending-mail/), so you need to relay email through another SMTP server as described below.   


## Firewall settings

No matter whether you send email directly (the default) or you relay email through another host (see how below), you'll probably need to allow outgoing traffic for TCP ports 25/587 (depending on configuration).


## Relaying email through another SMTP server

If you'd like to relay email through another SMTP server, feel free to redefine a few playbook variables.
Example:

```yaml
matrix_mailer_sender_address: "another.sender@example.com"
matrix_mailer_relay_use: true
matrix_mailer_relay_host_name: "mail.example.com"
matrix_mailer_relay_host_port: 587
matrix_mailer_relay_auth: true
matrix_mailer_relay_auth_username: "another.sender@example.com"
matrix_mailer_relay_auth_password: "some-password"
```

**Note**: only the secure submission protocol (using `STARTTLS`, usually on port `587`) is supported. **SMTPS** (encrypted SMTP, usually on port `465`) **is not supported**.


### Configuations for sending emails using Sendgrid
An easy and free SMTP service to set up is [Sendgrid](https://sendgrid.com/), the free tier allows for up to 100 emails per day to be sent. In the settings below you can provide any email for `matrix_mailer_sender_address`.

The only other thing you need to change is the `matrix_mailer_relay_auth_password`, which you can generate at https://app.sendgrid.com/settings/api_keys. The API key password looks something like `SG.955oW1mLSfwds7i9Yd6IA5Q.q8GTaB8q9kGDzasegdG6u95fQ-6zkdwrPP8bOeuI`.

Note that the `matrix_mailer_relay_auth_username` is literally the string `apikey`, it's always the same for Sendgrid.

```yaml
matrix_mailer_sender_address: "arbitrary@email.com"
matrix_mailer_relay_use: true
matrix_mailer_relay_host_name: "smtp.sendgrid.net"
matrix_mailer_relay_host_port: 587
matrix_mailer_relay_auth: true
matrix_mailer_relay_auth_username: "apikey"
matrix_mailer_relay_auth_password: "<your api key password>" 
```

## Troubleshooting

If you're having trouble with email not being delivered, it may be useful to inspect the mailer logs: `journalctl -f -u matrix-mailer`.
