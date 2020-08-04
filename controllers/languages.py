# Retic
from retic import Request, Response, Next, App as app

# Services
import services.languages.languages as languages
from retic.services.responses import success_response_service, error_response_service

# Constants


def get_all_languages(req: Request, res: Response, next: Next):
    """Save novels into db"""
    _languages_db = languages.get_all_db()
    """Check if exist an error"""
    if _languages_db['valid'] is False:
        return res.bad_request(_languages_db)
    """Transform data response"""
    _data_response = {
        "languages": _languages_db['data']
    }
    """Response the data to client"""
    res.ok(
        success_response_service(
            data=_data_response,
            msg=_languages_db['msg']
        )
    )
