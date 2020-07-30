"""Services for novels controller"""

# Retic
from retic import env, App as app


# Requests
import requests

# Binascii
import binascii

# Services
from retic.services.responses import success_response_service, error_response_service
import services.novels.chapters as chapters
import services.epub.epub as epub
import services.pdf.pdf as pdf
import services.mobi.mobi as mobi
import services.sendfiles.sendfiles as sendfiles
import services.lnpdf.lnpdf as lnpdf
import services.images.images as images
from services.general.general import get_mb_from_bytes_round
from services.general.database import files_to_dict

# Models
from models import Novel, Chapter, NovelPost

# Constants
NOVEL_CHAPTERS_LIMIT = app.config.get('NOVEL_CHAPTERS_LIMIT', callback=int)
COVER_DOUBLE_TITLE = app.config.get('COVER_DOUBLE_TITLE', callback=int)
NOVEL_DESCRIPTION_UPLOAD = app.config.get('NOVEL_DESCRIPTION_UPLOAD')
LANG_EN = {
    'name': 'english',
    'slug': 'novel-updates',
    'taxonomy': 'categories',
    'categories': "240",
    'href': 'en',
}
NOVEL_PREFIX_CH_EN = app.config.get('NOVEL_PREFIX_CH_EN')
URL_NOVELS_LATEST = app.apps['backend']['mtlnovel']['base_url'] + \
    app.apps['backend']['mtlnovel']['novels_latest']
URL_NOVELS_CHAPTERS = app.apps['backend']['mtlnovel']['base_url'] + \
    app.apps['backend']['mtlnovel']['novels_chapters']
WEBSITE_URL_COVER = app.config.get('WEBSITE_URL_COVER')
WEBSITE_TITLE_COVER = app.config.get('WEBSITE_TITLE_COVER')


def get_novels_from_website(limit, pages):
    """Prepare the payload"""
    _payload = {
        u"limit": limit,
        u"pages": pages
    }
    """Get all novels from website"""
    _novels = requests.get(URL_NOVELS_LATEST, params=_payload)
    """Check if the response is valid"""
    if _novels.status_code != 200:
        """Return error if the response is invalid"""
        raise Exception(_novels.text)
    """Get json response"""
    _novels_json = _novels.json()
    """Return novels"""
    return _novels_json.get('data')


def get_chapters_by_novels(novels, limit_publish, limit=NOVEL_CHAPTERS_LIMIT):
    """Define all variables"""
    _novel_chapters_ids = []
    _novels_chapters = []
    """For each novel do the following"""
    for _novel in novels:
        """Find novel in db"""
        _novel_db = get_by_slug_db(_novel['slug'])
        _novel_chapters_db = []
        # """Check if novel exists"""
        if _novel_db['valid'] is True:
            """Get all chapters ids"""
            _novel_chapters = chapters.get_chapters_from_db_by_novel(
                _novel_db['data']['novel']
            )
            _novel_chapters_ids = [
                _chapter.title for _chapter in _novel_chapters
            ]
            _novel_chapters_db = files_to_dict(_novel_chapters)
        """Get all chapters of the novels without ids that exists"""
        _novel_chapters = chapters.get_chapters_from_website(
            URL_NOVELS_CHAPTERS,
            _novel['slug'],
            _novel_chapters_ids,
            limit
        )
        """Check if it has any problem"""
        if not _novel_chapters:
            continue
        """Add chapters to novel"""
        _novel['chapters'] = _novel_chapters.get('chapters')
        _novel['oldchapters'] = _novel_chapters_db
        """Add info to novel"""
        _novel['info'] = _novel_chapters.get('novel')
        """The novel exists?"""
        _novel['db'] = _novel_db['data'] if _novel_db['valid'] is True else None
        """Add novel to list"""
        _novels_chapters.append(_novel)
        """Check if is the max"""
        if len(_novels_chapters) >= limit_publish:
            break
    return _novels_chapters


def get_by_slug_db(slug):
    """Find a file in the database by his slug

    :param slug: Slug of the novel in the database
    """

    """Find in database"""
    _session = app.apps.get("db_sqlalchemy")()
    _novel = _session.query(Novel, NovelPost).\
        join(NovelPost, Novel.novel == NovelPost.novel, isouter=True).\
        filter(Novel.slug == slug).\
        first()
    _session.close()

    """Check if the file exists"""
    if not _novel:
        return error_response_service(msg="Novel not found.")
    """Transform data"""
    _post = _novel.NovelPost.to_dict() if _novel.NovelPost else {}
    _data_response = {
        **_novel.Novel.to_dict(),
        u"post": None,
        **_post
    }
    return success_response_service(
        data=_data_response, msg="Novel found."
    )


