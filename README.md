# Awesome AI Rewrite

> 聚合全网 AI 逆向 / clean-room 重写的开源项目，一个索引，跟进行业最新动态。

最近 AI 逆向重写（clean-room reimplementation）爆火，从 Adobe 全家桶到 Claude Code、再到 REA 这类通用逆向框架。本仓库只做一件事：**聚合索引**这些开源项目，自动拉取最新 star / 语言 / 更新时间，按分类呈现，让你一眼看到行业在重写什么。

![项目数](https://img.shields.io/badge/项目数-25-brightgreen) ![总 Stars](https://img.shields.io/badge/总_Stars-1033.7k-yellow) ![更新时间](https://img.shields.io/badge/更新-2026-10-31%2003:59%20UTC-blue) ![自动更新](https://img.shields.io/badge/自动更新-GitHub_Actions-success)

**GitHub 仓库**：[qqxhb/awesome-ai-rewrite](https://github.com/qqxhb/awesome-ai-rewrite)

## 📊 数据概览

- 📦 收录项目：**25**
- ⭐ 累计 Stars：**1033.7k**
- 🔠 主流语言：Rust (11), Python (9), TypeScript (4), Java (1)

## 🔥 热门 TOP 10（按 Stars）

| # | 项目 | ⭐ | 语言 | 对标 |
| ---: | --- | ---: | --- | --- |
| 1 | [`morluto/rea`](https://github.com/morluto/rea) | 412.7k | TypeScript | 通用逆向框架 (REA) |
| 2 | [`openclaw/openclaw`](https://github.com/openclaw/openclaw) | 393.5k | TypeScript | Claude Code / AI Gateway |
| 3 | [`storytold/photocraft`](https://github.com/storytold/photocraft) | 75.3k | Rust | Adobe Photoshop |
| 4 | [`storytold/pdfcraft`](https://github.com/storytold/pdfcraft) | 18.8k | Rust | Adobe Acrobat |
| 5 | [`storytold/filmcraft`](https://github.com/storytold/filmcraft) | 17.0k | Rust | Adobe Premiere Pro |
| 6 | [`storytold/wordcraft`](https://github.com/storytold/wordcraft) | 16.8k | Rust | Microsoft Word |
| 7 | [`storytold/lightcraft`](https://github.com/storytold/lightcraft) | 15.1k | Rust | Adobe Lightroom |
| 8 | [`mrexodia/ida-pro-mcp`](https://github.com/mrexodia/ida-pro-mcp) | 13.2k | Python | IDA Pro + AI MCP |
| 9 | [`storytold/vectorcraft`](https://github.com/storytold/vectorcraft) | 11.1k | Rust | Adobe Illustrator |
| 10 | [`storytold/effectcraft`](https://github.com/storytold/effectcraft) | 8.2k | Rust | Adobe After Effects |

## 📚 分类索引

- [🎨 创意设计工具](#创意设计工具)（10）
- [🤖 AI Agent / 编码助手逆向](#ai-agent--编码助手逆向)（3）
- [🔧 AI 辅助逆向工程](#ai-辅助逆向工程)（2）
- [🧬 通用复制/克隆框架](#通用复制克隆框架)（4）
- [🔓 闭源 AI API 逆向](#闭源-ai-api-逆向)（6）

## 🎨 创意设计工具

> 对标 Photoshop / Illustrator / Premiere 等商业软件的 clean-room 重写。

共 **10** 个项目。

| 项目 | 对标 | 简介 | ⭐ | 语言 | License | 最近更新 |
| --- | --- | --- | ---: | --- | --- | --- |
| [`storytold/photocraft`](https://github.com/storytold/photocraft) | Adobe Photoshop | PhotoCraft: An open-source, photo editor written by scratch in pure Rust | 75.3k | Rust | Apache-2.0 | 2026-10-31 |
| [`storytold/pdfcraft`](https://github.com/storytold/pdfcraft) | Adobe Acrobat | PdfCraft: An open-source PDF reader and editor written by scratch in pure Rust | 18.8k | Rust | Apache-2.0 | 2026-10-31 |
| [`storytold/filmcraft`](https://github.com/storytold/filmcraft) | Adobe Premiere Pro | FilmCraft: An open-source, nonlinear video editor written by scratch in pure Rust | 17.0k | Rust | Apache-2.0 | 2026-10-31 |
| [`storytold/wordcraft`](https://github.com/storytold/wordcraft) | Microsoft Word | An open-source, clean-room reimplementation of Microsoft Word in pure Rust | 16.8k | Rust | Apache-2.0 | 2026-10-31 |
| [`storytold/lightcraft`](https://github.com/storytold/lightcraft) | Adobe Lightroom | LightCraft: An open-source non-destructive photo editor written by scratch in pure Rust | 15.1k | Rust | Apache-2.0 | 2026-10-31 |
| [`storytold/vectorcraft`](https://github.com/storytold/vectorcraft) | Adobe Illustrator | VectorCraft: An open-source, vector art tool written by scratch in pure Rust | 11.1k | Rust | Apache-2.0 | 2026-10-31 |
| [`storytold/effectcraft`](https://github.com/storytold/effectcraft) | Adobe After Effects | EffectCraft: An open-source motion graphics and compositing tool written by scratch in pure Rust | 8.2k | Rust | Apache-2.0 | 2026-10-31 |
| [`storytold/designcraft`](https://github.com/storytold/designcraft) | Adobe InDesign | DesignCraft: An open-source page and layout design editor written by scratch in pure Rust | 5.0k | Rust | Apache-2.0 | 2026-10-31 |
| [`storytold/deckcraft`](https://github.com/storytold/deckcraft) | Microsoft PowerPoint | Presentations and slide shows: an open-source, clean-room reimplementation of Microsoft PowerPoint in pure Rust. Part of the ArtCraft Craft… | 4.5k | Rust | Apache-2.0 | 2026-10-31 |
| [`storytold/soundcraft`](https://github.com/storytold/soundcraft) | Avid Pro Tools | An open-source, clean-room reimplementation of Avid Pro Tools in pure Rust | 3.9k | Rust | Apache-2.0 | 2026-10-31 |

## 🤖 AI Agent / 编码助手逆向

> 对标 Claude Code / Cursor 等闭源 AI 编码产品的开源重写。

共 **3** 个项目。

| 项目 | 对标 | 简介 | ⭐ | 语言 | License | 最近更新 |
| --- | --- | --- | ---: | --- | --- | --- |
| [`openclaw/openclaw`](https://github.com/openclaw/openclaw) | Claude Code / AI Gateway | The AI that really does things. Any OS. Any Platform. The lobster way. 🦞 | 393.5k | TypeScript | MIT | 2026-10-31 |
| [`alejandrobalderas/claude-code-from-source`](https://github.com/alejandrobalderas/claude-code-from-source) | Claude Code 架构逆向 | Architecture, patterns & internals of Anthropic's AI coding agent — reverse-engineered from source maps | 3.0k | TypeScript | - | 2026-10-30 |
| [`Enderfga/claw-orchestrator`](https://github.com/Enderfga/claw-orchestrator) | Claude Code / 多 Agent 编排 | Run Claude Code, Codex, Antigravity, Grok Build and OpenCode behind one runtime, and a run only counts as done when checks it didn't write… | 602 | TypeScript | MIT | 2026-10-30 |

## 🔧 AI 辅助逆向工程

> 把 AI / LLM / MCP 接入逆向工作流的工具与框架。

共 **2** 个项目。

| 项目 | 对标 | 简介 | ⭐ | 语言 | License | 最近更新 |
| --- | --- | --- | ---: | --- | --- | --- |
| [`mrexodia/ida-pro-mcp`](https://github.com/mrexodia/ida-pro-mcp) | IDA Pro + AI MCP | AI-powered reverse engineering assistant that bridges IDA Pro with language models through MCP. | 13.2k | Python | MIT | 2026-10-31 |
| [`bethington/ghidra-mcp`](https://github.com/bethington/ghidra-mcp) | Ghidra + AI MCP | Ghidra MCP Server — 200+ MCP tools for AI-powered reverse engineering. GUI plugin + headless server, lazy tool loading, convention enforcem… | 6.0k | Java | Apache-2.0 | 2026-10-31 |

## 🧬 通用复制/克隆框架

> 不针对特定产品，而是提供「逆向并重写任意应用」能力的框架。

共 **4** 个项目。

| 项目 | 对标 | 简介 | ⭐ | 语言 | License | 最近更新 |
| --- | --- | --- | ---: | --- | --- | --- |
| [`morluto/rea`](https://github.com/morluto/rea) | 通用逆向框架 (REA) | Reverse engineer anything with agents, from app behavior down to native binaries. | 412.7k | TypeScript | MIT | 2026-10-31 |
| [`Jakeschincariol/replica-skill`](https://github.com/Jakeschincariol/replica-skill) | 任意应用 clean-room 克隆 | Eleven free Claude skills that clone any app: reverse-engineer it, rebuild it, test it for bugs, then fix what its users hate. Free, MIT. | 6.7k | Python | MIT | 2026-10-31 |
| [`Integuru-AI/Integuru`](https://github.com/Integuru-AI/Integuru) | 逆向构建任意 API 集成 | The first AI agent that builds permissionless integrations through reverse engineering platforms' internal APIs. | 4.8k | Python | AGPL-3.0 | 2026-10-31 |
| [`kalil0321/reverse-api-engineer`](https://github.com/kalil0321/reverse-api-engineer) | 网站逆向成 API | Reverse engineer any website into a typed API client. Works with Claude Code, Codex, Cursor and OpenCode. | 2.2k | Python | MIT | 2026-10-31 |

## 🔓 闭源 AI API 逆向

> 逆向闭源 AI 产品的 Web/客户端 API，封装成可调用的开源接口。

共 **6** 个项目。

| 项目 | 对标 | 简介 | ⭐ | 语言 | License | 最近更新 |
| --- | --- | --- | ---: | --- | --- | --- |
| [`acheong08/EdgeGPT`](https://github.com/acheong08/EdgeGPT) | Bing Chat | Reverse engineered API of Microsoft's Bing Chat AI | 7.8k | Python | Unlicense | 2026-10-30 |
| [`HanaokaYuzu/Gemini-API`](https://github.com/HanaokaYuzu/Gemini-API) | Google Gemini | ✨ Reverse-engineered Python API for Google Gemini web app | 3.8k | Python | AGPL-3.0 | 2026-10-31 |
| [`0x676e67/ninja`](https://github.com/0x676e67/ninja) | ChatGPT 代理 | Reverse engineered ChatGPT proxy | 1.7k | Rust | GPL-3.0 | 2026-10-24 |
| [`sums001/Windows-Copilot-API`](https://github.com/sums001/Windows-Copilot-API) | Windows Copilot | Reverse engineered Windows Copilot into an OpenAI-compatible API. Access GPT-4 and GPT-5 models through a simple REST interface without API… | 1.3k | Python | MIT | 2026-10-30 |
| [`Strvm/meta-ai-api`](https://github.com/Strvm/meta-ai-api) | Meta AI | Llama 3 API 70B & 405B (MetaAI Reverse Engineered) | 407 | Python | - | 2026-10-16 |
| [`yihong0618/SunoSongsCreator`](https://github.com/yihong0618/SunoSongsCreator) | Suno 音乐 | About High quality songs generation by https://www.suno.ai/. Reverse engineered API. | 369 | Python | GPL-3.0 | 2026-10-28 |

## ⚙️ 工作原理

本仓库**不部署任何服务**，一切基于 GitHub 原生能力：

1. **`config.json`** — 人工维护的仓库清单与分类（唯一需要手改的文件）。
2. **`update.py`** — 纯 Python 标准库脚本，调用 GitHub API 拉取每个仓库的最新元数据。
3. **`projects.json`** — 机器可读的数据源（脚本自动生成）。
4. **`candidates.json`** — 自动发现的候选仓库（`--discover` 模式生成，人工审核后加入 config）。
5. **`README.md`** — 由脚本根据数据自动重写，呈现给人看。
6. **`.github/workflows/update.yml`** — GitHub Actions 定时（每日 UTC 00:00）自动运行并提交更新，也支持手动触发。

## 🔄 手动更新

```bash
# 可选：设置 token 提高速率限制（未认证 60 次/小时，认证 5000 次/小时）
# export GITHUB_TOKEN=ghp_xxx

python3 update.py                 # 更新已有仓库 + 重写 README
python3 update.py --discover      # 额外搜索新候选仓库，写入 candidates.json
```

## 🙋 贡献

想新增一个项目？只需两步：

1. 在 [`config.json`](./config.json) 的 `repos` 数组里追加一项：
   ```json
   { "full_name": "owner/repo", "category": "creative", "target": "对标产品" }
   ```
   `category` 取值见 `categories` 字段；`target` 写它逆向/重写的对象。
2. 运行 `python3 update.py` 重新生成 `projects.json` 与 `README.md`，然后提交 PR。

收录标准：以 AI 辅助逆向 / clean-room 重写闭源产品为核心的开源项目。通用逆向工具、纯模型权重仓库暂不收录。

## ⚠️ 免责声明

本仓库仅做**信息聚合索引**，不托管任何被逆向项目的源码或二进制。所列项目均为其作者的开源成果，请遵守各项目自身的 License 与适用法律。clean-room 重写不等于侵权，但使用者应自行评估法律风险。
