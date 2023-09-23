# Setting up the OIDC authentication module (optional, advanced)

The playbook can configure the OpenID Connect authentication for you. Currently only Microsoft Entra ID (formerly Azure Active Directory) is supported.

If you decide that you'd like to let this playbook configure it for you, you need some configuration like this:

```yaml
matrix_synapse_oidc_provider_microsoft_enabled: true
matrix_synapse_oidc_provider_microsoft_tenant_id: 
matrix_synapse_oidc_provider_microsoft_client_id: 
matrix_synapse_oidc_provider_microsoft_client_secret: 
matrix_synapse_oidc_provider_microsoft_icon: mxc://
```

## Where to get the values

You need to register an application in the Entra ID (AAD). Values you need:

1. Tenant ID
2. Application (client) ID
3. Client secret

In Authentication section, create Web Redirect URI: **https://matrix.example.com/_synapse/client/oidc/callback**

Easiest way to get an icon for provider is to upload it to any public (unencrypted) room and copy the mcx:// address from message source.
