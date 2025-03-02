import math
from dataclasses import dataclass
from enum import Enum
from typing import Annotated, Any, Generator, TypeVar
from collections.abc import Mapping

from fastapi import Depends
from sqlalchemy import desc
from sqlalchemy.orm import Query

T = TypeVar("T")
S = TypeVar("S")

MAX_PAGE_SIZE = 100


class SortDirection(str, Enum):
    Ascending = "asc"
    Descending = "desc"

    def apply(self, expr: Any):
        if self == SortDirection.Descending:
            return desc(expr)
        return expr


@dataclass
class PageResults(Mapping):
    page: int
    page_size: int
    total_pages: int

    def __getitem__(self, key: str):
        return getattr(self, key)

    def __iter__(self) -> Generator[str, None, None]:
        yield from ["page", "page_size", "total_pages"]

    def __len__(self) -> int:
        return 3


@dataclass
class PageParams:
    page: int
    page_size: int

    @property
    def offset(self) -> int:
        page = max(1, self.page)
        return self.limit * (page - 1)

    @property
    def limit(self) -> int:
        return min(self.page_size, MAX_PAGE_SIZE)

    def apply(
        self,
        query: Query[T],
    ) -> tuple[PageResults, list[T]]:
        page = PageResults(
            page=self.page,
            page_size=self.page_size,
            total_pages=math.ceil(query.count() / self.page_size),
        )
        query = query.offset(self.offset).limit(self.limit)

        return page, query.all()


@dataclass
class SortedPageParams(PageParams):
    sort_direction: SortDirection

    def apply(self, query: Query[T], *order_fields: Any) -> tuple[PageResults, list[T]]:
        # apply orderings
        for f in order_fields:
            query = query.order_by(self.sort_direction.apply(f))
        return super().apply(query)


def page_params(
    page: int = 1,
    page_size: int = 20,
):
    return PageParams(page=page, page_size=page_size)


def sorted_page_params(
    page: int = 1,
    page_size: int = 20,
    sort_direction: SortDirection = SortDirection.Descending,
):
    return SortedPageParams(page, page_size, sort_direction)


PageInfo = Annotated[PageParams, Depends(page_params)]
SortedPageInfo = Annotated[SortedPageParams, Depends(sorted_page_params)]
