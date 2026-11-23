import os
import requests


def basicDownload(url: str, filepath: str, chunk_size: int = 1024 * 1024):
    """
    支持断点续传的下载函数
    :param url: 下载链接
    :param filepath: 保存路径（含文件名）
    :param chunk_size: 每次写入的块大小，默认 1MB
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


# 使用示例
if __name__ == "__main__":
    basicDownload(
        url="",
        filepath="",
    )
