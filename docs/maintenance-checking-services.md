# Checking if services work

The playbook can perform a check to ensure that you've configured things correctly and that services are running.

To perform the check, run:

```sh
ansible-playbook -i inventory/hosts setup.yml --tags=self-check
```

The shortcut command with `just` program is also available: `just run-tags self-check`

If it's all green, everything is probably running correctly.

Besides this self-check, you can also check whether your server federates with the Matrix network by using the [Federation Tester](https://federationtester.matrix.org/) against your base domain (`example.com`), not the `matrix.example.com` subdomain.
