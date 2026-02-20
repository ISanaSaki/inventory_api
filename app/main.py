from fastapi import FastAPI, Request
from starlette.responses import JSONResponse

from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.rate_limiter import limiter
from app.core.security_headers import SecurityHeadersMiddleware

from app.auth.router import router as auth_router
from app.categories.router import router as categories_router
from app.products.router import router as products_router
from app.inventory.router import router as inventory_router
from app.suppliers.router import router as suppliers_router
from app.reports.router import router as reports_router
from app.audit.router import router as audit_router

app = FastAPI(title=settings.APP_NAME)

# ---- Rate limiting ----
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)

@app.exception_handler(RateLimitExceeded)
def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"detail": "Too many requests. Please try again later."},
    )

# ---- Security headers ----
app.add_middleware(SecurityHeadersMiddleware)

# ---- CORS hardening ----
ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    # "https://your-frontend.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=False,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
    max_age=600,
)

# ---- Routers ----
app.include_router(auth_router)
app.include_router(categories_router)
app.include_router(products_router)
app.include_router(inventory_router)
app.include_router(suppliers_router)
app.include_router(reports_router)
app.include_router(audit_router)