#!/bin/bash

# SPDX-FileCopyrightText: 2024 Slavi Pantaleev
#
# SPDX-License-Identifier: AGPL-3.0-or-later

set -euxo pipefail

# This script rebuilds the mautrix-meta-instagram Ansible role, using the mautrix-meta-messenger role as a source.

if [ $# -eq 0 ]; then
	echo "Error: No argument supplied. Please provide the path to the roles/custom directory."
	exit 1
fi

roles_path=$1

messenger_role_path=$roles_path/matrix-bridge-mautrix-meta-messenger
instagram_role_path=$roles_path/matrix-bridge-mautrix-meta-instagram

if [ ! -d $messenger_role_path ]; then
	echo "Cannot find: $messenger_role_path"
	exit 1
fi

if [ -d $instagram_role_path ]; then
	rm -rf $instagram_role_path
fi

cp -ar $messenger_role_path $instagram_role_path

find "$instagram_role_path" -type f | while read -r file; do
	sed --in-place 's/matrix_mautrix_meta_messenger_/matrix_mautrix_meta_instagram_/g' "$file"
	sed --in-place 's/mautrix-meta-messenger/mautrix-meta-instagram/g' "$file"
done

sed --in-place 's/matrix_mautrix_meta_instagram_meta_mode: \(.*\)/matrix_mautrix_meta_instagram_meta_mode: instagram/g' $instagram_role_path/defaults/main.yml
sed --in-place 's/matrix_mautrix_meta_instagram_identifier: \(.*\)/matrix_mautrix_meta_instagram_identifier: matrix-mautrix-meta-instagram/g' $instagram_role_path/defaults/main.yml

# Create the README.md file with the license header
cat > $instagram_role_path/README.md << 'EOF'
<!--
SPDX-FileCopyrightText: 2024 - 2025 MDAD Contributors

SPDX-License-Identifier: AGPL-3.0-or-later
-->
EOF

echo "" >> $instagram_role_path/README.md
echo "# matrix-mautrix-meta-instagram" >> $instagram_role_path/README.md
echo "" >> $instagram_role_path/README.md
echo "This bridge role is derived from the matrix-mautrix-meta-messenger Ansible role via automatic changes (see \`just rebuild-mautrix-meta-instagram\` or \`bin/rebuild-mautrix-meta-instagram.sh\`)." >> $instagram_role_path/README.md
echo "" >> $instagram_role_path/README.md
echo "If you'd like to make a change to this role, consider making it to the \`matrix-mautrix-meta-messenger\` role instead." >> $instagram_role_path/README.md
