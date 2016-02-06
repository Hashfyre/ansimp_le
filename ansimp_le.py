#!/usr/bin/env python

import sys
import logging

sys.path.append('./simp_le')
try:
    from simp_le import main as simp_le
except ImportError:
    raise ImportError('[ERROR] Module simp_le could not be imported.')

DOCUMENTATION = '''
---
module: ansimp_le
short_description: A simple Let's Encrypt Ansible Module.
version_added: "0.0";
author: Joy Bhattacherjee
email: joy.bhattacherjee@gmail.com
github: https://github.com/Hashfyre
notes:
    - This module is in Planning stage.
requirements:
description:
    - An Ansible Wrapper module over simp_le, a simple Let's Encrypt Client.
    - Webroot Manager
        - This client is just a sophisticated manager for:
            - $webroot/.well-known/acme-challenge
        - You can (optionally) specify 'default_root' option or,
        - override per-vhost with domain option
            - 'example.com:/var/www/other_html' syntax.
    - Registration
        - This client will automatically register an account with the ACME CA
          specified by 'server' option.
options:
    domains:
        description:
            - Domain name that will be included in the certificate.
            - Must be specified at least once.
        default: None
        required: false
        version_added: Not Added
    default_root:
        description:
            - Default webroot path
        default: None
        required: true
        version_added: Not Added
    plugins:
        description:
            - Input/output plugin of choice.
            - Can be specified multiple times.
            - Should be specified as many times as it is necessary
              to cover all components
        default: []
        reuired: true
        choices:
            - [ account_key.json', 'cert.der', 'cert.pem',
              'chain.pem', 'external.sh', 'full.pem',
              'fullchain.pem', 'key.der', 'key.pem' ]
        version_added: Not Added
    cert_key_size:
        description:
            - Certificate key size in BITS.
            - Fresh key is created for each renewal.
        default: 4096
        required: false
        version_added: Not Added
    valid_min:
        description:
            - Minimum validity of the resulting certificate.
        default: 2592000
        required: false
        version_added: Not Added
    reuse_key:
        description:
            - Reuse private key if it was previously persisted.
        default: False
        required: false
        choices: [ 'True', 'False' ]
        version_added: Not Added
    account_key_public_exponent:
        description:
            - Account key public exponent value in BITS.
        default: 65537
        required: false
        version_added: Not Added
    account_key_size:
        description:
            - Account key size in BITS.
        default: 4096
        required: false
        version_added: Not Added
    tos_SHA256:
        description:
            - SHA-256 hash of the contents of Terms Of Service URI contents.
        default:
            - 33d233c8ab558ba6c8ebc370a509acdded8b80e5d587aa5d192193f35226540f
        required: false
        version_added: Not Added
    email:
        description:
            - Email address
            - CA is likely to use it for
                - Certificate Expiry Reminder
                - Account Recovery
            - Highly recommended to set this value.
        default: None
        required: false
        version_added: Not Added
    user_agent:
        description:
            - User-Agent sent in all HTTP requests
            - Privacy Protection
                - Override with user_agent: ""
        default: simp_le/0
        required: false
        version_added: Not Added
    server:
        description:
            - Directory URI for the CA ACME API endpoint
        default: https://acme-v01.api.letsencrypt.org/directory
        required: false
        version_added: Not Added
    revoke:
        description:
            - Revoke existing certificate
        default: 'False'
        required: false
        choices: [ 'True', 'False' ]
        version_added: Not Added
'''

