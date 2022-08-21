# Obtaining an Access Token

When setting up some optional features like bots and bridges you will need to provide an access token for some user. This document provides documentation on how to obtain such an access token.

**Access tokens are sensitive information. Do not include them in any bug reports, messages, or logs. Do not share the access token with anyone.**

## Prerequisites

The user for whom you want to obtain an access token needs to already exist. You can use this playbook to [register a new user](registering-users.md), if you have not already.

Below, we describe 2 ways to generate an access token for a user - using [Element](#obtain-an-access-token-via-element) or [curl](#obtain-an-access-token-via-curl). For both ways you need the user's password.

## Obtain an access token via Element

1. In a private browsing session (incognito window), open Element.
1. Log in with the user's credentials.
1. In the settings page, choose "Help & About", scroll down to the bottom and expand the `Access Token` section (see screenshot below).
1. Copy the access token to your configuration.
1. Close the private browsing session. **Do not log out**. Logging out will invalidate the token, making it not work.

![Obtaining an access token with Element](assets/obtain_admin_access_token_element.png)


## Obtain an access token via curl

You can use the following command to get an access token for your user directly from the [Matrix Client-Server API](https://www.matrix.org/docs/guides/client-server-api#login):

```
curl -XPOST -d '{
    "identifier": { "type": "m.id.user", "user": "USERNAME" },
    "password": "PASSWORD",
    "type": "m.login.password",
    "device_id": "YOURDEVICEID"
}' 'https://matrix.YOURDOMAIN/_matrix/client/r0/login'
```
Change `USERNAME`, `PASSWORD`, and `YOURDOMAIN` accordingly.

`YOURDEVICEID` is optional and can be used to more easily identify the session later. When omitted (mind the commas in the JSON payload if you'll be omitting it), a random device ID will be generated.

Your response will look like this (prettified):

```
{
    "user_id":"@USERNAME:YOURDOMAIN",
    "access_token":">>>YOUR_ACCESS_TOKEN_IS_HERE<<<",
    "home_server":"YOURDOMAIN",
    "device_id":"YOURDEVICEID"
}
```