def save_novels_db(novels, language):
    """Define all variables"""
    _novels = []
    """For each novel do the following"""
    for _novel in novels:
        """Check that there are chapters"""
        if not _novel['chapters']:
            continue

        """Create session"""
        _session = app.apps.get("db_sqlalchemy")()
        """Check if the novel no exists in the db"""
        if not _novel['db']:
            """If not exists, save"""
            _novel_db = Novel(
                url=_novel['url'],
                year=_novel['year'],
                title=_novel['title'],
                slug=_novel['slug'],
                site=_novel['site'],
                language=language,
            )
            _session.add(_novel_db)
            _session.flush()
            _novel_id = _novel_db.novel
            """Add novel to list"""
            _novel['db'] = _novel_db.to_dict()
        else:
            """Set novel"""
            _novel_id = _novel['db']['novel']
        """Prepare all chapters"""
        _chapters_db = [
            Chapter(
                number=chapter['number'],
                content=chapter['content'],
                title=chapter['title'],
                novel=_novel_id
            ) for chapter in _novel['chapters']
        ]
        """Save chapters in database"""
        _session.add_all(_chapters_db)
        """Save in database"""
        _session.commit()
        """Close session"""
        _session.close()
        """Add novel to list"""
        _novels.append({
            **_novel,
            **_novel['info'],
            **_novel['db']
        })
    """Transform respose"""
    _data_response = {
        u"novels": _novels
    }
    """Response"""
    return success_response_service(
        data=_data_response,
        msg="Chapters saved."
    )


def build_all_novels_to_epub(novels, binary_response):
    """Build all novels to epub files

    :param novels: List of novels that you want to build to epub
    :param binary_response: Flag that assign if the response will has a binary file
    """

    """Define all variables"""
    _epub_novels = []
    """For each novel do the following"""
    for _novel in novels:
        """Check if has new chapters"""
        if not _novel['chapters']:
            continue
        """Add oldchapters to new chapters"""
        _novel['chapters'] = _novel['oldchapters']+_novel['chapters']
        """Build cover in HTML"""
        _cover = build_cover_html_from_novel(_novel)
        """Build the novel from html"""
        _build_novel = epub.build_epub_from_html(
            _novel['title'],
            _cover,
            [_novel],
            NOVEL_PREFIX_CH_EN,
            binary_response
        )
        """Check if the response has any problem"""
        if _build_novel['valid'] is False:
            continue
        """Get binary from the file"""
        _fbinary = binascii.a2b_base64(
            _build_novel['data']['book']['epub_b64']
        )
        """Add the novel to response list"""
        _epub_novels.append({
            **_novel,
            **_build_novel['data']['book'],
            u"epub_binary": _fbinary
        })
    """Return data"""
    return _epub_novels


def build_all_epub_to_pdf(books, binary_response):
    """Build all books to epub files

    :param books: List of epubs that you want to build to pdf
    :param binary_response: Flag that assign if the response will has a binary file
    """

    """Define all variables"""
    _pdf_books = []
    _pdf_books_files = []
    """For each novel do the following"""
    for _book in books:
        """Get bytes file"""
        _pdf_books_files.append(
            ('files', (_book['title'], _book['epub_binary']))
        )
    _build_files = pdf.build_pdfs_from_epub(
        _pdf_books_files,
        binary_response
    )
    """Check if the response has any problem"""
    if _build_files['valid'] is False:
        return _build_files
    """For each file get his bytes format"""
    for _build_file in _build_files['data']['files']:
        """Get binary from the file"""
        _fbinary = binascii.a2b_base64(
            _build_file['pdf']['pdf_b64']
        )
        """Search novel in the list"""
        _novel = search_novel(_build_file['pdf']['title'], books)
        """Add the novel to response list"""
        _pdf_books.append({
            **_novel,
            **_build_file['pdf'],
            u"pdf_binary": _fbinary
        })
    """Return data"""
    return _pdf_books


