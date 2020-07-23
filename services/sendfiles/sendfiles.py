# Retic
from retic import env, App as app

# Requests
import requests

# Binascii
import binascii

# Constants
URL_FILES = app.apps['backend']['sendfiles']['base_url'] + \
    app.apps['backend']['sendfiles']['files']


def upload_files(files):
    """Upload a list of files to storage

    :param files: List of files to upload
    """

    """Build epub file"""
    _files = requests.post(
        URL_FILES,
        files=files
    )
    """Check if the response is valid"""
    if _files.status_code != 200:
        """Return error if the response is invalid"""
        raise Exception("Invalid request.")
    """Get json response"""
    _files_json = _files.json()
    """Return data"""
    return _files_json
