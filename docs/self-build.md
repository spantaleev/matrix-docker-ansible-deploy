# Self building

The playbook supports the self building of a couple of components. This may be useful for architectures beside x86_64 that have no docker images right now (e g. the armv7 for the Raspberry Pi). Some roles have been updated, so they build the necessary image on the host. It needs more space, as some build tools need to be present (like Java, for mxisd).

To use these modification there is a variable that needs to be switched to enable this functionality. Add this to your vars.yaml file:
```
matrix_container_images_self_build = true
```
Setting that variable will self-build every role where applicable. Self-building can be set on a per-role basis as well.

List of roles where self-building the docker image is currently possible:
- synapse
- riot-web
- coturn
- mxisd
- matrix-bridge-mautrix-facebook
- matrix-bridge-mautrix-hangouts
