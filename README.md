JIRA Utils
============

This is the start to a collection of utility functions for the [jira-python](http://jira.readthedocs.io/en/latest/#) library that wraps around the JIRA API.

There will be more documentation coming soon and eventually I may try to push some of this upstream to [jira-python](http://jira.readthedocs.io/en/latest/#) if it makes sense.

## Getting Started
The Python JIRA library (jira-python) utilizes [oauthlib](https://oauthlib.readthedocs.io/en/latest/index.html) for it's oauth functionality (ex. `jira.JIRA(server_url, oauth=oauth`) and I've found some issues with the recent version of `oauthlib`.
- Use Python 3, otherwise `oauthlib` just doesn't work
- Run `pip install -r requirements.txt` to install the right versions of different libraries to work with `jira-python`
    - If you install Python 3 with brew you can use `pyvenv` to create a virtual environment to work with.
    - There are other crypto libraries included

1. Create a new ApplicationLink on your JIRA Server and make note of the `consumer_key` as well as the Private RSA key.
2. ...
