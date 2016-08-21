import json
from jira import JIRA

def load_secrets(path):
    """
    Loads JSON file containing oauth secrets.
    """
    with open(path, 'r') as f:
        return json.loads(f.read())


def save_secrets(data, path):
    """
    Saves oauth secrets to json at specified path.
    """
    with open(path, 'w') as f:
        f.write(json.dumps(data, indent=4))

def jira_oauth_session(server, secrets_path):
    secrets = load_secrets(secrets_path)
    return JIRA(server, oauth=secrets)
