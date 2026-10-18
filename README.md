# Nano Banana for AstrBot

Generate or edit one Nano Banana image in an AstrBot conversation through your own Ace Data Cloud account. `nano_banana_generate_image` submits one job, and `nano_banana_get_task` retrieves that same task until its final image is ready.

**This PR targets 0.1.1** with native help/admin lookup commands, bilingual configuration and illustrated setup. Existing 0.1.0 installations do not gain these entries until the source is merged and the package is published/updated.

This independent **Nano Banana integration is provided by Ace Data Cloud**. It is not an official plugin from the Nano Banana publisher or the AstrBot team. Use your own Ace account and API key.

[简体中文指南](readme/README_zh_Hans.md) · [Nano Banana Images API](https://platform.acedata.cloud/documents/nano-banana-images?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=nanobananaastrbot_readme_documents_nano_banana_images) · [Nano Banana Tasks API](https://platform.acedata.cloud/documents/nano-banana-tasks?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=nanobananaastrbot_readme_documents_nano_banana_tasks) · [Current prices](https://platform.acedata.cloud/services/nano-banana?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=nanobananaastrbot_readme_services_nano_banana)

## Find and install

Current upstream navigation (2026-10-18): **Plugins → Plugins → Plugin Market / Installed**. The earlier tested 4.28.2 English UI may label the section Extensions. Configure this service in the installed plugin gear; **do not paste its key into model-provider settings**.

**Publication status (2026-10-18): not yet listed in the official market.** After publication, open [AstrBot Cloud Plugin Market](https://cloud.astrbot.app/market), search **Nano Banana**, and verify **Nano Banana by Ace Data Cloud / acedatacloud**. For the current preview, use the repository URL below; a repository install is not official market publication.

The official AstrBot Cloud listing has not yet been published. The source release is merged; **Plugins → Plugins → Installed → Install Plugin (+) → Install from URL** with `https://github.com/AceDataCloud/NanoBananaAstrBot` can preview it. A URL installation does not prove market publication or installation.

## Configure your key

[Register or sign in to Ace](https://platform.acedata.cloud/console/applications?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=nanobananaastrbot_readme_signup) first. Initialize **General application** if it does not exist. The following images show the shared Ace Applications page, not AstrBot.

In [Ace Data Cloud Applications](https://platform.acedata.cloud/console/applications?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=nanobananaastrbot_readme_api_key), copy a generation API key from your General application or create a key that permits both `/nano-banana/images` and `/nano-banana/tasks`. Check the current price for your model and resolution before submitting. Paste the key into the plugin's **Ace Data Cloud generation API key with Nano Banana access** setting. Do not add `Bearer ` or use a `platform-...` management token. AstrBot masks the field in WebUI but stores the original value in its data directory, which should be protected.

For Agent-tool use, select a chat model that supports tool calling. Allow both Nano Banana tools in the conversation's profile and persona.

1. Open **General application**. Use **1** to copy the existing key, or **2 Manage Keys → Create** for a dedicated key.

![Copy an Ace key or open Manage Keys (redacted)](_assets/tutorial/get-api-key-en.png)

2. Use a name such as `AstrBot Nano Banana`. Set expiry/limits as needed and allow both `/nano-banana/images` and `/nano-banana/tasks`. The screenshot’s Dify tutorial name is an older example.

![Create an optional dedicated key (shared Ace page, not AstrBot)](_assets/tutorial/create-api-key-en.png)

Images reused and checked on 2026-10-18; original capture dates were not supplied. Credentials and balance are redacted. [Sources and version limits](_assets/tutorial/sources.json).

### Where to paste it in AstrBot

Open **Plugins → Plugins → Installed**, select the gear on **Nano Banana by Ace Data Cloud**, paste the key into **Ace Data Cloud generation API key with Nano Banana access** (stored as `api_key`), and save. No `Bearer ` prefix; never paste the key in chat.

![AstrBot official historical plugin configuration reference, not this plugin running](_assets/tutorial/astrbot-plugin-config-reference.png)

This is the official AstrBot `helloworld` configuration example, labelled v3.4.14 (build v3.4.9), not an Ace setup or run. The instructions above identify this plugin’s exact field and current navigation; later UI layouts may differ.

## Native commands without a chat model

| Input | Result |
| --- | --- |
| `/nanobanana_ace` | Show service, Token setup and lookup help; no external API call. |
| `/nanobanana_ace_task <task_id>` | AstrBot administrators only: retrieve one existing task, with status/final media; no LLM or generation. |

Commands use the default `/` prefix; adapt it if your instance uses another wake prefix. AstrBot enforces administrator identity. The instance shares this plugin key, so direct lookup is administrator-only; other users use Agent tools allowed by their profile/persona. For `pending`, query the same ID later; for `failed`, inspect the original task/trace.

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
