"""Services for Novels Requests Controller"""
# Retic
from retic import env, App as app

# Requests
import requests

# Services
from retic.services.responses import success_response_service, error_response_service
from services.general.database import files_to_dict
import services.novels.novels as novels
import services.email.email as email

# Models
from models import Request, Language, RequestNovelPost

# Constants
REQUEST_FROMADDR = app.config.get('REQUEST_FROMADDR')
REQUEST_SUBJECT = app.config.get('REQUEST_SUBJECT')

URL_NOVELFULL_SEARCH = app.apps['backend']['novelfull']['base_url'] + \
    app.apps['backend']['novelfull']['novels_search']
URL_MTLNOVEL_SEARCH = app.apps['backend']['mtlnovel']['base_url'] + \
    app.apps['backend']['mtlnovel']['novels_search']


def save_request_db(title, email, language, reference=None):
    """Define all variables"""
    """Create session"""
    _session = app.apps.get("db_sqlalchemy")()
    """Find in database"""
    _request = _session.query(Request).\
        filter(Request.title == title,
               Request.language == language,
               Request.is_active == 1).\
        first()
    """Check if it exists in db"""
    if _request:
        return error_response_service(msg="Request exists.")
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


def save_requests_from_file_db(file, email, language, reference=None):
    """Define all variables"""
    _requests = []
    """Read content from file"""
    _content = file.read().decode("utf-8")
    """Split in lines"""
    _lines = _content.split("\r\n")
    """For each line do the following"""
    for _title in _lines:
        _request = save_request_db(_title, email, language, reference)
        """Check if has any error"""
        if _request['valid']:
            _requests.append(_request['data'])
    """Response"""
    return success_response_service(
        data=_requests,
        msg="Requests created."
    )


def save_request_novel_post_db(posts, request):
    """Define all variables"""
    """Create session"""
    _session = app.apps.get("db_sqlalchemy")()
    """For each post do the following"""
    for _post in posts:
        _session.add(
            RequestNovelPost(
                post=_post['id'],
                novel=_post['meta']['id_eu_novel'],
                request=request,
            )
        )
    """Save in database"""
    _session.commit()
    """Close session"""
    _session.close()
    """Response"""
    return success_response_service(
        msg="Related request."
    )


def get_all_db():
    """Create session"""
    _session = app.apps.get("db_sqlalchemy")()
    """Find in database"""
    _requests = _session.query(Request).\
        filter(Request.is_completed == False,
               Request.is_active == True).\
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


def get_request_db(limit):
    """Create session"""
    _session = app.apps.get("db_sqlalchemy")()
    """Find in database"""
    _requests = _session.query(Request, Language).\
        filter(
            Request.is_completed == False,
            Request.is_active == True,
            Request.language == Language.language
    ).\
        limit(limit).\
        all()
    """Requests to json"""
    _requests_json = list()
    for _request in _requests:
        """Add file to list"""
        _requests_json.append({
            u"request": _request.Request.to_dict(),
            u"lang":  _request.Language.to_dict(),
        })
    """Close session"""
    _session.close()
    """Response"""
    return success_response_service(
        data=_requests_json,
        msg="Requests found."
    )


def get_novels_from_website(novels, limit_search):
    """Declare all variables"""
    _novels_not_found = []
    _novels_found = []
    """For each novel do the following"""
    for _novel in novels:
        _request = _novel['request']
        _lang = _novel['lang']
        """Prepare the payload"""
        _payload = {
            u"search": _request['title'],
            u"limit": limit_search,
            u"hreflang": _lang['hreflang'],
        }

        """Find novels on all avalaible website"""

        """NOVELFULL"""
        """Get all novels from website"""
        _novels_req = requests.get(URL_NOVELFULL_SEARCH, params=_payload)
        """Check if the response is valid"""
        if _novels_req.status_code != 200:
            """MTLNOVEL"""
            """Get all novels from website"""
            _novels_req = requests.get(URL_MTLNOVEL_SEARCH, params=_payload)

        """Check if the response is valid"""
        if _novels_req.status_code == 404:
            """Return error if the response is invalid"""
            _novels_not_found.append(_request)
        elif _novels_req.status_code == 200:
            """Get json response"""
            _novels_json = _novels_req.json()
            """Add novels"""
            _novels_found.append({
                u"info": _request,
                u"lang": _novel['lang'],
                u"requests": _novels_json['data']['novels']
            })
        else:
            """Return error if the response is invalid"""
            raise Exception(_novels_req.text)
    """Return novels"""
    return _novels_found, _novels_not_found


def deactivated_novels_without_results(novels):
    """Create session"""
    _session = app.apps.get("db_sqlalchemy")()
    _novels = [{**_novel, u"is_active": False} for _novel in novels]
    """For each novel deactive without results"""
    _session.bulk_update_mappings(
        Request,
        _novels
    )
    """Session commit"""
    _session.commit()
    """Close session"""
    _session.close()
    """Response"""
    return success_response_service(
        msg="Requests deactivated."
    )


