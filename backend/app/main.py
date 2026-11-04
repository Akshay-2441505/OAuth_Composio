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

@app.get("/")
def root():
    return {
        "name": "OAuth Compass API",
        "docs_url": "/docs",
        "health_url": "/api/health",
        "apps_url": "/api/apps",
    }
