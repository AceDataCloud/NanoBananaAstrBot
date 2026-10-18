"""Single-image Nano Banana submission and task lookup for AstrBot."""

from __future__ import annotations

import asyncio
import json
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener

API_BASE = "https://api.acedata.cloud"
BASE_MODELS = {
    "nano-banana",
    "nano-banana-2-lite",
    "nano-banana-2",
    "nano-banana-pro",
}
MODELS = BASE_MODELS | {model + ":official" for model in BASE_MODELS}
BASE_RATIOS = {"21:9", "1:1", "4:3", "3:2", "2:3", "5:4", "4:5", "3:4", "16:9", "9:16"}
EXTRA_RATIOS = {"1:4", "4:1", "1:8", "8:1"}
HIGH_RESOLUTION_MODELS = {"nano-banana-2", "nano-banana-pro"}
FAILED = {"failed", "error", "cancelled", "canceled", "rejected"}


class _NoRedirect(HTTPRedirectHandler):
    """Never forward the configured key to a redirected destination."""

    def redirect_request(self, request, fp, code, msg, headers, newurl):
        """Reject every API redirect."""
        return


OPENER = build_opener(_NoRedirect)


class NanoBananaError(RuntimeError):
    """An error safe to return to an AstrBot conversation."""


def _valid_https_url(url: str) -> bool:
    try:
        parsed = urlsplit(url)
    except ValueError:
        return False
    return bool(
        parsed.scheme == "https"
        and parsed.netloc
        and not parsed.username
        and not parsed.password
    )


class NanoBananaClient:
    """Submit one image or query an existing Nano Banana task."""

    def __init__(self, api_key: str) -> None:
        token = api_key.strip()
        if (
            not token
            or token.lower().startswith("bearer ")
            or token.startswith("platform-")
        ):
            raise NanoBananaError(
                "Set an Ace Data Cloud generation API key in plugin settings."
            )
        self._api_key = token

    def _post(self, path: str, payload: dict[str, Any]) -> tuple[dict[str, Any], str]:
        request = Request(
            API_BASE + path,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": "Bearer " + self._api_key,
                "Accept": "application/json",
                "Content-Type": "application/json",
                "User-Agent": "AceDataCloudAstrBot/0.1.1",
            },
            method="POST",
        )
        try:
            with OPENER.open(request, timeout=90) as response:
                body = json.load(response)
                trace_id = response.headers.get(
                    "x-trace-id", ""
                ) or response.headers.get("x-request-id", "")
        except HTTPError as exc:
            raise NanoBananaError(
                f"Ace Data Cloud returned HTTP {exc.code}. Check service access and request history."
            ) from None
        except (URLError, TimeoutError, OSError):
            raise NanoBananaError(
                "The API connection failed. Check request history before submitting again."
            ) from None
        except (ValueError, UnicodeError):
            raise NanoBananaError(
                "The API returned invalid JSON. Check request history before retrying."
            ) from None
        if not isinstance(body, dict):
            raise NanoBananaError("The API returned an unexpected response format.")
        return body, str(body.get("trace_id") or trace_id)

    async def submit(
        self,
        prompt: str,
        model: str = "nano-banana-2-lite",
        aspect_ratio: str = "1:1",
        resolution: str = "1K",
        image_url: str = "",
    ) -> dict[str, Any]:
        """Submit one asynchronous image generation or edit without retrying."""
        prompt = prompt.strip()
        if not prompt or len(prompt) > 4000:
            raise NanoBananaError("Provide an image prompt of 1–4000 characters.")
        if model not in MODELS:
            raise NanoBananaError("Choose a supported Nano Banana model ID.")
        base_model = model.removesuffix(":official")
        allowed_ratios = BASE_RATIOS | (
            EXTRA_RATIOS
            if base_model in {"nano-banana-2", "nano-banana-2-lite"}
            else set()
        )
        if aspect_ratio not in allowed_ratios:
            raise NanoBananaError("Choose an aspect ratio supported by this model.")
        if resolution not in {"1K", "2K", "4K"} or (
            resolution != "1K" and base_model not in HIGH_RESOLUTION_MODELS
        ):
            raise NanoBananaError("Choose a resolution supported by this model.")
        if image_url and not _valid_https_url(image_url):
            raise NanoBananaError("Provide an authorized HTTPS reference image URL.")
        payload: dict[str, Any] = {
            "action": "edit" if image_url else "generate",
            "prompt": prompt,
            "model": model,
            "aspect_ratio": aspect_ratio,
            "resolution": resolution,
            "count": 1,
            "async": True,
        }
        if image_url:
            payload["image_urls"] = [image_url]
        body, trace_id = await asyncio.to_thread(
            self._post, "/nano-banana/images", payload
        )
        if body.get("success") is False or body.get("error"):
            raise NanoBananaError(
                "Image submission was rejected. Check request history before trying again."
            )
        task_id = body.get("task_id")
        if not isinstance(task_id, str) or not task_id:
            raise NanoBananaError(
                "No task ID was returned. Check request history before submitting again."
            )
        return {
            "status": "submitted",
            "task_id": task_id,
            "trace_id": trace_id,
            "next_step": "Query this same task ID; do not submit another image while it is pending.",
        }

    async def query(self, task_id: str) -> dict[str, Any]:
        """Return final image URLs only after the existing task finishes."""
        task_id = task_id.strip()
        if not task_id or len(task_id) > 128:
            raise NanoBananaError("Pass the exact task ID from Nano Banana submission.")
        body, trace_id = await asyncio.to_thread(
            self._post,
            "/nano-banana/tasks",
            {"id": task_id, "action": "retrieve"},
        )
        if body.get("success") is False or body.get("error"):
            raise NanoBananaError("Task lookup failed. Check request history.")
        response = body.get("response")
        if isinstance(response, str):
            try:
                response = json.loads(response)
            except ValueError:
                response = None
        if not isinstance(response, dict):
            response = {}
        trace_id = str(response.get("trace_id") or trace_id)
        state = str(response.get("state") or response.get("status") or "").lower()
        data = response.get("data")
        item_states = (
            {
                str(item.get("state") or item.get("status") or "").lower()
                for item in data
                if isinstance(item, dict)
            }
            if isinstance(data, list)
            else set()
        )
        if (
            state in FAILED
            or item_states & FAILED
            or response.get("success") is False
            or response.get("error")
        ):
            return {
                "task_id": task_id,
                "trace_id": trace_id,
                "status": "failed",
                "success": False,
                "image_urls": [],
            }
        if (
            not response
            or ("finished_at" in body and body["finished_at"] is None)
            or response.get("success") is not True
        ):
            return {
                "task_id": task_id,
                "trace_id": trace_id,
                "status": "pending",
                "success": False,
                "image_urls": [],
            }
        items = response.get("data")
        urls = (
            [
                item["image_url"]
                for item in items
                if isinstance(item, dict)
                and isinstance(item.get("image_url"), str)
                and _valid_https_url(item["image_url"])
            ]
            if isinstance(items, list)
            else []
        )
        return {
            "task_id": task_id,
            "trace_id": trace_id,
            "status": "succeeded" if urls else "failed",
            "success": bool(urls),
            "image_urls": urls,
            "image_count": len(urls),
        }
