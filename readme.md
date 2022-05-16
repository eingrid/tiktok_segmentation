# TikTok Person/Background Segmentation


![](https://github.com/eingrid/tiktok_segmentation/blob/website/exmpl.png)

## Table of Contents
- [Description](#description)
- [How To Use](#description)

---
## Description 


This basic purpose of this project is to make an app that will make a segmentation of an input image. To accomplish this [U-Net](#https://arxiv.org/abs/1505.04597) model was trained on a [Segmentation Full Body TikTok Dancing Dataset](#https://www.kaggle.com/datasets/tapakah68/segmentation-full-body-tiktok-dancing-dataset) from Kaggle.

Project constists of Colab Notebook and a Website that are located in different branches.



## How To Use

Firsly, make sure that you have installed all requirements.


```shell
pip install -r /path/to/requirements.txt
```
or in conda
```shell
conda install --file requirements.txt
```

Also preferably to have version of CUDA 11.1 and Python 3.7.13.

To run website:
```shell
python3 website.py
```
And than go to http://127.0.0.1:5000 to open site in browser.
