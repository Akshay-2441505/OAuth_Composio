import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import engine, Base, SessionLocal
from app.seeds.seed_data import seed_database
from app.models.research_run import ResearchRun
from app.routers import health, apps, guides, research

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("oauth_compass")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: create tables and seed default data
    logger.info("Initializing database tables...")
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_database(db)
        logger.info("Database seeding completed.")
        
        # Stale run recovery: mark any orphaned research runs from an interrupted session as failed
        in_flight_statuses = ["queued", "identify", "search", "fetch", "analyze", "validate"]
        stale_runs = (
            db.query(ResearchRun)
            .filter(ResearchRun.status.in_(in_flight_statuses))
            .all()
        )
        for r in stale_runs:
            r.status = "failed"
            r.error_message = "Research run was interrupted by a server restart."
            logs = list(r.stage_log_json or [])
            logs.append({
                "name": "interrupted",
                "status": "failed",
                "message": "Research run was interrupted by a server restart.",
            })
            r.stage_log_json = logs
        if stale_runs:
            db.commit()
            logger.info(f"Recovered {len(stale_runs)} orphaned research runs.")
    finally:
        db.close()
    yield

app = FastAPI(
    title="OAuth Compass API",
    description="Developer readiness and research layer for OAuth integrations",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS middleware with configurable origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router)
app.include_router(apps.router)
app.include_router(guides.router)
app.include_router(research.router)

import os
from fastapi import Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# Check for production static build (e.g. Docker container or local frontend/dist)
_static_dir = os.path.join(os.path.dirname(__file__), "static")
if not os.path.isdir(_static_dir):
    _candidate = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "frontend", "dist"))
    if os.path.isdir(_candidate):
        _static_dir = _candidate

SPA_PREFIXES = ("overview", "apps", "guides", "generate", "runs", "saved")

@app.get("/")
def root(request: Request):
    accept = request.headers.get("accept", "")
    if "text/html" in accept and os.path.isdir(_static_dir):
        index_file = os.path.join(_static_dir, "index.html")
        if os.path.isfile(index_file):
            return FileResponse(index_file)
    return {
        "name": "OAuth Compass API",
        "docs_url": "/docs",
        "health_url": "/api/health",
        "apps_url": "/api/apps",
    }

if os.path.isdir(_static_dir):
    _assets_dir = os.path.join(_static_dir, "assets")
    if os.path.isdir(_assets_dir):
        app.mount("/assets", StaticFiles(directory=_assets_dir), name="assets")

    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        if full_path.startswith("api/") or full_path == "api":
            raise HTTPException(status_code=404, detail="API route not found")

        file_path = os.path.join(_static_dir, full_path)
        if full_path and os.path.isfile(file_path):
            return FileResponse(file_path)

        if any(full_path == p or full_path.startswith(f"{p}/") for p in SPA_PREFIXES):
            index_file = os.path.join(_static_dir, "index.html")
            if os.path.isfile(index_file):
                return FileResponse(index_file)

        raise HTTPException(status_code=404, detail="Not found")
