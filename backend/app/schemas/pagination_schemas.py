from typing import List

from pydantic import BaseModel

from app.schemas import BaseSchema


class PaginationSchema[T: BaseSchema](BaseModel):
    items: List[T]
    page: int
    last_page: int
    first_page: int = 1
    total_pages: int
    total_items: int
    items_by_page: int
    has_next_page: bool
    has_prev_page: bool
