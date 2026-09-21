import cv2
import numpy as np
import matplotlib.pyplot as plt


def gaussian_filter(src, kernel_size=5, sigma=1.5):
    """
    手写高斯滤波，不调用cv2.GaussianBlur
    :param src:输入灰度图
    :param kernel_size:核大小，奇数
    :param sigma:高斯标准差
    :return:滤波后图像
    """
    # 生成高斯核
    k = kernel_size // 2
    x, y = np.meshgrid(np.arange(-k, k+1), np.arange(-k, k+1))
    g = np.exp(-(x**2 + y**2)/(2*sigma**2))
    g = g / np.sum(g) #归一化

    # 边界填充
    src_pad = np.pad(src, pad_width=k, mode="reflect")
    out = np.zeros_like(src, dtype=np.float32)

    # 卷积运算
    h, w = src.shape
    for i in range(h):
        for j in range(w):
            patch = src_pad[i:i+kernel_size, j:j+kernel_size]
            out[i,j] = np.sum(patch * g)
    out = np.clip(out, 0, 255).astype(np.uint8)
    return out

if __name__ == "__main__":
    image_file = "blobs.png" # 修改成你的图片路径

    #任务2 高斯滤波测试
    blur_result = gaussian_filter(binary_img, kernel_size=5, sigma=2.0)
    plt.figure()
    plt.subplot(121),plt.imshow(binary_img,cmap="gray"),plt.title("原图"),plt.axis("off")
    plt.subplot(122),plt.imshow(blur_result,cmap="gray"),plt.title("手写高斯滤波"),plt.axis("off")
    plt.show()
