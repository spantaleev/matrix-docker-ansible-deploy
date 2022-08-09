#!/usr/bin/env bash
# This is a bash script for generating strong passwords for the Jitsi role in this ansible project:
# https://github.com/spantaleev/matrix-docker-ansible-deploy

function generatePassword() {
    openssl rand -hex 16
}

echo "# If this script fails, it's likely because you don't have the openssl tool installed."
echo "# Install it before using this script, or simply create your own passwords manually."

echo ""

JICOFO_AUTH_PASSWORD=$(generatePassword)
JVB_AUTH_PASSWORD=$(generatePassword)
JIBRI_RECORDER_PASSWORD=$(generatePassword)
JIBRI_XMPP_PASSWORD=$(generatePassword)

echo "# Paste these variables into your inventory/host_vars/matrix.DOMAIN/vars.yml file:"
echo ""
echo "matrix_jitsi_jicofo_auth_password: $JICOFO_AUTH_PASSWORD"
echo "matrix_jitsi_jvb_auth_password: $JVB_AUTH_PASSWORD"
echo "matrix_jitsi_jibri_recorder_password: $JIBRI_RECORDER_PASSWORD"
echo "matrix_jitsi_jibri_xmpp_password: $JIBRI_XMPP_PASSWORD"