def build_all_epub_to_mobi(books, binary_response):
    """Build all books to epub files

    :param books: List of epubs that you want to build to pdf
    :param binary_response: Flag that assign if the response will has a binary file
    """

    """Define all variables"""
    _mobi_books = []
    _mobi_books_files = []
    """For each novel do the following"""
    for _book in books:
        """Get bytes file"""
        _mobi_books_files.append(
            ('files', (_book['title'], _book['epub_binary']))
        )
    _build_files = mobi.build_mobi_from_epub(
        _mobi_books_files,
        binary_response
    )
    """Check if the response has any problem"""
    if _build_files['valid'] is False:
        return _build_files
    """For each file get his bytes format"""
    for _build_file in _build_files['data']['files']:
        """Get binary from the file"""
        _fbinary = binascii.a2b_base64(
            _build_file['mobi']['mobi_b64']
        )
        """Search novel in the list"""
        _novel = search_novel(_build_file['mobi']['title'], books)
        """Add the novel to response list"""
        _mobi_books.append({
            **_novel,
            **_build_file['mobi'],
            u"mobi_binary": _fbinary
        })
    """Return data"""
    return _mobi_books


def search_novel(title, books):
    """Search novel in the list"""
    for _book in books:
        if _book['title'] == title:
            return _book
    return None


def upload_to_storage(novels):
    """Upload files to storage

    :param novels: List of novel that you want to save into to storage
    """

    """Define all variables"""
    _uploaded_novels = []
    """For each novel do the following"""
    for _novel in novels:
        _files_to_upload = []
        """Create list to upload"""
        """Add the epub file"""
        _files_to_upload.append(
            ('files', (_novel['epub_title'], _novel['epub_binary']))
        )
        """Add the pdf file"""
        _files_to_upload.append(
            ('files', (_novel['pdf_title'], _novel['pdf_binary']))
        )
        """Add the mobi file"""
        _files_to_upload.append(
            ('files', (_novel['mobi_title'], _novel['mobi_binary']))
        )
        """Upload files"""
        _uploaded_files = sendfiles.upload_files(
            _files_to_upload,
            NOVEL_DESCRIPTION_UPLOAD.format(_novel['author'])
        )
        """Set direct download links in none"""
        _novel['epub_storage'] = \
            _novel['pdf_storage'] = \
            _novel['mobi_storage'] = None
        """Set direct download link to files"""
        for _upload in _uploaded_files['data']['success']:
            if _upload['extension'] == 'epub':
                _novel['epub_storage'] = _upload['code']
            elif _upload['extension'] == 'pdf':
                _novel['pdf_storage'] = _upload['code']
            elif _upload['extension'] == 'mobi':
                _novel['mobi_storage'] = _upload['code']
        """Check if the response has any problem"""
        if _uploaded_files['valid'] is True:
            _uploaded_novels.append({
                **_novel,
                **_uploaded_files.get('data')
            })
    """Return all uploaded novels"""
    return _uploaded_novels


