# Retic
from retic import env, App as app

# Requests
import requests

# Binascii
import binascii

# Constants
URL_FILES = app.apps['backend']['sendfiles']['base_url'] + \
    app.apps['backend']['sendfiles']['files']
URL_FOLDERS = app.apps['backend']['sendfiles']['base_url'] + \
    app.apps['backend']['sendfiles']['folders']


def upload_files(files, description):
    """Upload a list of files to storage

    :param files: List of files to upload
    :param description: Description of the upload
    """

    """Prepare the payload"""
    _payload = {
        u"description": description
    }

    """Build epub file"""
    _files = requests.post(
        URL_FILES,
        files=files,
        data=_payload
    )
    """Check if the response is valid"""
    if _files.status_code != 200:
        """Return error if the response is invalid"""
        raise Exception("Invalid request.")
    """Get json response"""
    _files_json = _files.json()
    """Return data"""
    return _files_json


def delete_folder(folder):
    """Upload a list of files to storage

    :param folder: Id of a folder that you want delete
    """

    """Prepare the payload"""
    _url = "{0}/{1}".format(URL_FOLDERS, folder)

    """Delete a folder"""
    _folder = requests.delete(
        _url
    )
    """Check if the response is valid"""
    if _folder.status_code != 200:
        """Return error if the response is invalid"""
        raise Exception("Invalid request.")
    """Get json response"""
    _folder_json = _folder.json()
    """Return data"""
    return _folder_json
