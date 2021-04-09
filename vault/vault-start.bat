pushd %~dp0
    set SCRIPT_PATH=%CD%
    vault server -config ./vault-server-config.hcl
popd