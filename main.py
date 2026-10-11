"""Nano Banana image tools for AstrBot through Ace Data Cloud."""

from __future__ import annotations

import json

from astrbot.api import AstrBotConfig
from astrbot.api.event import AstrMessageEvent, filter
from astrbot.api.star import Context, Star

from .client import NanoBananaClient, NanoBananaError


class NanoBananaPlugin(Star):
    """Expose one image submission and one existing-task lookup tool."""

    def __init__(self, context: Context, config: AstrBotConfig) -> None:
        super().__init__(context)
        self.config = config

    @filter.llm_tool(name="nano_banana_generate_image")
    async def nano_banana_generate_image(
        self,
        event: AstrMessageEvent,
        prompt: str,
        model: str = "nano-banana-2-lite",
        aspect_ratio: str = "1:1",
        resolution: str = "1K",
        image_url: str = "",
    ) -> str:
        """Submit one billable Nano Banana generation or edit job.

        Args:
            prompt(string): Image description or editing instruction.
            model(string): Explicit Nano Banana model or official variant.
            aspect_ratio(string): Output ratio such as 1:1 or 16:9.
            resolution(string): Model-supported 1K, 2K, or 4K size.
            image_url(string): Optional authorized HTTPS image to edit.

        Returns:
            JSON submission status and task ID, never a finished-image claim.
        """
        try:
            result = await NanoBananaClient(self.config.get("api_key", "")).submit(
                prompt, model, aspect_ratio, resolution, image_url
            )
        except NanoBananaError as exc:
            result = {"status": "error", "message": str(exc)}
        return json.dumps(result, ensure_ascii=False)

    @filter.llm_tool(name="nano_banana_get_task")
    async def nano_banana_get_task(self, event: AstrMessageEvent, task_id: str) -> str:
        """Query a prior Nano Banana task without generating another image.

        Args:
            task_id(string): Exact task ID from nano_banana_generate_image.

        Returns:
            JSON status and final image URLs only after task completion.
        """
        try:
            result = await NanoBananaClient(self.config.get("api_key", "")).query(
                task_id
            )
        except NanoBananaError as exc:
            result = {"status": "error", "message": str(exc), "task_id": task_id}
        return json.dumps(result, ensure_ascii=False)
