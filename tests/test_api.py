import asyncio

import pytest
from fastapi.testclient import TestClient

from capstone.backend.api.router.chatbot import get_agent
from capstone.backend.app import app


@pytest.mark.asyncio
async def test_health_check(client: TestClient):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_root_redirect(client: TestClient):
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 307
    assert response.headers["location"] == "/docs"


def test_chatbot_infer(client: TestClient):
    # Mock the LangChain agent's invocation
    from unittest.mock import MagicMock

    mock_agent = MagicMock()
    # Mock ainvoke to return a future since it's awaited
    f = asyncio.Future()
    f.set_result({"refine": "This is a mocked answer."})
    mock_agent.ainvoke.return_value = f

    # Define the override generator
    def override_get_agent():
        yield mock_agent

    app.dependency_overrides[get_agent] = override_get_agent

    try:
        response = client.post("/chatbot/infer", json={"question": "What is Automation?"})
        assert response.status_code == 200
        assert "answer" in response.json()
        assert response.json()["answer"] == "This is a mocked answer."
    finally:
        del app.dependency_overrides[get_agent]
