# Retic
from retic import App as app

# Requests
import requests

# Models
from models import Chapter


def get_chapters_from_website(url, slug_novel, chaptersIds, limit):
    """Prepare the payload"""
    _payload = {
        u"chapters_ids": chaptersIds,
        u"slug_novel": slug_novel,
        u"limit": limit
    }
    """Get all chapters from website"""
    _chapters = requests.get(url, params=_payload)
    """Check if the response is valid"""
    if _chapters.status_code != 200:
        """Return error if the response is invalid"""
        raise Exception("Invalid request.")
    """Get json response"""
    _chapters_json = _chapters.json()
    """Return chapters"""
    return _chapters_json.get('data')


def get_chapters_from_db_by_novel(novel):
    """Find in database"""
    _session = app.apps.get("db_sqlalchemy")()
    _chapters = _session.query(Chapter).\
        filter_by(novel=novel).\
        all()
    """Close session"""
    _session.close()
    """Return chapters"""
    return _chapters
