# AstrBot 的 Nano Banana 插件

通过自己的 Ace Data Cloud 账号，在 AstrBot 对话中生成或编辑单张 Nano Banana 图片。`nano_banana_generate_image` 提交一次任务，`nano_banana_get_task` 用相同 ID 查询最终结果。

[English guide](../README.md) · [Nano Banana 图片 API](https://platform.acedata.cloud/documents/nano-banana-images) · [Nano Banana 任务 API](https://platform.acedata.cloud/documents/nano-banana-tasks) · [当前价格](https://platform.acedata.cloud/services/nano-banana)

## 搜索与安装

在 AstrBot WebUI 打开 **Extensions → Plugins → AstrBot Plugin Market**，搜索 **Nano Banana**。核对卡片名称 **Nano Banana by Ace Data Cloud**、作者 **acedatacloud** 和 [Nano Banana 服务图标](https://cdn.acedata.cloud/859plc.jpg)，安装后到 **Installed** 检查加载状态。

AstrBot Cloud 官方上架尚未完成。源码合并发布后，可在 **Installed → Install (+) → Install from URL** 输入 `https://github.com/AceDataCloud/NanoBananaAstrBot` 预览。URL 安装不代表官方市场已上架或安装已验证。

## 配置 Key

到 [Ace Data Cloud Applications](https://platform.acedata.cloud/console/applications) 复制 General application 的生成 API Key，或创建同时允许 `/nano-banana/images` 和 `/nano-banana/tasks` 的 Key。提交前检查所选模型与分辨率的当前价格。在插件设置 **Ace Data Cloud generation API key with Nano Banana access** 中粘贴 Key 本身；不要加 `Bearer `，也不要使用 `platform-...` 管理 Token。AstrBot WebUI 会遮蔽字段，但数据目录会保存原值，请保护该目录。

选择支持工具调用的聊天模型，在当前 Profile 和 Persona 中允许两个 Nano Banana 工具。

## 只生成一次，再查同一任务

向机器人发送：

> 只调用一次 `nano_banana_generate_image`，生成蓝色背景上的黄色纸船。模型用 `nano-banana-2-lite`，分辨率 `1K`，比例 `1:1`。告诉我 task ID。

工具向 `POST /nano-banana/images` 提交一次异步任务，固定 `count: 1`，返回 `status: submitted` 和 task ID；此时并非最终图片。保留 ID，再问：

> 用 `nano_banana_get_task` 查询原来的 `<task_id>`，告诉我状态和最终图片 URL，不要再次生成。

若仍为 pending，稍后查询**同一 ID**。只有 `status: succeeded`、`success: true` 且返回最终 HTTPS 图片 URL 才表示完成。插件不会自动重试付费请求。

若要编辑有处理权限的图片，将其公开 HTTPS 地址传为 `image_url`，在 `prompt` 描述修改。插件支持 `nano-banana`、`nano-banana-2-lite`、`nano-banana-2`、`nano-banana-pro` 及对应 `:official` 版本。前两款只支持 `1K`；`nano-banana-2` 和 `nano-banana-pro` 还支持 `2K`、`4K`。常用比例包括 `1:1`、`16:9`、`9:16`。首版只接收一张参考图、生成一张结果；多参考图和批量输出暂未包含。

## 用量与排障

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
