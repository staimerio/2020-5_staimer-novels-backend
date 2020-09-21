# Retic
from retic import env, App as app

# Requests
import requests

# Constants
URL_LNPDF_POSTS = app.apps['backend']['lnpdf']['base_url'] + \
    app.apps['backend']['lnpdf']['posts']


def create_post(
    title,
    slug="",
    content="",
    excerpt="",
    categories=[],
    tags=[],
    types=[],
    genres=[],
    meta={},
):
    """Publish a new post on the website"""

    """Prepare payload for the request"""
    _payload = {
        u"title": title,
        u"slug": slug,
        u"content": content,
        u"excerpt": excerpt,
        u"categories": categories,
        u"tags": tags,
        u"types": types,
        u"genres": genres,
        u"meta": meta,
    }

    """Build epub file"""
    _post = requests.post(
        URL_LNPDF_POSTS,
        json=_payload,
    )
    """Check if the response is valid"""
    if _post.status_code != 200:
        """Return error if the response is invalid"""
        return None
    """Get json response"""
    _post_json = _post.json()
    """Return data"""
    return _post_json


def update_post(
    post_id,
    data=None,
):
    """Update a post on website"""

    """Prepare payload for the request"""
    _url = "{0}/{1}".format(URL_LNPDF_POSTS, post_id)
    _payload = {
        u"data": data or {}
    }
    """Build epub file"""
    _post = requests.put(
        _url,
        json=_payload,
    )
    """Check if the response is valid"""
    if _post.status_code != 200:
        """Return error if the response is invalid"""
        return None
    """Get json response"""
    _post_json = _post.json()
    """Return data"""
    return _post_json


def get_post(
    post_id,
):
    """Get a post on website"""

    """Prepare payload for the request"""
    _url = "{0}/{1}".format(URL_LNPDF_POSTS, post_id)
    """Build epub file"""
    _post = requests.get(
        _url
    )
    """Check if the response is valid"""
    if _post.status_code != 200:
        """Return error if the response is invalid"""
        return None
    """Get json response"""
    _post_json = _post.json()
    """Return data"""
    return _post_json


def search_post_by_slug(
    slug
):
    """Get a post on website"""

    """Prepare payload for the request"""
    _payload = {
        u"slug": slug
    }
    """Build epub file"""
    _post = requests.get(
        URL_LNPDF_POSTS,
        params=_payload
    )
    """Check if the response is valid"""
    if _post.status_code != 200:
        """Return error if the response is invalid"""
        return None
    """Get json response"""
    _post_json = _post.json()
    """Return data"""
    return _post_json
