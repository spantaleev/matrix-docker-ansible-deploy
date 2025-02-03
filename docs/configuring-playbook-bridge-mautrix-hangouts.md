# Setting up Mautrix Hangouts bridging (optional, deprecated)

🪦 The playbook used to be able to install and configure [mautrix-hangouts](https://github.com/mautrix/hangouts), but no longer includes this component, because Google Hangouts has been discontinued since the 1st of November 2022.

You may wish to use the [Google Chat bridge](https://github.com/mautrix/googlechat) instead.

## Uninstalling the bridge manually

If you still have the Hangouts bridge installed on your Matrix server, the playbook can no longer help you uninstall it and you will need to do it manually. To uninstall manually, run these commands on the server:

```sh
systemctl disable --now matrix-mautrix-hangouts.service

rm -rf /matrix/mautrix-hangouts

/matrix/postgres/bin/cli-non-interactive 'DROP DATABASE matrix_mautrix_hangouts;'
```
