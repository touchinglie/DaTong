import os
from os import path
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
