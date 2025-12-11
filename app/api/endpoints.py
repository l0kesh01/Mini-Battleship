from fastapi import APIRouter
from app.game.services.game_service import game_router  # now this works

router = APIRouter()

@router.get("/ping")
def ping():
    return {"status": "ok"}

# Include all game routes under /game
router.include_router(game_router, prefix="/game", tags=["Game"])
