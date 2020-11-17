"""Services for Novels Requests Controller"""
# Retic
from retic import env, App as app

# Services
from retic.services.responses import success_response_service, error_response_service

# Models
from models import Feedback

# Constants

def save_feedback_db(comment):
    """Define all variables"""
    """Create session"""
    _session = app.apps.get("db_sqlalchemy")()
    _item_db = Feedback(
        comment=comment
    )
    _session.add(_item_db)
    """Save in database"""
    _session.commit()
    """Add novel to list"""
    _request_json = _item_db.to_dict()
    """Close session"""
    _session.close()
    """Response"""
    return success_response_service(
        data=_request_json,
        msg="Feedback saved."
    )
