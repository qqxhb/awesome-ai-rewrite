#!/usr/bin/env python3
"""
update.py — AI 逆向工程开源索引 · 自动更新脚本

功能：
  1. 读取 config.json 中的仓库清单与分类
  2. 调用 GitHub API 拉取每个仓库的最新元数据（star / 语言 / 更新时间 / license 等）
  3. 生成 projects.json（机器可读数据源）
  4. 重写 README.md（产品化展示页）
  5. （可选）自动发现新的候选仓库，写入 candidates.json 供人工审核

用法：
  python3 update.py                    # 更新已有仓库 + 重写 README
  python3 update.py --discover         # 额外搜索新的候选仓库，写入 candidates.json
  GITHUB_TOKEN=xxx python3 update.py   # 提高 GitHub API 速率限制

设计原则：只用 Python 标准库，零依赖，可在 GitHub Actions 中直接运行。
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

BASE_DIR = Path(__file__).resolve().parent
CONFIG_PATH = BASE_DIR / "config.json"
PROJECTS_PATH = BASE_DIR / "projects.json"
CANDIDATES_PATH = BASE_DIR / "candidates.json"
README_PATH = BASE_DIR / "README.md"

GITHUB_API_BASE = "https://api.github.com"
REQUEST_TIMEOUT = 20
# 未认证 60 次/小时，认证 5000 次/小时。这里设一个保守间隔。
SLEEP_BETWEEN_REQUESTS = 0.5


def load_config() -> dict[str, Any]:
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def github_headers() -> dict[str, str]:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "ai-reverse-engineering-index-updater",
    }
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def fetch_repo(full_name: str) -> dict[str, Any] | None:
    """拉取单个仓库元数据，失败返回 None。"""
    url = f"{GITHUB_API_BASE}/repos/{full_name}"
    req = urllib.request.Request(url, headers=github_headers())
    try:
        with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return {
                "full_name": data.get("full_name", full_name),
                "name": data.get("name", ""),
                "owner": data.get("owner", {}).get("login", ""),
                "description": data.get("description") or "",
                "html_url": data.get("html_url", ""),
                "homepage": data.get("homepage") or "",
                "stars": data.get("stargazers_count", 0),
                "forks": data.get("forks_count", 0),
                "watchers": data.get("subscribers_count", 0),
                "open_issues": data.get("open_issues_count", 0),
                "language": data.get("language") or "",
                "topics": data.get("topics") or [],
                "license": (data.get("license") or {}).get("spdx_id") or "",
                "created_at": data.get("created_at", ""),
                "updated_at": data.get("updated_at", ""),
                "pushed_at": data.get("pushed_at", ""),
                "archived": data.get("archived", False),
            }
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print(f"  ✗ {full_name} → 404 不存在，跳过")
        elif e.code == 403:
            print(f"  ✗ {full_name} → 403 限流（请设置 GITHUB_TOKEN），跳过")
        else:
            print(f"  ✗ {full_name} → HTTP {e.code}，跳过")
        return None
    except Exception as e:  # noqa: BLE001
        print(f"  ✗ {full_name} → {type(e).__name__}: {e}，跳过")
        return None


def load_cached_projects() -> dict[str, dict[str, Any]]:
    """加载已有的 projects.json 作为缓存，key 为 full_name。"""
    if not PROJECTS_PATH.exists():
        return {}
    try:
        with open(PROJECTS_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        return {p["full_name"]: p for p in data.get("projects", [])}
    except Exception:
        return {}


def fetch_all_repos(
    repo_entries: list[dict[str, str]], cache: dict[str, dict[str, Any]]
) -> list[dict[str, Any]]:
    """拉取所有仓库元数据。失败时回退到缓存中的旧数据。"""
    results: list[dict[str, Any]] = []
    total = len(repo_entries)
    for idx, entry in enumerate(repo_entries, 1):
        full_name = entry["full_name"]
        print(f"[{idx}/{total}] 拉取 {full_name} ...")
        meta = fetch_repo(full_name)
        if meta is not None:
            meta["category"] = entry.get("category", "")
            meta["target"] = entry.get("target", "")
            results.append(meta)
        elif full_name in cache:
            # 回退到缓存
            cached = dict(cache[full_name])
            cached["category"] = entry.get("category", cached.get("category", ""))
            cached["target"] = entry.get("target", cached.get("target", ""))
            print(f"  ↻ {full_name} → 使用缓存数据")
            results.append(cached)
        time.sleep(SLEEP_BETWEEN_REQUESTS)
    return results


def sort_projects(projects: list[dict[str, Any]], key: str = "stars") -> list[dict[str, Any]]:
    return sorted(projects, key=lambda p: p.get(key, 0), reverse=True)


# ---------------------------------------------------------------------------
# 自动发现候选仓库
# ---------------------------------------------------------------------------

def search_repos(query: str, per_page: int = 30) -> list[dict[str, Any]]:
    """调用 GitHub Search API 搜索仓库。"""
    params = urllib.parse.urlencode({"q": query, "per_page": per_page, "sort": "stars", "order": "desc"})
    url = f"{GITHUB_API_BASE}/search/repositories?{params}"
    req = urllib.request.Request(url, headers=github_headers())
    try:
        with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data.get("items", [])
    except urllib.error.HTTPError as e:
        if e.code == 403:
            print(f"  ✗ 搜索限流（{query[:30]}...），请设置 GITHUB_TOKEN")
        else:
            print(f"  ✗ 搜索失败 HTTP {e.code}")
        return []
    except Exception as e:  # noqa: BLE001
        print(f"  ✗ 搜索异常 {type(e).__name__}: {e}")
        return []


def discover_candidates(config: dict[str, Any]) -> list[dict[str, Any]]:
    """根据 config.discovery 关键词搜索新仓库，过滤已收录的。"""
    discovery = config.get("discovery", {})
    keywords = discovery.get("keywords", [])
    min_stars = int(discovery.get("min_stars", 100))
    max_results = int(discovery.get("max_results_per_keyword", 20))
    exclude_owners = set(discovery.get("exclude_owners", []))

    known = {entry["full_name"].lower() for entry in config.get("repos", [])}

    seen: set[str] = set()
    candidates: list[dict[str, Any]] = []

    for kw in keywords:
        print(f"🔍 搜索关键词: {kw}")
        items = search_repos(kw, per_page=max_results)
        time.sleep(SLEEP_BETWEEN_REQUESTS)
        for item in items:
            full_name = item.get("full_name", "")
            key = full_name.lower()
            if key in seen or key in known:
                continue
            if item.get("stargazers_count", 0) < min_stars:
                continue
            owner = item.get("owner", {}).get("login", "")
            if owner in exclude_owners:
                continue
            if item.get("fork"):
                continue
            seen.add(key)
            candidates.append({
                "full_name": full_name,
                "description": item.get("description") or "",
                "stars": item.get("stargazers_count", 0),
                "language": item.get("language") or "",
                "html_url": item.get("html_url", ""),
                "updated_at": item.get("updated_at", ""),
                "topics": item.get("topics") or [],
            })

    candidates.sort(key=lambda x: x["stars"], reverse=True)
    return candidates


def write_candidates(candidates: list[dict[str, Any]]) -> None:
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total": len(candidates),
        "note": "以下是自动发现的候选仓库，请人工审核后把需要的加入 config.json 的 repos 数组。",
        "candidates": candidates,
    }
    with open(CANDIDATES_PATH, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"\n✓ 已写入 {CANDIDATES_PATH.name}（{len(candidates)} 个候选）")
    if candidates:
        print("\n🔥 候选 TOP 10：")
        for i, c in enumerate(candidates[:10], 1):
            print(f"  {i}. {c['full_name']}  ⭐{fmt_stars(c['stars'])}  — {truncate(c['description'], 60)}")


def write_projects_json(projects: list[dict[str, Any]], config: dict[str, Any]) -> None:
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "project": config.get("project", {}),
        "total": len(projects),
        "total_stars": sum(p.get("stars", 0) for p in projects),
        "projects": projects,
    }
    with open(PROJECTS_PATH, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"✓ 已写入 {PROJECTS_PATH.name}（{len(projects)} 个项目）")


# ---------------------------------------------------------------------------
# README 渲染
# ---------------------------------------------------------------------------

def fmt_stars(n: int) -> str:
    if n >= 1000:
        return f"{n / 1000:.1f}k"
    return str(n)


def fmt_date(iso: str) -> str:
    """把 ISO 时间转成 'YYYY-MM-DD'。"""
    if not iso:
        return "-"
    try:
        return datetime.fromisoformat(iso.replace("Z", "+00:00")).strftime("%Y-%m-%d")
    except ValueError:
        return iso[:10]


def truncate(text: str, max_len: int) -> str:
    text = (text or "").replace("\n", " ").strip()
    if len(text) <= max_len:
        return text
    return text[: max_len - 1].rstrip() + "…"


def render_category_section(
    cat_key: str, cat_meta: dict[str, Any], projects: list[dict[str, Any]], max_desc: int
) -> str:
    cat_projects = [p for p in projects if p.get("category") == cat_key]
    if not cat_projects:
        return ""
    lines: list[str] = []
    lines.append(f"## {cat_meta.get('name', cat_key)}")
    lines.append("")
    if cat_meta.get("description"):
        lines.append(f"> {cat_meta['description']}")
        lines.append("")
    lines.append(f"共 **{len(cat_projects)}** 个项目。")
    lines.append("")
    lines.append("| 项目 | 对标 | 简介 | ⭐ | 语言 | License | 最近更新 |")
    lines.append("| --- | --- | --- | ---: | --- | --- | --- |")
    for p in cat_projects:
        name = p["full_name"]
        link = p.get("html_url", f"https://github.com/{name}")
        target = p.get("target", "") or "-"
        desc = truncate(p.get("description", ""), max_desc) or "-"
        stars = fmt_stars(p.get("stars", 0))
        lang = p.get("language", "") or "-"
        lic = p.get("license", "") or "-"
        updated = fmt_date(p.get("updated_at", ""))
        lines.append(
            f"| [`{name}`]({link}) | {target} | {desc} | {stars} | {lang} | {lic} | {updated} |"
        )
    lines.append("")
    return "\n".join(lines)


def render_readme(config: dict[str, Any], projects: list[dict[str, Any]]) -> str:
    proj = config.get("project", {})
    settings = config.get("settings", {})
    max_desc = int(settings.get("readme_max_desc_length", 140))
    categories = config.get("categories", {})
    total = len(projects)
    total_stars = sum(p.get("stars", 0) for p in projects)
    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    # 统计语言分布 top 5
    lang_count: dict[str, int] = {}
    for p in projects:
        lang = p.get("language") or "Unknown"
        lang_count[lang] = lang_count.get(lang, 0) + 1
    top_langs = sorted(lang_count.items(), key=lambda x: x[1], reverse=True)[:5]

    # 按 star 排序的前 10
    top10 = sort_projects(projects, "stars")[:10]

    out: list[str] = []

    # Hero
    out.append(f"# {proj.get('name', 'AI 逆向工程开源索引')}")
    out.append("")
    out.append(f"> {proj.get('tagline', '')}")
    out.append("")
    out.append(proj.get("description", ""))
    out.append("")

    # 徽标
    gh_repo = proj.get("github_repo", "")
    out.append(
        f"![项目数](https://img.shields.io/badge/项目数-{total}-brightgreen) "
        f"![总 Stars](https://img.shields.io/badge/总_Stars-{fmt_stars(total_stars)}-yellow) "
        f"![更新时间](https://img.shields.io/badge/更新-{generated_at.replace(' ', '%20')}-blue) "
        f"![自动更新](https://img.shields.io/badge/自动更新-GitHub_Actions-success)"
    )
    out.append("")

    if gh_repo:
        out.append(f"**GitHub 仓库**：[{gh_repo}](https://github.com/{gh_repo})")
        out.append("")

    # 数据概览
    out.append("## 📊 数据概览")
    out.append("")
    out.append(f"- 📦 收录项目：**{total}**")
    out.append(f"- ⭐ 累计 Stars：**{fmt_stars(total_stars)}**")
    out.append(f"- 🔠 主流语言：{', '.join(f'{l} ({c})' for l, c in top_langs)}")
    out.append("")

    # 🔥 热门 TOP 10
    out.append("## 🔥 热门 TOP 10（按 Stars）")
    out.append("")
    out.append("| # | 项目 | ⭐ | 语言 | 对标 |")
    out.append("| ---: | --- | ---: | --- | --- |")
    for i, p in enumerate(top10, 1):
        name = p["full_name"]
        link = p.get("html_url", f"https://github.com/{name}")
        stars = fmt_stars(p.get("stars", 0))
        lang = p.get("language", "") or "-"
        target = p.get("target", "") or "-"
        out.append(f"| {i} | [`{name}`]({link}) | {stars} | {lang} | {target} |")
    out.append("")

    # 分类索引
    out.append("## 📚 分类索引")
    out.append("")
    toc = []
    for cat_key, cat_meta in categories.items():
        cnt = sum(1 for p in projects if p.get("category") == cat_key)
        if cnt == 0:
            continue
        anchor = cat_meta.get("name", cat_key).lower()
        # GitHub 锚点：去掉特殊符号，空格转 -
        import re
        anchor = re.sub(r"[^\w\s-]", "", anchor).strip().replace(" ", "-")
        toc.append(f"- [{cat_meta.get('name', cat_key)}](#{anchor})（{cnt}）")
    out.extend(toc)
    out.append("")

    # 各分类详情
    for cat_key, cat_meta in categories.items():
        section = render_category_section(cat_key, cat_meta, projects, max_desc)
        if section:
            out.append(section)

    # 工作原理
    out.append("## ⚙️ 工作原理")
    out.append("")
    out.append(
        "本仓库**不部署任何服务**，一切基于 GitHub 原生能力：\n"
        "\n"
        "1. **`config.json`** — 人工维护的仓库清单与分类（唯一需要手改的文件）。\n"
        "2. **`update.py`** — 纯 Python 标准库脚本，调用 GitHub API 拉取每个仓库的最新元数据。\n"
        "3. **`projects.json`** — 机器可读的数据源（脚本自动生成）。\n"
        "4. **`candidates.json`** — 自动发现的候选仓库（`--discover` 模式生成，人工审核后加入 config）。\n"
        "5. **`README.md`** — 由脚本根据数据自动重写，呈现给人看。\n"
        "6. **`.github/workflows/update.yml`** — GitHub Actions 定时（每日 UTC 00:00）自动运行并提交更新，也支持手动触发。"
    )
    out.append("")

    # 手动更新
    out.append("## 🔄 手动更新")
    out.append("")
    out.append("```bash")
    out.append("# 可选：设置 token 提高速率限制（未认证 60 次/小时，认证 5000 次/小时）")
    out.append("# export GITHUB_TOKEN=ghp_xxx")
    out.append("")
    out.append("python3 update.py                 # 更新已有仓库 + 重写 README")
    out.append("python3 update.py --discover      # 额外搜索新候选仓库，写入 candidates.json")
    out.append("```")
    out.append("")

    # 贡献
    out.append("## 🙋 贡献")
    out.append("")
    out.append(
        "想新增一个项目？只需两步：\n"
        "\n"
        "1. 在 [`config.json`](./config.json) 的 `repos` 数组里追加一项：\n"
        "   ```json\n"
        '   { "full_name": "owner/repo", "category": "creative", "target": "对标产品" }\n'
        "   ```\n"
        "   `category` 取值见 `categories` 字段；`target` 写它逆向/重写的对象。\n"
        "2. 运行 `python3 update.py` 重新生成 `projects.json` 与 `README.md`，然后提交 PR。\n"
        "\n"
        "收录标准：以 AI 辅助逆向 / clean-room 重写闭源产品为核心的开源项目。通用逆向工具、纯模型权重仓库暂不收录。"
    )
    out.append("")

    # 免责声明
    out.append("## ⚠️ 免责声明")
    out.append("")
    out.append(
        "本仓库仅做**信息聚合索引**，不托管任何被逆向项目的源码或二进制。"
        "所列项目均为其作者的开源成果，请遵守各项目自身的 License 与适用法律。"
        "clean-room 重写不等于侵权，但使用者应自行评估法律风险。"
    )
    out.append("")

    return "\n".join(out)


def write_readme(content: str) -> None:
    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✓ 已重写 {README_PATH.name}")


def main() -> int:
    parser = argparse.ArgumentParser(description="AI 逆向工程开源索引 · 自动更新脚本")
    parser.add_argument(
        "--discover",
        action="store_true",
        help="额外搜索新的候选仓库，写入 candidates.json（不自动加入索引）",
    )
    args = parser.parse_args()

    if not CONFIG_PATH.exists():
        print(f"✗ 找不到 {CONFIG_PATH}")
        return 1

    config = load_config()
    repo_entries = config.get("repos", [])
    if not repo_entries:
        print("✗ config.json 中没有 repos")
        return 1

    print(f"▶ 开始更新，共 {len(repo_entries)} 个仓库...")
    if not (os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")):
        print("  ℹ 未设置 GITHUB_TOKEN，速率限制为 60 次/小时")

    cache = load_cached_projects()
    if cache:
        print(f"  ↻ 已加载 {len(cache)} 条缓存数据作为回退")

    projects = fetch_all_repos(repo_entries, cache)
    projects = sort_projects(projects, config.get("settings", {}).get("sort_by", "stars"))

    write_projects_json(projects, config)

    readme = render_readme(config, projects)
    write_readme(readme)

    if args.discover:
        print("\n▶ 开始自动发现候选仓库...")
        candidates = discover_candidates(config)
        write_candidates(candidates)

    print(f"\n✅ 完成：{len(projects)}/{len(repo_entries)} 个项目更新成功")
    return 0


if __name__ == "__main__":
    sys.exit(main())
