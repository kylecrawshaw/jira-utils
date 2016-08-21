import os
import random
import string
import webbrowser

from oauthlib.oauth1 import SIGNATURE_RSA
from requests_oauthlib import OAuth1Session


def _auto_auth_flow(token_auth_url, username=None, password=None):
    """
    Performs login for user automatically with RoboBrowser by locating the login
    form, filling it out and submitting it. Authorize form is then submitted.

    Arguments:
        token_auth_url (str): url of server with auth token url params
        username (str): username of the JIRA user that will be authenticated
        password (str): matching password for `username`
    """
    # These only need to be imported if `auto=True` when `jira_oauth_flow` is called
    from robobrowser import RoboBrowser
    from getpass import getpass

    # Create a new RoboBrowser instance and open the `token_auth_url`
    browser = RoboBrowser(parser='html.parser')
    browser.open(token_auth_url)

    # Prompt for username and/or password if left unset
    if username is None:
        username = input('JIRA Username: ')

    if password is None:
        password = getpass('JIRA Password: ')

    # Locate login form from page contents
    login_form = browser.get_form()

    # Fill out and submit login form
    login_form['username'].value = username
    login_form['password'].value = password
    browser.submit_form(login_form)

    # Locate and submit approval form which will complete the auth process
    approve_form = browser.get_form()
    browser.submit_form(approve_form, submit=approve_form['approve'])


def jira_oauth_flow(server, consumer_key, key_cert, auto=False, username=None, password=None):
    """
    Runs the oauth flow to grant an oauth access_token and access_token_secret.

    Arguments:
        server (str): full url to JIRA server to auth against
        consumer_key (str): created during the setup of an Application Link in JIRA
        rsa_key (str): rsa_key created during the setup of an Application Link in JIRA
        auto (bool): if True robobrowser will be used to automatically authorize oauth without
                     launching a browser. If both `username` and `password` are set, there will
                     be no user interaction.

    Returns:
        secrets (dict): contains all secrets required for oauth with jira-python

        Ex.
            {
                "server": "https://giantcorp.atlassian.net",
                "oauth": {
                    "consumer_key": "rand89kemuj6773hnden#$"
                    "access_token": "328jJEid7290sKASI#!@",
                    "access_token_secret": "38DJuiefb21kuweNDWEU",
                    "key_cert": "-----BEGIN RSA PRIVATE KEY-----\nrandom_rsa_key_data_here\n-----END RSA PRIVATE KEY-----\n",
                }
            }
    """
    # Remove / if it exists at the end of `server`
    server = server.strip('/')

    # The URLs for the JIRA instance
    request_token_url = '{server}/plugins/servlet/oauth/request-token'.format(server=server)
    authorize_url = '{server}/plugins/servlet/oauth/authorize'.format(server=server)
    access_token_url = '{server}/plugins/servlet/oauth/access-token'.format(server=server)

    # Create a new instance of Oauth1Session to handle our requests
    oauth = OAuth1Session(consumer_key,
                          signature_type='auth_header',
                          signature_method=SIGNATURE_RSA,
                          rsa_key=key_cert)

    # Fetch the initial request token and build `token_url`
    # with `oauth_token` url param
    request_token = oauth.fetch_request_token(request_token_url)
    token_url = "{base}?oauth_token={token}".format(base=authorize_url,
                                                    token=request_token['oauth_token'])

    # Run authorization flow. If `auto=False`, the default browser will be launched and loging/authorization will occur
    # in the browser. Otherwise, RoboBrowser will be used removing the need for browser interaction.
    if auto:
        _auto_auth_flow(token_url, username=username, password=password)
    else:
        webbrowser.open(token_url)
        input("Press any key to continue")
    oauth._client.client.verifier = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(25))

    access_token = oauth.fetch_access_token(access_token_url)

    # Create dictionary with all the information needed to create a new jira.JIRA instance with oauth.
    oauth_secrets = {
        'consumer_key': consumer_key,
        'access_token': access_token['oauth_token'],
        'access_token_secret': access_token['oauth_token_secret'],
        'key_cert': key_cert
    }

    return oauth_secrets

