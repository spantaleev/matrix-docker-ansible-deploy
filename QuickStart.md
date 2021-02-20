### 0. What is Ansible? How does it work?

[Ansible](https://www.ansible.com/) is an automation program. This "playbook" is a collection of tasks/scripts that will set up a [Matrix](https://matrix.org/) server for you, so you don't have to perform these tasks manually.

We have written these automated tasks for you and all you need to do is execute them using the Ansible program.

You can install Ansible and this playbook code repository on your own computer and tell it to install Matrix services at the server living at `matrix.DOMAIN`. We recommend installing Ansible on your own computer.  (**Optional/Advanced**: If you want to download Ansible and the playbook directly on your server, see [dedicated Ansible documentation page](ansible.md))

### 1. Installing Ansible and this playbook on MacOS

Ensure you have Homebrew installed.  If you need to install Homebrew, open your terminal and run

`/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`

Next, to install Ansible on your machine, run this command in the terminal:

`brew install ansible`

Finally, to install this playbook, run this command in the terminal:

`git clone https://github.com/spantaleev/matrix-docker-ansible-deploy.git`

### 2. Prepare your Domain/DNS

This guide requires the ability to create CNAME records with your DNS.  You may be able to do this at the website where you purchased your domain.  You can also follow simple guides to point your domain to Cloudfare, and if your domain is pointed to Cloudfare, you can configure the DNS in your Cloudfare account.

**First**, choose a domain name that will only be used for your Matrix homeserver.  If you don't have one yet, purchase a domain.

If you want help deciding, the domain of your Matrix homeserver is like the domain at the end of an email address.

An email address like casey@example.com would look like **casey:example.com** as a Matrix username.  And if a friend named Mika wanted to join Casey's matrix server, Mika's username could be **mika:example.com**

So you can be clever, fun, simple, creative, inspired, whatever you want with your Matrix homeserver's domain.  For example:

* With the domain `waynefamily.org`, a username could look like **alfred:waynefamily.org**

* With the domain `nebuchadnezzar.ship`, a username could look like **tank:nebuchadnezzar.ship**

* With the domain `councilofricks.com`, a username could look like **prezmorty:councilofricks.com**

Once you have a domain for your Matrix homeserver, continue.

**Second**, on your domain registrar or Cloudfare, configure the following DNS records for your `<your-domain>`.

| Type  | Host                         | Priority | Weight | Port | Target                 |
| ----- | ---------------------------- | -------- | ------ | ---- | ---------------------- |
| CNAME | `element`                    | -        | -      | -    | `matrix.<your-domain>` |
| SRV   | `_matrix-identity._tcp`      | 10       | 0      | 443  | `matrix.<your-domain>` |
| CNAME | `dimension`              | -        | -      | -    | `matrix.<your-domain>` |
| CNAME | `jitsi`                  | -        | -      | -    | `matrix.<your-domain>` |
| CNAME | `stats`                 | -        | -      | -    | `matrix.<your-domain>` |

After saving these records, it should looks something like this

![Image of DNS record table on Cloudfare](https://i.imgur.com/bBLz5MG.png)

[*Note:* If you are using Cloudflare DNS, make sure that all records to `DNS only` (click on the DNS cloud icon to make it grey). Otherwise, fetching certificates will fail.]

**Third**, configure a simple email server for your domain.  Most domain registrars have a built-in option for this.  Fastmail.com also makes it simple.

(Why?  In order to make your website HTTPS secured, the Ansible playbook automates a free service called Let's Encrypt, and this is simpler if you have an email address on your domain -- e.g. **casey@yourdomain.com** instead of **casey@gmail.com**)

Setting up email for your domiain will likely require you to create a few more DNS records -- some MX records, some additional CNAME records, some TXT records.  This is all expected, just follow the instructions of the service you're using.

### 3. Setting up your VPS

We now have a domain name for our Matrix homeserver, but we don't acutally have the server.  Nothing exists at our domain.

To have a working Matrix homeserver, we need a server.

For simplicity, we'll be purchasing a Virtual Private Server (VPS) from an online provider.  These servers usually cost between $5 and $15 per month.

Here are some providers you can choose from.  When selecting a provider, make sure they have servers physicall located near you -- in a nearby country or continent:

**For Europe**:  
* https://contabo.com/en/
* https://www.hetzner.com/

**For USA/Global**: 
* https://www.vultr.com/
* https://www.digitalocean.com/. 
* https://www.linode.com/

Once you create an account with one of those services, you'll be selecting your type of VPS.  If you're confused about which to select, go with the offering that's in the $5 - $15 monthly price range.

(*Note: These providers often offer free trial credits for new users, before or after you create your account.  Those promotions won't always be active, but keep an eye out for them during the set-up process.*)

You'll also have a choice of Operating System (OS) and specs (RAM, location).  

For the Operating System, in this guide, we'll be choosing **Debian 10 x64**.  

For RAM, make sure to choose an option with at least 2000MB/2GB.  

For location, choose the location that is closest to you/the people who will be using the server.  (If that includes the US and Europe, locations like New York and New Jersey can be good choices)

Finally, create your server.  This will take a few minutes, as your provider spins up your virtual server with your Operating System and RAM of choice.

When this is complete, you'll have a chance to name your new server and see the details - most importantly, the **IP Address** of your server.

### 4. Connecting domain to VPS

Return to the website where you configured your DNS records earlier (either your domain registrar or Cloudfare).

Now, add two more DNS records, which will instruct `<your-domain>` and `<matrix.your-domain>` to point to your server's IP Address.

| Type  | Host                         | Priority | Weight | Port | Target                 |
| ----- | ---------------------------- | -------- | ------ | ---- | ---------------------- |
| A     | `matrix`                     | -        | -      | -    | `server's IP address`     |
| A     | `example.com`                     | -        | -      | -    | `server's IP address`     |

***Note:*** If you are using Cloudflare DNS, make sure that all records to `DNS only` (click on the DNS cloud icon to make it grey).

So your table should include the following records:

| Type  | Host                         | Priority | Weight | Port | Target                 |
| ----- | ---------------------------- | -------- | ------ | ---- | ---------------------- |
| A     | `matrix`                     | -        | -      | -    | `server's IP address`     |
| A     | `example.com`                     | -        | -      | -    | `server's IP address`     |
| CNAME | `element`                    | -        | -      | -    | `matrix.<your-domain>` |
| SRV   | `_matrix-identity._tcp`      | 10       | 0      | 443  | `matrix.<your-domain>` |
| CNAME | `dimension`              | -        | -      | -    | `matrix.<your-domain>` |
| CNAME | `jitsi`                  | -        | -      | -    | `matrix.<your-domain>` |
| CNAME | `stats`                 | -        | -      | -    | `matrix.<your-domain>` |

(If you configured email, you'll also have some MX records, some additional CNAMEs, and possibly a TXT record)

Once you have added these records, it will take some time for the changes to take affect and for <your-domain> to point to your server's IP address.

You can check on this progress with a tool like https://www.whatsmydns.net/.  Once most of the locations are green, you're good to go.

### 5. Configuring the Ansible Playbook

In the terminal, `cd` into your `matrix-docker-ansible-deploy` repository. Then run the following commands:

1. `mkdir inventory/host_vars/matrix.<your-domain>` (This creates a directory to hold your configuration)
2. `cp examples/vars.yml inventory/host_vars/matrix.<your-domain>/vars.yml` (This copies a sample configuration file to the newly created directory)
3. `cp examples/hosts inventory/hosts` (This compies the sample inventory hosts file to the newly created directory)

Now, open `matrix-docker-ansible-deploy` with your code editor, and complete the following steps:

**First,** open `inventory/host_vars/matrix.<your-domain>/vars.yml`

1. Replace `YOUR_BARE_DOMAIN_NAME_HERE` with your domain name (e.g. example.com)

2. Add the email that you configured on your domain as the value for `matrix_ssl_lets_encrypt_support_email`

3. Generate a random, secure password, and add that as the value for `matrix_coturn_turn_static_auth_secret`.  Make sure to backup this password as well (save it somewhere else, or write it down)

4. Generate a random, secure password, and add that as the value for `matrix_synapse_macaroon_secret_key`.  Make sure to backup this password as well (save it somewhere else, or write it down)

5. Generate a random, secure password, and add that as the value for `matrix_postgres_connection_password`.  Make sure to backup this password as well (save it somewhere else, or write it down)

6. Add `matrix_nginx_proxy_base_domain_serving_enabled: true` to the end of the file.  (This is utilized later in for serving the base domain)

7. Save this file when complete.

**Second,** open `inventory/hosts`

1. On line 19, replace <your-domain> with your domain (e.g. example.com) and replace `<your-server's external IP address>` with your server's IP address.

2. Save this file when complete.

### 6. Installing Ansible

In the terminal, `cd` into your `matrix-docker-ansible-deploy` repository. Then run the following command:

`ansible-playbook -i inventory/hosts setup.yml --tags=setup-all`

*If you see errors due to a lack of SSH/pasword, try running this command instead:*

`ansible-playbook -i inventory/hosts setup.yml --tags=setup-all --ask-pass`

(*When you're prompted to enter your password, copy your server's password from the webpage where you see it's IP address, and use CTRL-V to paste the password into the terminal.*)

If successfuly, the Ansible playbook should immediately start running.

(Whichever command works for you, feel free to run it any time you feel something is off with your server or you want to apply new settings.)

When this command is finished executing, you'll see a **PLAY RECAP** in the terminal.  If you have any failed tasks, try to understand what went wrong by looking through the logs.  Google any errors/failed tasks that you find, and search for those keywords in the [GitHub repository](https://github.com/spantaleev/matrix-docker-ansible-deploy) and the [Issues section](https://github.com/spantaleev/matrix-docker-ansible-deploy/issues).

If you're unable to debug your issue, you can go through the detailed Ansible docs.  Starting with [Prerequisites](https://github.com/spantaleev/matrix-docker-ansible-deploy/blob/master/docs/prerequisites.md), then [Configuring DNS](https://github.com/spantaleev/matrix-docker-ansible-deploy/blob/master/docs/configuring-dns.md), then [Configuring this Ansible Playbook](https://github.com/spantaleev/matrix-docker-ansible-deploy/blob/master/docs/configuring-playbook.md)(skip the "Other configuration options" until you successfully install the ansible playbook.), and finally [Installing](https://github.com/spantaleev/matrix-docker-ansible-deploy/blob/master/docs/installing.md).

Once you have run `ansible-playbook -i inventory/hosts setup.yml --tags=setup-all` (or `ansible-playbook -i inventory/hosts setup.yml --tags=setup-all --ask-pass`) successfully with 0 failed tasks, you can start the services by running the following command in the terminal:

`ansible-playbook -i inventory/hosts setup.yml --tags=start` 

(or `ansible-playbook -i inventory/hosts setup.yml --tags=start --ask-pass` if you needed to use --ask-pass above)

If succesful, you should see 0 failed tasks in the **PLAY RECAP**.  (Also, this should have automatically Configured Service Discovery via .well-known for you.)

### 7. Check if your services work

This playbook can perform a check to ensure that you've configured things correctly and that services are running.

To perform the check, run:

```bash
ansible-playbook -i inventory/hosts setup.yml --tags=self-check
```

If it's all green, everything is probably running correctly.

Besides this self-check, you can also check your server by using the [Federation Tester](https://federationtester.matrix.org/) and entering `<your-domain>`.  If it's all green, everything is probably running correctly.  If there is any red, there is probably an issue.

Other checks:

1. Visit `https://<your-domain>`.  Ensure that <your-domain> can be served over HTTPS (not unsecured HTTP).  If you have any issues, make sure your vars.yml configuration is correct and `<your-domain>` is successfully pointing to your server's IP address (check https://www.whatsmydns.net/ to confirm).  If this is configured successfully, you should see "Hello from `<your-domain>`!" when `https://<your-domain>` loads.

2. The JSON content on `https://matrix.<your-domain>/.well-known/matrix/server`should be identical to the content on `https://<your-domain>/.well-known/matrix/server`

3. The JSON content on `https://matrix.<your-domain>/.well-known/matrix/client`should be identical to the content on `https://<your-domain>/.well-known/matrix/client`

### 8. Next steps

At this point, if everything is configured successfully, you can explore **Things to do next** from the [Installation docs](https://github.com/spantaleev/matrix-docker-ansible-deploy/blob/master/docs/installing.md), including:

* [Registering your first (admin) user](https://github.com/spantaleev/matrix-docker-ansible-deploy/blob/master/docs/registering-users.md)
* [Setting up additional services (e.g. chat bridges)](https://github.com/spantaleev/matrix-docker-ansible-deploy/blob/master/docs/configuring-playbook.md#other-configuration-options), starting with [Setting up Dimension](https://github.com/spantaleev/matrix-docker-ansible-deploy/blob/master/docs/configuring-playbook-dimension.md)

Once you've registered your first user, if you visit `matrix.<your-domain>` or `element.<your-domain>`, you should be able to sign in and communicate with others in the Matrix universe!

**Usage guidelines:** For performance reasons, avoid joining large Matrix chatrooms from your homeserver account, as this may require more power than your virtual server can offer.  One-to-one conversations and small chat rooms are best.  For more details on this subject, see **What kind of server specs do I need?** at [FAQs](https://github.com/spantaleev/matrix-docker-ansible-deploy/blob/1aec5f9735160f68a58ff0e8e874bab50a1f16e9/docs/faq.md).

You should also now be comfortable and familiar enough with the Ansible playbook and commands to follow [the extensive documentation/options/configurations online](https://github.com/spantaleev/matrix-docker-ansible-deploy/blob/master/docs/configuring-playbook.md).  You can also join/ask questions in the community support room: [#matrix-docker-ansible-deploy:devture.com](https://matrix.to/#/#matrix-docker-ansible-deploy:devture.com)
