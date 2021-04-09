import os
import subprocess

VAULT_HOST='localhost'
VAULT_ADDR='https://' + VAULT_HOST + ':8200'
VAULT_CERT='./certs/localhost.crt'

VAULT_KEY_SHARES=1
VAULT_KEY_THRESH=1

def vault_init():
    vault_cmd = [
        'vault',
        'operator', 'init',
        '-key-shares='      + str(VAULT_KEY_SHARES),
        '-key-threshold='    + str(VAULT_KEY_THRESH)
    ]

    root_token = ''
    unseal_keys = []

    try:
        print('vault-ini.py | INFO  | Executing command: ', ' '.join(vault_cmd))

        output = subprocess.check_output(vault_cmd, stderr=subprocess.STDOUT, shell=True)
        
        for line in output.splitlines():
            line = line.decode('UTF-8')
            print('     > ', line)

            if 'Unseal Key' in line:
                separator_pos = line.index(':')
                unseal_keys.append(line[separator_pos + 2 : ])

            if 'Initial Root Token' in line:
                separator_pos = line.index(':')
                root_token = line[separator_pos + 2 : ]

        for key in unseal_keys:
            print('vault-ini.py | INFO  | unseal key: ', key)
        print('vault-ini.py | INFO  | root token: ', root_token)

    except subprocess.CalledProcessError as e:
        print('vault-ini.py | ERROR | ', e)
        
    return root_token, unseal_keys

def save_vault_keys(root_token, unseal_keys):
     with open('../vault_root_token', 'w') as f:
         f.write(root_token)

     with open('../vault_unseal_keys', 'w') as f:
         for key in unseal_keys:
             f.write(key)

if __name__ == "__main__":
    print('---------------------------------------------------------------------')
    root_token, unseal_keys = vault_init()
    save_vault_keys(root_token, unseal_keys)
    print('---------------------------------------------------------------------')