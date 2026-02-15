from sqlalchemy.orm import Query
from sqlalchemy import asc, desc


def apply_sorting(query: Query, model, sort_by: str | None, sort_order: str):
    if sort_by and hasattr(model, sort_by):
        column = getattr(model, sort_by)
        if sort_order == "desc":
            query = query.order_by(desc(column))
        else:
            query = query.order_by(asc(column))
    return query


def apply_pagination(query: Query, offset: int, page_size: int):
    return query.offset(offset).limit(page_size)