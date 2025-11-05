<!--
SPDX-FileCopyrightText: 2024 - 2025 Slavi Pantaleev
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Setting up Matrix Authentication Service (optional)

The playbook can install and configure [Matrix Authentication Service](https://github.com/element-hq/matrix-authentication-service/) (MAS) — a service operating alongside your existing [Synapse](./configuring-playbook-synapse.md) homeserver and providing [better authentication, session management and permissions in Matrix](https://matrix.org/blog/2023/09/better-auth/).

Matrix Authentication Service is an implementation of [MSC3861: Next-generation auth for Matrix, based on OAuth 2.0/OIDC](https://github.com/matrix-org/matrix-spec-proposals/pull/3861) and still work in progress, tracked at the [areweoidcyet.com](https://areweoidcyet.com/) website.

**Before going through with starting to use Matrix Authentication Service**, make sure to read:

- the [Reasons to use Matrix Authentication Service](#reasons-to-use-matrix-authentication-service) section below
- the [Expectations](#expectations) section below
- the [FAQ section on areweoidcyet.com](https://areweoidcyet.com/#faqs)

**If you've already been using Synapse** and have user accounts in its database, you can [migrate to Matrix Authentication Service](#migrating-an-existing-synapse-homeserver-to-matrix-authentication-service).

## Reasons to use Matrix Authentication Service

You may be wondering whether you should make the switch to Matrix Authentication Service (MAS) or keep using your existing authentication flow via Synapse (password-based or [OIDC](./configuring-playbook-synapse.md#synapse--openid-connect-for-single-sign-on)-enabled).

Matrix Authentication Service is **still an experimental service** and **not a default** for this Ansible playbook.

The [Expectations](#expectations) section contains a list of what works and what doesn't (**some services don't work with MAS yet**), as well as the **relative irreversability** of the migration process.

Below, we'll try to **highlight some potential reasons for switching** to Matrix Authentication Service:

- To use SSO in [Element X](https://element.io/blog/element-x-ignition/). The old [Synapse OIDC](./configuring-playbook-synapse.md#synapse--openid-connect-for-single-sign-on) login flow is only supported in old Element clients and will not be supported in Element X. Element X will only support the new SSO-based login flow provided by MAS, so if you want to use SSO with Element X, you will need to switch to MAS.

- To help drive adoption of the "Next-generation auth for Matrix" by switching to what's ultimately coming anyway

- To help discover (and potentially fix) MAS integration issues with this Ansible playbook

- To help discover (and potentially fix) MAS integration issues with various other Matrix components (bridges, bots, clients, etc.)

- To reap some of the security benefits that Matrix Authentication Service offers, as outlined in the [Better authentication, session management and permissions in Matrix](https://matrix.org/blog/2023/09/better-auth/) article.

## Prerequisites

- ⚠️ the [Synapse](configuring-playbook-synapse.md) homeserver implementation (which is the default for this playbook). Other homeserver implementations ([Dendrite](./configuring-playbook-dendrite.md), [Conduit](./configuring-playbook-conduit.md), etc.) do not support integrating with Matrix Authentication Service yet.

- ❌ **disabling all password providers** for Synapse (things like [shared-secret-auth](./configuring-playbook-shared-secret-auth.md), [rest-auth](./configuring-playbook-rest-auth.md), [LDAP auth](./configuring-playbook-ldap-auth.md), etc.) More details about this are available in the [Expectations](#expectations) section below.

## Expectations

This section details what you can expect when switching to the Matrix Authentication Service (MAS).

- ❌ **Synapse password providers will need to be disabled**. You can no longer use [shared-secret-auth](./configuring-playbook-shared-secret-auth.md), [rest-auth](./configuring-playbook-rest-auth.md), [LDAP auth](./configuring-playbook-ldap-auth.md), etc. When the authentication flow is handled by MAS (not by Synapse anymore), it doesn't make sense to extend the Synapse authentication flow with additional modules. Many bridges used to rely on shared-secret-auth for doing double-puppeting (impersonating other users), but most (at least the mautrix bridges) nowadays use [Appservice Double Puppet](./configuring-playbook-appservice-double-puppet.md) as a better alternative. Older/maintained bridges may still rely on shared-secret-auth, as do other services like [matrix-corporal](./configuring-playbook-matrix-corporal.md).

- ❌ Certain **tools like [Synapse Admin](./configuring-playbook-synapse-admin.md) do not have full compatibility with MAS yet**. Synapse Admin already supports OIDC auth, browsing users (which Synapse will internally fetch from MAS) and updating user avatars. However, editing users (passwords, etc.) now needs to happen directly against MAS using the [MAS Admin API](https://element-hq.github.io/matrix-authentication-service/api/index.html), which Synapse Admin cannot interact with yet. You may be interested in using [Element Admin](./configuring-playbook-element-admin.md) for these purposes.

- ❌ **Some services experience issues when authenticating via MAS**:

  - [Reminder bot](configuring-playbook-bot-matrix-reminder-bot.md) seems to be losing some of its state on each restart and may reschedule old reminders once again

- ❌ **Encrypted appservices** do not work yet (related to [MSC4190](https://github.com/matrix-org/matrix-spec-proposals/pull/4190) and [PR 17705 for Synapse](https://github.com/element-hq/synapse/pull/17705)), so all bridges/bots that rely on encryption will fail to start (see [this issue](https://github.com/spantaleev/matrix-docker-ansible-deploy/issues/3658) for Hookshot). You can use these bridges/bots only if you **keep end-to-bridge encryption disabled** (which is the default setting).

- ⚠️ [Migrating an existing Synapse homeserver to Matrix Authentication Service](#migrating-an-existing-synapse-homeserver-to-matrix-authentication-service) is **possible**, but requires **some playbook-assisted manual work**. Migration is **reversible with no or minor issues if done quickly enough**, but as users start logging in (creating new login sessions) via the new MAS setup, disabling MAS and reverting back to the Synapse user database will cause these new sessions to break.

- ⚠️ Delegating user authentication to MAS causes **your Synapse server to be completely dependent on one more service** for its operations. MAS is quick & lightweight and should be stable enough already, but this is something to keep in mind when making the switch.

- ⚠️ If you've got [OIDC configured in Synapse](./configuring-playbook-synapse.md#synapse--openid-connect-for-single-sign-on), you will need to migrate your OIDC configuration to MAS by adding an [Upstream OAuth2 configuration](#upstream-oauth2-configuration).

- ⚠️ A [compatibility layer](https://element-hq.github.io/matrix-authentication-service/setup/homeserver.html#set-up-the-compatibility-layer) is installed — all `/_matrix/client/*/login` (etc.) requests will be routed to MAS instead of going to the homeserver. This is done both publicly (e.g. `https://matrix.example.com/_matrix/client/*/login`) and on the internal Traefik entrypoint (e.g. `https://matrix-traefik:8008/_matrix/client/*/login`) which helps addon services reach the homeserver's Client-Server API. You typically don't need to do anything to make this work, but it's good to be aware of it, especially if you have a [custom webserver setup](./configuring-playbook-own-webserver.md).

- ✅ Your **existing login sessions will continue to work** (you won't get logged out). Migration will require a bit of manual work and minutes of downtime, but it's not too bad.

- ✅ Various clients ([Cinny](./configuring-playbook-client-cinny.md), [Element Web](./configuring-playbook-client-element-web.md), Element X, FluffyChat) will be able to use the **new SSO-based login flow** provided by Matrix Authentication Service

- ✅ The **old login flow** (called `m.login.password`) **will still continue to work**, so clients (old Element Web, etc.) and bridges/bots that don't support the new OIDC-based login flow will still work

- ✅ [Registering users](./registering-users.md) via **the playbook's `register-user` tag remains unchanged**. The playbook automatically does the right thing regardless of homeserver implementation (Synapse, Dendrite, etc.) and whether MAS is enabled or not. When MAS is enabled, the playbook will forward user-registration requests to MAS. Registering users via the command-line is no longer done via the `/matrix/synapse/bin/register` script, but via `/matrix/matrix-authentication-service/bin/register-user`.

- ✅ Users that are prepared by the playbook (for bots, bridges, etc.) will continue to be registered automatically as expected. The playbook automatically does the right thing regardless of homeserver implementation (Synapse, Dendrite, etc.) and whether MAS is enabled or not. When MAS is enabled, the playbook will forward user-registration requests to MAS.

## Installation flows

### New homeserver

For new homeservers (which don't have any users in their Synapse database yet), follow the [Adjusting the playbook configuration](#adjusting-the-playbook-configuration) instructions and then proceed with [Installing](#installing).

### Existing homeserver

Other homeserver implementations ([Dendrite](./configuring-playbook-dendrite.md), [Conduit](./configuring-playbook-conduit.md), etc.) do not support integrating with Matrix Authentication Service yet.

For existing Synapse homeservers:

- when following the [Adjusting the playbook configuration](#adjusting-the-playbook-configuration) instructions, make sure to **disable the integration between Synapse and MAS** by **uncommenting** the `matrix_authentication_service_migration_in_progress: true` line as described in the [Marking an existing homeserver for migration](#marking-an-existing-homeserver-for-migration) section below.

- then follow the [Migrating an existing Synapse homeserver to Matrix Authentication Service](#migrating-an-existing-synapse-homeserver-to-matrix-authentication-service) instructions to perform the installation and migration

## Adjusting DNS records (optional)

By default, this playbook installs the Matrix Authentication Service on the `matrix.` subdomain, at the `/auth` path (https://matrix.example.com/auth). This makes it easy to install it, because it **doesn't require additional DNS records to be set up**. If that's okay, you can skip this section.

If you wish to adjust it, see the section [below](#adjusting-the-matrix-authentication-service-url-optional) for details about DNS configuration.

## Adjusting the playbook configuration

To enable Matrix Authentication Service, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
matrix_authentication_service_enabled: true

# Generate this encryption secret with: `openssl rand -hex 32`
matrix_authentication_service_config_secrets_encryption: ''

# When migrating an existing homeserver to Matrix Authentication Service, uncomment the line below.
# Learn more about the migration process in the "Marking an existing homeserver for migration" section below.
# For brand-new installations which start directly on MAS, this line can be removed.
# matrix_authentication_service_migration_in_progress: true
```

In the sub-sections that follow, we'll cover some additional configuration options that you may wish to adjust.

There are many other configuration options available. Consult the [`defaults/main.yml` file](../roles/custom/matrix-authentication-service/defaults/main.yml) in the [matrix-authentication-service role](../roles/custom/matrix-authentication-service/) to discover them.

### Adjusting the Matrix Authentication Service URL (optional)

By tweaking the `matrix_authentication_service_hostname` and `matrix_authentication_service_path_prefix` variables, you can easily make the service available at a **different hostname and/or path** than the default one.

Example additional configuration for your `vars.yml` file:

```yaml
# Change the default hostname and path prefix
matrix_authentication_service_hostname: auth.example.com
matrix_authentication_service_path_prefix: /
```

If you've changed the default hostname, you may need to create a CNAME record for the Matrix Authentication Service domain (`auth.example.com`), which targets `matrix.example.com`.

When setting, replace `example.com` with your own.

### Marking an existing homeserver for migration

The [configuration above](#adjusting-the-playbook-configuration) instructs existing users wishing to migrate to add `matrix_authentication_service_migration_in_progress: true` to their configuration.

This is done temporarily. The migration steps are described in more detail in the [Migrating an existing Synapse homeserver to Matrix Authentication Service](#migrating-an-existing-synapse-homeserver-to-matrix-authentication-service) section below.

### Upstream OAuth2 configuration

To make Matrix Authentication Service delegate to an existing upstream OAuth 2.0/OIDC provider, you can use its [`upstream_oauth2.providers` setting](https://element-hq.github.io/matrix-authentication-service/reference/configuration.html#upstream_oauth2providers).

The playbook exposes a `matrix_authentication_service_config_upstream_oauth2_providers` variable for controlling this setting.

<details>
<summary>Click to expand the example configuration:</summary>

Example additional configuration for your `vars.yml` file:

```yaml
matrix_authentication_service_config_upstream_oauth2_providers:
  - # A unique identifier for the provider
    # Must be a valid ULID
    id: 01HFVBY12TMNTYTBV8W921M5FA
    # This can be set if you're migrating an existing (legacy) Synapse OIDC configuration.
    # The value used here would most likely be "oidc" or "oidc-provider".
    # See: https://element-hq.github.io/matrix-authentication-service/setup/migration.html#map-any-upstream-sso-providers
    synapse_idp_id: null
    # The issuer URL, which will be used to discover the provider's configuration.
    # If discovery is enabled, this *must* exactly match the `issuer` field
    # advertised in `<issuer>/.well-known/openid-configuration`.
    issuer: https://example.com/
    # A human-readable name for the provider,
    # which will be displayed on the login page
    #human_name: Example
    # A brand identifier for the provider, which will be used to display a logo
    # on the login page. Values supported by the default template are:
    #  - `apple`
    #  - `google`
    #  - `facebook`
    #  - `github`
    #  - `gitlab`
    #  - `twitter`
    #brand_name: google
    # The client ID to use to authenticate to the provider
    client_id: mas-fb3f0c09c4c23de4
    # The client secret to use to authenticate to the provider
    # This is only used by the `client_secret_post`, `client_secret_basic`
    # and `client_secret_jwk` authentication methods
    #client_secret: f4f6bb68a0269264877e9cb23b1856ab
    # Which authentication method to use to authenticate to the provider
    # Supported methods are:
    #   - `none`
    #   - `client_secret_basic`
    #   - `client_secret_post`
    #   - `client_secret_jwt`
    #   - `private_key_jwt` (using the keys defined in the `secrets.keys` section)
    token_endpoint_auth_method: client_secret_post
    # Which signing algorithm to use to sign the authentication request when using
    # the `private_key_jwt` or the `client_secret_jwt` authentication methods
    #token_endpoint_auth_signing_alg: RS256
    # The scopes to request from the provider
    # In most cases, it should always include `openid` scope
    scope: "openid email profile"
    # How the provider configuration and endpoints should be discovered
    # Possible values are:
    #  - `oidc`: discover the provider through OIDC discovery,
    #     with strict metadata validation (default)
    #  - `insecure`: discover through OIDC discovery, but skip metadata validation
    #  - `disabled`: don't discover the provider and use the endpoints below
    #discovery_mode: oidc
    # Whether PKCE should be used during the authorization code flow.
    # Possible values are:
    #  - `auto`: use PKCE if the provider supports it (default)
    #    Determined through discovery, and disabled if discovery is disabled
    #  - `always`: always use PKCE (with the S256 method)
    #  - `never`: never use PKCE
    #pkce_method: auto
    # The provider authorization endpoint
    # This takes precedence over the discovery mechanism
    #authorization_endpoint: https://example.com/oauth2/authorize
    # The provider token endpoint
    # This takes precedence over the discovery mechanism
    #token_endpoint: https://example.com/oauth2/token
    # The provider JWKS URI
    # This takes precedence over the discovery mechanism
    #jwks_uri: https://example.com/oauth2/keys
    # How user attributes should be mapped
    #
    # Most of those attributes have two main properties:
    #   - `action`: what to do with the attribute. Possible values are:
    #      - `ignore`: ignore the attribute
    #      - `suggest`: suggest the attribute to the user, but let them opt out
    #      - `force`: always import the attribute, and don't fail if it's missing
    #      - `require`: always import the attribute, and fail if it's missing
    #   - `template`: a Jinja2 template used to generate the value. In this template,
    #      the `user` variable is available, which contains the user's attributes
    #      retrieved from the `id_token` given by the upstream provider.
    #
    # Each attribute has a default template which follows the well-known OIDC claims.
    #
    claims_imports:
      # The subject is an internal identifier used to link the
      # user's provider identity to local accounts.
      # By default it uses the `sub` claim as per the OIDC spec,
      # which should fit most use cases.
      subject:
        #template: "{% raw %}{{ user.sub }}{% endraw %}"
      # The localpart is the local part of the user's Matrix ID.
      # For example, on the `example.com` server, if the localpart is `alice`,
      #  the user's Matrix ID will be `@alice:example.com`.
      localpart:
        #action: force
        #template: "{% raw %}{{ user.preferred_username }}{% endraw %}"
      # The display name is the user's display name.
      #displayname:
        #action: suggest
        #template: "{% raw %}{{ user.name }}{% endraw %}"
      # An email address to import.
      email:
        #action: suggest
        #template: "{% raw %}{{ user.email }}{% endraw %}"
        # Whether the email address must be marked as verified.
        # Possible values are:
        #  - `import`: mark the email address as verified if the upstream provider
        #     has marked it as verified, using the `email_verified` claim.
        #     This is the default.
        #   - `always`: mark the email address as verified
        #   - `never`: mark the email address as not verified
        #set_email_verification: import
```
</details>

💡 Refer to the [`upstream_oauth2.providers` setting](https://element-hq.github.io/matrix-authentication-service/reference/configuration.html#upstream_oauth2providers) for the most up-to-date schema and example for providers. The value shown above here may be out of date.

⚠️ The syntax for existing [OIDC providers configured in Synapse](./configuring-playbook-synapse.md#synapse--openid-connect-for-single-sign-on) is slightly different, so you will need to adjust your configuration when switching from Synapse OIDC to MAS upstream OAuth2.

⚠️ When [migrating an existing homeserver](#migrating-an-existing-synapse-homeserver-to-matrix-authentication-service) which contains OIDC-sourced users, you will need to:

- [Configure upstream OIDC provider mapping for syn2mas](#configuring-upstream-oidc-provider-mapping-for-syn2mas)
- go through the [migrating an existing homeserver](#migrating-an-existing-synapse-homeserver-to-matrix-authentication-service) process
- remove all Synapse OIDC-related configuration (`matrix_synapse_oidc_*`) to prevent it being in conflict with the MAS OIDC configuration

### Extending the configuration

There are some additional things you may wish to configure about the component.

Take a look at:

- `roles/custom/matrix-authentication-service/defaults/main.yml` for some variables that you can customize via your `vars.yml` file
- `roles/custom/matrix-authentication-service/templates/config.yaml.j2` for the component's default configuration. You can override settings (even those that don't have dedicated playbook variables) using the `matrix_authentication_service_configuration_extension_yaml` variable

## Installing

Now that you've [adjusted the playbook configuration](#adjusting-the-playbook-configuration) and [your DNS records](#adjusting-dns-records), you can run the playbook with [playbook tags](playbook-tags.md) as below:

<!-- NOTE: let this conservative command run (instead of install-all) to make it clear that failure of the command means something is clearly broken. -->
```sh
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start
```

**Notes**:

- The shortcut commands with the [`just` program](just.md) are also available: `just install-all` or `just setup-all`

  `just install-all` is useful for maintaining your setup quickly ([2x-5x faster](../CHANGELOG.md#2x-5x-performance-improvements-in-playbook-runtime) than `just setup-all`) when its components remain unchanged. If you adjust your `vars.yml` to remove other components, you'd need to run `just setup-all`, or these components will still remain installed. Note these shortcuts run the `ensure-matrix-users-created` tag too.

- If you're in the process of migrating an existing Synapse homeserver to MAS, you should now follow the rest of the steps in the [Migrating an existing Synapse homeserver to Matrix Authentication Service](#migrating-an-existing-synapse-homeserver-to-matrix-authentication-service) guide.

💡 After installation, you should [verify that Matrix Authentication Service is installed correctly](#verify-that-matrix-authentication-service-is-installed-correctly).

## Migrating an existing Synapse homeserver to Matrix Authentication Service

Our migration guide is loosely based on the upstream [Migrating an existing homeserver](https://element-hq.github.io/matrix-authentication-service/setup/migration.html) guide.

Migration is done via a sub-command called `syn2mas`, which the playbook could run for you (in a container).

The installation + migration steps are like this:

1. [Adjust your configuration](#adjusting-the-playbook-configuration) to **disable the integration between the homeserver and MAS**. This is done by **uncommenting** the `matrix_authentication_service_migration_in_progress: true` line.

2. Perform the initial [installation](#installing). At this point:

    - Matrix Authentication Service will be installed. Its database will be empty, so it cannot validate existing access tokens or authentication users yet.

    - The homeserver will still continue to use its local database for validating existing access tokens.

    - Various [compatibility layer URLs](https://element-hq.github.io/matrix-authentication-service/setup/homeserver.html#set-up-the-compatibility-layer) are not yet installed. New login sessions will still be forwarded to the homeserver, which is capable of completing them.

    - The `matrix-user-creator` role would be suppressed, so that it doesn't automatically attempt to create users (for bots, etc.) in the MAS database. These user accounts likely already exist in Synapse's user database and could be migrated over (via syn2mas, as per the steps below), so creating them in the MAS database would have been unnecessary and potentially problematic (conflicts during the syn2mas migration).

3. Consider taking a full [backup of your Postgres database](./maintenance-postgres.md#backing-up-postgresql). This is done just in case. The **syn2mas migration command does not delete any data**, so it should be possible to revert to your previous setup by merely disabling MAS and re-running the playbook (no need to restore a Postgres backup). However, do note that as users start logging in (creating new login sessions) via the new MAS setup, disabling MAS and reverting back to the Synapse user database will cause these new sessions to break.

4. [Migrate your data from Synapse to Matrix Authentication Service using syn2mas](#migrate-your-data-from-synapse-to-matrix-authentication-service-using-syn2mas)

5. [Adjust your configuration](#adjusting-the-playbook-configuration) again, to:

  - remove the `matrix_authentication_service_migration_in_progress: false` line

  - if you had been using [OIDC providers configured in Synapse](./configuring-playbook-synapse.md#synapse--openid-connect-for-single-sign-on), remove all Synapse OIDC-related configuration (`matrix_synapse_oidc_*`) to prevent it being in conflict with the MAS OIDC configuration

5. Perform the [installation](#installing) again. At this point:

    - The homeserver will start delegating authentication to MAS.

    - The compatibility layer URLs will be installed. New login sessions will be completed by MAS.

6. [Verify that Matrix Authentication Service is installed correctly](#verify-that-matrix-authentication-service-is-installed-correctly)

### Migrate your data from Synapse to Matrix Authentication Service using syn2mas

You can invoke the `syn2mas` tool via the playbook by running the playbook's `matrix-authentication-service-mas-cli-syn2mas` tag. We recommend first doing a [dry-run](#performing-a-syn2mas-dry-run) and then a [real migration](#performing-a-real-syn2mas-migration).

#### Configuring syn2mas

If you're using [OIDC with Synapse](./configuring-playbook-synapse.md#synapse--openid-connect-for-single-sign-on), you will need to [Configuring upstream OIDC provider mapping for syn2mas](#configuring-upstream-oidc-provider-mapping-for-syn2mas).

If you only have local (non-OIDC) users in your Synapse database, you can likely run `syn2mas` as-is (without doing additional configuration changes).

When you're done with potentially configuring `syn2mas`, proceed to doing a [dry-run](#performing-a-syn2mas-dry-run) and then a [real migration](#performing-a-real-syn2mas-migration).

##### Configuring upstream OIDC provider mapping for syn2mas

Since Matrix Authentication Service v0.16.0 (which replaced the standalone `syn2mas` tool with a `mas-cli syn2mas` sub-command), OIDC configuration (mapping from your old OIDC configuration to your new one, etc) is meant to be configured in the Matrix Authentication Service configuration (via `matrix_authentication_service_config_upstream_oauth2_providers`) as a `synapse_idp_id` property for each provider.

You can refer to the [Map any upstream SSO providers](https://element-hq.github.io/matrix-authentication-service/setup/migration.html#map-any-upstream-sso-providers) section of the MAS documentation for figuring out how to set the `synapse_idp_id` value in `matrix_authentication_service_config_upstream_oauth2_providers` correctly.

#### Performing a syn2mas dry-run

Having [configured syn2mas](#configuring-syn2mas), we recommend doing a [dry-run](https://en.wikipedia.org/wiki/Dry_run_(testing)) first to verify that everything will work out as expected.

A dry-run would not cause downtime, because it avoids stopping Synapse.

To perform a dry-run, run:

```sh
just run-tags matrix-authentication-service-mas-cli-syn2mas -e matrix_authentication_service_syn2mas_migrate_dry_run=true
```

Observe the command output (especially the last line of the the syn2mas output). If you are confident that the migration will work out as expected, you can proceed with a [real migration](#performing-a-real-syn2mas-migration).

#### Performing a real syn2mas migration

Before performing a real migration make sure:

- you've familiarized yourself with the [expectations](#expectations)

- you've performed a Postgres backup, just in case

- you're aware of the irreversibility of the migration process without disruption after users have created new login sessions via the new MAS setup

- you've [configured syn2mas](#configuring-syn2mas), especially if you've used [OIDC with Synapse](./configuring-playbook-synapse.md#synapse--openid-connect-for-single-sign-on)

- you've performed a [syn2mas dry-run](#performing-a-syn2mas-dry-run) and don't see any issues in its output

To perform a real migration, run the `matrix-authentication-service-mas-cli-syn2mas` tag **without** the `matrix_authentication_service_syn2mas_migrate_dry_run` variable:

```sh
just run-tags matrix-authentication-service-mas-cli-syn2mas
```

Having performed a `syn2mas` migration once, trying to do it again will report errors (e.g. "Error: The MAS database is not empty: rows found in at least `users`. Please drop and recreate the database, then try again.").

## Verify that Matrix Authentication Service is installed correctly

After [installation](#installing), run the `doctor` subcommand of the [`mas-cli` command-line tool](https://element-hq.github.io/matrix-authentication-service/reference/cli/index.html) to verify that MAS is installed correctly.

You can do it:

- either via the Ansible playbook's `matrix-authentication-service-mas-cli-doctor` tag: `just run-tags matrix-authentication-service-mas-cli-doctor`

- or by running the `mas-cli` script on the server (which invokes the `mas-cli` tool inside a container): `/matrix/matrix-authentication-service/bin/mas-cli doctor`

If successful, you should see some output that looks like this:

```
💡 Running diagnostics, make sure that both MAS and Synapse are running, and that MAS is using the same configuration files as this tool.
✅ Matrix client well-known at "https://example.com/.well-known/matrix/client" is valid
✅ Homeserver is reachable at "http://matrix-synapse:8008/_matrix/client/versions"
✅ Homeserver at "http://matrix-synapse:8008/_matrix/client/v3/account/whoami" is reachable, and it correctly rejected an invalid token.
✅ The Synapse admin API is reachable at "http://matrix-synapse:8008/_synapse/admin/v1/server_version".
✅ The Synapse admin API is reachable with authentication at "http://matrix-synapse:8008/_synapse/admin/v1/background_updates/status".
✅ The legacy login API at "https://matrix.example.com/_matrix/client/v3/login" is reachable and is handled by MAS.
```

## Usage

### Management

You can use the [`mas-cli` command-line tool](https://element-hq.github.io/matrix-authentication-service/reference/cli/index.html) (exposed via the `/matrix/matrix-authentication-service/bin/mas-cli` script) to perform administrative tasks against MAS.

This documentation page already mentions:

- the `mas-cli doctor` sub-command in the [Verify that Matrix Authentication Service is installed correctly](#verify-that-matrix-authentication-service-is-installed-correctly) section, which you can run via the CLI and via the Ansible playbook's `matrix-authentication-service-mas-cli-doctor` tag

- the `mas-cli manage register-user` sub-command in the [Registering users](./registering-users.md) documentation

There are other sub-commands available. Run `/matrix/matrix-authentication-service/bin/mas-cli` to get an overview.

### User registration

After Matrix Authentication Service is [installed](#installing), users need to be managed there (unless you're managing them in an [upstream OAuth2 provider](#upstream-oauth2-configuration)).

You can register users new users as described in the [Registering users](./registering-users.md) documentation (via `mas-cli manage register-user` or the Ansible playbook's `register-user` tag).

### Working around email deliverability issues

Matrix Authentication Service only sends emails when:

- it verifies email addresses for users who are self-registering with a password

- a user tries to add an email to their account

If Matrix Authentication Service tries to send an email and it fails because [your email-sending configuration](./configuring-playbook-email.md) is not working, you may need to work around email deliverability.

If email delivery is not working, **you can retrieve the email verification code from the Matrix Authentication Service's logs** (`journalctl -fu matrix-authentication-service`).

Alternatively, you can use the [`mas-cli` management tool](#management) to manually verify email addresses for users. Example: `/matrix/matrix-authentication-service/bin/mas-cli manage verify-email some.username email@example.com`

## Troubleshooting

As with all other services, you can find the logs in [systemd-journald](https://www.freedesktop.org/software/systemd/man/systemd-journald.service.html) by logging in to the server with SSH and running `journalctl -fu matrix-authentication-service`.
