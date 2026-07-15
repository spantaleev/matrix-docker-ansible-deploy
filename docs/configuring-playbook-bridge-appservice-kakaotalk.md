<!--
SPDX-FileCopyrightText: 2022 Dennis Ciba
SPDX-FileCopyrightText: 2022 - 2026 Slavi Pantaleev
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara
SPDX-FileCopyrightText: 2024 MDAD project contributors

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Setting up Appservice Kakaotalk bridging (optional, removed)

🪦 The playbook used to be able to install and configure [matrix-appservice-kakaotalk](https://src.miscworks.net/fair/matrix-appservice-kakaotalk) (a bridge to [Kakaotalk](https://www.kakaocorp.com/page/service/service/KakaoTalk?lang=ENG)), but no longer includes this component.

The bridge could only be installed by self-building its source code, and its upstream repository has become unreachable, which makes installation impossible. The bridge was also based on the now-unmaintained [node-kakao](https://github.com/storycraft/node-kakao) library, and there have been reports that using it may get your Kakaotalk account banned.

## Uninstalling the component manually

If you still have matrix-appservice-kakaotalk installed on your Matrix server, the playbook can no longer help you uninstall it and you will need to do it manually. To uninstall manually, run these commands on the server:

```sh
systemctl disable --now matrix-appservice-kakaotalk.service

systemctl disable --now matrix-appservice-kakaotalk-node.service

rm -rf /matrix/appservice-kakaotalk
```
