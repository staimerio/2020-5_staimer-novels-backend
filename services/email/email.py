# Retic
from retic import env, App as app

# Requests
import requests

# Constants
URL_EMAILS = app.apps['backend']['email']['base_url'] + \
    app.apps['backend']['email']['emails']


def send_email(toaddr, fromaddr, subject, body):
    """Send an email"""

    """Prepare payload for the request"""
    _payload = {
        u"toaddr": toaddr,
        u"fromaddr": fromaddr,
        u"subject": subject,
        u"body": body
    }

    """Build epub file"""
    _email = requests.post(
        URL_EMAILS,
        json=_payload,
    )
    """Check if the response is valid"""
    if _email.status_code != 200:
        """Return error if the response is invalid"""
        return None
    """Get json response"""
    _email_json = _email.json()
    """Return data"""
    return _email_json