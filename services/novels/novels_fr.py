"""Services for novels controller"""

# Retic
from retic import env, App as app

# Requests
import requests

# Services
from retic.services.responses import success_response_service, error_response_service

# Models

# Constants
URL_NOVELS_LATEST = app.apps['backend']['mtlnovel']['base_url'] + \
    app.apps['backend']['mtlnovel']['novels_latest']


def get_novels_from_website(limit, pages):
    """Prepare the payload"""
    _payload = {
        u"limit": limit,
        u"pages": pages,
        u"lang": 'fr',
    }
    """Get all novels from website"""
    _novels = requests.get(URL_NOVELS_LATEST, params=_payload)
    """Check if the response is valid"""
    if _novels.status_code != 200:
        """Return error if the response is invalid"""
        raise Exception(_novels.text)
    """Get json response"""
    _novels_json = _novels.json()
    """Return novels"""
    return _novels_json.get('data')
