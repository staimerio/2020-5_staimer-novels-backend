# Retic
from retic import App as app

# Requests
import requests

# Constants
URL_BUILD_FROM_HTML = app.apps['backend']['epub']['base_url'] + \
    app.apps['backend']['epub']['build_from_html']
URL_DOWNLOADS = app.apps['backend']['epub']['base_url'] + \
    app.apps['backend']['epub']['downloads']


def build_epub_from_html(filename, cover, sections, prefix, binary_response=False):
    """Build a epub from html

    :param filename: Name of the file
    :param cover: Cover on HTML
    :param sections: Sections are like volumes inside in a Epub file,
    those contain chapters
    :param prefix: Prefix for the chapter title
    :param binary_response: Flag that assign if the response will has a binary file
    """

    """Prepare the payload"""
    _payload = {
        u"title": filename,
        u"cover": cover,
        u"sections": sections,
        u"prefix": prefix,
    }
    _params = {
        u"binary_response": binary_response
    }
    """Build epub file"""
    _book = requests.post(URL_BUILD_FROM_HTML, json=_payload, params=_params)
    """Check if the response is valid"""
    if _book.status_code != 200:
        """Return error if the response is invalid"""
        raise Exception(_book.text)
    """Get json response"""
    _book_json = _book.json()
    """Return data"""
    return _book_json
