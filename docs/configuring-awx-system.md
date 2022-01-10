# Configuring AWX System (optional)

An AWX setup for managing multiple Matrix servers.

This section is used in an AWX system that can create and manage multiple [Matrix](http://matrix.org/) servers. You can issue members an AWX login to their own 'organisation', which they can use to manage/configure 1 to N servers.

Members can be assigned a server from Digitalocean, or they can connect their own on-premises server. These playbooks are free to use in a commercial context with the 'MemberPress Plus' plugin. They can also be run in a non-commercial context.

The AWX system is arranged into 'members' each with their own 'subscriptions'. After creating a subscription the user enters the 'provision stage' where they defined the URLs they will use, the servers location and whether or not there's already a website at the base domain. They then proceed onto the 'deploy stage' where they can configure their Matrix server.

This system can manage the updates, configuration, import and export, backups and monitoring on its own. It is an extension of the popular deploy script [spantaleev/matrix-docker-ansible-deploy](https://github.com/spantaleev/matrix-docker-ansible-deploy).


## Other Required Playbooks

The following repositories allow you to copy and use this setup:

[Create AWX System](https://gitlab.com/GoMatrixHosting/create-awx-system) - Creates and configures the AWX system for you.

[Ansible Create Delete Subscription Membership](https://gitlab.com/GoMatrixHosting/ansible-create-delete-subscription-membership) - Used by the AWX system to create memberships and subscriptions. Also includes other administrative playbooks for updates, backups and restoring servers.

[Ansible Provision Server](https://gitlab.com/GoMatrixHosting/ansible-provision-server) - Used by AWX members to perform initial configuration of their DigitalOcean or On-Premises server.

[GMHosting External Tools](https://gitlab.com/GoMatrixHosting/gmhosting-external-tools) - Extra tools we run outside of AWX, some of which are experimental.


## Does I need an AWX setup to use this? How do I configure it? 

Yes, you'll need to configure an AWX instance, the [Create AWX System](https://gitlab.com/GoMatrixHosting/create-awx-system) repository makes it easy to do. Just follow the steps listed in ['/docs/Installation_AWX.md' of that repository](https://gitlab.com/GoMatrixHosting/create-awx-system/-/blob/master/docs/Installation_AWX.md). 

For simpler installation steps you can use to get started with this system, check out our minimal installation guide at ['/doc/Installation_Minimal_AWX.md of that repository'](https://gitlab.com/GoMatrixHosting/create-awx-system/-/blob/master/docs/Installation_Minimal_AWX.md).


## Does I need a front-end WordPress site? And a DigitalOcean account? 

You do not need a front-end WordPress site or the MemberPress plugin to use this setup. It can be run on it's own in a non-commercial context.

You also don't need a DigitalOcean account, although this will limit you to only being able to connect 'On-Premises' servers.
