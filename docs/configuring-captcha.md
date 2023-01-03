(Adapted from the [upstream project](https://github.com/matrix-org/synapse/blob/develop/docs/CAPTCHA_SETUP.md))

# Overview
Captcha can be enabled for this home server. This file explains how to do that.
The captcha mechanism used is Google's [ReCaptcha](https://www.google.com/recaptcha/). This requires API keys from Google. If your homeserver is Dendrite then [hCapcha](https://www.hcaptcha.com) can be used instead.

## ReCaptcha

### Getting keys

Requires a site/secret key pair from:

<http://www.google.com/recaptcha/admin>

Must be a reCAPTCHA **v2** key using the "I'm not a robot" Checkbox option

### Setting ReCaptcha keys

Once registered as above, set the following values:

```yaml
# for Synapse
matrix_synapse_enable_registration_captcha: true
matrix_synapse_recaptcha_public_key: 'YOUR_SITE_KEY'
matrix_synapse_recaptcha_private_key: 'YOUR_SECRET_KEY'

# for Dendrite
matrix_dendrite_client_api_enable_registration_captcha: true
matrix_dendrite_client_api_recaptcha_public_key: 'YOUR_SITE_KEY'
matrix_dendrite_client_api_recaptcha_private_key: 'YOUR_SECRET_KEY'
```

## hCaptcha

### Getting keys

Requires a site/secret key pair from:

<https://dashboard.hcaptcha.com/sites/new>

### Setting hCaptcha keys

```yaml
matrix_dendrite_client_api_enable_registration_captcha: true
matrix_dendrite_client_api_recaptcha_public_key: 'YOUR_SITE_KEY'
matrix_dendrite_client_api_recaptcha_private_key: 'YOUR_SECRET_KEY'

matrix_dendrite_client_api_recaptcha_siteverify_api: 'https://hcaptcha.com/siteverify'
matrix_dendrite_client_api_recaptcha_api_js_url: 'https://js.hcaptcha.com/1/api.js'
matrix_dendrite_client_api_recaptcha_form_field: 'h-captcha-response'
matrix_dendrite_client_api_recaptcha_sitekey_class: 'h-captcha'
```
