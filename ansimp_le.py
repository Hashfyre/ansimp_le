#!/usr/bin/env python

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
        version_added: Not Added
    default_root:
        description:
            - Default webroot path
        default: None
        version_added: Not Added
    plugins:
        description:
            - Input/output plugin of choice.
            - Can be specified multiple times.
            - Should be specified as many times as it is necessary
              to cover all components
        default: []
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
        version_added: Not Added
    valid_min:
        description:
            - Minimum validity of the resulting certificate.
        default: 2592000
        version_added: Not Added
    reuse_key:
        description:
            - Reuse private key if it was previously persisted.
        default: False
        choices: [ 'True', 'False' ]
        version_added: Not Added
    account_key_public_exponent:
        description:
            - Account key public exponent value in BITS.
        default: 65537
        version_added: Not Added
    account_key_size:
        description:
            - Account key size in BITS.
        default: 4096
        version_added: Not Added
    tos_SHA256:
        description:
            - SHA-256 hash of the contents of Terms Of Service URI contents.
        default:
            - 33d233c8ab558ba6c8ebc370a509acdded8b80e5d587aa5d192193f35226540f
        version_added: Not Added
    email:
        description:
            - Email address
            - CA is likely to use it for
                - Certificate Expiry Reminder
                - Account Recovery
            - Highly recommended to set this value.
        default: None
        version_added: Not Added
    user_agent:
        description:
            - User-Agent sent in all HTTP requests
            - Privacy Protection
                - Override with user_agent: ""
        default: simp_le/0
        version_added: Not Added
    server:
        description:
            - Directory URI for the CA ACME API endpoint
        default: https://acme-v01.api.letsencrypt.org/directory
        version_added: Not Added
    revoke:
        description:
            - Revoke existing certificate
        default: False
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
                    domain=dict(),
                    default_root=dict(),
                    plugins=dict(),
                    cert_key_size=dict()
                    valid_min=dict(),
                    reuse_key=dict(),
                    account_key_public_exponent=dict()
                    account_key_size=dict(),
                    tos_SHA256=dict(),
                    email=dict(),
                    user_agent=dict(),
                    server=dict(),
                    revoke=dict()
                )
            )


if __name__ == '__main__':
    main(sys.argv[1:])
