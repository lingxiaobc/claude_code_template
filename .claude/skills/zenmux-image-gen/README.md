# zenmux-image-gen

通过 [ZenMux](https://zenmux.ai) 平台调用 `openai/gpt-image-2` 模型生成图片的 Claude Code 技能。

## 目录结构

```
.claude/skills/zenmux-image-gen/
├── README.md           # 本文件 — 技能说明文档
├── SKILL.md            # 技能定义文件 — Claude Code 触发规则、参数映射、工作流程
└── generate_image.py   # Python 生图脚本 — 封装 API 调用、重试、质量降级逻辑
```

## 快速开始

### 1. 安装依赖

```bash
pip install requests
```

### 2. 配置 API Key

需要 [ZenMux](https://zenmux.ai) 平台的 API Key。支持两种配置方式（优先级从高到低）：

#### 方式 A：环境变量（推荐用于 CI/CD）

```bash
export ZENMUX_API_KEY="sk-ai-v1-your-api-key-here"
```

#### 方式 B：Claude Code 配置文件（推荐用于本地开发）

在项目根目录的 `.claude/settings.local.json` 中添加：

```json
{
  "env": {
    "ZENMUX_API_KEY": "sk-ai-v1-your-api-key-here"
  }
}
```

> **注意**：`settings.local.json` 已在 `.gitignore` 中，不会被提交到版本库。请勿将 API Key 硬编码到 `settings.json`（该文件会被提交）。

### 3. 使用

在 Claude Code 中直接用自然语言请求即可触发该技能：

```
生成一张橘猫看夕阳的图片
```

```
给我画一张赛博朋克风格的城市夜景，手机壁纸尺寸
```

```
create an illustration of a dragon in watercolor style
```

Claude Code 会自动识别意图、构建 prompt、调用脚本生成图片。

## 手动调用脚本

也可以直接在命令行调用 `generate_image.py`：

```bash
python .claude/skills/zenmux-image-gen/generate_image.py \
  --prompt "A cute orange tabby cat sitting on a windowsill, warm sunset, professional photography" \
  --output "./output/my_image.png" \
  --size "1024x1024" \
  --quality "medium"
```

### 参数说明

| 参数 | 必填 | 默认值 | 说明 |
|------|------|--------|------|
| `--prompt` | ✅ | — | 图片描述文本，英文效果最佳 |
| `--output` | ✅ | — | 输出图片文件路径（自动创建目录） |
| `--size` | ❌ | `1024x1024` | 图片尺寸，可选：`1024x1024`、`1024x1536`、`1536x1024`、`auto` |
| `--quality` | ❌ | `medium` | 图片质量，可选：`low`、`medium`、`high`、`auto` |
| `--output-format` | ❌ | `png` | 输出格式，可选：`png`、`jpeg`、`webp` |
| `--output-compression` | ❌ | — | 压缩级别 0-100（仅 jpeg/webp） |
| `--background` | ❌ | — | 背景设置，可选：`transparent`、`opaque`、`auto` |
| `--config` | ❌ | 自动查找 | `settings.local.json` 路径（默认从脚本位置向上查找） |
| `--max-retries` | ❌ | `3` | API 请求失败时的重试次数 |

### 输出格式

脚本向 stdout 输出 JSON：

```json
{"success": true, "attempt": 1, "image_path": "output/my_image.png"}
```

```json
{"success": false, "attempt": 3, "error": "网络连接失败，请检查网络"}
```

| 字段 | 说明 |
|------|------|
| `success` | 是否生成成功 |
| `attempt` | 第几次尝试成功/失败 |
| `image_path` | 成功时输出图片路径 |
| `error` | 失败时的错误信息 |

## 质量等级与性能

| 质量等级 | 响应时间 | 说明 |
|----------|----------|------|
| `low` | ~15s | 快速出图，适合预览 |
| `medium` | ~50s | **默认推荐**，质量与速度平衡 |
| `high` | ⚠️ 不稳定 | 服务端约 60 秒超时，脚本会自动降级到 `medium` |
| `auto` | 取决于平台 | 由模型自行决定 |

> **注意**：`quality=high` 会触发自动降级机制——脚本检测到连接失败后自动切换到 `medium` 质量，无需手动干预。

## 工作流程

```
用户请求 → SKILL.md 触发技能
         → Claude 构建英文 prompt
         → 调用 generate_image.py
         → 脚本发送 API 请求（带 session retry）
         → 成功 → 保存图片 → Read 展示给用户
         → high 失败 → 自动降级到 medium 重试
         → 全部失败 → 返回错误信息
```

## 常见问题

### API Key 缺失

**报错**：`API Key 缺失。请在 .claude/settings.local.json 中配置...`

**解决**：参照上方 [配置 API Key](#2-配置-api-key) 章节。

### 认证失败

**报错**：`HTTP 401: ...` 或 `HTTP 403: ...`

**解决**：检查 API Key 是否正确、是否过期。登录 ZenMux 平台确认 Key 状态。

### 内容被拒

**报错**：`HTTP 422: ...`

**解决**：调整图片描述，避免敏感或违规内容。

### 网络连接失败

**报错**：`网络连接失败，请检查网络`

**解决**：
1. 确认可以访问 `https://zenmux.ai`
2. 如果使用代理，确保已正确配置
3. 脚本会自动重试 3 次，间歇性网络问题通常可自动恢复

### 缺少 requests 库

**报错**：`缺少 requests 库，请运行: pip install requests`

**解决**：`pip install requests`

## 技能边界

- **本技能**：AI 模型直接生成图片（照片、插画、绘画等）
- **canvas-design**：用代码生成视觉设计（海报、PDF 等）
- **algorithmic-art**：用代码生成算法艺术（粒子系统、流场等）

跨边界需求（如"生成图片后做成海报"）应先使用本技能生图，再由用户决定下一步。
