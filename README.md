# Nano Banana for AstrBot

Generate or edit one Nano Banana image in an AstrBot conversation through your own Ace Data Cloud account. `nano_banana_generate_image` submits one job, and `nano_banana_get_task` retrieves that same task until its final image is ready.

[简体中文指南](readme/README_zh_Hans.md) · [Nano Banana Images API](https://platform.acedata.cloud/documents/nano-banana-images) · [Nano Banana Tasks API](https://platform.acedata.cloud/documents/nano-banana-tasks) · [Current prices](https://platform.acedata.cloud/services/nano-banana)

## Find and install

In AstrBot WebUI, open **Extensions → Plugins → AstrBot Plugin Market** and search **Nano Banana**. Confirm the card says **Nano Banana by Ace Data Cloud**, the author is **acedatacloud**, and the logo matches the [Nano Banana service icon](https://cdn.acedata.cloud/859plc.jpg). Install it, then check **Installed** for load errors.

The official AstrBot Cloud listing has not yet been published. After the source release is merged, **Installed → Install (+) → Install from URL** with `https://github.com/AceDataCloud/NanoBananaAstrBot` can preview it. A URL installation does not prove market publication or installation.

## Configure your key

In [Ace Data Cloud Applications](https://platform.acedata.cloud/console/applications), copy a generation API key from your General application or create a key that permits both `/nano-banana/images` and `/nano-banana/tasks`. Check the current price for your model and resolution before submitting. Paste the key into the plugin's **Ace Data Cloud generation API key with Nano Banana access** setting. Do not add `Bearer ` or use a `platform-...` management token. AstrBot masks the field in WebUI but stores the original value in its data directory, which should be protected.

Select a chat model that supports tool calling. Allow both Nano Banana tools in the conversation's profile and persona.

## Generate once, then query

Ask the bot:

> Use `nano_banana_generate_image` once to make a yellow paper boat on a plain blue background. Use `nano-banana-2-lite`, resolution `1K`, aspect ratio `1:1`. Show me the task ID.

The tool sends one asynchronous `POST /nano-banana/images` request with `count: 1`. It returns `status: submitted` and a task ID, not a finished image. Keep that ID and ask:

> Use `nano_banana_get_task` with the exact task ID `<task_id>`. Tell me its status and final image URL. Do not generate another image.

If pending, query the same ID later. Only `status: succeeded`, `success: true`, and a final HTTPS image URL indicate completion. The plugin never retries a paid submission automatically.

To edit an image you own or may process, include its public HTTPS URL as `image_url` and describe the change in `prompt`. The plugin supports `nano-banana`, `nano-banana-2-lite`, `nano-banana-2`, `nano-banana-pro`, and their `:official` variants. The first two models support only `1K`; `nano-banana-2` and `nano-banana-pro` also support `2K` and `4K`. Common aspect ratios include `1:1`, `16:9`, and `9:16`. This first version accepts one reference image and generates one output; multi-image references and batch output are outside its scope.

## Verify and troubleshoot

In Ace Data Cloud usage, match a returned trace ID when available. Pricing differs by model, resolution, and final output; check current pricing rather than treating an estimate as a charge. A task lookup reads an existing job and does not submit another generation.

| Symptom | Check |
| --- | --- |
| Plugin fails to load | AstrBot version, **Failed to Load Plugins**, and **Data & Logs → Logs**. |
| Tools are missing | Plugin enabled, active profile and persona allow both tools, chat model supports tool calling. |
| HTTP 401/403 | Key type, both allowed API paths, and account access. |
| Network error after submission | Inspect request history before generating again; a timeout may already have created a paid task. |
| Pending task | Query the same task ID later. |
| Failed task | Use the task or trace ID to inspect request history. |

The key goes only to `https://api.acedata.cloud`; redirects are rejected. The plugin exposes only task status and final image URLs to the model, without raw provider data. It uses Python's standard library and needs no runtime package installation.

## Verified local run and brand asset

On official AstrBot `v4.28.2`, an isolated editable installation registered both tools. ChatUI submitted one `nano-banana-2-lite` 1K image and later queried the same task ID through `nano_banana_get_task`, without another generation. The final JPEG responded HTTP 200, `image/jpeg`, and decoded at 1024×1024. The exact generation trace matched a successful `/nano-banana/images` usage row with 0.126 Credits deducted; the current cost rule lists 0.14 Credits before the account discount. See the [sanitized evidence](tests/e2e-results.json). This is a local editable installation; official Cloud review, market installation, and a first call from a market installation remain open.

`logo.png` is a PNG encoding of the current [Nano Banana service icon](https://cdn.acedata.cloud/859plc.jpg), with no redrawing. The source JPEG SHA-256 is `047c3d1a8252a18ccfb65ac09f3f1e2a87ea70525db01fd54f5d70bc312d9814`; the packaged PNG SHA-256 is `22bffc409143a7863f1fb7de04f385c13cdcac799fdba89db152fdaaf55d7379`.
