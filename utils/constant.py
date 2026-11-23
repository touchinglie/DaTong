"""
Every constant value will be set below here.
"""

CCPD2020PICSIZE = (720, 1160)

class ChinaMainLandLinks:

    def __init__(self):
        self.COCO2017TRAIN = "https://www.modelscope.cn/datasets/PAI/COCO2017/resolve/master/train2017.zip?view=false"
        self.COCO2017VAL = "https://www.modelscope.cn/datasets/PAI/COCO2017/resolve/master/val2017.zip?view=false"
        self.COCO2017TEST = "http://images.cocodataset.org/zips/test2017.zip"
        self.COCO2017TRAINVALANNOTATIONS = "https://www.modelscope.cn/datasets/PAI/COCO2017/resolve/master/annotations_trainval2017.zip?view=false"

class InternationalLinks:

    def __init__(self):
        self.COCO2017TRAIN = "http://images.cocodataset.org/zips/train2017.zip"
        self.COCO2017VAL = "http://images.cocodataset.org/zips/val2017.zip"
        self.COCO2017TEST = "http://images.cocodataset.org/zips/test2017.zip"
        self.COCO2017TRAINVALANNOTATIONS = (
            "http://images.cocodataset.org/annotations/annotations_trainval2017.zip"
        )
