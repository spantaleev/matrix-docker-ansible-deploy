# Setting up Mautrix Whatsapp

The playbook can install and configure [mautrix-whatsapp](https://github.com/tulir/mautrix-whatsapp) for you.

See the project's [documentation](https://github.com/tulir/mautrix-whatsapp/wiki) to learn what it does and why it might be useful to you.

Use the following playbook configuration:
```
matrix_mautrix_whatsapp_enabled: true
```

You then need to start a chat with `@whatsappbot:{{ hostname_identity }}`
