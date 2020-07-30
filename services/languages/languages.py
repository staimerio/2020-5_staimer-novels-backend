"""Services for Languages Controller"""
# Retic
from retic import env, App as app

# Services
from retic.services.responses import success_response_service, error_response_service
from services.general.database import files_to_dict

# Models
from models import Language


def get_all_db():
    """Create session"""
    _session = app.apps.get("db_sqlalchemy")()
    """Find in database"""
    _languages = _session.query(Language).\
        all()
    """Requests to json"""
    _languages_json = files_to_dict(_languages)
    """Close session"""
    _session.close()
    """Response"""
    return success_response_service(
        data=_languages_json,
        msg="Languages found."
    )
