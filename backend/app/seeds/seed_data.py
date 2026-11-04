import uuid
from datetime import datetime, timezone
from sqlalchemy.orm import Session

from app.models.app import App
from app.models.guide import Guide
from app.models.source import Source
from app.seeds.data_github import GITHUB_APP, GITHUB_SOURCES, GITHUB_GUIDE_CONTENT
from app.seeds.data_google import GOOGLE_APP, GOOGLE_SOURCES, GOOGLE_GUIDE_CONTENT
from app.seeds.data_slack import SLACK_APP, SLACK_SOURCES, SLACK_GUIDE_CONTENT

SEEDS = [
    (GITHUB_APP, GITHUB_SOURCES, GITHUB_GUIDE_CONTENT),
    (GOOGLE_APP, GOOGLE_SOURCES, GOOGLE_GUIDE_CONTENT),
    (SLACK_APP, SLACK_SOURCES, SLACK_GUIDE_CONTENT),
]

def seed_database(db: Session):
    for app_data, sources_data, guide_content in SEEDS:
        existing_app = db.query(App).filter(App.slug == app_data["slug"]).first()
        if not existing_app:
            app_id = str(uuid.uuid4())
            new_app = App(
                id=app_id,
                slug=app_data["slug"],
                name=app_data["name"],
                website_url=app_data["website_url"],
                provider_domain=app_data["provider_domain"],
                category=app_data["category"],
                auth_types=app_data["auth_types"],
                managed_oauth_status=app_data["managed_oauth_status"],
                managed_oauth_source_url=app_data["managed_oauth_source_url"],
            )
            db.add(new_app)
            db.flush()

            guide_id = f"guide_{app_data['slug']}"
            new_guide = Guide(
                id=guide_id,
                app_id=new_app.id,
                slug=app_data["slug"],
                origin="seeded",
                status="validated",
                content_json=guide_content,
                version=1,
                last_researched_at=datetime.now(timezone.utc),
                is_public=True,
            )
            db.add(new_guide)
            db.flush()

            for s in sources_data:
                source = Source(
                    id=s["id"],
                    guide_id=new_guide.id,
                    title=s["title"],
                    url=s["url"],
                    domain=s["domain"],
                    source_type=s["source_type"],
                    is_official=s["is_official"],
                    retrieved_at=datetime.now(timezone.utc),
                    http_status=s["http_status"],
                    fetch_status=s["fetch_status"],
                    relevance_note=s["relevance_note"],
                )
                db.add(source)

            db.commit()

