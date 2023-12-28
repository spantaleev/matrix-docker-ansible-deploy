# 2022

For [matrix-docker-ansible-deploy](https://github.com/spantaleev/matrix-docker-ansible-deploy/), 2022 started with **breaking the** [**Synapse**](https://github.com/matrix-org/synapse) **monopoly** by [adding support](https://github.com/spantaleev/matrix-docker-ansible-deploy/blob/ba09705f7fbaf0108652ecbe209793b1d935eba7/CHANGELOG.md#dendrite-support) for the [Dendrite](https://github.com/matrix-org/dendrite) Matrix homeserver in early January. This required various internal changes so that the [Ansible](https://www.ansible.com/) playbook would not be Synapse-centric anymore. This groundwork paved the way for continuing in this direction and we [added support](https://github.com/spantaleev/matrix-docker-ansible-deploy/blob/ba09705f7fbaf0108652ecbe209793b1d935eba7/CHANGELOG.md#conduit-support) for [Conduit](https://conduit.rs/) in August.

When it comes to the `matrix-docker-ansible-deploy` Ansible playbook, 2022 was the year of the non-Synapse homeserver implementation. In practice, none of these homeserver implementations seem ready for prime-time yet and there is no migration path when coming from Synapse. Having done our job of adding support for these alternative homeserver implementations, we can say that we're not getting in the way of future progress. It's time for the Dendrite developers to push harder (development-wise) and for the Synapse developers to take a well-deserved long (infinite) break, and we may get to see more people migrating away from Synapse in the next year(s).

Support for the following new **bridges** was added:

*   [Postmoogle](https://github.com/spantaleev/matrix-docker-ansible-deploy/blob/ba09705f7fbaf0108652ecbe209793b1d935eba7/CHANGELOG.md#postmoogle-email-bridge-support) for bi-directional email bridging, which supersedes my old and simplistic [email2matrix](https://github.com/devture/email2matrix) one-way bridge-bot
*   [mautrix-discord](https://github.com/spantaleev/matrix-docker-ansible-deploy/blob/ba09705f7fbaf0108652ecbe209793b1d935eba7/CHANGELOG.md#mautrix-discord-support)
*   [go-skype-bridge](https://github.com/spantaleev/matrix-docker-ansible-deploy/blob/ba09705f7fbaf0108652ecbe209793b1d935eba7/CHANGELOG.md#go-skype-bridge-bridging-support)
*   [matrix-appservice-kakaotalk](https://github.com/spantaleev/matrix-docker-ansible-deploy/blob/ba09705f7fbaf0108652ecbe209793b1d935eba7/CHANGELOG.md#matrix-appservice-kakaotalk-support)

Support for the following new **bots** was added:

*   [buscarron bot](https://github.com/spantaleev/matrix-docker-ansible-deploy/blob/ba09705f7fbaf0108652ecbe209793b1d935eba7/CHANGELOG.md#buscarron-bot-support)
*   [Honoroit bot](https://github.com/spantaleev/matrix-docker-ansible-deploy/blob/ba09705f7fbaf0108652ecbe209793b1d935eba7/CHANGELOG.md#honoroit-bot-support)
*   [matrix-registration-bot](https://github.com/spantaleev/matrix-docker-ansible-deploy/blob/ba09705f7fbaf0108652ecbe209793b1d935eba7/CHANGELOG.md#matrix-registration-bot-support)
*   [matrix-hookshot](https://github.com/spantaleev/matrix-docker-ansible-deploy/blob/ba09705f7fbaf0108652ecbe209793b1d935eba7/CHANGELOG.md#matrix-hookshot-bridging-support)
*   [maubot](https://github.com/spantaleev/matrix-docker-ansible-deploy/blob/ba09705f7fbaf0108652ecbe209793b1d935eba7/CHANGELOG.md#maubot-support)

Support for the following new **components and services** was added:

*   [Borg backup](https://github.com/spantaleev/matrix-docker-ansible-deploy/blob/ba09705f7fbaf0108652ecbe209793b1d935eba7/CHANGELOG.md#borg-backup-support)
*   [Cactus Comments](https://github.com/spantaleev/matrix-docker-ansible-deploy/blob/ba09705f7fbaf0108652ecbe209793b1d935eba7/CHANGELOG.md#cactus-comments-support)
*   [Cinny](https://github.com/spantaleev/matrix-docker-ansible-deploy/blob/ba09705f7fbaf0108652ecbe209793b1d935eba7/CHANGELOG.md#cinny-support) client support
*   [ntfy](https://github.com/spantaleev/matrix-docker-ansible-deploy/blob/ba09705f7fbaf0108652ecbe209793b1d935eba7/CHANGELOG.md#ntfy-push-notifications-support) notifications
*   [matrix-ldap-registration-proxy](https://github.com/spantaleev/matrix-docker-ansible-deploy/blob/ba09705f7fbaf0108652ecbe209793b1d935eba7/CHANGELOG.md#matrix-ldap-registration-proxy-support)
*   [matrix\_encryption\_disabler support](https://github.com/spantaleev/matrix-docker-ansible-deploy/blob/ba09705f7fbaf0108652ecbe209793b1d935eba7/CHANGELOG.md#matrix_encryption_disabler-support)
*   [synapse-s3-storage-provider](https://github.com/spantaleev/matrix-docker-ansible-deploy/blob/ba09705f7fbaf0108652ecbe209793b1d935eba7/CHANGELOG.md#synapse-s3-storage-provider-support) to stop the Synapse media store from being a scalability problem. This brought along [another feature](https://github.com/spantaleev/matrix-docker-ansible-deploy/blob/ba09705f7fbaf0108652ecbe209793b1d935eba7/CHANGELOG.md#synapse-container-image-customization-support) - an easier way to customize the Synapse container image without having to fork and self-build all of it from scratch

Besides these major user-visible changes, a lot of work also happened **under the hood**:

*   we made [major improvements to Synapse workers](https://github.com/spantaleev/matrix-docker-ansible-deploy/blob/ba09705f7fbaf0108652ecbe209793b1d935eba7/CHANGELOG.md#potential-backward-compatibility-break-major-improvements-to-synapse-workers) - adding support for stream writers and for running multiple workers of various kinds (federation senders, pushers, background task processing workers, etc.)
*   we [improved the compatibility of (Synapse + workers) with the rest of the playbook](https://github.com/spantaleev/matrix-docker-ansible-deploy/blob/ba09705f7fbaf0108652ecbe209793b1d935eba7/CHANGELOG.md#backward-compatibility-break-changing-how-reverse-proxying-to-synapse-works---now-via-a-matrix-synapse-reverse-proxy-companion-service) by introducing a new `matrix-synapse-reverse-proxy-companion-service` service
*   we started [splitting various Ansible roles out of the Matrix playbook and into independent roles](https://github.com/spantaleev/matrix-docker-ansible-deploy/blob/ba09705f7fbaf0108652ecbe209793b1d935eba7/CHANGELOG.md#the-playbook-now-uses-external-roles-for-some-things) (e.g. `matrix-postgres` -> [com.devture.ansible.role.postgres](https://github.com/devture/com.devture.ansible.role.postgres)), which could be included in other Ansible playbooks. In fact, these roles already power a few **interesting other sibling playbooks**:
    *   [gitea-docker-ansible-deploy](https://github.com/spantaleev/gitea-docker-ansible-deploy), for deploying a [Gitea](https://gitea.io/) (self-hosted [Git](https://git-scm.com/) service) server
    *   [nextcloud-docker-ansible-deploy](https://github.com/spantaleev/nextcloud-docker-ansible-deploy), for deploying a [Nextcloud](https://nextcloud.com/) groupware server
    *   [vaultwarden-docker-ansible-deploy](https://github.com/spantaleev/vaultwarden-docker-ansible-deploy), for deploying a [Vaultwarden](https://github.com/dani-garcia/vaultwarden) password manager server (unofficial [Bitwarden](https://bitwarden.com/) compatible server)

These sibling playbooks co-exist nicely with one another due to using [Traefik](https://traefik.io/) for reverse-proxying, instead of trying to overtake the whole server by running their own [nginx](https://nginx.org/) reverse-proxy. Hopefully soon, the Matrix playbook will follow suit and be powered by Traefik by default.

Last, but not least, to optimize our [etke.cc managed Matrix hosting service](https://etke.cc/)'s performance (but also individual Ansible playbook runs for people self-hosting by themselves using the playbook), we've [improved playbook runtime 2-5x](https://github.com/spantaleev/matrix-docker-ansible-deploy/blob/ba09705f7fbaf0108652ecbe209793b1d935eba7/CHANGELOG.md#2x-5x-performance-improvements-in-playbook-runtime) by employing various Ansible tricks.