def publish_novels(novels):
    """Publish all novels but it check if the post exists,
    in this case, it will update the post.

    :param novels: List of novel to will publish
    """

    """Define all variables"""
    _published_novels = []
    """For each novels do to the following"""
    for _novel in novels:
        """Add epub version"""
        _storage = "{0},{1},{2},{3},{4}\n".format(
            _novel['lang'],
            'epub',
            get_mb_from_bytes_round(_novel['epub_size'], 2),
            _novel['epub_storage'],
            _novel['epub_title'],
        )
        """Add pdf version"""
        _storage += "{0},{1},{2},{3},{4}\n".format(
            _novel['lang'],
            'pdf',
            get_mb_from_bytes_round(_novel['pdf_size'], 2),
            _novel['pdf_storage'],
            _novel['pdf_title'],
        )
        """Add mobi version"""
        _storage += "{0},{1},{2},{3},{4}".format(
            _novel['lang'],
            'mobi',
            get_mb_from_bytes_round(_novel['mobi_size'], 2),
            _novel['mobi_storage'],
            _novel['mobi_title'],
        )
        """If the post exists, update the posts"""
        if 'post' in _novel and _novel['post']:
            """Get post by id"""
            _oldpost = lnpdf.get_post(_novel['post'])
            """Get old storage folder"""
            _old_storage_folder = _oldpost['data']['meta']['storage_folder']
            """Set metadata about the post"""
            _oldpost['data']['meta']['storage_data'] = _storage
            _oldpost['data']['meta']['storage_folder'] = _novel['code']
            _oldpost['data']['meta']['last_ch'] = _novel['chapters'][-1]['number']
            _oldpost['data']['meta']['last_vol'] = 1
            _post = lnpdf.update_post(
                _oldpost['data']['id'],
                {u'meta': _oldpost['data']['meta']}
            )
            """Check if is a valid post"""
            if _post and _post['valid']:
                """Delete old folder"""
                _deleted_folder = sendfiles.delete_folder(
                    _old_storage_folder
                )
                """Add post to the list"""
                _published_novels.append(_post['data'])
        else:
            """If the posts doesn't exists, create the post"""
            """Upload cover"""
            _cover = images.upload_images_from_urls(
                urls=[_novel['cover']],
                watermark_code="lnpdf.png"
            )
            """Set metadata about the post"""
            _metadata = {
                "cover": _cover['data']['images'][-1]['link'],
                "author": _novel['author'],
                "status": _novel['status'],
                "last_ch": _novel['chapters'][-1]['number'],
                "last_vol": 1,
                "year": _novel['year'],
                "storage_data": _storage,
                "storage_folder":  _novel['code'],
                "url":  _novel['url'],
                "id_eu_novel": _novel['novel'],
            }
            _post = lnpdf.create_post(
                title=_novel['title'],
                slug=_novel['slug'],
                categories=[
                    {
                        u"name": LANG_EN['name'],
                        u"slug":LANG_EN['slug'],
                    }
                ],
                tags=[
                    {u"name": _novel['author']},
                    {u"name": _novel['status']},
                    {u"name": _novel['year']},
                    {u"name": _novel['lang']},
                ],
                types=[
                    {u"name": _novel['type']},
                ],
                genres=[
                    {u"name": _item} for _item in _novel['categories']
                ],
                meta=_metadata,
            )
            """Check if is a valid post"""
            if _post and _post['valid']:
                """Add post to novel"""
                _novel_post = save_post_novel_db(
                    _post['data']['id'],
                    _novel['novel']
                )
                """Add post to the list"""
                _published_novels.append(_post['data'])
    """Return the posts list"""
    return success_response_service(
        data=_published_novels
    )


def save_post_novel_db(post, novel):
    """Create session"""
    _session = app.apps.get("db_sqlalchemy")()
    """Check if the novel no exists in the db"""
    _post_db = NovelPost(
        novel=novel,
        post=post
    )
    _session.add(_post_db)
    """Save in database"""
    _session.commit()
    """Get post data"""
    _post_json = _post_db.to_dict()
    """Close session"""
    _session.close()
    """Transform respose"""
    _data_response = {
        u"post": _post_json
    }
    """Response"""
    return success_response_service(
        data=_data_response,
        msg="Post saved."
    )


def build_cover_html_from_novel(novel):
    """Build a cover in HTML from a novel"""
    _content = '''
        <html>
            <head></head>
            <body style="text-align: center; font-family: none;">
                <div style="margin: 55px 55px 55px 55px; text-align: center;">'''
    _content += '<h1 style="font-size: 2rem; text-transform: uppercase;">''' + \
        novel['title']+'</h1>'
    _content += '<div><p>'+novel['status']+' - '+str(
        novel['year'])+' - '+novel['type']+' - '+novel['lang'].capitalize()+'</p>'
    _content += '<p>'+" | ".join(novel['categories'])+'</p>'
    _content += '</div><br /><br /><br /><br /><br /><br /><br /><br />'
    _content += '<br /><br /><br /><br /><br /><br /><br /><br />'
    _content += '<br /><br /><br /><br />' if len(
        novel['title']) < COVER_DOUBLE_TITLE else ""
    _content += '<h2 style="font-size: 3.5rem; text-transform: uppercase; margin: 10px 10px 10px 10px;">' + \
        novel['author']+'</h2>'
    _content += '<a class="badge-link" href="'+WEBSITE_URL_COVER + \
        '" target="_blank" style="text-decoration: none; -webkit-transition: color 200ms ease; transition: color 200ms ease; ">'
    _content += '<span class = "badge badge-pro" style = "padding: 3px 3px; font-weight: bold; text-transform: uppercase; color: #272727; border-radius: 7px;" >'+WEBSITE_TITLE_COVER+'</span>'
    _content += '</a></div></body></html>'
    _content = _content.replace("\n", "")
    return _content
