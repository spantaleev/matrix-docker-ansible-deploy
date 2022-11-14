(Adapted from the [upstream project](https://github.com/matrix-org/synapse/blob/develop/docs/CAPTCHA_SETUP.md))

# Overview
Captcha can be enabled for this home server. This file explains how to do that.
The captcha mechanism used is Google's [ReCaptcha](https://www.google.com/recaptcha/). This requires API keys from Google.

## Getting keys

Requires a site/secret key pair from:

<http://www.google.com/recaptcha/admin>

Must be a reCAPTCHA **v2** key using the "I'm not a robot" Checkbox option

## Setting ReCaptcha Keys

Once registered as above, set the following values:

```yaml
matrix_synapse_enable_registration_captcha: true
matrix_synapse_recaptcha_public_key: 'YOUR_SITE_KEY'
matrix_synapse_recaptcha_private_key: 'YOUR_SECRET_KEY'
```
