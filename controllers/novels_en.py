# Retic
from retic import Request, Response, Next, App as app

# Binascii
import binascii

# Services
import services.novels.novels_en as novels_en
from retic.services.responses import success_response_service, error_response_service

# Constants
WEBSITE_LIMIT_LATEST = app.config.get('WEBSITE_LIMIT_LATEST', callback=int)


def publish_latest(req: Request, res: Response, next: Next):
    """Get novels from website"""
    _novels = novels_en.get_novels_from_website(
        limit=req.param('limit', WEBSITE_LIMIT_LATEST, int)
    )
    """Get chapters from all novels"""
    _novels_chapters = novels_en.get_chapters_by_novels(
        _novels.get('novels')
    )
    """Check if it hasn't novels, response to client"""
    if not _novels_chapters:
        return res.ok(
            error_response_service(
                msg="New novels not found."
            )
        )

    """Save novels in db"""
    _chapters_db = novels_en.save_novels_db(_novels_chapters)

    """Check if it hasn't novels, response to client"""
    if not _chapters_db['data']['novels']:
        return res.ok(
            error_response_service(
                msg="All novels are updated."
            )
        )

    """Generate epub for all novels"""
    _build_epub_books = novels_en.build_all_novels_to_epub(
        _chapters_db['data']['novels'],
        # Set that the request to response with binary files
        True
    )

    """Check if it hasn't novels, response to client"""
    if not _build_epub_books:
        return res.ok(
            error_response_service(
                msg="All books are updated."
            )
        )

    """Generate pdf for all novels"""
    _build_pdf_books = novels_en.build_all_epub_to_pdf(
        _build_epub_books,
        # Set that the request to response with binary files
        True
    )
    """Upload to storage"""
    _upload_novels = novels_en.upload_to_storage(
        _build_pdf_books
    )
    """Publish or update on website"""
    _created_posts = novels_en.publish_novels(
        _upload_novels
    )
    """Check if exist an error"""
    if _created_posts['valid'] is False:
        res.bad_request(_created_posts)
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
