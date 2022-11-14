---
name: Bug report
about: Create a report to help us improve
title: ''
labels: ''
assignees: ''

---

**Describe the bug**
A clear and concise description of what the bug is.

<!--
NOTE: This Ansible playbook installs tens of separate services. If you're having a problem with a specific service, it is likely that the problem is not with our deployment method, but with the service itself. You may wish to report that problem at the source, upstream, and not to us
-->

**To Reproduce**
My `vars.yml` file looks like this:

```yaml
Paste your vars.yml file here.
Make sure to remove any secret values before posting your vars.yml file publicly.
```

<!-- Below this line, tell us what you're doing to reproduce the problem. -->


**Expected behavior**
A clear and concise description of what you expected to happen.

**Matrix Server:**
 - OS: [e.g. Ubuntu 21.04]
 - Architecture [e.g. amd64, arm32, arm64]

**Ansible:**
If your problem appears to be with Ansible, tell us:
- where you run Ansible -- e.g. on the Matrix server itself; on another computer (which OS? distro? standard installation or containerized Ansible?)
- what version of Ansible you're running (see `ansible --version`)

<!--
The above is only applicable if you're hitting a problem with Ansible itself.
We don't need this information in most cases. Delete this section if not applicable.
-->

**Client:**
 - Device: [e.g. iPhone6]
 - OS: [e.g. iOS8.1]
 - Browser [e.g. stock browser, safari]
 - Version [e.g. 22]

<!--
The above is only applicable if you're hitting a problem with a specific device, but not with others.
We don't need this information in most cases. Delete this section if not applicable.
-->

**Additional context**
Add any other context about the problem here.
