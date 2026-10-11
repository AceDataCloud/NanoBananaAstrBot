"""Single-image Nano Banana transport and terminal-result boundaries."""

from __future__ import annotations

import json
from unittest.mock import patch

import pytest

from client import NanoBananaClient, NanoBananaError


class FakeResponse:
    def __init__(self, payload: dict) -> None:
        self.payload = payload
        self.headers = {"x-trace-id": "trace-banana"}

    def __enter__(self):
        return self

    def __exit__(self, *_):
        return False

    def read(self, *_):
        return json.dumps(self.payload).encode()


@pytest.mark.asyncio
async def test_generate_submits_one_async_image():
    calls = []

    def fake_open(request, timeout):
        calls.append((request.full_url, json.loads(request.data), timeout))
        return FakeResponse({"task_id": "task-123"})

    with patch("client.OPENER.open", side_effect=fake_open):
        result = await NanoBananaClient("test-key").submit("A yellow paper boat")
    assert calls == [
        (
            "https://api.acedata.cloud/nano-banana/images",
            {
                "action": "generate",
                "prompt": "A yellow paper boat",
                "model": "nano-banana-2-lite",
                "aspect_ratio": "1:1",
                "resolution": "1K",
                "count": 1,
                "async": True,
            },
            90,
        )
    ]
    assert result["status"] == "submitted"
    assert result["task_id"] == "task-123"
    assert "image_urls" not in result


@pytest.mark.asyncio
async def test_edit_uses_authorized_https_reference_and_official_model():
    with patch(
        "client.OPENER.open", return_value=FakeResponse({"task_id": "task-456"})
    ) as opening:
        await NanoBananaClient("test-key").submit(
            "Make the boat blue",
            model="nano-banana-2:official",
            aspect_ratio="16:9",
            resolution="2K",
            image_url="https://example.org/boat.png",
        )
    payload = json.loads(opening.call_args.args[0].data)
    assert payload["action"] == "edit"
    assert payload["image_urls"] == ["https://example.org/boat.png"]
    assert payload["model"] == "nano-banana-2:official"


@pytest.mark.asyncio
async def test_lookup_withholds_preview_until_finished():
    submitted = {"id": "task-123", "trace_id": "trace-banana"}
    preview = {
        "finished_at": None,
        "response": {
            "success": True,
            "data": [{"image_url": "https://cdn.example.org/preview.png"}],
        },
    }
    finished = {
        "finished_at": 123.0,
        "response": {
            "success": True,
            "data": [{"image_url": "https://cdn.example.org/final.png"}],
            "supplier": "internal-only",
        },
    }
    with patch(
        "client.OPENER.open",
        side_effect=[
            FakeResponse(submitted),
            FakeResponse(preview),
            FakeResponse(finished),
        ],
    ) as opening:
        first = await NanoBananaClient("test-key").query("task-123")
        second = await NanoBananaClient("test-key").query("task-123")
        last = await NanoBananaClient("test-key").query("task-123")
    assert opening.call_count == 3
    assert first["status"] == second["status"] == "pending"
    assert first["image_urls"] == second["image_urls"] == []
    assert last["status"] == "succeeded"
    assert last["image_urls"] == ["https://cdn.example.org/final.png"]
    assert "supplier" not in str(last)


@pytest.mark.asyncio
async def test_invalid_input_never_submits_a_paid_job():
    with patch("client.OPENER.open") as opening, pytest.raises(NanoBananaError):
        await NanoBananaClient("test-key").submit(" ")
    assert opening.call_count == 0
    with patch("client.OPENER.open") as opening, pytest.raises(NanoBananaError):
        await NanoBananaClient("test-key").submit(
            "A boat", model="nano-banana-2-lite", resolution="2K"
        )
    assert opening.call_count == 0
    with patch("client.OPENER.open") as opening, pytest.raises(NanoBananaError):
        await NanoBananaClient("test-key").submit(
            "A boat", image_url="http://example.org/boat.png"
        )
    assert opening.call_count == 0
