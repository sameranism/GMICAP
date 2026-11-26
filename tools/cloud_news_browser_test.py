"""Cloud-only smoke test: actual browser, built UI, API and disposable databases."""

from __future__ import annotations

import os
import socket
import threading
import time
from pathlib import Path
from uuid import uuid4

import psycopg
import pytest
import uvicorn
from alembic import command
from alembic.config import Config
from playwright.sync_api import expect, sync_playwright
from psycopg import sql
from sqlalchemy.engine import make_url
from starlette.staticfiles import StaticFiles

from backend.app.dependencies import build_services
from backend.app.main import create_app
from backend.core.auth import Principal, issue_session
from backend.core.permissions import Grant
from backend.modules.domestic.feed_client import FeedResponse, FixtureFeedTransport

ROOT = Path(__file__).resolve().parents[1]
SOURCE = "SRC-CLOUD-TEST"
FEED_URL = "https://example.invalid/rss"
TITLE = "Cloud integration fixture article"
RSS = b"""<rss version="2.0"><channel><title>Test feed</title>
<item><title>Cloud integration fixture article</title>
<link>https://example.invalid/news/cloud</link>
<description>Synthetic test article for real application code.</description>
</item></channel></rss>"""


def test_browser_reads_persistent_news(monkeypatch, tmp_path):
    admin_url = os.environ.get("ETEMAD_TEST_PG_ADMIN_URL")
    assert admin_url, "Disposable PostgreSQL must be configured"
    admin = make_url(admin_url)
    assert admin.host == "127.0.0.1" and admin.database == "postgres"
    assert admin.username == "fixture_admin" and not admin.query
    assert (ROOT / "frontend/dist/index.html").is_file(), "Build frontend first"
    suffix = uuid4().hex[:12]
    names = {role: f"etemad_test_{role}_{suffix}" for role in ("central", "domestic")}
    environ = {
        "ETEMAD_NEWS_STORAGE": "postgres",
        "ETEMAD_SESSION_KEY": uuid4().hex + uuid4().hex,
        "ETEMAD_FEED_MODE": "fixture",
        "ETEMAD_OBJECT_ROOT": str(tmp_path / "objects"),
    }
    created = []
    services = None
    server = None
    worker = None
    listener = None
    with psycopg.connect(admin_url, autocommit=True) as control:
        try:
            monkeypatch.chdir(ROOT / "backend")
            for role, name in names.items():
                control.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(name)))
                created.append(name)
                key = f"ETEMAD_DB_{role.upper()}_URL"
                environ[key] = admin.set(drivername="postgresql+psycopg", database=name).render_as_string(
                    hide_password=False
                )
                monkeypatch.setenv(key, environ[key])
            command.upgrade(Config("alembic.ini"), "head")
            command.upgrade(Config("alembic_domestic.ini"), "head")
            monkeypatch.chdir(ROOT)

            services = build_services(environ)
            services.sources.register({
                "source_id": SOURCE, "site_url": "https://example.invalid",
                "feed_url": FEED_URL, "api_base_url": None, "country": "IR",
                "language": "en", "stream": "domestic", "auth_ref": None,
                "license_scope": "summary", "enabled": True,
            })
            assert isinstance(services.transport, FixtureFeedTransport)
            services.transport.responses = {
                FEED_URL: FeedResponse(url=FEED_URL, status_code=200, body=RSS)
            }
            services.grants.grant(Grant("eic-cloud", "editor_in_chief", "source_registry", SOURCE, "poll"))
            services.grants.grant(Grant("eic-cloud", "editor_in_chief", "newsroom", "feed", "read"))
            token = issue_session(Principal("eic-cloud", "editor_in_chief"), services.session_key)
            denied = issue_session(Principal("staff-cloud", "staff"), services.session_key)
            app = create_app(services=services)
            app.mount("/", StaticFiles(directory=ROOT / "frontend/dist", html=True), name="ui")
            listener = socket.socket()
            listener.bind(("127.0.0.1", 0))
            port = listener.getsockname()[1]
            server = uvicorn.Server(uvicorn.Config(app, log_level="warning", access_log=False))
            worker = threading.Thread(target=server.run, kwargs={"sockets": [listener]}, daemon=True)
            worker.start()
            deadline = time.monotonic() + 15
            while not server.started and worker.is_alive() and time.monotonic() < deadline:
                time.sleep(0.05)
            assert server.started, "Loopback application did not start"
            origin = f"http://127.0.0.1:{port}"
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                try:
                    page = browser.new_page(viewport={"width": 1440, "height": 900})
                    requests = []
                    page.on("request", lambda request: requests.append(request.url))
                    page.goto(origin)
                    expect(page.locator("#session-token")).to_be_visible()
                    expect(page.get_by_text(TITLE, exact=True)).to_have_count(0)
                    response = page.request.post(
                        origin + f"/v1/ingest/{SOURCE}/poll",
                        headers={"Authorization": "Bearer " + token},
                    )
                    assert response.status == 200
                    assert response.json()["collected"] == 1
                    page.locator("#session-token").fill(denied)
                    page.get_by_role("button", name="اتصال", exact=True).click()
                    expect(page.get_by_role("alert")).to_have_text("دسترسی به این میز مجاز نیست.")
                    expect(page.get_by_text(TITLE, exact=True)).to_have_count(0)
                    page.get_by_role("button", name="قطع نشست", exact=True).click()
                    page.locator("#session-token").fill(token)
                    page.get_by_role("button", name="اتصال", exact=True).click()
                    expect(page.get_by_role("heading", name=TITLE, exact=True)).to_be_visible()
                    assert len(services.pipeline.repository) == len(services.pipeline.processed) == 1
                    page.get_by_role("button", name="خارجی", exact=True).click()
                    expect(page.get_by_text("در این جریان خبری نیست.", exact=True)).to_be_visible()
                    page.get_by_role("button", name="داخلی", exact=True).click()
                    expect(page.get_by_role("heading", name=TITLE, exact=True)).to_be_visible()
                    page.set_viewport_size({"width": 390, "height": 844})
                    expect(page.get_by_role("heading", name=TITLE, exact=True)).to_be_visible()
                    assert not any("/v1/demo/news" in url for url in requests)
                    output = ROOT / "cloud-browser-evidence"
                    output.mkdir(exist_ok=True)
                    page.screenshot(path=output / "newsroom-mobile.png", full_page=True)
                    page.get_by_role("button", name="قطع نشست", exact=True).click()
                    expect(page.locator("#session-token")).to_be_visible()
                    expect(page.get_by_text(TITLE, exact=True)).to_have_count(0)
                finally:
                    browser.close()
        finally:
            if server:
                server.should_exit = True
            if worker:
                worker.join(timeout=15)
            if listener:
                listener.close()
            if services:
                services.registry.dispose()
            for name in reversed(created):
                control.execute(sql.SQL("DROP DATABASE {} WITH (FORCE)").format(sql.Identifier(name)))
