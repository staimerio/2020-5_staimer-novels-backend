# Retic
from retic import App as app

# Requests
import requests

# Models
from models import Chapter

# Services
from retic.services.responses import success_response_service, error_response_service


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
        return None
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


def get_chapters_by_novel_db(novel):
    """Find chapters by novel id

    :param novel: Identificator for novel
    """

    """Find in database"""
    _session = app.apps.get("db_sqlalchemy")()
    _chapters = _session.query(
        Chapter.chapter,
        Chapter.number,
        Chapter.title,
    ).\
        filter(
            Chapter.novel == novel,
            Chapter.is_deleted == False,
            Chapter.is_active == True
    ).\
        all()
    _session.close()

    """Check if the file exists"""
    if not _chapters:
        return error_response_service(msg="Chapters not found.")
    """Transform data"""
    _chapters_json = [
        {
            u"chapter": _chapter[0],
            u"number": _chapter[1],
            u"title": _chapter[2],
        } for _chapter in _chapters
    ]
    return success_response_service(
        data=_chapters_json, msg="Chapters found."
    )


def get_chapter_by_id_db(chapter):
    """Find chapter by id

    :param chapter: Identificator for chapter
    """

    """Find in database"""
    _session = app.apps.get("db_sqlalchemy")()
    _chapter = _session.query(Chapter).\
        filter(
            Chapter.chapter == chapter,
            Chapter.is_deleted == False,
            Chapter.is_active == True
    ).\
        first()
    _session.close()

    """Check if the file exists"""
    if not _chapter:
        return error_response_service(msg="Chapter not found.")
    """Transform data"""
    _chapter_json = _chapter.to_dict()
    """Response data"""
    return success_response_service(
        data=_chapter_json, msg="Chapter found."
    )
