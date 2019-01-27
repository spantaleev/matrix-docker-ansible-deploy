# Adjusting email-sending settings (optional)

By default, this playbook sets up an [Exim](https://www.exim.org/) email server through which all Matrix services send emails.

The email server would attempt to deliver emails directly to their final destination.
This may or may not work, depending on your domain configuration (SPF settings, etc.)

By default, emails are sent from `matrix@<your-domain-name>` (as specified by the `matrix_mailer_sender_address` playbook variable).


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


## Troubleshooting

If you're having trouble with email not being delivered, it may be useful to inspect the mailer logs: `journalctl -f -u matrix-mailer`.
