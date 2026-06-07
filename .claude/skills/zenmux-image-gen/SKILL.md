---
name: zenmux-image-gen
description: Generate images using AI via ZenMux platform. Use this skill when users ask to generate, create, draw, or produce images, pictures, photos, illustrations, or artwork. Trigger on phrases like "生成图片", "给我画一张", "创建图像", "generate an image", "draw me", "create a picture", "make an illustration", "AI画图", "AI绘画", or any request involving visual image creation by AI. Also use when users want to refine, iterate on, or modify previously generated images. Do NOT use for code-based visual art (canvas-design, algorithmic-art handle those).
---

# zenmux-image-gen

通过 ZenMux 平台调用 `openai/gpt-image-2` 模型生成图片。

## 参数收集

从用户请求中提取以下参数，尽量从上下文推断，减少询问次数。仅在无法推断时使用 AskUserQuestion 工具询问用户。

| 用户参数 | API映射 | 可选值 | 默认值 |
|----------|---------|--------|--------|
| 内容描述 | prompt字段 | 任意文本 | 必填 |
| 风格 | 融入prompt文本 | 摄影/插画/油画/水彩/动漫/赛博朋克/极简/3D渲染 | 自然摄影 |
| 用途 | 影响size推断 | 头像/壁纸/手机壁纸/海报/博客配图 | 通用 |
| 尺寸 | size字段 | 1024x1024, 1024x1536, 1536x1024, auto | 1024x1024 |
| 清晰度 | quality字段 | low, medium, high, auto | medium |

**用途到尺寸映射**：
- 头像/图标 → 1024x1024
- 桌面壁纸/横幅 → 1536x1024
- 手机壁纸/海报 → 1024x1536
- 未指定/通用 → 1024x1024

所有参数确定后，向用户展示摘要并确认后再生图。

## Prompt 构建

始终使用英文构建 prompt（模型对英文理解更好）。

**结构**：`[主体描述], [风格/艺术媒介], [构图/视角], [光照/氛围/色彩], [质量修饰]`

gpt-image-2 偏好自然语言描述，不要堆砌关键词标签。

**风格映射**：
- 摄影 → "professional photography, natural lighting, detailed"
- 插画 → "digital illustration, vibrant colors, detailed"
- 油画 → "oil painting, rich brushstrokes, canvas texture"
- 水彩 → "watercolor, soft washes, delicate transparency"
- 动漫 → "anime style, cel-shaded, vibrant"
- 赛博朋克 → "cyberpunk aesthetic, neon lights, futuristic"
- 极简 → "minimalist, clean lines, negative space"
- 3D渲染 → "3D render, realistic materials, studio lighting"

## 脚本调用

```bash
python .claude/skills/zenmux-image-gen/generate_image.py \
  --prompt "构建好的英文prompt" \
  --output "./output/generated_TIMESTAMP.png" \
  --size "1024x1024" \
  --quality "high"
```

- 输出路径默认：`./output/generated_YYYYMMDD_HHMMSS.png`
- 首次使用时检查依赖：如脚本报错缺少 requests，执行 `pip install requests`
- Bash 调用时设置 timeout=180000（180秒）

## 视觉验证（最多3次）

```
第1次：用构建的 prompt 生图
  → 使用 Read 工具读取生成的图片
  → 分析：内容匹配度、视觉质量、风格符合度
  → 满意 → 展示给用户
  → 不满意 → 进入第2次

第2次：优化 prompt（补充视觉细节：颜色、构图、光线、风格关键词）
  → 生图 → Read → 验证
  → 满意 → 展示
  → 不满意 → 进入第3次

第3次：大幅改写 prompt（换角度描述，添加否定描述避免已知问题）
  → 生图 → Read → 验证
  → 满意 → 展示
  → 仍不满意 → 展示当前最佳结果 + 详细问题分析 + 方案建议
```

## 失败处理

**3次均不满意时**，向用户提供：
1. 当前最佳图片（Read 展示）
2. 详细分析：哪个元素缺失、风格偏差、质量问题
3. 方案建议：调整描述方式、更换风格方向、提供参考图、简化/复杂化 prompt

**脚本返回 success:false 时**：
- 解析 error 字段，向用户说明具体原因
- API Key 缺失 → 引导配置 settings.local.json
- 认证失败 → 提示检查 API Key 有效性
- 速率限制 → 建议稍后重试
- 内容被拒 → 建议调整描述

## 与其他技能的边界

- **本技能**：AI 模型直接生成图片
- **canvas-design**：用代码生成视觉设计（海报、PDF 等）
- **algorithmic-art**：用代码生成交互式/算法艺术
- 如用户需求跨越边界（如"生成图片然后做成海报"），先使用本技能生图，再由用户决定下一步
