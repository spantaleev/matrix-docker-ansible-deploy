<!--
SPDX-FileCopyrightText: 2020 - 2025 Slavi Pantaleev
SPDX-FileCopyrightText: 2020 Horvath Gergely
SPDX-FileCopyrightText: 2020 Marcel Partap
SPDX-FileCopyrightText: 2021 - 2022 MDAD project contributors
SPDX-FileCopyrightText: 2021 Aaron Raimist
SPDX-FileCopyrightText: 2021 Panagiotis Georgiadis
SPDX-FileCopyrightText: 2022 Arthur Brugière
SPDX-FileCopyrightText: 2023 Shreyas Ajjarapu
SPDX-FileCopyrightText: 2024 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Self-building

**Caution: self-building does not have to be used on its own. See the [Alternative Architectures](alternative-architectures.md) page.**

The playbook supports self-building of various components, which don't have a container image for your architecture (see the [container images we use](container-images.md)). For `amd64`, self-building is not required.

For other architectures (e.g. `arm32`, `arm64`), ready-made container images are used when available. If there's no ready-made image for a specific component and said component supports self-building, an image will be built on the host. Building images like this takes more time and resources (some build tools need to get installed by the playbook to assist building).

To make use of self-building, you don't need to do anything. If a component has an image for the specified architecture, the playbook will use it directly. If not, it will build the image on the server itself.

Note that **not all components support self-building yet**.

Possibly outdated list of roles where self-building the Docker image is currently possible:
- `matrix-synapse`
- `matrix-synapse-admin`
- `matrix-client-element`
- `matrix-client-hydrogen`
- `matrix-client-cinny`
- `matrix-registration`
- `matrix-coturn`
- `matrix-corporal`
- `matrix-dimension`
- `matrix-ma1sd`
- `exim-relay`
- `matrix-bridge-hookshot`
- `matrix-bridge-appservice-irc`
- `matrix-bridge-appservice-slack`
- `matrix-bridge-beeper-linkedin`
- `matrix-bridge-mautrix-googlechat`
- `matrix-bridge-mautrix-telegram`
- `matrix-bridge-mautrix-signal`
- `matrix-bridge-mautrix-gmessages`
- `matrix-bridge-mautrix-whatsapp`
- `matrix-bridge-mx-puppet-steam`
- `matrix-bot-mjolnir`
- `matrix-bot-honoroit`
- `matrix-bot-matrix-reminder-bot`
- `matrix-bot-maubot`
- `matrix-pantalaimon`

Adding self-building support to other roles is welcome. Feel free to contribute!

If you'd like **to force self-building** even if an image is available for your architecture, look into the `matrix_*_self_build` variables provided by individual roles.
