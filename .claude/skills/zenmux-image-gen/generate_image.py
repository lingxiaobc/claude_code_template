"""
ZenMux Image Generator - 通过 ZenMux 平台调用 openai/gpt-image-2 生图

Usage:
    python generate_image.py --prompt "描述" --output 输出路径 [选项]

Output:
    JSON to stdout: {"success": bool, "image_path": str, "error": str, "attempt": int}
"""

import argparse
import base64
import json
import sys
import time
from pathlib import Path

try:
    import requests
except ImportError:
    print(json.dumps({
        "success": False,
        "error": "缺少 requests 库，请运行: pip install requests",
        "attempt": 0
    }, ensure_ascii=False))
    sys.exit(1)

API_URL = "https://zenmux.ai/api/v1/images/generations"
MODEL = "openai/gpt-image-2"
REQUEST_TIMEOUT = 120


def load_api_key(config_path=None):
    """从环境变量或配置文件加载 API Key。

    优先级：环境变量 ZENMUX_API_KEY > 配置文件 env.ZENMUX_API_KEY
    """
    # 1. 环境变量
    key = __import__("os").environ.get("ZENMUX_API_KEY", "").strip()
    if key:
        return key

    # 2. 配置文件
    if config_path:
        paths_to_check = [Path(config_path)]
    else:
        # 自动向上查找 .claude/settings.local.json
        current = Path(__file__).resolve()
        for parent in list(current.parents):
            candidate = parent / ".claude" / "settings.local.json"
            if candidate.exists():
                paths_to_check = [candidate]
                break
        else:
            paths_to_check = []

    for config_file in paths_to_check:
        if config_file and config_file.exists():
            try:
                with open(config_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                key = data.get("env", {}).get("ZENMUX_API_KEY", "").strip()
                if key and key != "YOUR_ZENMUX_API_KEY":
                    return key
            except (json.JSONDecodeError, OSError):
                pass

    return ""


def generate_image(prompt, size, quality, api_key, output_format=None,
                   output_compression=None, background=None):
    """调用 ZenMux API 生成图片，返回响应 JSON。"""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    body = {
        "model": MODEL,
        "prompt": prompt,
        "n": 1,
        "size": size,
        "quality": quality,
        "response_format": "b64_json",
    }

    if output_format:
        body["output_format"] = output_format
    if output_compression is not None:
        body["output_compression"] = output_compression
    if background:
        body["background"] = background

    response = requests.post(API_URL, headers=headers, json=body,
                             timeout=REQUEST_TIMEOUT)
    response.raise_for_status()
    return response.json()


def save_image(response_data, output_path):
    """从 API 响应中提取图片数据并保存到文件。"""
    item = response_data["data"][0]

    # 优先使用 b64_json
    if "b64_json" in item and item["b64_json"]:
        image_bytes = base64.b64decode(item["b64_json"])
    elif "url" in item and item["url"]:
        img_response = requests.get(item["url"], timeout=60)
        img_response.raise_for_status()
        image_bytes = img_response.content
    else:
        raise ValueError("API 响应中未包含图片数据（b64_json 或 url）")

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "wb") as f:
        f.write(image_bytes)

    return str(output_path)


def output_result(success, attempt, image_path=None, error=None):
    """输出 JSON 结果到 stdout。"""
    result = {"success": success, "attempt": attempt}
    if image_path:
        result["image_path"] = image_path
    if error:
        result["error"] = error
    print(json.dumps(result, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser(
        description="ZenMux Image Generator - 调用 openai/gpt-image-2 生图")
    parser.add_argument("--prompt", required=True, help="图片描述")
    parser.add_argument("--output", required=True, help="输出文件路径")
    parser.add_argument("--size", default="1024x1024",
                        choices=["1024x1024", "1024x1536", "1536x1024", "auto"],
                        help="图片尺寸 (默认: 1024x1024)")
    parser.add_argument("--quality", default="high",
                        choices=["low", "medium", "high", "auto"],
                        help="图片质量 (默认: high)")
    parser.add_argument("--output-format", default=None,
                        choices=["png", "jpeg", "webp"],
                        help="输出格式 (默认: png)")
    parser.add_argument("--output-compression", type=int, default=None,
                        help="压缩级别 0-100 (仅 jpeg/webp)")
    parser.add_argument("--background", default=None,
                        choices=["transparent", "opaque", "auto"],
                        help="背景设置")
    parser.add_argument("--config", default=None,
                        help="settings.local.json 路径")
    parser.add_argument("--max-retries", type=int, default=3,
                        help="API 异常重试次数 (默认: 3)")

    args = parser.parse_args()

    # 加载 API Key
    api_key = load_api_key(args.config)
    if not api_key:
        output_result(False, 0,
                      error="API Key 缺失。请在 .claude/settings.local.json "
                            "中配置 env.ZENMUX_API_KEY，或设置环境变量 "
                            "ZENMUX_API_KEY。")
        sys.exit(1)

    # 验证 output-compression 范围
    if args.output_compression is not None:
        if not 0 <= args.output_compression <= 100:
            output_result(False, 0,
                          error="--output-compression 必须在 0-100 之间")
            sys.exit(1)

    # 带重试的生图
    last_error = ""
    for attempt in range(1, args.max_retries + 1):
        try:
            response_data = generate_image(
                prompt=args.prompt,
                size=args.size,
                quality=args.quality,
                api_key=api_key,
                output_format=args.output_format,
                output_compression=args.output_compression,
                background=args.background,
            )
            image_path = save_image(response_data, args.output)
            output_result(True, attempt, image_path=image_path)
            sys.exit(0)

        except requests.exceptions.HTTPError as e:
            status_code = e.response.status_code if e.response is not None else "unknown"
            try:
                error_body = e.response.json() if e.response is not None else {}
                error_msg = error_body.get("error", {}).get("message", str(e))
            except (json.JSONDecodeError, AttributeError):
                error_msg = str(e)
            last_error = f"HTTP {status_code}: {error_msg}"
            if status_code in (401, 403):
                # 认证失败不重试
                break
            if status_code == 422:
                # 内容被拒不重试
                break

        except requests.exceptions.Timeout:
            last_error = "请求超时（120秒），请稍后重试"

        except requests.exceptions.ConnectionError:
            last_error = "网络连接失败，请检查网络"

        except ValueError as e:
            last_error = str(e)
            break

        except Exception as e:
            last_error = f"未知错误: {str(e)}"
            break

        if attempt < args.max_retries:
            time.sleep(2)

    output_result(False, attempt, error=last_error)
    sys.exit(1)


if __name__ == "__main__":
    main()
