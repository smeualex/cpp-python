import os
import sys
import errno
import logging
import datetime
import subprocess

from os import path

from VaultHttpClient import VaultHttpClient

log = logging.getLogger("vault-client")


class Vault:
    def __init__(self, vault_client):
        self.cli = vault_client

    def seal(self):
        self.cli.seal()

    def unseal(self):
        self.cli.unseal()

    def unsealIfSealed(self):
        # get vault sealed info
        response = self.cli.get("/sys/health")
        # unseal it if it's sealed
        if(response["sealed"]):
            log.info('Vault is sealed. Unsealing the vault')
            self.cli.unseal()

    def listVaultUsers(self):
        response = self.cli.list_vault_users()
        log.info("Found users: ")
        users = response['data']['keys']
        for user in users:
            log.info('     {}'.format(user))

    def createToken(self, username, email, comment='', valid_time='1h', policies=[], renewable=False, log_response=False):
        # build the meta dictionary
        meta = { 'user': username, 'email': email }
        if len(comment) > 0:
            meta['comment'] = comment

        response = self.cli.create_token(meta, valid_time, policies, renewable)
         
        if log_response:
            log.debug('----------------------------------------------------------')
            log.debug('Created a token: ')
            log.debug('     - token policies: {}'.format(response["auth"]["token_policies"]))
            log.debug('     - token:          {}'.format(response["auth"]["client_token"]))
            log.debug('     - accessor:       {}'.format(response["auth"]["accessor"]))
            log.debug('     - metadata:       {}'.format(response["auth"]["metadata"]))
            log.debug('     - duration:       {}'.format(response["auth"]["lease_duration"]))
            log.debug('     - renewable:      {}'.format(response["auth"]["renewable"]))
            log.debug('     - token_type:     {}'.format(response["auth"]["token_type"]))
            log.debug('     - orphan:         {}'.format(response["auth"]["orphan"]))
            log.debug('----------------------------------------------------------')

        return response

    def renew_self_token(self, token, renew_time='10m'):
        payload = { 'increment': renew_time }
        auth_header = { 'X-Vault-Token': token }
        return self.cli.post('/auth/token/renew-self', auth_header, payload)

def get_vault_server_certificate():
    if not path.exists("server_cert.pem"):
        log.info('  >> server certificate not found; invoking openssl client to get it')
        openssl_cmd = ['get_server_cert.bat']
        retCode = subprocess.check_call(openssl_cmd, stderr=subprocess.STDOUT, shell=True)
    else:
        log.info('  >> server certificate found')

def init():
    # set up logging
    now = datetime.datetime.now()
    str_now = now.strftime('%Y%m%d_%H%M%S')

    log_file_name = 'vault-.log'
    cwd = os.path.dirname(os.path.realpath(__file__))
    try:
        os.makedirs('logs')
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    log_file = os.path.join(cwd, 'logs', log_file_name)
    logging.basicConfig(
            handlers=[
                logging.FileHandler(log_file, 'w', 'utf-8'),                    # log to file
                logging.StreamHandler(sys.stdout)],                             # log to console
            level=logging.DEBUG,
            format='%(asctime)s | %(levelname)5.5s | %(name)10s | %(message)s')

    get_vault_server_certificate()

    # we are going
    log.info('')
    log.info('-' * 80)
    log.info('-- Program started')

def basic_vault_test():
    vault_http_client = VaultHttpClient()
    # our main object for interacting with vault
    v=Vault(vault_http_client)
    v.unsealIfSealed()
    # user auth needs to be enabled first
    # v.listVaultUsers()
    # create a renewable token valid for 1m
    response = v.createToken("Python-test", "somemail@mail.com", 'This is a token', 
                             valid_time="1m", renewable=True, log_response=True)
    if response['auth']['renewable']:
        my_token = response['auth']['client_token']
        v.renew_self_token(my_token, '2m')

if __name__ == "__main__":
    # global initialization - logging and other stuff
    init()
    # vault http interface
    basic_vault_test()