from datetime import datetime
from fastapi import APIRouter
from sqlalchemy.orm import Session
from uuid import uuid4

from api.lib.api.models.ping import PingList, PingRequest, PingResponse
from api.lib.db.sql import engine
import api.lib.db.sql.models as sql
from api.lib.api.page import SortedPageInfo

router = APIRouter(prefix="/ping", tags=["Ping"])


@router.post("/", response_model=PingResponse)
def ping(req: PingRequest) -> PingResponse:
    with Session(engine) as s:
        p = sql.Ping(
            id=str(uuid4()),
            data=req.data,
            timestamp=datetime.now(),
        )
        s.add(p)
        s.commit()
        return PingResponse(
            id=p.id,
            data=p.data,
            timestamp=p.timestamp,
        )


@router.get("/")
def get_pings(page_info: SortedPageInfo) -> PingList:
    with Session(engine) as s:
        query = s.query(sql.Ping)
        page, rows = page_info.apply(query, sql.Ping.timestamp)
        return PingList(
            results=[PingResponse.from_sql(r) for r in rows],
            **page,
        )
