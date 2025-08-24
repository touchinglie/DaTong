import os
from os import path
import time
import shutil
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

"""
考虑到数据集规模可能极大（1GB~3TB）
故加载时只记录数据绝对路径，通过shutil移动（复杂IO操作，多线程）完成数据目录格式重分配
而对于标签来说，类名文件只需重命名即可，其余标签坐标归一化或计算则是计算密集型操作（多进程）
"""
softwarePath = os.getcwd().replace("\\", "/")
DataList = []
YolokindList = []
CCPDkindList = []
DataAmount = 0
LoadFinished = threading.Event()
LoadFinished.clear()


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


checkFolders(f"{softwarePath}/output")


def SafeThreading(functions) -> threading.Thread:
    aThread = threading.Thread(target=functions)
    aThread.daemon = True
    return aThread


def CheckThreadFinishYolo() -> None:
    global YolokindList
    global DataAmount
    global LoadFinished
    while True:
        print(f"Done:{len(YolokindList)} Total:{DataAmount}")
        if len(YolokindList) == DataAmount:
            LoadFinished.set()
            break
        else:
            time.sleep(1)


def CheckThreadFinishCCPD() -> None:
    global CCPDkindList
    global DataAmount
    global LoadFinished
    while True:
        print(f"Done:{len(CCPDkindList)} Total:{DataAmount}")
        if len(CCPDkindList) == DataAmount:
            LoadFinished.set()
            break
        else:
            time.sleep(1)


def scanner_file(url) -> None:
    global DataList
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
                DataList.append(real_path)
        elif path.isdir(real_path):
            # 递归输出文件夹下的文件
            scanner_file(real_path)
        else:
            print("其他情况")
            pass


def judgeYoloKind(PathString: str) -> None:
    global YolokindList
    if "classes.txt" in PathString:
        YolokindList.append((6, PathString))
    temp = "".join(PathString.split("/")[:-1])
    if "label" in temp or "labels" in temp:
        if "train" in temp:
            YolokindList.append((0, PathString))
        if "test" in temp:
            YolokindList.append((1, PathString))
        if "val" in temp:
            YolokindList.append((2, PathString))
    elif "pic" in temp or "images" in temp:
        if "train" in temp:
            YolokindList.append((3, PathString))
        if "test" in temp:
            YolokindList.append((4, PathString))
        if "val" in temp:
            YolokindList.append((5, PathString))
    else:
        raise ValueError("That is not corrected Yolo format dataset!")


def judgeYoloContent(PathString: str) -> None:
    global YolokindList
    if "label" in PathString:
        YolokindList.append((0, PathString))
    elif "pic" in PathString:
        YolokindList.append((1, PathString))
    else:
        raise ValueError("That is not corrected Yolo format dataset!")


# 下面要改成读splits目录下的三个txt文件（test、train、val）来走官方默认的分割数据集
# 读完按行读取添加进对于列表里
# 每行path前面记得加数据集的目录位置（可以用"/".join(PathString.split("/")[:-2])确定）
# 自定义分割另写一个函数
def judgeCCPD2019Kind(PathString: str) -> None:
    global CCPDkindList
    if "jpg" in PathString:
        CCPDkindList.append((0, PathString))
    if "classes.txt" in PathString:
        CCPDkindList.append((0, PathString))
    elif "train.txt" in PathString:
        if "tfPath" not in globals().keys():
            tfPath = "/".join(PathString.split("/")[:-2]) + "/"
        with open(PathString, "r") as trainfile:
            tfcontent = trainfile.readlines()
        for tfline in tfcontent:
            CCPDkindList.append((1, tfPath + tfline))
    elif "val.txt" in PathString:
        if "vfPath" not in globals().keys():
            vfPath = "/".join(PathString.split("/")[:-2]) + "/"
        with open(PathString, "r") as valfile:
            vfcontent = valfile.readlines()
        for vfline in vfcontent:
            CCPDkindList.append((2, vfPath + vfline))
    elif "test.txt" in PathString:
        if "testfPath" not in globals().keys():
            testfPath = "/".join(PathString.split("/")[:-2]) + "/"
        with open(PathString, "r") as testfile:
            testfcontent = testfile.readlines()
        for testfline in testfcontent:
            CCPDkindList.append((3, testfPath + testfline))
    elif "txt" in PathString:
        CCPDkindList.append((4, PathString))
    else:
        raise ValueError("That is not corrected CCPD format dataset!")


def judgeCCPD2020Kind(PathString: str) -> None:
    global CCPDkindList
    if "jpg" in PathString:
        CCPDkindList.append((0, PathString))
    elif "classes.txt" in PathString:
        CCPDkindList.append((1, PathString))
    elif "txt" in PathString:
        CCPDkindList.append((2, PathString))
    else:
        raise ValueError("That is not corrected CCPD format dataset!")


# Load Yolo Dataset
def loadYolo(Path, AnyKind: bool, threadAmount=None) -> list:
    global YolokindList
    global DataList
    global DataAmount
    global LoadFinished

    SearchPath = Path
    scanner_file(SearchPath)
    DataAmount = len(DataList)
    kindList = []
    JudgePools = ThreadPoolExecutor(
        max_workers=threadAmount, thread_name_prefix="Thread"
    )
    if AnyKind:
        for dataPath in DataList:
            JudgePools.submit(judgeYoloKind, dataPath)
    else:
        for dataPath in DataList:
            JudgePools.submit(judgeYoloContent, dataPath)
    SafeThreading(CheckThreadFinishYolo).start()
    print("Now loading...")
    LoadFinished.wait()
    LoadFinished.clear()
    kindList = YolokindList
    YolokindList = []
    JudgePools.shutdown()
    DataList = []
    return kindList


# Load DarkYolo Dataset
def loadDark(Path):
    pass


# Load For Current Dataset
# Load CCPD Dataset
def loadCCPD(Path, Kind: tuple[int, str], threadAmount=None) -> list:
    global CCPDkindList
    global DataList
    global DataAmount
    global LoadFinished

    SearchPath = Path
    scanner_file(SearchPath)
    DataAmount = len(DataList)
    kindList = []
    JudgePools = ThreadPoolExecutor(
        max_workers=threadAmount, thread_name_prefix="Thread"
    )
    if Kind[0] == 2019:
        if Kind[1] == "official":
            for dataPath in DataList:
                JudgePools.submit(judgeCCPD2019Kind, dataPath)
    else:
        for dataPath in DataList:
            JudgePools.submit(judgeCCPD2020Kind, dataPath)
    SafeThreading(CheckThreadFinishCCPD).start()
    print("Now loading...")
    LoadFinished.wait()
    LoadFinished.clear()
    kindList = CCPDkindList
    CCPDkindList = []
    JudgePools.shutdown()
    DataList = []
    return kindList


if __name__ == "__main__":
    print(os.getcwd().replace("\\", "/"))
    print(f"Result:{loadYolo("I:/实验室数据集/dataset", False)}")
    print(f"Result:{loadYolo("I:/个人数据集/goldenbrick", True)}")
    print(
        f"Result:{loadCCPD("J:/Object-detection/dataset/CCPD2019", (2019,"official"))}"
    )
