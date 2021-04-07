@echo off

set VAULT_HOST=192.168.50.110
set VAULT_ADDR=https://%VAULT_HOST%:8200
set VAULT_CACERT=./certs/localhost_san.crt

rem Init the vault with 1 key and a threshold of 1 (for testing purposes)
vault operator init -key-shares=1 -key-threshold=1

rem OR
rem curl --request PUT --data @payloads/init-1-1.json https://localhost:8200/v1/sys/init