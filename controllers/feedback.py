# Retic
from retic import Request, Response, Next, App as app

# Services
from services.feedback import feedback
from retic.services.validations import validate_obligate_fields
from retic.services.responses import success_response_service, error_response_service

# Constants


def save_feedback(req: Request, res: Response):
    """Add request from a user"""

    """Validate obligate params"""
    _validate = validate_obligate_fields({
        u'comment': req.param('comment'),
    })

    """Check if has errors return a error response"""
    if _validate["valid"] is False:
        return res.bad_request(
            error_response_service(
                "The param {} is necesary.".format(_validate["error"])
            )
        )

    """Save novels into db"""
    _item_db = feedback.save_feedback_db(
        comment=req.param('comment'),
    )
    """Check if exist an error"""
    if _item_db['valid'] is False:
        return res.bad_request(_item_db)
    """Transform data response"""
    _data_response = {
        "feedback": _item_db['data']
    }
    """Response the data to client"""
    res.ok(
        success_response_service(
            data=_data_response,
            msg=_item_db['msg']
        )
    )
