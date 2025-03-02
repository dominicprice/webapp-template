from pydantic import BaseModel
from pydantic.alias_generators import to_camel


class APIModel(BaseModel):
    class Config:
        alias_generator = to_camel
        populate_by_name = True


class Page(APIModel):
    page: int
    page_size: int
    total_pages: int
