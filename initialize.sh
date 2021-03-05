#!/bin/bash

# clear out old variables if they exist
if test -f ./vars.yml*; then
  rm ./vars.yml*
fi
if test -f ./hosts*; then
  rm ./hosts*
fi
rm -rf inventory/host_vars/*
if test -f inventory/hosts*; then
  rm inventory/hosts*
fi

# prompt the user for basic info
read -p "Enter the base domain (e.g. example.com): " domain
read -p "Enter the external IP address: " address

# initialize vars.yml
mkdir inventory/host_vars/matrix.$domain
cp examples/vars.yml inventory/host_vars/matrix.$domain/vars.yml
sed -i "s/matrix_domain: YOUR_BARE_DOMAIN_NAME_HERE/matrix_domain: $domain/" inventory/host_vars/matrix.$domain/vars.yml

read -p "Enable automatic SSL certificate management? (y/n): " cert

if [[ $cert == "n" || $cert == "N" ]]
then
  sed -i "s/matrix_ssl_lets_encrypt_support_email: ''/matrix_ssl_retrieval_method: /" inventory/host_vars/matrix.$domain/vars.yml
else
  read -p "Provide an email for contact from Let's Encrypt: " email
  sed -i "s/matrix_ssl_lets_encrypt_support_email: '/matrix_ssl_lets_encrypt_support_email: \'$email/" inventory/host_vars/matrix.$domain/vars.yml
fi

pw=$(openssl rand -hex 64)
sed -i "s/matrix_coturn_turn_static_auth_secret: '/matrix_coturn_turn_static_auth_secret: \'$pw/" inventory/host_vars/matrix.$domain/vars.yml
pw=$(openssl rand -hex 64)
sed -i "s/matrix_synapse_macaroon_secret_key: '/matrix_synapse_macaroon_secret_key: \'$pw/" inventory/host_vars/matrix.$domain/vars.yml
pw=$(openssl rand -hex 64)
sed -i "s/matrix_postgres_connection_password: '/matrix_postgres_connection_password: \'$pw/" inventory/host_vars/matrix.$domain/vars.yml

# initialize hosts
cp examples/hosts inventory/hosts
sed -i "s/matrix.<your-domain> ansible_host=<your-server's external IP address>/matrix.$domain ansible_host=$address/" inventory/hosts

read -p "Are you running this Ansible playbook on the same server as the one you're installing to? (y/n): " same

if [[ $same == "y" || $same == "Y" ]]
then
  sed -i "s/ansible_ssh_user=root/ansible_ssh_user=root ansible_connection=local/" inventory/hosts
fi

# create symbolic links to make the config files more accessible
ln -s inventory/host_vars/matrix.$domain/vars.yml .
ln -s inventory/hosts .

echo "The files 'vars.yml' and 'hosts' are ready to be configured."