EXAMPLES = '''
- name: Get LE Certificate for a NginX Server
  ansimp_le:
    email: you@example.com
    domains: '{{ item[0] }}'
    plugins: '{{ item[1] }}'
    default_root: "/var/www/html"
 with_items:
    - [ 'example.com', 'www.example.com', 'example.net:/var/www/other_html']
    - [ 'fullchain.pem', 'key.pem' ]

 Returns: ssl_certificate_key, ssl_certificate

- name: Get LE Certificate for an Apache >= 2.4.8 Server
  ansimp_le:
    email: you@example.com
    domains: '{{ item[0] }}'
    plugins: '{{ item[1] }}'
    default_root: "/var/www/html"
 with_items:
    - [ 'example.com', 'www.example.com', 'example.net:/var/www/other_html']
    - [ 'fullchain.pem', 'key.pem' ]

 Returns: SSLCertificateKeyFile, SSLCertificateFile

- name: Get LE Certificate for an Apache < 2.4.8 Server
  ansimp_le:
    email: you@example.com
    domains: '{{ item[0] }}'
    plugins: '{{ item[1] }}'
    default_root: "/var/www/html"
 with_items:
    - [ 'example.com', 'www.example.com', 'example.net:/var/www/other_html']
    - [ 'cert.pem', 'fullchain.pem', 'key.pem' ]

 Returns: SSLCertificateKeyFile, SSLCertificateFile, SSLCertificateChainFile
'''

RETURN = '''
SSL Certificate:
'''


def main():
    module = AnsibleModule(
                argument_spec=dict(
                    domain=dict(default='None', required=False),
                    default_root=dict(default='None', required=False),
                    plugins=dict(default=[], required=False, choices=[
                                'account_key.json', 'cert.der', 'cert.pem',
                                'chain.pem', 'external.sh', 'full.pem',
                                'fullchain.pem', 'key.der', 'key.pem'
                                 ]),
                    cert_key_size=dict(default='4096', required=False),
                    valid_min=dict(default='2592000', require=False),
                    reuse_key=dict(default='False', required=False, choices=[
                                    'True',
                                    'False']),
                    account_key_public_exponent=dict(default='65537', required=False),
                    account_key_size=dict(default='4096', required=False),
                    tos_SHA256=dict(default='33d233c8ab558ba6c8ebc370a509acdded8b80e5d587aa5d192193f35226540f',
                                    required=False
                                    ),
                    email=dict(default='None', required=False),
                    user_agent=dict(default='simp_le/0'),
                    server=dict(default='https://acme-v01.api.letsencrypt.org/directory',
                                required=False
                                ),
                    revoke=dict(default='False', required=False, choices=['True','False'])
                )
            )

    logging.basicConfig(filename='example.log', filemode='w', level=logging.WARNING)

    def createcliarglist(module):
        domain_value = module.params['domain']
        default_root_value = module.params['default_root']
        plugins_value = module.params['plugins']
        cert_key_size_value = module.params['cert_key_size']
        valid_min_value =  module.params['valid_min']
        reuse_key_value = module.params['reuse_key']
        account_key_public_exponent_value = module.params['account_key_public_exponent']
        account_key_size_value = module.params['account_key_size']
        tos_SHA256_value = module.params['tos_SHA256']
        email_value = module.params['email']
        user_agent_value = module.params['user_agent']
        server_value = module.params['server']
        revoke_value = module.params['revoke']

        argv_list = ['-d',
                    domain_value,
                    '--default_root',
                    default_root_value,
                    '-f',
                    plugins_value,
                    '--cert_key_size',
                    cert_key_size_value,
                    '--valid_min',
                    valid_min_value,
                    '--reuse_key',
                    reuse_key_value,
                    '--account_key_public_exponent',
                    account_key_public_exponent_value,
                    '--account_key_size',
                    account_key_size_value,
                    '--tos_sha256',
                    tos_SHA256_value,
                    '--email',
                    email_value,
                    '--user_agent',
                    user_agent_value,
                    '--server',
                    server_value,
                    '--revoke',
                    revoke_value]
        logging.warning('argv_list %s', argv_list)
        return argv_list


    simp_le(createcliarglist(module))

    module.exit_json(
        changed=True
    )

    module.fail_json(
        msg="[ERROR] Something happened!"
    )


from ansible.module_utils.basic import *
if __name__ == '__main__':
    main()
