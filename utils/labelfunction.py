import traceback
import sys

# 标签类别转换函数


def indexInt(indexClass: dict) -> dict:
    """returns a dict with integer keys and string values 
    based on the input dict with string keys and string values.

    Args:
        indexClass (dict): dict like {"0":"person","1":"bicycle"}

    Returns:
        dict: dict like {0:"person",1:"bicycle"}
    """
    return {int(k): v for k, v in indexClass.items()}


def indexStr(indexClass: dict) -> dict:
    """returns a dict with string keys and string values 
    based on the input dict with integer keys and string values.

    Args:
        indexClass (dict): dict like {0:"person", 1:"bicycle"}

    Returns:
        dict: dict like {"person":0 ,"bicycle":1}
    """
    return {v: k for k, v in indexClass.items()}


def indexMapping(indexStrDict: dict, indexStrList: list[str]) -> list[int]:
    return [indexStrDict[label] for label in indexStrList if label in indexStrDict]


def remapIntClassIndex(accIntClass: list[int]) -> dict:
    remapIntClassDict = {accIntClass[i]: i for i in range(len(accIntClass))}
    return remapIntClassDict


def indexFilter(accIntClass: list[int], labelIntDict: dict, strictFilter: bool, remapIntClassDict: dict = {}) -> dict:
    resDict = {}
    for labelIntName, labelIntContent in labelIntDict.items():
        if labelIntContent['annotations']:
            for labelIntAnno in labelIntContent['annotations']:
                if labelIntAnno[0] in accIntClass:
                    if strictFilter: 
                        filteredAnnotations = [anno for anno in labelIntContent['annotations'] if anno[0] in accIntClass]
                        filteredAnnotations = [ [remapIntClassDict[anno[0]], *anno[1:]] for anno in filteredAnnotations] if remapIntClassDict else filteredAnnotations
                        resDict[labelIntName] = {'url': labelIntContent['url'], 'split': labelIntContent['split'], 'annotations': filteredAnnotations}
                    else:
                        resDict[labelIntName] = labelIntContent
                    break
    return resDict


def labelFilter(labelDict: dict, accClass: list[str], indexClass: dict, strictFilter: bool,remapOrNot: bool) -> dict:
    remapIntClassDict = {}
    labelIntDict = indexInt(indexClass)
    labelStrDict = indexStr(labelIntDict)
    accIntClass = indexMapping(labelStrDict, accClass)
    print("accIntClass: ", accIntClass)
    if remapOrNot:
        remapIntClassDict = remapIntClassIndex(accIntClass)
        print("remapIntClassDict: ", remapIntClassDict)
    return indexFilter(accIntClass, labelDict, strictFilter,remapIntClassDict)


def labelJoin(labelIntAnno: list) -> str:
    labelIntAnno = map(str, labelIntAnno)
    return " ".join(labelIntAnno) + "\n"


def clsnameWriter(strClassList: list[str], path: str) -> int:
    try:
        if len(strClassList) == 0:
            raise ValueError(f"clsnameWriter: strClassList must be non-empty.")
        with open(path, "w") as f:
            f.writelines(strClassList)
        return 0
    except Exception as e:
        exc_type, exc_value, exc_obj = sys.exc_info()
        traceback.print_tb(exc_obj)
        return 1


def labelWriter(labelIntAnnos: list[list], path: str) -> int:
    try:
        if len(labelIntAnnos) == 0:
            raise ValueError(f"labelWriter: labelIntAnnos must be non-empty.")
        labelIntAnnos = map(labelJoin, labelIntAnnos)
        with open(path, "w") as f:
            f.writelines(labelIntAnnos)
        return 0
    except Exception as e:
        exc_type, exc_value, exc_obj = sys.exc_info()
        traceback.print_tb(exc_obj)
        return 1