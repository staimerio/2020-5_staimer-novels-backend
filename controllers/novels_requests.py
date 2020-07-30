# Retic
from retic import Request, Response, Next, App as app

# Services
import services.novels.novels_requests as novels_requests
from retic.services.validations import validate_obligate_fields
from retic.services.responses import success_response_service, error_response_service

# Constants


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
