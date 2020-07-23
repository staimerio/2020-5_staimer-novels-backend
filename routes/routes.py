# Retic
from retic import Router

# Controllers
import controllers.novels_en as novels_en

router = Router()

# Novels EN
router.post("/novels/latest/en", novels_en.publish_latest)
