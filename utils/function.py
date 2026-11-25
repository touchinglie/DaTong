import os
from os import path
from pathlib import Path
import sys
import time
import shutil
from psutil import cpu_count
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import lru_cache

@lru_cache()
def detectCPUThreads() -> int:
    return cpu_count()

def SafeThreading(functions) -> threading.Thread:
    aThread = threading.Thread(target=functions)
    aThread.daemon = True
    return aThread


def get_app_utils_dir() -> str:
    """返回用户实际工作目录下工具文件夹绝对路径"""
    if getattr(sys, "frozen", False):
        # PyInstaller 打包后运行：sys.executable 指向 exe 本身
        return os.path.dirname(os.path.abspath(sys.executable))
    else:
        # 普通脚本运行：__file__ 指向脚本本身
        return os.path.dirname(os.path.abspath(__file__))


def get_app_root_dir() -> str:
    """返回用户实际工作目录下项目根目录绝对路径"""
    return Path(get_app_utils_dir()).parent


def checkFolders(folderPath: str) -> None:
    if not path.exists(folderPath):
        os.mkdir(folderPath)
        if not path.exists(folderPath):
            raise IOError("The folder isn't been created expected.")

    if path.isfile(folderPath):
        print(f"Never create file named '{folderPath}' in working directory")
        raise ValueError(
            f"Delete {folderPath} file which located in working directory first!"
        )

def scanner_file(url) -> None:
    global dataList
    # 查看指定目录下的文件
    files = os.listdir(url)
    # print(files)``
    for i in files:
        # real_path = url + "\\" + i
        # real_path = url + os.sep + i
        real_path = path.join(url, i)
        if path.isfile(real_path):
            s = real_path.split(".")
            ss = s[len(s) - 1]
            if ss == "jpg" or ss == "png" or ss == "jpeg" or ss == "txt":
                if "\\" in real_path:
                    real_path = real_path.replace("\\", "/")
                # print(real_path)
                dataList.append(real_path)
        elif path.isdir(real_path):
            # 递归输出文件夹下的文件
            scanner_file(real_path)
        else:
            print("其他情况")
            pass
