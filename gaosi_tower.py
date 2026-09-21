import cv2
import numpy as np
import matplotlib.pyplot as plt


def gaussian_pyramid(src, level=4, kernel_size=5, sigma=1.5):
    """
    生成高斯金字塔
    :param src:输入灰度图像
    :param level:金字塔层数
    :return:金字塔列表，第0层原图
    """
    pyramid = []
    current = src.copy()
    pyramid.append(current)
    for _ in range(level-1):
        #先高斯滤波
        blur = gaussian_filter(current, kernel_size, sigma)
        #下采样：隔点删除
        next_level = blur[::2, ::2]
        pyramid.append(next_level)
        current = next_level
    #可视化金字塔
    plt.figure(figsize=(14,4))
    for idx, layer in enumerate(pyramid):
        plt.subplot(1, level, idx+1)
        plt.imshow(layer, cmap="gray")
        plt.title(f"Level {idx}, shape{layer.shape}")
        plt.axis("off")
    plt.suptitle("高斯金字塔（手写高斯滤波）")
    plt.tight_layout()
    plt.show()
    return pyramid