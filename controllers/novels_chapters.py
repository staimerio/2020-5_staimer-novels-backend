# Retic
from retic import Request, Response, Next, App as app

# Services
import services.novels.chapters as chapters
from retic.services.responses import success_response_service, error_response_service


def get_chapters_by_novel(req: Request, res: Response, next: Next):
    """Get chapters from db"""
    _requests_db = chapters.get_chapters_by_novel_db(
        req.param('novel')
    )
    """Check if exist an error"""
    if _requests_db['valid'] is False:
        return res.bad_request(_requests_db)
    """Transform data response"""
    _data_response = {
        "chapters": _requests_db['data']
    }
    """Response the data to client"""
    res.ok(
        success_response_service(
            data=_data_response,
            msg=_requests_db['msg']
        )
    )


def get_chapter_by_id(req: Request, res: Response, next: Next):
    """Get chapter from db"""
    _requests_db = chapters.get_chapter_by_id_db(
        req.param('chapter')
    )
    """Check if exist an error"""
    if _requests_db['valid'] is False:
        return res.bad_request(_requests_db)
    """Transform data response"""
    _data_response = {
        "chapter": _requests_db['data']
    }
    """Response the data to client"""
    res.ok(
        success_response_service(
            data=_data_response,
            msg=_requests_db['msg']
        )
    )
