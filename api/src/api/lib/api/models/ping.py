from datetime import datetime
from api.lib.api.models.common import APIModel, Page
import api.lib.db.sql.models as sql


class PingRequest(APIModel):
    data: str


class PingResponse(APIModel):
    id: str
    data: str
    timestamp: datetime

    @staticmethod
    def from_sql(m: sql.Ping) -> "PingResponse":
        return PingResponse(
            id=m.id,
            data=m.data,
            timestamp=m.timestamp,
        )


class PingList(Page):
    results: list[PingResponse]
