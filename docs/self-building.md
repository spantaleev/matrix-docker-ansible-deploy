# Self-building

**Caution: self-building does not have to be used on its own. See the [Alternative Architectures](alternative-architectures.md) page.**

The playbook supports the self-building of some of its components. This may be useful for architectures besides x86_64, which have no Docker images right now (e g. the armv7 for the Raspberry Pi). Some playbook roles have been updated, so they build the necessary image on the host. It needs more space, as some build tools need to be present (like Java, for ma1sd).

To use these modification there is a variable that needs to be switched to enable this functionality. Add this to your `vars.yaml` file:
```yaml
matrix_container_images_self_build: true
```
Setting that variable will self-build every role which supports self-building. Self-building can be set on a per-role basis as well.

List of roles where self-building the Docker image is currently possible:
- `matrix-synapse`
- `matrix-riot-web`
- `matrix-coturn`
- `matrix-ma1sd`
- `matrix-mautrix-facebook`
- `matrix-mautrix-hangouts`
- `matrix-mx-puppet-skype`

Adding self-building support to other roles is welcome. Feel free to contribute!
