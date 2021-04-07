@echo off

set VAULT_HOST=localhost
set VAULT_ADDR=https://%VAULT_HOST%:8200
set VAULT_CACERT=./certs/localhost.crt

rem Init the vault with 1 key and a threshold of 1 (for testing purposes)
vault operator init -key-shares=1 -key-threshold=1