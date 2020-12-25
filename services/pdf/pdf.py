# Retic
from retic import env, App as app

# Requests
import requests

# Binascii
import binascii

# Constants
URL_BUILD_FROM_EPUB = app.apps['backend']['pdf']['base_url'] + \
    app.apps['backend']['pdf']['build_from_epub']
URL_BUILD_FROM_HTML = app.apps['backend']['pdf']['base_url'] + \
    app.apps['backend']['pdf']['build_from_html']


def build_pdfs_from_epub(files, binary_response=False):
    """Build a pdf file from pdf file

    :param files: List of Epub file to convert to pdf
    :param binary_response: Flag that assign if the response will has a binary file
    """

    """Prepare the payload"""
    _payload = {

    }
    _params = {
        u"binary_response": binary_response
    }
    """Build pdf file"""
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


def build_pdf_from_html(filename, cover, sections, prefix, binary_response=False, resources=[], encode_style=0):
    """Build a pdf from html

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
        u"resources": resources,
        u"encode_style": encode_style,
    }
    _params = {
        u"binary_response": binary_response
    }
    """Build pdf file"""
    _book = requests.post(URL_BUILD_FROM_HTML, json=_payload, params=_params)
    """Check if the response is valid"""
    if _book.status_code != 200:
        """Return error if the response is invalid"""
        raise Exception(_book.text)
    """Get json response"""
    _book_json = _book.json()
    """Return data"""
    return _book_json
