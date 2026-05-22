# Claude Code 配置模板仓库

快速初始化新项目的 AI 辅助开发环境。克隆后即可获得标准化的 Claude Code 配置基础设施。

## 快速开始

```bash
# 1. 克隆此模板到新项目目录
git clone <此仓库地址> <你的项目名>
cd <你的项目名>

# 2. 删除模板的 git 历史，初始化你自己的仓库
rm -rf .git
git init

# 3. 配置本地环境变量
cp .claude/settings.local.json.example .claude/settings.local.json
# 编辑 settings.local.json，填入你的 API 配置

# 4. 首次提交
git add .
git commit -m "init: 项目初始化"
```

## 目录结构

```
.claude/
├── agents/                    # 自定义专用代理
│   ├── project-searcher.md    # 项目内容搜索代理（强制代理）
│   └── web-searcher.md        # 联网搜索代理（强制代理）
├── hooks/                     # 自动化钩子
│   └── auto-commit.sh         # PostToolUse 自动提交脚本
├── skills/                    # 自定义技能
│   └── plan-tasks/            # 大规模变更任务规划技能
│       └── SKILL.md
├── settings.json              # 主配置（钩子、共享设置，提交至仓库）
└── settings.local.json        # 本地覆盖（API 密钥、模型配置，不提交）
```

## 核心机制

### 强制代理模式

- **project-searcher**：所有项目内部搜索必须通过此代理，主程序不得直接使用 Grep/Glob/Read
- **web-searcher**：所有联网搜索必须通过此代理，主程序不得直接使用 WebSearch/WebFetch
- 代理使用 haiku 模型，经济高效

### 自动提交

每次 Edit/Write/NotebookEdit 操作后，`auto-commit.sh` 自动暂存并提交变更。
- 自动跳过 `.git/` 目录和 `settings.local.json`
- 提交格式：`auto: [update|create] [文件名]`

### 任务规划技能

当变更涉及多个文件时，`plan-tasks` 技能自动激活，生成结构化的任务明细列表并逐项跟踪。

## 配置说明

### settings.json（共享配置，提交至仓库）

钩子定义和团队共享设置。当前配置了 PostToolUse 自动提交钩子。

### settings.local.json（本地配置，不提交）

每个开发者独立配置，包含：
- 模型选择和 API 端点
- 认证凭据
- 个人偏好设置

首次使用时参考 `settings.local.json.example` 创建。

## 自定义

### 添加新代理

在 `.claude/agents/` 下创建 `.md` 文件，使用以下 frontmatter：

```markdown
---
name: my-agent
description: "代理描述"
tools: Tool1, Tool2
disallowedTools: Tool3
model: haiku
color: blue
---

代理的具体指令...
```

### 添加新技能

在 `.claude/skills/` 下创建子目录和 `SKILL.md` 文件。

### 修改钩子

编辑 `.claude/settings.json` 中的 `hooks` 配置，钩子脚本放在 `.claude/hooks/` 目录。

## 注意事项

- `settings.local.json` 已在 `.gitignore` 中，不会提交敏感信息
- `auto-commit.sh` 支持 Windows Git Bash 和 Linux/macOS 环境
- 代理模型默认为 haiku，如需更改请编辑各代理 `.md` 文件中的 `model` 字段
