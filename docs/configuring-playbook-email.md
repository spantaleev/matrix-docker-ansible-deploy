# Adjusting email-sending settings (optional)

By default, this playbook sets up a [postfix](http://www.postfix.org/) email server through which all Matrix services send emails.

The email server would attempt to deliver emails directly to their final destination.
This may or may not work, depending on your domain configuration (SPF settings, etc.)

By default, emails are sent from `matrix@<your-domain-name>` (as specified by the `matrix_mailer_sender_address` playbook variable).

Furthmore, if you'd like to relay email through another SMTP server, feel free to redefine a few more playbook variables.
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