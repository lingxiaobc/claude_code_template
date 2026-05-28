# Claude Code 项目模板

一键初始化带有完整 AI 辅助开发环境的项目模板。内置多代理协作架构、自动提交钩子、20+ 专业技能，开箱即用。

## 快速开始

```bash
# 1. 克隆模板
git clone <此仓库地址> <你的项目名>
cd <你的项目名>

# 2. 重置为你的仓库
rm -rf .git
git init

# 3. 配置 API 密钥
cp .claude/settings.local.json.example .claude/settings.local.json
# 编辑 settings.local.json，填入你的 API 地址和认证令牌

# 4. 提交初始状态
git add .
git commit -m "init: 项目初始化"
```

启动 Claude Code 后即可直接使用，无需额外配置。

## 架构概览

```
.claude/
├── agents/                   # 专用子代理
│   ├── project-searcher.md   #   项目内容搜索（强制）
│   └── web-searcher.md       #   联网搜索（强制）
├── hooks/                    # 自动化钩子
│   └── auto-commit.sh        #   文件变更自动提交
├── skills/                   # 技能库（20+ 技能）
│   ├── plan-tasks/           #   任务规划（主程序专属）
│   ├── skill-creator/        #   技能创建（主程序专属）
│   ├── backend-engineering-workflow/
│   ├── frontend-development-workflow/
│   ├── database-engineering/
│   ├── claude-api/
│   └── ...                   #   更多技能见下方列表
├── settings.json             # 共享配置（提交至仓库）
└── settings.local.json       # 本地配置（API 密钥，不提交）
```

## 核心机制

### 多代理协作

主程序作为调度者和审核者，不直接执行任务，而是委派给子代理完成：

- **独立任务** → 并行开多个子代理同时执行
- **有关联的任务** → 通过 Team 协作组协调，共享任务列表和信息
- **主程序全程把控方向**，审核产出，发现偏差时及时干预修正

### 强制代理

所有搜索操作必须通过专用代理，主程序不得绕过：

| 代理 | 职责 | 可用工具 |
|------|------|----------|
| `project-searcher` | 项目内搜索（文件、代码、目录） | Grep, Glob, Read |
| `web-searcher` | 联网查询（文档、API、外部信息） | WebSearch, WebFetch |

### 自动提交

每次文件编辑（Edit/Write/NotebookEdit）后，`auto-commit.sh` 自动暂存并提交：
- 自动跳过 `.git/`、`settings.local.json`、大于 10MB 的文件
- 提交格式：`auto: [update|create] <文件名>`

## 技能列表

技能分为两类：**主程序专属**（仅主程序可调用）和**通用技能**（可授权给子代理）。

### 主程序专属

| 技能 | 说明 |
|------|------|
| `plan-tasks` | 大规模变更的任务规划，在 `TASK/` 目录生成结构化任务明细，逐项跟踪 |
| `skill-creator` | 创建和管理新技能 |

### 开发工作流

| 技能 | 说明 |
|------|------|
| `backend-engineering-workflow` | 后端服务全流程：API 开发、数据库集成、性能优化、测试 |
| `frontend-development-workflow` | 前端开发全流程：UI 构建、组件开发、状态管理 |
| `database-engineering` | 数据库工程：Schema 设计、迁移、查询优化、索引策略 |
| `claude-api` | Claude API / Anthropic SDK 应用的构建、调试和优化 |
| `mcp-builder` | MCP 服务器构建 |
| `webapp-testing` | Web 应用测试 |

### 设计与创意

| 技能 | 说明 |
|------|------|
| `frontend-design` | 前端 UI 设计 |
| `canvas-design` | Canvas 可视化设计 |
| `algorithmic-art` | 基于 p5.js 的生成艺术 |
| `theme-factory` | 主题/样式工厂 |
| `brand-guidelines` | 品牌规范设计 |
| `web-artifacts-builder` | Web 组件构建 |

### 文档与办公

| 技能 | 说明 |
|------|------|
| `doc-coauthoring` | 文档协作撰写 |
| `docx` | Word 文档生成 |
| `pdf` | PDF 文档处理 |
| `pptx` | PowerPoint 演示文稿生成 |
| `xlsx` | Excel 电子表格处理 |
| `internal-comms` | 内部沟通文档 |

### 其他

| 技能 | 说明 |
|------|------|
| `slack-gif-creator` | Slack GIF 动图创建 |

## 任务执行流程

```
用户请求
  │
  ▼
主程序接收 → 分析需求，判断是否需要任务规划
  │
  ├── 简单任务（单文件/单函数级别）
  │     └── 直接委派单个子代理执行
  │
  └── 复杂任务（多文件/多模块）
        │
        ▼
    plan-tasks 生成任务计划（TASK/ 目录）
        │
        ▼
    分析任务依赖关系
        │
        ├── 独立任务 → 并行开子代理执行
        │
        └── 关联任务 → Team 协作组执行
              │
              ▼
        审核子代理产出 ←→ 发现偏差则退回修正
              │
              ▼
        所有任务完成 → 汇报结果
```

## 配置说明

### settings.local.json（本地配置）

每个开发者独立配置，不提交至仓库：

```json
{
    "model": "sonnet",
    "availableModels": ["sonnet", "opus", "haiku"],
    "effortLevel": "high",
    "env": {
        "ANTHROPIC_BASE_URL": "你的 API 地址",
        "ANTHROPIC_AUTH_TOKEN": "你的认证令牌",
        "ANTHROPIC_DEFAULT_SONNET_MODEL": "模型名称",
        "ANTHROPIC_DEFAULT_HAIKU_MODEL": "模型名称"
    }
}
```

参考 `settings.local.json.example` 创建。

### settings.json（共享配置）

钩子定义和团队共享设置，提交至仓库。当前配置了 PostToolUse 自动提交钩子。

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

使用主程序调用 `skill-creator` 技能，或在 `.claude/skills/` 下创建子目录和 `SKILL.md`。

### 修改钩子

编辑 `.claude/settings.json` 中的 `hooks` 配置，钩子脚本放在 `.claude/hooks/` 目录。

## 注意事项

- `settings.local.json` 已在 `.gitignore` 中，敏感信息不会泄露
- `auto-commit.sh` 兼容 Windows Git Bash 和 Linux/macOS
- 代理默认使用 haiku 模型以控制成本，可在各代理 `.md` 文件中修改 `model` 字段
- `plan-tasks` 和 `skill-creator` 为主程序专属技能，不可委托给子代理
