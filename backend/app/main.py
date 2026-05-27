from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import time
import uuid
import logging

from app.core.config import settings
from app.core.database import Base, engine
from app.routers import session, auth, analytics

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level.upper(), logging.INFO),
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger("api")

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
)

# CORS middleware should be one of the outermost to catch everything
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    request_id = str(uuid.uuid4())[:8]
    start = time.perf_counter()

    logger.info(
        "req_start | id=%s method=%s path=%s",
        request_id,
        request.method,
        request.url.path,
    )

    try:
        response = await call_next(request)
    except Exception as e:
        logger.error("Unhandled error: %s", str(e), exc_info=True)
        raise e

    elapsed_ms = (time.perf_counter() - start) * 1000
    logger.info(
        "req_end   | id=%s status=%d elapsed=%.1fms",
        request_id,
        response.status_code,
        elapsed_ms,
    )

    response.headers["X-Request-ID"] = request_id
    return response

app.include_router(session.router, prefix="/api/v1")
app.include_router(analytics.router, prefix="/api/v1")
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])


@app.get("/health")
def health():
    return {"status": "ok", "version": settings.app_version}
