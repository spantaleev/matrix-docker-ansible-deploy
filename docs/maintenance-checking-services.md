# Checking if services work

This playbook can perform a check to ensure that you've configured things correctly and that services are running.

To perform the check, run:

```bash
ansible-playbook -i inventory/hosts setup.yml --tags=self-check
```

If it's all green, everything is probably running correctly.

Besides this self-check, you can also check your server using the [Federation Tester](https://federationtester.matrix.org/).
