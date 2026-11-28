<!-- Generated from README.md by AceDataCloud/Index plans/plugin-readme-audit/render_channel_readmes.py. -->

# Nano Banana

<img src="../logo.png" width="96" height="96" alt="Nano Banana">

Generate or edit one Nano Banana image in an AstrBot conversation through your own Ace Data Cloud account. `nano_banana_generate_image` submits one job, and `nano_banana_get_task` retrieves that same task until its final image is ready.

This independent **Nano Banana integration is provided by Ace Data Cloud**. It is not an official plugin from the Nano Banana publisher or the AstrBot team. Use your own Ace account and API key.

[简体中文指南](README_zh_Hans.md) · [Nano Banana Images API](https://platform.acedata.cloud/documents/nano-banana-images?utm_source=github&utm_medium=referral&utm_campaign=evergreen) · [Nano Banana Tasks API](https://platform.acedata.cloud/documents/nano-banana-tasks?utm_source=github&utm_medium=referral&utm_campaign=evergreen) · [Current prices](https://platform.acedata.cloud/services/nano-banana?utm_source=github&utm_medium=referral&utm_campaign=evergreen)

## Find and install

Current upstream navigation (2026-10-18): **Plugins → Plugins → Plugin Market / Installed**. The earlier tested 4.28.2 English UI may label the section Extensions. Configure this service in the installed plugin gear; **do not paste its key into model-provider settings**.

Search the [AstrBot Cloud plugin market](https://cloud.astrbot.app/market) for **Nano Banana** and check the publisher `acedatacloud`.

To install from source, enter `https://github.com/AceDataCloud/NanoBananaAstrBot` under **Plugins → Installed → Install Plugin (+) → Install from URL**.

## Configure your key

[Register or sign in to Ace](https://platform.acedata.cloud/console/applications?utm_source=github&utm_medium=referral&utm_campaign=evergreen) first. Initialize **General application** if it does not exist. The following images show the shared Ace Applications page, not AstrBot.

In [Ace Data Cloud Applications](https://platform.acedata.cloud/console/applications?utm_source=github&utm_medium=referral&utm_campaign=evergreen), copy a generation API key from your General application or create a key that permits both `/nano-banana/images` and `/nano-banana/tasks`. Check the current price for your model and resolution before submitting. Paste the key into the plugin's **Ace Data Cloud generation API key with Nano Banana access** setting. Do not add `Bearer ` or use a `platform-...` management token. AstrBot masks the field in WebUI but stores the original value in its data directory, which should be protected.

For Agent-tool use, select a chat model that supports tool calling. Allow both Nano Banana tools in the conversation's profile and persona.

1. Open **General application**. Use **1** to copy the existing key, or **2 Manage Keys → Create** for a dedicated key.

![Copy an Ace key or open Manage Keys (redacted)](../_assets/tutorial/get-api-key-en.png)

2. Use a name such as `AstrBot Nano Banana`. Set expiry/limits as needed and allow both `/nano-banana/images` and `/nano-banana/tasks`. The screenshot’s Dify tutorial name is an older example.

![Create an optional dedicated key (shared Ace page, not AstrBot)](../_assets/tutorial/create-api-key-en.png)

Images reused and checked on 2026-10-18; original capture dates were not supplied. Credentials and balance are redacted. [Sources and version limits](../_assets/tutorial/sources.json).

### Where to paste it in AstrBot

Open **Plugins → Plugins → Installed**, select the gear on **Nano Banana**, paste the key into **Ace Data Cloud generation API key with Nano Banana access** (stored as `api_key`), and save. No `Bearer ` prefix; never paste the key in chat.

[AstrBot plugin configuration guide](https://docs.astrbot.app/en/dev/star/plugin-new.html)

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

### Cancelled tasks and interrupted waiting

An explicit failed/cancelled/rejected task is terminal: the plugin returns `status: failed`, `success: false` and no media, even if `finished_at` is still empty. It does not resubmit. Cancelling a local chat/command stops waiting locally; it does **not** cancel an upstream generation, and an already-started HTTP request may still finish. Inspect the original task/history and keep the same ID; there is no upstream-cancel command in this plugin.

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

On official AstrBot `v4.28.2`, an isolated editable installation registered both tools. ChatUI submitted one `nano-banana-2-lite` 1K image and later queried the same task ID through `nano_banana_get_task`, without another generation. The final JPEG responded HTTP 200, `image/jpeg`, and decoded at 1024×1024. The exact generation trace matched a successful `/nano-banana/images` usage row with 0.126 Credits deducted; the current cost rule lists 0.14 Credits before the account discount. See the [sanitized evidence](../tests/e2e-results.json). This is a local editable installation; official Cloud review, market installation, and a first call from a market installation remain open.

The plugin includes original 256×256 artwork. [SVG source](../_assets/artwork/logo.svg)

## Reproduce the no-cost host check

From this repository in an isolated Python 3.12 environment:

```bash
uv venv --python 3.12 .venv-host
uv pip install --python .venv-host/bin/python astrbot==4.29.0
.venv-host/bin/python scripts/verify_host.py
```

The check needs no API Key and starts no server. It imports real AstrBot
decorators, registers both commands/two tools, checks admin/non-admin access,
masked-key schema, missing-Key handling and cancellation propagation with
socket access blocked. Fake events and mocked cancellation do not establish
a full message-dispatcher, market install, live generation, task ownership,
new billing or signup/conversion result. Use normal `python -m pytest -q`
for transport and command regression tests.
