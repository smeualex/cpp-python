# Sample project to call python modules from C++

As a more complex example we'll use Python to make REST calls to HashiCorp's Vault.

## Prerequisites

The following tools\components must be preinstalled:

- CMake
- C++ compiler (MSVC++)
- Python > 3.7 with `requests` module
- Vault
- openssl

Before running the vault server and our client a server certificate must be create.

> Vault will not accept CNs, only SANs !!!

Or you can use the test certificates in this repo found at `/vault/certs`.

## Description

`build.py` will call CMake to build the `python-call.exe` which will import the `vault-client.py` python module and call functions from it.

## Starting the Vault server

1. Call `/bin/vault/vault-start.bat` to start an uninitialized vault server
2. **[Only on first start]** Call `/bin/vault/vault-init.py` to initialize the vault
    > for testing we'll use 1 unseal key
    > The script will save the unseal key and root token in `/bin` in `vault_root_token` and `vault_unseal_key` files
3. The vault should be started and initialized
    > any configuration have to be made using the root_roken

## python-call.exe
Calling the main executable will call the `vault-client.py` script and do some operations on the vault.

## Generate self signed certificates on Linux
Following script worked best:

```bash
#!/bin/bash
ROOT_DIR=/vagrant

export SAN="DNS:localhost,DNS:127.0.0.1"

cat \
    /etc/ssl/openssl.cnf \
    - \
    <<-CONFIG > ./config/localhost.cnf

[ san ]
subjectAltName="${SAN}"
CONFIG

key_location=./certs
key_name=localhost
valid_days=365

openssl req \
    -x509 \
    -sha256 \
    -nodes \
    -newkey rsa:2048 \
    -days  ${valid_days} \
    -reqexts san \
    -extensions san \
    -subj "/CN=mail_or_domain_or_name" \
    -config ./config/localhost.cnf \
    -out ${key_location}/${key_name}.crt \
    -keyout ${key_location}/${key_name}.key


openssl dhparam \
    -out /tmp/dhparams.pem \
    2048

cat /tmp/dhparams.pem \
    >> ${key_location}/${key_name}.crt
```