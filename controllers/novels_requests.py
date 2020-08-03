# Retic
from retic import Request, Response, Next, App as app

# Services
import services.novels.novels_requests as novels_requests
from retic.services.validations import validate_obligate_fields
from retic.services.responses import success_response_service, error_response_service

# Constants
WEBSITE_LIMIT_PUBLISH_REQUESTS = app.config.get(
    'WEBSITE_LIMIT_PUBLISH_REQUESTS', callback=int)
WEBSITE_LIMIT_PUBLISH_CHAPTERS_REQUESTS = app.config.get(
    'WEBSITE_LIMIT_PUBLISH_CHAPTERS_REQUESTS', callback=int)
WEBSITE_LIMIT_SEARCH_LIMIT = app.config.get(
    'WEBSITE_LIMIT_SEARCH_LIMIT', callback=int)
URL_NOVELS_CHAPTERS = app.apps['backend']['novelfull']['base_url'] + \
    app.apps['backend']['novelfull']['novels_chapters']


def requests(req: Request, res: Response, next: Next):
    """Add request from a user"""

    """Validate obligate params"""
    _validate = validate_obligate_fields({
        u'title': req.param('title'),
        u'email': req.param('email'),
        u'language': req.param('language'),
    })

    """Check if has errors return a error response"""
    if _validate["valid"] is False:
        return res.bad_request(
            error_response_service(
                "The param {} is necesary.".format(_validate["error"])
            )
        )

    """Save novels into db"""
    _requests_db = novels_requests.save_request_db(
        title=req.param('title'),
        email=req.param('email'),
        language=req.param('language')
    )
    """Check if exist an error"""
    if _requests_db['valid'] is False:
        res.bad_request(_requests_db)
    """Transform data response"""
    _data_response = {
        "request": _requests_db['data']
    }
    """Response the data to client"""
    res.ok(
        success_response_service(
            data=_data_response,
            msg=_requests_db['msg']
        )
    )


def get_all_requests(req: Request, res: Response, next: Next):
    """Save novels into db"""
    _requests_db = novels_requests.get_all_db()
    """Check if exist an error"""
    if _requests_db['valid'] is False:
        res.bad_request(_requests_db)
    """Transform data response"""
    _data_response = {
        "requests": _requests_db['data']
    }
    """Response the data to client"""
    res.ok(
        success_response_service(
            data=_data_response,
            msg=_requests_db['msg']
        )
    )


def publish_requests(req: Request, res: Response):
    """Get novels from database"""
    _requests_db = novels_requests.get_request_db(
        limit=req.param('limit', WEBSITE_LIMIT_PUBLISH_REQUESTS, int),
    )
    """Get novels from website"""
    _novels_found, _novels_not_found = novels_requests.get_novels_from_website(
        _requests_db['data'],
        limit_search=req.param(
            'limit_search', WEBSITE_LIMIT_SEARCH_LIMIT, int),

    )
    """Deactivated all novels without results"""
    if _novels_not_found:
        _novels = novels_requests.deactivated_novels_without_results(
            _novels_not_found
        )
    """Get chapters from all novels"""
    _novels_chapters = novels_requests.publish_requests(
        _novels_found,
        limit_publish=req.param('limit_publish', WEBSITE_LIMIT_PUBLISH_CHAPTERS_REQUESTS, int),
        url_novels_chapters=URL_NOVELS_CHAPTERS
    )
    """Check if exist an error"""
    if _novels_chapters['valid'] is False:
        return res.bad_request(_novels_chapters)
    """Transform data response"""
    _data_response = {
        "novels": _novels_chapters['data']
    }
    """Response the data to client"""
    res.ok(
        success_response_service(
            data=_data_response,
            msg="Posts created."
        )
    )
