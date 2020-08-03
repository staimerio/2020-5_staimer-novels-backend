"""Services for Language Controller"""
# Retic
from retic import env, App as app

# Services
from retic.services.responses import success_response_service, error_response_service

# Models
from models import Language

def get_language_hreflang_db(hreflang):
    """Create session"""
    _session = app.apps.get("db_sqlalchemy")()
    """Find in database"""
    _language = _session.query(Language).\
        filter(Language.hreflang == hreflang).\
        first()
    """Requests to json"""
    _language_json = _language.to_dict()
    """Close session"""
    _session.close()
    """Response"""
    return success_response_service(
        data=_language_json,
        msg="Language found."
    )

