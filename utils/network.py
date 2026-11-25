import os
import requests
from pathlib import Path


def basicDownload(url: str, filepath: str, chunk_size: int = 1024 * 1024):
    """
    支持断点续传的下载函数

    Args:
        url: 下载链接
        filepath: 保存路径（含文件名）
        chunk_size: 每次写入的块大小，默认 1MB
    """
    # 已下载文件的大小（如果存在）
    downloaded = os.path.getsize(filepath) if os.path.exists(filepath) else 0

    headers = {}
    if downloaded > 0:
        headers["Range"] = f"bytes={downloaded}-"

    with requests.get(url, headers=headers, stream=True, timeout=30) as r:
        # 若服务器不支持断点续传（返回 200 而非 206），则从头开始
        if downloaded > 0 and r.status_code == 200:
            print("服务器不支持断点续传，从头下载")
            downloaded = 0
        elif downloaded > 0 and r.status_code == 206:
            print(f"从 {downloaded} 字节处继续下载")
        elif r.status_code == 416:
            print("文件已下载完整")
            return
        r.raise_for_status()

        # 计算总大小（用于进度显示）
        total = r.headers.get("Content-Length")
        total = int(total) + downloaded if total else None

        mode = "ab" if downloaded > 0 else "wb"
        with open(filepath, mode) as f:
            for chunk in r.iter_content(chunk_size=chunk_size):
                if chunk:  # 过滤 keep-alive 空块
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total:
                        percent = downloaded / total * 100
                        print(
                            f"\r下载进度: {percent:5.1f}%  "
                            f"({downloaded/1048576:.1f}/{total/1048576:.1f} MB)",
                            end="",
                            flush=True,
                        )


def fetch_export_response(
    owner: str,
    dataset: str,
    api_key: str,
    version: int | None = None,
    timeout: int = 30,
) -> dict:
    """
    请求 Ultralytics 数据集导出端点，返回完整的 HTTP 响应信息。

    Args:
        owner: 数据集所有者（用户名或团队名）
        dataset: 数据集名称（如 "coco2017"）
        api_key: Ultralytics API Key（ul_ 开头）
        version: 可选，指定版本号；不传则获取当前状态
        timeout: 请求超时秒数

    Returns:
        dict: 包含以下键值对的字典:
            "ok": bool,
            "status_code": int,
            "body": dict | str | None,
            "headers": dict,
            "error": str | None,
    """
    url = f"https://platform.ultralytics.com/api/datasets/{owner}/{dataset}/export"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json",
    }
    params = {}
    if version is not None:
        params["v"] = version

    result = {
        "ok": False,
        "status_code": None,
        "body": None,
        "headers": {},
        "error": None,
    }

    try:
        resp = requests.get(url, headers=headers, params=params, timeout=timeout)
    except requests.RequestException as e:
        result["error"] = str(e)
        return result

    result["status_code"] = resp.status_code
    result["headers"] = dict(resp.headers)
    result["ok"] = resp.status_code < 400

    # 尽量解析 JSON，失败则保留文本
    try:
        result["body"] = resp.json()
    except ValueError:
        result["body"] = resp.text

    return result


def download_coco2017_ndjson(
    api_key: str,
    owner: str = "ultralytics",
    dataset: str = "coco2017",
    output_path: str = "coco2017.ndjson",
    version: int | None = None,
    timeout: int = 30,
) -> dict:
    """
    获取最新的 COCO2017 NDJSON 文件并保存到脚本工作目录。

    流程：
    1. 调用 fetch_export_response 获取导出响应；
    2. 校验状态码和 downloadUrl；
    3. 下载 NDJSON 文件并保存。

    Returns:
        dict: 包含以下键值对的字典:
            "ok": bool,
            "message": str,
            "export_response": dict,   # 第一步的完整响应
            "download_status": int | None,
            "file_path": str | None,
        
    """

    result = {
        "ok": False,
        "message": "",
        "export_response": None,
        "download_status": None,
        "file_path": None,
    }

    # Step 1: 获取导出响应
    export_resp = fetch_export_response(
        owner=owner,
        dataset=dataset,
        api_key=api_key,
        version=version,
        timeout=timeout,
    )
    result["export_response"] = export_resp

    if not export_resp["ok"]:
        result["message"] = (
            f"导出接口失败，HTTP {export_resp['status_code']}，"
            f"body: {export_resp['body']}"
        )
        return result

    # Step 2: 提取 downloadUrl
    body = export_resp["body"]
    if not isinstance(body, dict):
        result["message"] = f"导出响应 body 不是 JSON 对象: {body}"
        return result

    download_url = body.get("downloadUrl")
    if not download_url:
        result["message"] = "导出响应中未找到 downloadUrl。" f"完整 body: {body}"
        return result

    cached = body.get("cached", False)
    print(f"[导出] downloadUrl 已获取（cached={cached}）")

    # Step 3: 下载文件（签名 URL 通常无需再带 Authorization）
    abs_path = Path.cwd() / output_path
    try:
        with requests.get(download_url, stream=True, timeout=timeout) as r:
            result["download_status"] = r.status_code
            if r.status_code >= 400:
                result["message"] = f"文件下载失败，HTTP {r.status_code}"
                return result

            with open(abs_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
    except requests.RequestException as e:
        result["message"] = f"文件下载异常: {e}"
        return result

    result["ok"] = True
    result["message"] = f"NDJSON 已保存至: {abs_path}"
    result["file_path"] = str(abs_path)
    return result


# 使用示例
if __name__ == "__main__":
    basicDownload(
        url="",
        filepath="",
    )
