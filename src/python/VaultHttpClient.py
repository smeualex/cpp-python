import json
import logging
import requests
from http import HTTPStatus

log = logging.getLogger("VaultHttpClient")

class VaultHttpClient:
    def __read_root_token(self, file_name):
        key = ''
        with open(file_name, 'r') as f:
            key = f.readline()
        return key

    def __init__(self):
        self.host      = "localhost"
        self.port      = "8200"
        self.apiV      = "v1"
        self.__cert      = "./server_cert.pem"
        self.__baseUrl   = "https://" + self.host + ":" + self.port + "/" + self.apiV
        
        self.__unsealKey = self.__read_root_token('vault_unseal_keys')
        self.__rootToken = self.__read_root_token('vault_root_token')

        log.info('unseal key: {}'.format(self.__unsealKey))
        log.info('root token: {}'.format(self.__rootToken))

    def get(self, endpoint, headers={}, json_payload={}):
        return self.__perform_request('GET', endpoint, headers, json_payload)

    def list(self, endpoint, headers={}, json_payload={}):
        return self.__perform_request('LIST', endpoint, headers, json_payload)

    def put(self, endpoint, headers={}, json_payload={}):
        return self.__perform_request('PUT', endpoint, headers, json_payload)

    def post(self, endpoint, headers={}, json_payload={}):
        return self.__perform_request('POST', endpoint, headers, json_payload)


    def seal(self):
        return self.put("/sys/seal", self.__get_vault_auth_header())

    def unseal(self):
        return self.put("/sys/unseal", json_payload={ "key": self.__unsealKey })

    def list_vault_users(self):
        return self.list("/auth/userpass/users", self.__get_vault_auth_header())

    def create_token(self, meta={}, valid_time='1h', policies=[], renewable=False):
        payload = {
            'meta': meta,
            'ttl': valid_time,
            'renewable': renewable
        }
        if len(policies) > 0:
            payload['policies'] = policies

        return self.post("/auth/token/create", headers=self.__get_vault_auth_header(), json_payload=payload) 

    def __vault_response_is_ok(self, response):
        is_content_type_ok=True
        if 'Content-Type' in response.headers:
            is_content_type_ok = (response.headers['Content-Type']=='application/json')
        return ( 
            response.status_code != HTTPStatus.NO_CONTENT and 
            is_content_type_ok == True and
            len(response.text) > 0
        )

    def __perform_request(self, http_method, endpoint, headers, json_payload):
       try:
           response = requests.request(http_method, 
                                       self.__baseUrl + endpoint,
                                       headers=headers,
                                       json=json_payload,
                                       verify=self.__cert)
           self.__log_response(response)
           if self.__vault_response_is_ok(response):
               # check response status and if we actually have json
               jsonObj = response.json()
               print("     Response: ")
               print(json.dumps(jsonObj, indent=2))
               return jsonObj
           
           return {}
       except requests.exceptions.Timeout as e:
           # Maybe set up for a retry, or continue in a retry loop
           print("Timeout")
           print(e)
       except requests.exceptions.TooManyRedirects as e:
           # Tell the user their URL was bad and try a different one
           print("Too many redirects")
           print(e)
       except requests.exceptions.RequestException as e:
           print("Fatal exception")
           print(e)
       except IOError as e:
           print("Fatal exception")
           print(e)
           # catastrophic error. bail.
           # raise SystemExit(e)

    def __log_response(self, response):
        log.debug('----------------------------------------------------------')
        log.debug(' << Response')
        log.debug('     Status Code: {}'.format(response.status_code))
        if(len(response.headers) > 0):
            log.debug('     Headers: ')
            for header in response.headers.items():
                log.debug('         {}'.format(header))
        
        log.debug('     Text response: ')
        log.debug('')
        if(response.status_code == HTTPStatus.NO_CONTENT):
            log.debug('     empty response')
        else:
            log.debug('     {}'.format(response.text))
        log.debug('----------------------------------------------------------')

    def __get_root_token(self):
        return self.__rootToken

    def __get_vault_auth_header(self):
        return { 'X-Vault-Token' : self.__get_root_token() }