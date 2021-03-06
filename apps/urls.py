# Retic
from retic import App as app

"""Define all other apps"""
BACKEND_MTLNOVEL = {
    u"base_url": app.config.get('APP_BACKEND_MTLNOVEL'),
    u"novels_latest": "/novels/latest",
    u"novels_chapters": "/novels/chapters",
    u"novels_search": "/novels",
}

BACKEND_NOVELFULL = {
    u"base_url": app.config.get('APP_BACKEND_NOVELFULL'),
    u"novels_search": "/novels",
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
    # u"build_from_epub": "/build/from-epub2pdf",
    u"build_from_html": "/build/from-html",
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

BACKEND_EMAIL = {
    u"base_url": app.config.get('APP_BACKEND_EMAIL'),
    u"emails": "/emails",
}

BACKEND_RANOBELIB = {
    u"base_url": app.config.get('APP_BACKEND_RANOBELIB'),
    u"novels_latest": "/novels/latest",
    u"novels_chapters": "/novels/chapters",
}
BACKEND_NOVELLELEGGERE = {
    u"base_url": app.config.get('APP_BACKEND_NOVELLELEGGERE'),
    u"novels_latest": "/novels/latest",
    u"novels_chapters": "/novels/chapters",
}

APP_LNPDF = {
    u"base_url": app.config.get('APP_APP_LNPDF'),
    u"proxy_images": "/proxyimages.php",
}
APP_BACKEND = {
    u"mtlnovel": BACKEND_MTLNOVEL,
    u"epub": BACKEND_EPUB,
    u"pdf": BACKEND_PDF,
    u"mobi": BACKEND_MOBI,
    u"sendfiles": BACKEND_SENDFILES,
    u"lnpdf": BACKEND_LNPDF,
    u"images": BACKEND_IMAGES,
    u"novelfull": BACKEND_NOVELFULL,
    u"email": BACKEND_EMAIL,
    u"ranobelib": BACKEND_RANOBELIB,
    u"apilnpdf": APP_LNPDF,
    u"novelleleggere": BACKEND_NOVELLELEGGERE,
}

"""Add Backend apps"""
app.use(APP_BACKEND, "backend")