def completed_novels_with_results(novels):
    """Create session"""
    _session = app.apps.get("db_sqlalchemy")()
    _novels = [{**_novel, u"is_completed": True, u"is_active": False}
               for _novel in novels]
    """For each novel deactive without results"""
    _session.bulk_update_mappings(
        Request,
        _novels
    )
    """Session commit"""
    _session.commit()
    """Close session"""
    _session.close()
    """Response"""
    return success_response_service(
        msg="Requests deactivated."
    )


def publish_requests(requests, limit_publish):
    """Publish all result for the search"""
    """Declare all variables"""
    _novels_posts = []
    """Check it has novels"""
    if not requests:
        return error_response_service(msg="Requests not found.")
    """For each request do the following"""
    for _novel in requests:
        _request = _novel['info']
        """Publish novels"""
        _created_posts = novels.publish_novels(
            _novel.get('requests'),
            limit_publish,
            _request['language'],
            _novel.get('lang')
        )
        """Completed requests"""
        _completed_requests = completed_novels_with_results(
            [_request]
        )
        """Check if it's valid"""
        if not _created_posts['valid']:
            continue
        """Add request to list"""
        _novels_posts += _created_posts['data']
        """Create relation between novel, request and post"""
        _req_novel_post = save_request_novel_post_db(
            _novels_posts,
            _request['request']
        )
        """Check if it has email address"""
        if _request['email']:
            """Create email body"""
            if _novel['lang']['hreflang'] == 'es':
                _email_body = create_requests_email_body_es(
                    _novel,
                    _novels_posts
                )
            else:
                _email_body = create_requests_email_body_en(
                    _novel,
                    _created_posts['data']
                )
            """Send email to address"""
            _email = email.send_email(
                toaddr=_request['email'],
                fromaddr=REQUEST_FROMADDR,
                subject=REQUEST_SUBJECT+_novel["info"]['title'],
                body=_email_body
            )
        """Publish only novel"""
        break
    """Return to request"""
    return success_response_service(
        data=_novels_posts
    )


def create_requests_email_body_en(novel, posts):
    """Create email body"""
    _content = "<html><head></head><body><table width=\"500\" height=\"38\" align=\"center\" border=\"0\" cellspacing=\"0\" cellpadding=\"0\" style=\"border-top-left-radius:2px;border-top-right-radius:2px\"><tbody><tr><td width=\"500\" valign=\"middle\" align=\"center\" style=\"font-family: monospace;font-weight: 400;\"><h1>Light Novel PDF</h1></td></tr></tbody><tbody><tr><td width=\"500\" valign=\"middle\" align=\"left\"><p>Dear user,</p> <br/><p>Welcome to Light Novel PDF!</p><p>Please follow the links to visit your novels request about <b>{0}</b>, if you have any questions please tell us.</p> <br/><p>Thanks for visiting us!</p><p>Best regards,</p><p>Light Novel PDF Team</p></td></tr><tr><td> <br/><hr></td></tr></tbody></table><table width=\"500\" height=\"38\" bgcolor=\"#313640\" align=\"center\" border=\"0\" cellspacing=\"0\" cellpadding=\"0\" style=\"border-top-left-radius:2px;border-top-right-radius:2px\"><tbody><tr><td width=\"20\"></td><td width=\"440\" valign=\"middle\" align=\"left\"><h3 style=\"color:#ffffff;font-size:11px;line-height:11px;font-weight:bold;padding:0;margin:0\"> TITLE</h3></td><td width=\"20\"></td><td width=\"130\" valign=\"middle\" align=\"center\"><h3 style=\"color:#ffffff;font-size:11px;line-height:11px;font-weight:bold;padding:0;margin:0\"> URL</h3></td><td width=\"20\"></td></tr></tbody></table>".\
        format(novel["info"]['title'])
    _content += "<table width=\"500\" align=\"center\" bgcolor=\"#ffffff\" border=\"0\" cellspacing=\"0\" cellpadding=\"0\" style=\"border:1px solid #cccccc\"><tbody>"
    for _post in posts:
        _content += "<tr><td width=\"20\"><img src=\"{5}\" style=\" width: 50px; margin: 10px 10px 10px 10px; \"></td><td width=\"440\" height=\"86\" valign=\"top\" align=\"left\" style=\"padding:16px 0\"> <a href=\"{0}\" style\"color:#0070bf;font-weight:bold;font-size:16px;line-height:18px;padding:0;margin:0\" target=\"_blank\">{1}</a><div style=\"color:#404040;font-size:5px;line-height:5px;padding:0;margin:0\">&nbsp;</div><div style=\"color:#404040;font-size:12px;line-height:14px;padding:0;margin:0\">Volume {2} - Chapter {3}</div><div style=\"color:#404040;font-size:5px;line-height:5px;padding:0;margin:0\">&nbsp;</div><div style=\"color:#808080;font-size:12px;line-height:16px;padding:0;margin:0\"><span style=\"color:#404040;font-weight:bold\">Author: </span> {4}</div></td><td width=\"20\"></td><td width=\"130\" align=\"left\" valign=\"top\" style=\"padding:16px 0\"><table width=\"130\" align=\"center\" cellpadding=\"0\" cellspacing=\"0\" style=\"font-family:Arial,sans-serif;margin:0;padding:0\"><tbody><tr><td align=\"center\" style=\"margin:0;line-height:18px;font-size:14px;text-align:center\"><a href=\"{0}\" style=\"font-size:14px;text-decoration:none;color:#ffffff;font-weight:bold;padding:8px 14px;display:block;background-color:#77be53;border-radius:2px\" target=\"_blank\"> See Novel </a></td></tr></tbody></table></td><td width=\"20\"></td></tr>".\
            format(
                _post['link'], _post['title']['rendered'],
                _post['meta']['last_vol'], _post['meta']['last_ch'],
                _post['meta']['author'], _post['meta']['cover'],
            )
    _content += "</tbody></table></body></html>"
    return _content


