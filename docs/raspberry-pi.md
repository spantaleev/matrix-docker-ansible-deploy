# Raspberry Pi

The playbook support for Raspberry Pi is now in beta(ish). The problem is that, docker containers are not architecture independent, and most of them are not build for arm. Some roles have been updated, so they built the necessary image on the host. It needs more space, as some build tools need to be present (like Java, for mxisd).

To use these modification there is a variable that needs to be switched to enable this functionality. Add this to your vars.yaml file:
```
matrix_raspberry_pi = true
```

List of roles that builtds the image:
- synapse
- coturn
- mxisd
- matrix-bridge-mautrix-facebook
- matrix-bridge-mautrix-hangouts

nginx hopefully works as it has an arm image already.
