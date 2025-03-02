from api.server.routes import ping
from fastapi import APIRouter

router = APIRouter(prefix="/api")
router.include_router(ping.router)
