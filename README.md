# AI Knowledge Distiller V1.2 / AI 知识蒸馏助手

一个用于 Codex 的 Skill：筛选 X / 网页 / 视频字幕 / GitHub 资源 / 课程转写稿的实际学习价值，将知识提炼成长期可复用的 Markdown，并在**明确授权**的前提下辅助检索、增量更新 Obsidian 笔记。

## 能做什么

- 阶段 0：价值筛选；已知、低价值内容可以建议跳过。
- 阶段 A：知识提炼草稿与人工审核；**不自行进入阶段 B**。
- 阶段 B：批准后生成 Markdown、实操指南或资源合集；保留原始来源及状态，区分原文与推断。
- Obsidian 模式（默认目标）：有读取授权且知道 Vault 路径时，检索已有正式笔记与原始课程转写稿，比较知识点，建议跳过/合并/新建。
- 普通 Markdown 模式：不依赖 Obsidian，直接输出 Markdown 成果；不虚构 Vault 去重结果。
- Vault 写入：阶段 A 审核与实际写入是不同权限；修改前必须展示候选及 Diff，获得二次明确批准，并检查 Git 状态。

## 安装

将此仓库的 `ai-knowledge-distiller` Skill 目录（即含 `SKILL.md`、`references/` 等文件的整个目录）复制到 Codex 实际使用的用户级 Skills 目录（通常是 `$CODEX_HOME/skills/ai-knowledge-distiller`；如未设置 CODEX_HOME，在支持的环境通常是 `~/.codex/skills/ai-knowledge-distiller`）。不要将 Vault 放进 Skill 目录。重新启动/刷新 Codex 后尝试 `$ai-knowledge-distiller`。

本仓库 ZIP 采用文件夹名 `ai-knowledge-distiller-v1.2` 以便辨认；安装时可将该整个文件夹重命名为 `ai-knowledge-distiller`，保持内部结构不变。

## 快速开始

- “使用 `$ai-knowledge-distiller` 分析以下 X 帖子，先执行阶段 A，等待我确认。”
- “使用 `$ai-knowledge-distiller`，我没有 Obsidian，请使用普通 Markdown 模式整理这三个 GitHub 项目。”
- “使用 `$ai-knowledge-distiller`，请只读检索我的 Obsidian Vault 与这篇文章相似的已有知识，给出跳过/合并/新建建议；不要修改文件。”

## 重要限制

- 脚本只能提供候选搜索和路径/Git 预检，不会自动判断语义重复，也不会自动写入文件。
- 长篇转写稿可能缺标题/YAML，搜索命中不代表知识覆盖；必须阅读上下文。
- Git 检查不能完全排除并发编辑、文件系统链接和格式问题；用户应检查 Diff、保存自己的备份。
- V1.2 新增的集成规则仍需在用户的实际 Codex 环境重新验证。之前的四场景模拟测试结果由用户报告，不能作为本 ZIP 已被独立验证的证明。
- 未包含任何私人 Obsidian Vault 或本地测试数据。

## 结构

- `SKILL.md` — Codex 入口
- `references/AI知识蒸馏助手_V1.1_正式规范.md` — 保留的 V1.1 规则
- `references/Obsidian集成_V1.2_增补规范.md` — V1.2 增补
- `assets/` — 阶段 B 与阶段 A 模板
- `scripts/` — 可选只读工具
- `evals/` — 回归测试清单

## 版本

- V1.1：阶段 0/A/B、资源合集、低价值跳过、来源与人工审核。
- V1.2：Obsidian/Markdown 双模式、正式笔记与原始资料分层、长文检索、报告格式和 Vault 写入安全门禁。

## 许可证

本项目采用 [MIT License](LICENSE)，Copyright (c) 2026 Haluwjm-Lexie。