from fastapi import APIRouter, Depends, HTTPException,Query
from sqlalchemy.orm import Session
from app.categories.schemas import CategoryCreate, CategoryOut,CategoryList
from app.categories.service import create_category, get_categories, get_category, update_category, delete_category
from app.core.database import get_db
from app.core.dependencies import require_role,pagination_params,sorting_params
from app.common.enums import Role

router = APIRouter(
    prefix="/categories",
    tags=["Categories"],
    dependencies=[
        Depends(require_role([Role.ADMIN]))
    ]
)

@router.post("/", response_model=CategoryOut)
def create_cat(category: CategoryCreate, db: Session = Depends(get_db)):
    try:
        return create_category(db, category)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=CategoryList)
def list_categories(
    db: Session = Depends(get_db),
    pagination: dict = Depends(pagination_params),
    sorting: dict = Depends(sorting_params),
    search: str | None = Query(None),
):
    return get_categories(
        db=db,
        page=pagination["page"],
        page_size=pagination["page_size"],
        offset=pagination["offset"],
        sort_by=sorting["sort_by"],
        sort_order=sorting["sort_order"],
        search=search,
    )

@router.get("/{category_id}", response_model=CategoryOut)
def retrieve_category(category_id: int, db: Session = Depends(get_db)):
    cat = get_category(db, category_id)
    if not cat:
        raise HTTPException(status_code=404, detail="Category not found")
    return cat

@router.put("/{category_id}", response_model=CategoryOut)
def update_cat(category_id: int, category: CategoryCreate, db: Session = Depends(get_db)):
    updated = update_category(db, category_id, category)
    if not updated:
        raise HTTPException(status_code=404, detail="Category not found")
    return updated

@router.delete("/{category_id}", response_model=CategoryOut)
def delete_cat(category_id: int, db: Session = Depends(get_db)):
    deleted = delete_category(db, category_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Category not found")
    return deleted