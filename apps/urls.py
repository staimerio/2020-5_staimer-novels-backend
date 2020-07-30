# Retic
from retic import App as app

"""Define all other apps"""
BACKEND_MTLNOVEL = {
    u"base_url": app.config.get('APP_BACKEND_MTLNOVEL'),
    u"novels_latest": "/novels/latest",
    u"novels_chapters": "/novels/chapters",
}

BACKEND_EPUB = {
    u"base_url": app.config.get('APP_BACKEND_EPUB'),
    u"build_from_html": "/build/from-html",
    u"downloads": "/downloads",
}

BACKEND_PDF = {
    u"base_url": app.config.get('APP_BACKEND_PDF'),
    u"build_from_epub": "/build/from-epub",
}

BACKEND_MOBI = {
    u"base_url": app.config.get('APP_BACKEND_MOBI'),
    u"build_from_epub": "/build/from-epub",
}

BACKEND_SENDFILES = {
    u"base_url": app.config.get('APP_BACKEND_SENDFILES'),
    u"files": "/files",
    u"folders": "/folders",
}

BACKEND_LNPDF = {
    u"base_url": app.config.get('APP_BACKEND_LNPDF'),
    u"posts": "/posts",
}

BACKEND_IMAGES = {
    u"base_url": app.config.get('APP_BACKEND_IMAGES'),
    u"images_remote": "/images/remote",
}

APP_BACKEND = {
    u"mtlnovel": BACKEND_MTLNOVEL,
    u"epub": BACKEND_EPUB,
    u"pdf": BACKEND_PDF,
    u"mobi": BACKEND_MOBI,
    u"sendfiles": BACKEND_SENDFILES,
    u"lnpdf": BACKEND_LNPDF,
    u"images": BACKEND_IMAGES
}

"""Add Backend apps"""
app.use(APP_BACKEND, "backend")
