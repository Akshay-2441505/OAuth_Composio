import pytest
from app.schemas.guide import GuideSchema
from app.seeds.data_github import GITHUB_GUIDE_CONTENT
from app.seeds.data_google import GOOGLE_GUIDE_CONTENT
from app.seeds.data_slack import SLACK_GUIDE_CONTENT

def test_github_seed_conforms_to_guide_schema():
    guide = GuideSchema.model_validate(GITHUB_GUIDE_CONTENT)
    assert guide.app.name == "GitHub"
    assert guide.readiness.complexity == "medium"
    assert guide.time_estimates.active_setup.confidence in ["low", "medium", "high"]
    assert len(guide.steps) > 0
    assert len(guide.sources) > 0
    # Check that GitHub App vs OAuth App distinction is explicit in steps
    step_titles = [s.title for s in guide.steps]
    assert any("GitHub App vs. OAuth App" in title for title in step_titles)

def test_google_seed_conforms_to_guide_schema():
    guide = GuideSchema.model_validate(GOOGLE_GUIDE_CONTENT)
    assert guide.app.name == "Google Workspace & Cloud"
    assert guide.readiness.complexity == "high"
    assert guide.approval.required == "conditional"
    assert len(guide.steps) > 0
    assert len(guide.sources) > 0

def test_slack_seed_conforms_to_guide_schema():
    guide = GuideSchema.model_validate(SLACK_GUIDE_CONTENT)
    assert guide.app.name == "Slack"
    assert guide.readiness.complexity == "medium"
    assert guide.time_estimates.external_wait.status == "none"
    assert len(guide.steps) > 0
    assert len(guide.sources) > 0

def test_evidence_refs_exist_in_sources():
    for content in [GITHUB_GUIDE_CONTENT, GOOGLE_GUIDE_CONTENT, SLACK_GUIDE_CONTENT]:
        guide = GuideSchema.model_validate(content)
        source_ids = {s.id for s in guide.sources}
        for step in guide.steps:
            for ref in step.evidence_refs:
                assert ref in source_ids, f"Ref {ref} missing from sources in {guide.app.name}"
        for blocker in guide.blockers:
            for ref in blocker.evidence_refs:
                assert ref in source_ids, f"Ref {ref} missing from sources in {guide.app.name}"

