# 预计完成的功能有：
## UI界面
* tkinter
* 选择加载文件夹路径、显示数据数目、获取数据集大小、选择输入输出数据集格式
  
## 根据指定的格式转换成另一指定的格式
* （分开做还是做一种中介格式？）
* 如果做中介格式的话，数据集太大怎么办？
* 分开做万一格式太多，每两种都得做一个转换函数怎么办？
  
## 自动分割数据集（用户可选）
* 转之前做还是之后做？
* 给train/test/val划分比例吗？


# 目前寻找到的数据集格式有：
## Image：
* Yolo
  support: .jpeg, .txt, .yaml
  Label's name need to be same as both directory name and image name.
  ```
  root/
    label/
        classes.txt
        train/
            1.jpg
            2.jpg
            ...
        test/
            1.jpg
            2.jpg
            ...
        val/
            1.jpg
            2.jpg
            ...
    pic/
        train/
            1.txt
            2.txt
            ...
        test/
            1.txt
            2.txt
            ...
        val/
            1.txt
            2.txt
            ...
  ```
* Darknet Yolo
  ```
    root/
    ├── category.names        # .names category label file
    ├── train                 # train dataset
    │   ├── 000001.jpg
    │   ├── 000001.txt
    │   ├── 000002.jpg
    │   ├── 000002.txt
    │   ├── 000003.jpg
    │   └── 000003.txt
    ├── train.txt              # train dataset path .txt file
    ├── val                    # val dataset
    │   ├── 000043.jpg
    │   ├── 000043.txt
    │   ├── 000057.jpg
    │   ├── 000057.txt
    │   ├── 000070.jpg
    │   └── 000070.txt
    └── val.txt                # val dataset path .txt file
    ```
* COCO
* Labelme
* Keras
  support: .jpeg, .jpg, .png, .bmp, .gif
    ```
    main_directory/
        ...class_a/
            ......a_image_1.jpg
            ......a_image_2.jpg
        ...class_b/
            ......b_image_1.jpg
            ......b_image_2.jpg
    ```
* VOC
* createML
* MNIST
* CIFAR10
* Apache Parquet
* Lmdb
* Leveldb(Deprecated)
* bdd100k
* CCPD
* Matlab mat
* ffcv

## Timeseries
* Planned

## Text
* Keras
  support: .txt
    ```
    main_directory/
        ...class_a/
            ......a_text_1.txt
            ......a_text_2.txt
        ...class_b/
            ......b_text_1.txt
            ......b_text_2.txt
    ```

## Audio
* Keras
  support: .wav
    ```
    main_directory/
        ...class_a/
            ......a_audio_1.wav
            ......a_audio_2.wav
        ...class_b/
            ......b_audio_1.wav
            ......b_audio_2.wav
    ```

* 考虑到数据集规模可能极大（1GB~3TB）
* 故加载时只记录数据绝对路径，通过shutil移动（复杂IO操作，多线程）完成数据目录格式重分配
* 而对于标签来说，类名文件只需重命名即可，其余标签坐标归一化或计算则是计算密集型操作（多进程）