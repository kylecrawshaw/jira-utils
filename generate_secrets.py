#!/usr/bin/env python

import os
from argparse import ArgumentParser
from jira_utils import oauth, save_secrets
from requests_oauthlib.oauth1_session import TokenRequestDenied

def parsed_args():
    """
    Helper function to setup argument parser and parse command line arguments.
    """
    parser = ArgumentParser()
    parser.add_argument('server', help='URL for a JIRA server or cloud instance')
    parser.add_argument('--consumer-key', '-c', required=True, help='Consumer Key for JIRA Oauth Application')
    parser.add_argument('--rsa-key', '-k', required=True, help='Path where output CSV should be saved.')
    parser.add_argument('--username', '-u', help='Username for a JIRA account to auth with')
    parser.add_argument('--password', '-p', help='Password for JIRA user')
    parser.add_argument('--auto', '-a', default=False, action='store_true',
                        help='Autoruns oauth flow without requiring browser interaction')
    parser.add_argument('--out', '-o', default='secrets.json', help='Output path for secrets.')
    return parser.parse_args()


def main():
    args = parsed_args()
    if not os.path.exists(args.rsa_key):
        raise SystemExit('Provided RSA Key could not be found')

    with open(args.rsa_key) as f:
        key_cert = f.read()

    try:
        oauth_secrets = oauth.jira_oauth_flow(args.server, args.consumer_key, key_cert,
                                         auto=args.auto, username=args.username,
                                         password=args.password)
    except TokenRequestDenied:
        raise SystemExit('Oauth request denied.')
    save_secrets(oauth_secrets, args.out)
if __name__ == '__main__':
    main()
