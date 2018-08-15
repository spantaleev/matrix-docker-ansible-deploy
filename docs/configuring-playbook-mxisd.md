# Adjusting mxisd Identity Server configuration (optional)

By default, this playbook configures an [mxisd](https://github.com/kamax-io/mxisd) Identity Server for you.

This server is private by default, potentially at the expense of user discoverability.


## Matrix.org lookup forwarding

To ensure maximum discovery, you can make your identity server also forward lookups to the central matrix.org Identity server (at the cost of potentially leaking all your contacts information).

Enabling this is discouraged and you'd better [learn more](https://github.com/kamax-io/mxisd/blob/master/docs/features/identity.md#lookups) before proceeding.

Enabling matrix.org forwarding can happen with the following configuration:

```yaml
matrix_mxisd_matrixorg_forwarding_enabled: true
```


## Additional features

What this playbook configures for your is some bare minimum Identity Server functionality, so that you won't need to rely on external 3rd party services.

Still, mxisd can do much more.
You can refer to the [mxisd website](https://github.com/kamax-io/mxisd) for more details.

You can override the `matrix_mxisd_template_config` variable and use your own custom configuration template.


## Troubleshooting

If email address validation emails sent by mxisd are not reaching you, you should look into [Adjusting email-sending settings](configuring-playbook-email.md).