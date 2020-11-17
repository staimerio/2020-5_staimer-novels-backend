# Retic
from retic import Router

# Controllers
import controllers.novels_en as novels_en
import controllers.novels_es as novels_es
import controllers.novels_id as novels_id
import controllers.novels_fr as novels_fr
import controllers.novels_zh as novels_zh
import controllers.novels_requests as novels_requests
import controllers.novels_chapters as novels_chapters
import controllers.languages as languages
import controllers.feedback as feedback

router = Router()

# Novels EN
router.post("/novels/latest/en", novels_en.publish_latest)

# Novels ES
router.post("/novels/latest/es", novels_es.publish_latest)

# Novels ID
router.post("/novels/latest/id", novels_id.publish_latest)

# Novels FR
router.post("/novels/latest/fr", novels_fr.publish_latest)

# Novels ZH
router.post("/novels/latest/zh", novels_zh.publish_latest)

# Routes for requests
router \
    .post("/novels/requests", novels_requests.add_requests) \
    .get("/novels/requests", novels_requests.get_all_requests)

# Routes for publish requests
router \
    .post("/novels/requests/publish", novels_requests.publish_requests)

# Routes for languages
router \
    .get("/novels/languages", languages.get_all_languages)

# Routes for novels
router \
    .get("/novels/:novel", novels_chapters.get_chapters_by_novel)

# Routes for novels chapters
router \
    .get("/novels/chapters/:chapter", novels_chapters.get_chapter_by_id)

# Routes for requests
router \
    .post("/feedback", feedback.save_feedback)