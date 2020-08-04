# Retic
from retic import Request, Response, Next, App as app

# Binascii
import binascii

# Services
import services.novels.novels_en as novels_en
import services.novels.novels as novels
import services.novels.languages as languages
from retic.services.responses import success_response_service, error_response_service

# Constants
WEBSITE_LIMIT_LATEST = app.config.get('WEBSITE_LIMIT_LATEST', callback=int)
WEBSITE_PAGES_LATEST = app.config.get('WEBSITE_PAGES_LATEST', callback=int)
WEBSITE_LIMIT_PUBLISH_LATEST = app.config.get(
    'WEBSITE_LIMIT_PUBLISH_LATEST', callback=int)
NOVEL_LANGUAGE_ID = app.config.get(
    'NOVEL_LANGUAGE_ID', callback=int)
URL_NOVELS_CHAPTERS = app.apps['backend']['mtlnovel']['base_url'] + \
    app.apps['backend']['mtlnovel']['novels_chapters']


def publish_latest(req: Request, res: Response, next: Next):
    """Get novels from website"""
    _novels = novels_en.get_novels_from_website(
        limit=req.param('limit', WEBSITE_LIMIT_LATEST, int),
        pages=req.param('pages', WEBSITE_PAGES_LATEST, int)
    )
    """Get the langauge"""
    _lang = languages.get_language_hreflang_db("en")
    """Publish novels"""
    _created_posts = novels.publish_novels(
        _novels.get('novels'),
        req.param('limit_publish', WEBSITE_LIMIT_PUBLISH_LATEST, int),
        NOVEL_LANGUAGE_ID,
        _lang.get('data'),
        URL_NOVELS_CHAPTERS
    )
    """Check if exist an error"""
    if _created_posts['valid'] is False:
        return res.bad_request(_created_posts)
    """Transform data response"""
    _data_response = {
        "posts": _created_posts['data']
    }
    """Response the data to client"""
    res.ok(
        success_response_service(
            data=_data_response,
            msg="Posts created."
        )
    )
