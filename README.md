# Claude Code 项目模板

一键初始化带有完整 AI 辅助开发环境的项目模板。内置多代理协作架构、Worktree 安全隔离、自动提交钩子、20+ 专业技能，开箱即用。

## 这是什么？

如果你在用 [Claude Code](https://docs.anthropic.com/en/docs/claude-code)（Anthropic 官方 CLI 工具）写代码，这个模板帮你：

- **不用每次从零配置** — 克隆即用，`.claude/` 目录下已经配好了代理、钩子、技能
- **多代理协作** — 主程序调度，子代理干活，互不干扰
- **安全隔离** — 子代理在独立 worktree 中改代码，主程序审核通过后才合并，不会搞坏你的主分支
- **自动提交** — 每次文件改动自动生成 commit，不怕丢进度

## 快速开始

### 前提条件

- 已安装 [Claude Code CLI](https://docs.anthropic.com/en/docs/claude-code)
- 有可用的 Anthropic API 密钥（或兼容的 API 服务）

### 3 步初始化

```bash
# 1. 克隆模板到你的新项目目录
git clone https://gitee.com/lingxiaobc/claude_code_template.git <你的项目名>
cd <你的项目名>

# 2. 重置 Git 为你自己的仓库
rm -rf .git
git init

# 3. 配置你的 API 密钥
cp .claude/settings.local.json.example .claude/settings.local.json
# 编辑 settings.local.json，填入你的 API 地址和认证令牌（见下方"配置"章节）

# 4. 提交初始状态
git add .
git commit -m "init: 项目初始化"
```

启动 Claude Code（在终端运行 `claude`），即可开始使用。

## 目录结构

```
你的项目/
├── .claude/                        # Claude Code 配置目录
│   ├── agents/                     # 子代理定义
│   │   ├── project-searcher.md     #   项目内搜索代理
│   │   └── web-searcher.md         #   联网搜索代理
│   ├── hooks/                      # 自动化钩子
│   │   └── auto-commit.sh          #   文件变更自动提交
│   ├── skills/                     # 技能库（20+ 技能）
│   │   ├── plan-tasks/             #   任务规划（主程序专属）
│   │   ├── skill-creator/          #   技能创建（主程序专属）
│   │   └── ...                     #   其他技能
│   ├── settings.json               # 共享配置（提交至仓库）
│   └── settings.local.json         # 你的本地配置（API 密钥，不提交）
├── CLAUDE.md                       # 行为准则和架构说明
└── README.md                       # 本文件
```

## 核心概念

### 主程序 vs 子代理

这个模板的核心思路是 **"主程序不动手，子代理干脏活"**：

| 角色 | 职责 | 类比 |
|------|------|------|
| **主程序** | 接收请求、规划任务、审核结果、把控方向 | 项目经理 |
| **子代理** | 编码、搜索、查资料等具体执行工作 | 开发工程师 |

### Worktree 隔离（安全机制）

子代理改代码时**不会直接改你的主分支**。流程如下：

```
子代理收到任务
  │
  ▼
在独立 worktree（工作副本）中修改文件
  │
  ▼
主程序审核变更内容
  │
  ├── 审核通过 → 合并到 main 分支，清理 worktree
  │
  └── 审核不通过 → 退回子代理修正
```

这意味着即使子代理改出了问题代码，你的 main 分支也不会被污染。

### 强制代理

搜索操作必须通过专用代理，主程序不能直接搜索：

| 代理 | 作用 | 怎么用 |
|------|------|--------|
| `project-searcher` | 在项目内搜索文件和代码 | 查文件在哪、查函数定义、查引用 |
| `web-searcher` | 联网搜索外部信息 | 查文档、查 API 用法、查技术方案 |

### 自动提交

每次文件编辑后，`auto-commit.sh` 会自动生成一条 commit：
- 提交格式：`auto: update 文件名` 或 `auto: create 文件名`
- 自动跳过 `.git/`、`settings.local.json`、大于 10MB 的文件

## 配置说明

### settings.local.json（你的本地配置）

这个文件存放你的 API 密钥等敏感信息，已在 `.gitignore` 中，**不会提交到仓库**。

复制示例文件后编辑：

```bash
cp .claude/settings.local.json.example .claude/settings.local.json
```

完整格式参考 `settings.local.json.example`，需要你填写的字段：

```json
{
    "model": "sonnet",
    "availableModels": ["sonnet", "opus", "haiku", "opusplan"],
    "effortLevel": "high",
    "env": {
        "ANTHROPIC_BASE_URL": "填你的 API 地址",
        "ANTHROPIC_AUTH_TOKEN": "填你的认证令牌",
        "ANTHROPIC_DEFAULT_OPUS_MODEL": "opus 模型名称",
        "ANTHROPIC_DEFAULT_SONNET_MODEL": "sonnet 模型名称",
        "ANTHROPIC_DEFAULT_HAIKU_MODEL": "haiku 模型名称"
    },
    "permissions": {
        "allow": []
    }
}
```

| 字段 | 说明 |
|------|------|
| `ANTHROPIC_BASE_URL` | API 服务地址（第三方兼容服务填对应地址） |
| `ANTHROPIC_AUTH_TOKEN` | 认证令牌 |
| `ANTHROPIC_DEFAULT_*_MODEL` | 各级别模型的实际名称（按你的服务商要求填写） |

示例文件中还包含团队协作、遥测开关等环境变量，一般保持默认即可，详见 `.claude/settings.local.json.example`。

### settings.json（共享配置）

钩子定义和团队共享设置，提交至仓库。当前配置了 PostToolUse 自动提交钩子。

## 技能列表

技能是预定义的工作流模板，按需使用。

### 主程序专属

| 技能 | 说明 |
|------|------|
| `plan-tasks` | 大规模变更任务规划，生成结构化任务清单 |
| `skill-creator` | 创建和管理新技能 |

### 开发工作流

| 技能 | 说明 |
|------|------|
| `backend-engineering-workflow` | 后端全流程：API、数据库、测试 |
| `frontend-development-workflow` | 前端全流程：UI、组件、状态管理 |
| `database-engineering` | 数据库：Schema、迁移、查询优化 |
| `claude-api` | Claude API / Anthropic SDK 开发 |
| `mcp-builder` | MCP 服务器构建 |
| `webapp-testing` | Web 应用测试 |

### 设计与创意

| 技能 | 说明 |
|------|------|
| `frontend-design` | 前端 UI 设计 |
| `canvas-design` | Canvas 可视化设计 |
| `algorithmic-art` | p5.js 生成艺术 |
| `theme-factory` | 主题/样式工厂 |
| `brand-guidelines` | 品牌规范 |
| `web-artifacts-builder` | Web 组件构建 |

### 文档与办公

| 技能 | 说明 |
|------|------|
| `doc-coauthoring` | 文档协作撰写 |
| `docx` | Word 文档 |
| `pdf` | PDF 处理 |
| `pptx` | PowerPoint 演示文稿 |
| `xlsx` | Excel 表格 |
| `internal-comms` | 内部沟通文档 |

## 自定义扩展

### 添加新代理

在 `.claude/agents/` 下创建 `.md` 文件：

```markdown
---
name: my-agent
description: "代理描述"
tools: Tool1, Tool2
disallowedTools: Tool3
model: haiku
---

代理的具体指令...
```

### 添加新技能

用主程序调用 `/skill-creator` 技能，或在 `.claude/skills/` 下手动创建。

### 修改钩子

编辑 `.claude/settings.json` 中的 `hooks` 部分，钩子脚本放在 `.claude/hooks/`。

## 任务执行流程

```
你的请求
  │
  ▼
主程序接收 → 分析需求
  │
  ├── 简单任务（改个变量、加个函数）
  │     └── 单个子代理在 worktree 中完成
  │
  └── 复杂任务（多文件、多模块）
        │
        ▼
    plan-tasks 生成任务清单
        │
        ▼
    分析任务依赖
        │
        ├── 无依赖 → 多个子代理并行执行（各自独立 worktree）
        │
        └── 有关联 → Team 协作组（共享任务列表）
              │
              ▼
    主程序审核每个 worktree 中的变更
        │
        ├── 通过 → 合并到 main
        └── 不通过 → 退回修正
```

## 常见问题

**Q: 自动提交太吵了，能关掉吗？**
编辑 `.claude/settings.json`，删除 `hooks` 部分。

**Q: 子代理默认用 haiku 模型，太弱了怎么办？**
编辑对应代理的 `.md` 文件，把 `model: haiku` 改成 `model: sonnet`。

**Q: 我想用自己的 API 服务（非官方）？**
在 `settings.local.json` 中设置 `ANTHROPIC_BASE_URL` 和 `ANTHROPIC_AUTH_TOKEN` 即可。

**Q: `settings.local.json` 会被提交吗？**
不会，它已在 `.gitignore` 中。
