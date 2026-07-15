<!--
SPDX-FileCopyrightText: 2020 - 2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2020 Justin Croonenberghs
SPDX-FileCopyrightText: 2022 MDAD project contributors
SPDX-FileCopyrightText: 2024 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

(Adapted from the [upstream project](https://github.com/element-hq/synapse/blob/develop/docs/CAPTCHA_SETUP.md))

# Overview

Captcha can be enabled for this home server. This file explains how to do that.

The captcha mechanism used is Google's [ReCaptcha](https://www.google.com/recaptcha/). This requires API keys from Google. If your homeserver is Dendrite then [hCapcha](https://www.hcaptcha.com) can be used instead.

If you are using [Matrix Authentication Service](configuring-playbook-matrix-authentication-service.md), captcha is configured there instead (it handles registration), and [Cloudflare Turnstile](https://www.cloudflare.com/application-services/products/turnstile/) is supported as well. See [Matrix Authentication Service](#matrix-authentication-service) below.

## ReCaptcha

### Getting keys

Requires a site/secret key pair from:

<http://www.google.com/recaptcha/admin>

Must be a reCAPTCHA **v2** key using the "I'm not a robot" Checkbox option

### Setting ReCaptcha keys

Once registered as above, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

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

## Matrix Authentication Service

When [Matrix Authentication Service](configuring-playbook-matrix-authentication-service.md) is enabled, registration and other account operations are handled by it, so captcha protection is configured there (the Synapse and Dendrite settings above do not apply).

Matrix Authentication Service supports [ReCaptcha v2](http://www.google.com/recaptcha/admin), [Cloudflare Turnstile](https://www.cloudflare.com/application-services/products/turnstile/) and [hCaptcha](https://dashboard.hcaptcha.com/sites/new). Obtain a site/secret key pair from your chosen service, then add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
# Valid values: recaptcha_v2, cloudflare_turnstile, hcaptcha
matrix_authentication_service_config_captcha_service: recaptcha_v2
matrix_authentication_service_config_captcha_site_key: 'YOUR_SITE_KEY'
matrix_authentication_service_config_captcha_secret_key: 'YOUR_SECRET_KEY'
```
