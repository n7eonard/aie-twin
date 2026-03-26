"""
backend/test_main.py
Run: pytest backend/test_main.py -v
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from starlette.testclient import TestClient

from backend.main import app

# ── Mock factory ─────────────────────────────────────────────────────────────
MOCK_ANT_OK = {
    "id": "msg_test",
    "type": "message",
    "role": "assistant",
    "content": [{"type": "text", "text": '{"intro":"Test","selections":[]}'}],
    "model": "claude-haiku-4-5",
    "stop_reason": "end_turn",
    "usage": {"input_tokens": 10, "output_tokens": 20},
}


def mock_http(status: int = 200, body: dict | None = None) -> AsyncMock:
    resp = MagicMock()
    resp.status_code = status
    resp.json.return_value = body or MOCK_ANT_OK
    client = AsyncMock()
    client.post = AsyncMock(return_value=resp)
    return client


# Skill: TestClient sends host "testclient" — add it to allowed_hosts in tests
# Done via raise_server_exceptions=True and patching ALLOWED_HOSTS in config
TEST_CLIENT_KWARGS = dict(
    base_url="http://testclient",
    raise_server_exceptions=True,
)

# ── Health ────────────────────────────────────────────────────────────────────
class TestHealth:
    def test_ok(self):
        # Skill: 'with TestClient(app)' triggers lifespan
        with TestClient(app, **TEST_CLIENT_KWARGS) as c:
            r = c.get("/health")
        assert r.status_code == 200
        assert r.json() == {"status": "ok"}

    def test_method_not_allowed(self):
        with TestClient(app, **TEST_CLIENT_KWARGS) as c:
            r = c.post("/health")
        assert r.status_code == 405


# ── Chat validation ───────────────────────────────────────────────────────────
class TestChatValidation:
    def test_missing_messages_field(self):
        with TestClient(app, **TEST_CLIENT_KWARGS) as c:
            r = c.post("/api/chat", json={"model": "claude-haiku-4-5"})
        assert r.status_code == 400
        assert "messages" in r.json()["error"]

    def test_empty_messages_list(self):
        with TestClient(app, **TEST_CLIENT_KWARGS) as c:
            r = c.post("/api/chat", json={"messages": []})
        assert r.status_code == 400

    def test_invalid_json(self):
        with TestClient(app, **TEST_CLIENT_KWARGS) as c:
            r = c.post(
                "/api/chat",
                content=b"not-json",
                headers={"Content-Type": "application/json"},
            )
        assert r.status_code == 400

    def test_messages_not_a_list(self):
        with TestClient(app, **TEST_CLIENT_KWARGS) as c:
            r = c.post("/api/chat", json={"messages": "hello"})
        assert r.status_code == 400


# ── Chat happy path ───────────────────────────────────────────────────────────
# Starlette bakes the lifespan into the router at construction time, so
# patching backend.main.lifespan after the fact has no effect.
# Correct approach: patch httpx.AsyncClient.post directly — the real lifespan
# creates a genuine client, but its .post is intercepted by the mock.
class TestChatProxy:
    def test_successful_proxy(self):
        resp = MagicMock()
        resp.status_code = 200
        resp.json.return_value = MOCK_ANT_OK
        with patch("httpx.AsyncClient.post", new=AsyncMock(return_value=resp)):
            with TestClient(app, **TEST_CLIENT_KWARGS) as c:
                r = c.post(
                    "/api/chat",
                    json={"messages": [{"role": "user", "content": "hello"}]},
                )
        assert r.status_code == 200
        assert "content" in r.json()

    def test_anthropic_error_becomes_502(self):
        resp = MagicMock()
        resp.status_code = 429
        resp.json.return_value = {"error": {"message": "Rate limit exceeded"}}
        with patch("httpx.AsyncClient.post", new=AsyncMock(return_value=resp)):
            with TestClient(app, **TEST_CLIENT_KWARGS) as c:
                r = c.post(
                    "/api/chat",
                    json={"messages": [{"role": "user", "content": "hello"}]},
                )
        assert r.status_code == 502
        assert "Rate limit" in r.json()["error"]


# ── CORS ──────────────────────────────────────────────────────────────────────
class TestCORS:
    def test_cors_header_on_allowed_origin(self):
        with TestClient(app, **TEST_CLIENT_KWARGS) as c:
            r = c.get("/health", headers={"Origin": "http://localhost:3000"})
        assert r.status_code == 200
        assert "access-control-allow-origin" in r.headers

    def test_options_preflight(self):
        with TestClient(app, **TEST_CLIENT_KWARGS) as c:
            r = c.options(
                "/api/chat",
                headers={
                    "Origin": "http://localhost:3000",
                    "Access-Control-Request-Method": "POST",
                },
            )
        # CORSMiddleware handles OPTIONS
        assert r.status_code in (200, 204)


# ── Schema ────────────────────────────────────────────────────────────────────
class TestSchema:
    def test_openapi_schema_returns_yaml(self):
        # OpenAPIResponse returns YAML (application/vnd.oai.openapi), not JSON
        with TestClient(app, **TEST_CLIENT_KWARGS) as c:
            r = c.get("/api/schema")
        assert r.status_code == 200
        assert "openapi" in r.headers.get("content-type", "")
        assert "openapi:" in r.text or "openapi: " in r.text
        assert "paths:" in r.text
