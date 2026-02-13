from fastapi import FastAPI
from app.core.config import settings
from app.core.database import Base
from app.core.database import engine
from app.auth.router import router as auth_router
from app.categories.router import router as categories_router
from app.products.router import router as products_router
from app.inventory.router import router as inventory_router
from app.suppliers.router import router as suppliers_router
from app.reports.router import router as reports_router
from app.audit.router import router as audit_router

app = FastAPI(title=settings.APP_NAME)

app.include_router(auth_router)
app.include_router(categories_router)
app.include_router(products_router)
app.include_router(inventory_router)
app.include_router(suppliers_router)
app.include_router(reports_router)
app.include_router(audit_router)