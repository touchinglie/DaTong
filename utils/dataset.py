import os
import shutil
import dataloader as dlr

# 输出端


def GoYolo():
    folderChecker = os.listdir(f"{dlr.softwarePath}/output")
    if len(folderChecker) == 0:
        savePath = f"{dlr.softwarePath}/output/0"
    else:
        folderNum = int(sorted(folderChecker)[-1]) + 1
        savePath = f"{dlr.softwarePath}/output/{folderNum}"
    dlr.checkFolders(savePath)

    # 创建标签目录
    dlr.checkFolders(savePath + "/label")
    dlr.checkFolders(savePath + "/label/train")
    dlr.checkFolders(savePath + "/label/test")
    dlr.checkFolders(savePath + "/label/val")

    # 创建数据目录
    dlr.checkFolders(savePath + "/pic")
    dlr.checkFolders(savePath + "/pic/train")
    dlr.checkFolders(savePath + "/pic/test")
    dlr.checkFolders(savePath + "/pic/val")


def GoDark():
    pass