def create_requests_email_body_es(novel, posts):
    """Create email body"""
    _content = "<html><head></head><body><table width=\"500\" height=\"38\" align=\"center\" border=\"0\" cellspacing=\"0\" cellpadding=\"0\" style=\"border-top-left-radius:2px;border-top-right-radius:2px\"><tbody><tr><td width=\"500\" valign=\"middle\" align=\"center\" style=\"font-family: monospace;font-weight: 400;\"><h1>Light Novel PDF</h1></td></tr></tbody><tbody><tr><td width=\"500\" valign=\"middle\" align=\"left\"><p>Querido usuario,</p> <br/><p>¡Bienvenido a Light Novel PDF!</p><p>Por favor sigue los siguientes enlaces para visitar las novelas relacionadas a <b>{0}</b>, si tienes alguna duda o sugerencia, por favor escríbenos.</p> <br/><p>¡Gracias por visitarnos!</p><p>Saludos,</p><p>Equipo Light Novel PDF</p></td></tr><tr><td> <br/><hr></td></tr></tbody></table><table width=\"500\" height=\"38\" bgcolor=\"#313640\" align=\"center\" border=\"0\" cellspacing=\"0\" cellpadding=\"0\" style=\"border-top-left-radius:2px;border-top-right-radius:2px\"><tbody><tr><td width=\"20\"></td><td width=\"440\" valign=\"middle\" align=\"left\"><h3 style=\"color:#ffffff;font-size:11px;line-height:11px;font-weight:bold;padding:0;margin:0\"> TÍTULO</h3></td><td width=\"20\"></td><td width=\"130\" valign=\"middle\" align=\"center\"><h3 style=\"color:#ffffff;font-size:11px;line-height:11px;font-weight:bold;padding:0;margin:0\"> URL</h3></td><td width=\"20\"></td></tr></tbody></table>".\
        format(novel["info"]['title'])
    _content += "<table width=\"500\" align=\"center\" bgcolor=\"#ffffff\" border=\"0\" cellspacing=\"0\" cellpadding=\"0\" style=\"border:1px solid #cccccc\"><tbody>"
    for _post in posts:
        _content += "<tr><td width=\"20\"><img src=\"{5}\" style=\" width: 50px; margin: 10px 10px 10px 10px; \"></td><td width=\"440\" height=\"86\" valign=\"top\" align=\"left\" style=\"padding:16px 0\"> <a href=\"{0}\" style\"color:#0070bf;font-weight:bold;font-size:16px;line-height:18px;padding:0;margin:0\" target=\"_blank\">{1}</a><div style=\"color:#404040;font-size:5px;line-height:5px;padding:0;margin:0\">&nbsp;</div><div style=\"color:#404040;font-size:12px;line-height:14px;padding:0;margin:0\">Volumen {2} - Capítulo {3}</div><div style=\"color:#404040;font-size:5px;line-height:5px;padding:0;margin:0\">&nbsp;</div><div style=\"color:#808080;font-size:12px;line-height:16px;padding:0;margin:0\"><span style=\"color:#404040;font-weight:bold\">Autor: </span> {4}</div></td><td width=\"20\"></td><td width=\"130\" align=\"left\" valign=\"top\" style=\"padding:16px 0\"><table width=\"130\" align=\"center\" cellpadding=\"0\" cellspacing=\"0\" style=\"font-family:Arial,sans-serif;margin:0;padding:0\"><tbody><tr><td align=\"center\" style=\"margin:0;line-height:18px;font-size:14px;text-align:center\"><a href=\"{0}\" style=\"font-size:14px;text-decoration:none;color:#ffffff;font-weight:bold;padding:8px 14px;display:block;background-color:#77be53;border-radius:2px\" target=\"_blank\"> Ver Novela </a></td></tr></tbody></table></td><td width=\"20\"></td></tr>".\
            format(
                _post['link'], _post['title']['rendered'],
                _post['meta']['last_vol'], _post['meta']['last_ch'],
                _post['meta']['author'], _post['meta']['cover'],
            )
    _content += "</tbody></table></body></html>"
    return _content
