# AstrBot 的 Nano Banana 插件

通过自己的 Ace Data Cloud 账号，在 AstrBot 对话中生成或编辑单张 Nano Banana 图片。`nano_banana_generate_image` 提交一次任务，`nano_banana_get_task` 用相同 ID 查询最终结果。

**本 PR 的目标版本为 0.1.1**：新增原生帮助及管理员查询指令、双语配置和图文说明。合并和市场发布前，当前 0.1.0 安装不会自动获得这些入口。

这是 **Ace Data Cloud 提供的 Nano Banana 独立集成**，不是 Nano Banana 厂商或 AstrBot 团队的官方插件。使用自己的 Ace 账号和 API Key；不要填写其他平台的密钥。

[English guide](../README.md) · [Nano Banana 图片 API](https://platform.acedata.cloud/documents/nano-banana-images?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=nanobananaastrbot_readme_documents_nano_banana_images) · [Nano Banana 任务 API](https://platform.acedata.cloud/documents/nano-banana-tasks?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=nanobananaastrbot_readme_documents_nano_banana_tasks) · [当前价格](https://platform.acedata.cloud/services/nano-banana?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=nanobananaastrbot_readme_services_nano_banana)

## 搜索与安装

当前上游文档（2026-10-18）：侧栏 **插件 → 顶部插件 → 插件市场 / 已安装**；旧 4.28.2 英文界面可能显示 Extensions。插件参数在已安装卡片齿轮里设置，**不要把服务插件 Key 填进模型提供商**。

**发布状态（2026-10-18）：尚未在官方市场上架。** 正式发布后，先打开 [AstrBot Cloud 插件市场](https://cloud.astrbot.app/market)，搜索 **Nano Banana**，再核对 **Nano Banana by Ace Data Cloud / acedatacloud**。当前请用下面的 Git 仓地址手动安装；不要把仓库安装说成官方市场收录。

AstrBot Cloud 官方上架尚未完成。源码已合并，可在 **Plugins → Plugins → Installed → Install Plugin (+) → Install from URL** 输入 `https://github.com/AceDataCloud/NanoBananaAstrBot` 预览。URL 安装不代表官方市场已上架或安装已验证。

## 配置 Key

先[注册或登录 Ace](https://platform.acedata.cloud/console/applications?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=nanobananaastrbot_readme_signup)；首次没有通用应用时，先初始化 **General application**。下图取自同一 Ace 应用管理页面，不是 AstrBot 界面。

到 [Ace Data Cloud Applications](https://platform.acedata.cloud/console/applications?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=nanobananaastrbot_readme_api_key) 复制 General application 的生成 API Key，或创建同时允许 `/nano-banana/images` 和 `/nano-banana/tasks` 的 Key。提交前检查所选模型与分辨率的当前价格。在插件设置 **Ace Data Cloud generation API key with Nano Banana access** 中粘贴 Key 本身；不要加 `Bearer `，也不要使用 `platform-...` 管理 Token。AstrBot WebUI 会遮蔽字段，但数据目录会保存原值，请保护该目录。

使用 Agent 工具时，选择支持工具调用的聊天模型，在当前 Profile 和 Persona 中允许两个 Nano Banana 工具。

1. 打开 **General application**，用图中 **1** 复制现有 Key，或点 **2 Manage Keys → Create** 创建专用 Key。

![复制 Ace Key 或管理专用 Key（已脱敏）](../_assets/tutorial/get-api-key-en.png)

2. 可把名称设为 `AstrBot Nano Banana`，按需要设置到期/限额；Allowed APIs 同时包含 `/nano-banana/images` 和 `/nano-banana/tasks`。截图的 Dify tutorial 只是旧示例名称。

![创建专用 Key（共享 Ace 页面，非 AstrBot）](../_assets/tutorial/create-api-key-en.png)

图片于 2026-10-18 复用核验，原始拍摄日期未提供；凭据与余额已脱敏。 [来源和版本边界](../_assets/tutorial/sources.json)。

### 在 AstrBot 粘贴的位置

打开 **插件 → 插件 → 已安装**，点击 **Nano Banana by Ace Data Cloud** 卡片齿轮，把 Key 填入 **Ace Data Cloud generation API key with Nano Banana access**（保存字段为 `api_key`）并保存。不要填 `Bearer `；也不要在聊天里输入 Key。

![AstrBot 官方历史插件配置参考，非本插件运行截图](../_assets/tutorial/astrbot-plugin-config-reference.png)

此图是 AstrBot 官方 `helloworld` 配置示例，界面标签 v3.4.14（构建 v3.4.9），不是 Ace 配置或运行证明。上方说明给出了本插件的准确字段和当前菜单；新版本布局可能不同。

## 无需聊天模型的原生指令

| 输入 | 作用 |
| --- | --- |
| `/nanobanana_ace` | 显示本服务、Token 配置和查询用法，不请求外部 API。 |
| `/nanobanana_ace_task <task_id>` | 仅 AstrBot 管理员：查询一个已有任务，返回状态与最终媒体，不调用 LLM 或生成。 |

指令采用默认 `/` 前缀；自定义唤醒前缀时相应替换。管理员身份由 AstrBot 判断；同一实例的插件 Key 是共享配置，因此查询指令默认限管理员。其他用户继续使用受当前人格/配置允许的 Agent 工具。`pending` 时稍后只查同一编号，`failed` 时按原 task/trace 排查。

## 只生成一次，再查同一任务

向机器人发送：

> 只调用一次 `nano_banana_generate_image`，生成蓝色背景上的黄色纸船。模型用 `nano-banana-2-lite`，分辨率 `1K`，比例 `1:1`。告诉我 task ID。

工具向 `POST /nano-banana/images` 提交一次异步任务，固定 `count: 1`，返回 `status: submitted` 和 task ID；此时并非最终图片。保留 ID，再问：

> 用 `nano_banana_get_task` 查询原来的 `<task_id>`，告诉我状态和最终图片 URL，不要再次生成。

若仍为 pending，稍后查询**同一 ID**。只有 `status: succeeded`、`success: true` 且返回最终 HTTPS 图片 URL 才表示完成。插件不会自动重试付费请求。

若要编辑有处理权限的图片，将其公开 HTTPS 地址传为 `image_url`，在 `prompt` 描述修改。插件支持 `nano-banana`、`nano-banana-2-lite`、`nano-banana-2`、`nano-banana-pro` 及对应 `:official` 版本。前两款只支持 `1K`；`nano-banana-2` 和 `nano-banana-pro` 还支持 `2K`、`4K`。常用比例包括 `1:1`、`16:9`、`9:16`。首版只接收一张参考图、生成一张结果；多参考图和批量输出暂未包含。

## 用量与排障

### 任务取消与本地中断

任务明确 failed/cancelled/rejected 时视为终态：即使 `finished_at` 尚未填入，也返回 `status: failed`、`success: false`，不显示媒体、不重新提交。本地取消聊天或指令只中断等待，**不会取消服务端生成**，已开始的 HTTP 请求仍可能完成。保留原 task ID 并查请求历史；本插件没有服务端取消任务指令。

在 Ace Data Cloud 用量页按返回的 trace ID 匹配。价格随模型、分辨率和最终结果变化，请以当前价格为准，不把预估当成实扣。任务查询只读取已有作业，不会再提交生成。

| 现象 | 检查项 |
| --- | --- |
| 插件加载失败 | AstrBot 版本、**Failed to Load Plugins**、**Data & Logs → Logs**。 |
| 看不到工具 | 插件启用、当前 Profile/Persona 允许两个工具、聊天模型支持工具调用。 |
| HTTP 401/403 | Key 类型、两个 Allowed APIs 路径和账号权限。 |
| 提交后网络错误 | 再次生成前查请求历史；超时请求可能已创建付费任务。 |
| 任务 pending | 稍后查询同一个 task ID。 |
| 任务 failed | 按 task ID 或 trace ID 查看请求历史。 |

Key 只发送到 `https://api.acedata.cloud`，重定向会被拒绝。插件仅向模型返回任务状态和最终图片链接，不透出上游原始数据。运行只需 Python 标准库。

## 已验证的本地运行与图标

官方 AstrBot `v4.28.2` 的隔离实例注册了两个工具。ChatUI 用 `nano-banana-2-lite` 提交一次 1K 图片任务，并通过 `nano_banana_get_task` 查询同一 task ID，没有再次生成。最终 JPEG 为 HTTP 200、`image/jpeg`，解码尺寸 1024×1024。生成 trace 精确匹配一条成功的 `/nano-banana/images` 用量，实扣 0.126 Credits；当前成本规则为折扣前 0.14 Credits。详见[脱敏证据](../tests/e2e-results.json)。这仍是本地 editable 安装；Cloud 审核、官方市场安装及市场安装后的首次调用尚未完成。

`logo.png` 是当前 [Nano Banana 服务图标](https://cdn.acedata.cloud/859plc.jpg) 的 PNG 编码，未重新绘制。源 JPEG SHA-256 为 `047c3d1a8252a18ccfb65ac09f3f1e2a87ea70525db01fd54f5d70bc312d9814`；打包 PNG SHA-256 为 `22bffc409143a7863f1fb7de04f385c13cdcac799fdba89db152fdaaf55d7379`。

## 复现免费宿主检查

在本仓库中使用独立 Python 3.12 环境：

```bash
uv venv --python 3.12 .venv-host
uv pip install --python .venv-host/bin/python astrbot==4.29.0
.venv-host/bin/python scripts/verify_host.py
```

无需 API Key，不启动服务。检查导入真实 AstrBot 装饰器、注册两个指令/两个工具，
验证管理员允许/非管理员拒绝、Key 遮罩 schema、空 Key 错误与取消传播，并阻止 socket 连接。
事件和取消为测试替身，不能据此声称完整消息分发、官方市场安装、真实生成、任务归属、
新账单或注册转化已验。传输和指令回归使用常规 `python -m pytest -q`。
