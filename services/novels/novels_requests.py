"""Services for Novels Requests Controller"""
# Retic
from retic import env, App as app

# Services
from retic.services.responses import success_response_service, error_response_service
from services.general.database import files_to_dict

# Models
from models import Request


def save_request_db(title, email, language, reference=None):
    """Define all variables"""
    """Create session"""
    _session = app.apps.get("db_sqlalchemy")()
    _request_db = Request(
        title=title,
        email=email,
        language=language,
        reference=reference
    )
    _session.add(_request_db)
    """Save in database"""
    _session.commit()
    """Add novel to list"""
    _request_json = _request_db.to_dict()
    """Close session"""
    _session.close()
    """Response"""
    return success_response_service(
        data=_request_json,
        msg="Request created."
    )


def get_all_db():
    """Create session"""
    _session = app.apps.get("db_sqlalchemy")()
    """Find in database"""
    _requests = _session.query(Request).\
        filter(Request.is_completed == False).\
        all()
    """Requests to json"""
    _requests_json = files_to_dict(_requests)
    """Close session"""
    _session.close()
    """Response"""
    return success_response_service(
        data=_requests_json,
        msg="Requests found."
    )
