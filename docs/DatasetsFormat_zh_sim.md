# 2D目标识别数据集下载地址与格式总结

本文档整理常见 2D 目标识别数据集的下载地址、标注格式与目录结构，便于选择与格式对齐。

<!-- 注意，以下凡是注释的内容均不可信，尚未人工验证。 -->

### COCO

COCO 是 2D 目标检测最常用的基准数据集之一，YOLO 系模型通常使用 COCO 2017 版本。

#### 下载地址

##### 支持无账户直链的下载源
1. 官方下载服务器（cocodataset.org）位于AWS美国
2. 华为modelscope社区服务器（www.modelscope.cn）位于中国

- 2017 Train images（118K / 18GB）
    - [官方下载源](http://images.cocodataset.org/zips/train2017.zip)
    - [华为modelscope下载源](https://www.modelscope.cn/datasets/PAI/COCO2017/resolve/master/train2017.zip?view=false)

- 2017 Val images（5K / 1GB）
    - [官方下载源](http://images.cocodataset.org/zips/val2017.zip)
    - [华为modelscope下载源](https://www.modelscope.cn/datasets/PAI/COCO2017/resolve/master/val2017.zip?view=false)

- 2017 Test images（41K / 6GB）
    - [官方下载源](http://images.cocodataset.org/zips/test2017.zip)

- 2017 Train/Val annotations（241MB）
    - [官方下载源](http://images.cocodataset.org/annotations/annotations_trainval2017.zip)
    - [华为modelscope下载源](https://www.modelscope.cn/datasets/PAI/COCO2017/resolve/master/annotations_trainval2017.zip?view=false)

COCO 官网为 `https://cocodataset.org/#download`；YOLO 场景下标签通常使用 COCO2017 内Train/Val annotations的 `instances_train2017.json` 与 `instances_val2017.json`。

##### 有限制的下载源
1. [百度飞桨paddle](https://aistudio.baidu.com/datasetdetail/97273)位于中国
2. [OpenDataLab](https://opendatalab.com/OpenDataLab/COCO_2017/tree/main/raw) 位于中国

#### 标签格式规范

##### COCO 2017 格式

- coco原格式数据集目录层样：
```
coco2017/
├── annotations
│   ├── instances_train2017.json
│   ├── instances_val2017.json
├── test2017  [40670 entries exceeds filelimit, not opening dir]
├── train2017  [118287 entries exceeds filelimit, not opening dir]
└── val2017  [5000 entries exceeds filelimit, not opening dir]
```

<!-- - COCO JSON 格式

COCO 原生标注为单个 JSON 文件，目标检测使用 `instances_*.json`。关键字段结构如下：

```json
{
  "images": [{ "id": int, "file_name": str, "width": int, "height": int }],
  "annotations": [
    {
      "id": int,
      "image_id": int,
      "category_id": int,
      "bbox": [x, y, width, height],
      "area": float,
      "iscrowd": 0
    }
  ],
  "categories": [{ "id": int, "name": str }]
}
```

- `bbox` 为像素坐标，`[x, y, width, height]`，`x, y` 是**左上角**坐标。
- `category_id` 从 COCO 的 80 类映射中取值（如 person = 1）。 -->

### PASCAL VOC

VOC 是经典的小规模目标检测数据集，常用 VOC2007 与 VOC2012，共 20 个类别。

**官方入口**：`http://www.robots.ox.ac.uk/~vgg/projects/pascal/VOC/`。VOC2012 的 train/val 打包文件为 [`VOCtrainval_11-May-2012.tar`](https://www.robots.ox.ac.uk/~vgg/projects/pascal/VOC/voc2012/VOCtrainval_11-May-2012.tar)（约 2GB）。Ultralytics 也提供 VOC 数据集页面，可直接用于 YOLO 格式加载。
<!-- 
### 3. Open Images V7

Google 发布的大规模检测数据集，训练图像约 170 万张，验证图像约 4.2 万张，标注以 CSV 形式组织。

**官方格式说明与下载入口**：`https://storage.googleapis.com/openimages/web/download.html`。检测任务的核心标注文件为 `<subset>-annotations-bbox.csv`，图像 ID 列表在 `<subset>-image_ids_and_rotation.csv` 中。

### 4. Ultralytics 常用其他检测数据集

Ultralytics 文档还列出了多个与 YOLO 兼容的检测数据集，均提供统一的 YAML 入口：

| 数据集     | 简要说明                      |
| ---------- | ----------------------------- |
| Objects365 | 365 类，训练图像 170 万+      |
| LVIS       | 1,203 类，大规模检测与分割    |
| VisDrone   | 无人机视角检测与跟踪          |
| KITTI      | 自动驾驶场景 2D 检测          |
| SKU-110K   | 零售密集检测，170 万+ 边界框  |
| TT100K     | 交通标志，221 类              |
| xView      | 俯视图像，60 类，100 万+ 目标 |

这些数据集的 YAML 配置文件通常位于 `ultralytics/cfg/datasets/` 下，使用方式为 `yolo train data=<name>.yaml`。


## 二、核心标注格式规范

### 1. COCO JSON 格式（原生格式）

COCO 原生标注为单个 JSON 文件，目标检测使用 `instances_*.json`。关键字段结构如下：

```json
{
  "images": [{ "id": int, "file_name": str, "width": int, "height": int }],
  "annotations": [
    {
      "id": int,
      "image_id": int,
      "category_id": int,
      "bbox": [x, y, width, height],
      "area": float,
      "iscrowd": 0
    }
  ],
  "categories": [{ "id": int, "name": str }]
}
```

- `bbox` 为像素坐标，`[x, y, width, height]`，`x, y` 是**左上角**坐标。
- `category_id` 从 COCO 的 80 类映射中取值（如 person = 1）。
- 分割标注中还包含 `segmentation` 字段（RLE 或 polygon）。

Ultralytics 提供 `convert_coco` 工具可将 COCO JSON 转为 YOLO txt 格式。

### 2. PASCAL VOC XML 格式

每张图像对应一个同名 `.xml` 文件，标注信息以 `<annotation>` 为根元素，每个目标放在 `<object>` 中：

```xml
<annotation>
  <filename>image.jpg</filename>
  <size>
    <width>W</width><height>H</height><depth>3</depth>
  </size>
  <object>
    <name>class_name</name>
    <bndbox>
      <xmin>...</xmin>
      <ymin>...</ymin>
      <xmax>...</xmax>
      <ymax>...</ymax>
    </bndbox>
  </object>
</annotation>
```

- `bndbox` 使用**绝对像素坐标**，`xmin/ymin` 为左上角，`xmax/ymax` 为右下角。
- VOC 共 20 类，类别名以字符串形式写在 `<name>` 中，无需单独 ID 映射。

### 3. YOLO txt 格式

YOLO 格式是 Ultralytics 模型直接训练所使用的标注格式。核心规则如下：

- 每张图像对应一个同名 `.txt` 文件；若图像中无目标，可不提供 txt 文件。
- 每行一个目标：`class_id x_center y_center width height`。
- 所有坐标均为**归一化值**（0–1）：`x_center`、`width` 除以图像宽度，`y_center`、`height` 除以图像高度。
- `class_id` 从 0 开始，类别映射在数据集 YAML 的 `names` 字段中定义。

### 4. Open Images CSV 格式

Open Images 的检测标注为 CSV 文件，核心字段包括：

```csv
ImageID,Source,LabelName,Confidence,XMin,XMax,YMin,YMax,IsOccluded,IsTruncated,IsGroupOf,IsDepiction,IsInside
```

- 边界框使用**归一化坐标**：`XMin/XMax/YMin/YMax` 取值范围为 0–1。
- `LabelName` 是类别标识符（如 `/m/0bt9lr`），需要通过 `class-descriptions.csv` 映射为可读名称。
- 类别体系为层级结构，不同于 COCO/VOC 的扁平 ID 映射。


## 三、Ultralytics YOLO 数据集目录结构

无论原始标注来自 COCO、VOC 还是其他来源，转换为 YOLO 格式后，推荐按以下目录组织：

```
dataset_root/
├── images/
│   ├── train/          # 训练图像
│   ├── val/            # 验证图像
│   └── test/           # 测试图像（可选）
├── labels/
│   ├── train/          # 与 images/train 同名的 .txt
│   ├── val/            # 与 images/val 同名的 .txt
│   └── test/
└── data.yaml           # 数据集配置文件
```

Ultralytics 在查找标签时，会将图像路径中的最后一个 `/images/` 替换为 `/labels/`，因此 `images/` 与 `labels/` 必须是**同级目录**。

### data.yaml 最小配置示例

```yaml
path: ./dataset_root
train: images/train
val: images/val
test:          # 可选
names:
  0: class_a
  1: class_b
```

`train/val/test` 可以接受目录路径、图像列表、`.txt` 图像路径文件，或以 `./` 开头的相对路径 txt 文件。


## 四、格式对比速查

| 维度          | COCO JSON              | VOC XML                    | YOLO txt                 | Open Images CSV              |
| ------------- | ---------------------- | -------------------------- | ------------------------ | ---------------------------- |
| 每图对应文件  | 单个 JSON 汇总全部     | 每图一个 `.xml`            | 每图一个 `.txt`          | 单个 CSV 汇总全部            |
| 坐标表示      | 像素 `[x, y, w, h]`    | 像素 `xmin/ymin/xmax/ymax` | 归一化 `xc/yc/w/h`       | 归一化 `XMin/XMax/YMin/YMax` |
| 类别字段      | `category_id`（整数）  | `<name>`（字符串）         | `class_id`（整数，从 0） | `LabelName`（层级标识符）    |
| YOLO 直接可用 | 需 `convert_coco` 转换 | 需转换                     | 原生可用                 | 需转换                       |

**选用建议**：若直接训练 Ultralytics YOLO 系模型，优先将数据统一整理为 YOLO txt + `images/`/`labels/` 结构；若需要保留分割或更丰富的标注信息，可保留 COCO JSON 作为源格式，再通过转换工具生成 YOLO 标签。


**参考来源**

- bendfunction GitBook：COCO 图像与标注下载链接
- Ultralytics 文档：YOLO 格式定义、目录约定、支持数据集列表、COCO 转换工具
- COCO bbox 字段说明；VOC XML 结构；Open Images CSV 字段 -->