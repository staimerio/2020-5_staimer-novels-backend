# Retic
from retic import env, App as app

# Constants
URL_NOVELFULL_CHAPTERS = app.apps['backend']['novelfull']['base_url'] + \
    app.apps['backend']['novelfull']['novels_chapters']
URL_MTLNOVEL_CHAPTERS = app.apps['backend']['mtlnovel']['base_url'] + \
    app.apps['backend']['mtlnovel']['novels_chapters']


def get_ur_chapters_from_site(site):
    """Get an MTLNovel instance from a language"""
    if site == "mtlnovelcom":
        return URL_MTLNOVEL_CHAPTERS
    elif site == "esmtlnovelcom":
        return URL_MTLNOVEL_CHAPTERS
    elif site == "novelfullcom":
        return URL_NOVELFULL_CHAPTERS
    elif site == "idmtlnovelcom":
        return URL_MTLNOVEL_CHAPTERS
    raise ValueError("Site {0} is invalid.".format(site))
