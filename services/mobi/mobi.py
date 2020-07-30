# Retic
from retic import env, App as app

# Requests
import requests

# Binascii
import binascii

# Constants
URL_BUILD_FROM_EPUB = app.apps['backend']['mobi']['base_url'] + \
    app.apps['backend']['mobi']['build_from_epub']


def build_mobi_from_epub(files, binary_response=False):
    """Build a mobi file from epub file

    :param files: List of Epub file to convert to mobi
    :param binary_response: Flag that assign if the response will has a binary file
    """

    """Prepare the payload"""
    _payload = {
        
    }
    _params = {
        u"binary_response": binary_response
    }
    """Build epub file"""
    _files = requests.post(
        URL_BUILD_FROM_EPUB,
        data=_payload,
        params=_params,
        files=files
    )
    """Check if the response is valid"""
    if _files.status_code != 200:
        """Return error if the response is invalid"""
        raise Exception(_files.text)
    """Get json response"""
    _files_json = _files.json()
    """Return data"""
    return _files_json
