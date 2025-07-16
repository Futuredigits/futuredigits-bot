from .life_path import router as life_path_router
from .soul_urge import router as soul_urge_router
from .expression import router as expression_router
from .personality import router as personality_router
from .destiny import router as destiny_router
from .birthday import router as birthday_router
from .compatibility import router as compatibility_router

all_routers = [
    life_path_router,
    soul_urge_router,
    expression_router,
    personality_router,
    destiny_router,
    birthday_router,
    compatibility_router,
]
