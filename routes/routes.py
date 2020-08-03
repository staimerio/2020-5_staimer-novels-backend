# Retic
from retic import Router

# Controllers
import controllers.novels_en as novels_en
import controllers.novels_requests as novels_requests
import controllers.languages as languages

router = Router()

# Novels EN
router.post("/novels/latest/en", novels_en.publish_latest)

# Routes for requests
router \
    .post("/novels/requests", novels_requests.requests) \
    .get("/novels/requests", novels_requests.get_all_requests)

# Routes for publish requests
router \
    .post("/novels/requests/publish", novels_requests.publish_requests)

# Routes for languages
router \
    .get("/novels/languages", languages.get_all_languages)
