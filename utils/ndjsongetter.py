"""
Made for reading ultralytics ndjson file, and get the data from it.
"""

from network import basicDownload
import os
from multiprocessing.pool import Pool, ThreadPool
import json


def getLineFromNDJSON(file_path: str)-> list:

    if not file_path.endswith(".ndjson"):
        raise ValueError("File must be a .ndjson file")

    lineList = []

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:          # 跳过空行
                continue
            
            obj = json.loads(line)  # 每行解析成一个 dict / list
            # print(obj)
            # 获取内部信息，按普通 dict/list 访问即可

            lineList.append(obj)
    return lineList


def getInfoFromDict(lineList: list[dict]) -> dict:
    # print(lineList[0])
    info = lineList[0]
    # print(info)

    if info['type'] != "dataset":
        raise ValueError("The first line must be a dataset type")
    print(f"Dataset Name: {info['name']}")

    classNames = info['class_names']
    print(f"Class Names: {classNames}")

    return classNames


def getImgInfoFromList(lineList: list[dict]) -> dict:
    imgInfoDict = {}
    for info in lineList:
        if info['type'] == "image":
            if 'annotations' not in info.keys():
                imgInfoDict[info['file']] = {'url': info['url'], 'split': info['split'], 'annotations': []}
                continue
            imgInfoDict[info['file']] = {'url': info['url'], 'split': info['split'], 'annotations': info['annotations']['boxes']}
    return imgInfoDict


def getSaveDir(saveDir, fileName):
    filePath = os.path.join(saveDir, fileName)
    return filePath


def DownloadImgFromDict(imgInfoDict: dict, saveDir: str, threadNum: int):
    if not os.path.exists(saveDir):
        os.makedirs(saveDir)

    # 使用线程池进行并发下载
    with ThreadPool(threadNum) as pool:
        pool.starmap(basicDownload, [(imgInfo['url'], getSaveDir(saveDir, fileName)) for fileName, imgInfo in imgInfoDict.items()])


if __name__ == "__main__":
    lineList = getLineFromNDJSON("coco2017.ndjson")
    classNames = getInfoFromDict(lineList)
    imgInfo = getImgInfoFromList(lineList)
    # print("image info: ", imgInfo)
    from psutil import cpu_count
    threadNum = cpu_count() // 2
    # print(imgInfo.items())
    DownloadImgFromDict(imgInfo, "downloaded_images", threadNum)
