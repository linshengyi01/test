import cv2
import numpy as np
import matplotlib.pyplot as plt

# 解决中文显示为方块/乱码的问题
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
# 解决负号显示异常的问题
plt.rcParams['axes.unicode_minus'] = False

# ===================== 1. 形态学变换 =====================
def morphology_demo(img_path):
    # 读取灰度图像
    img_gray = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    # 二值化
    _, img_bin = cv2.threshold(img_gray, 127, 255, cv2.THRESH_BINARY)

    # 自定义3*3矩形结构化元素
    kernel = np.ones((3, 3), dtype=np.uint8)

    # 腐蚀、膨胀、开运算、闭运算
    img_erode = cv2.erode(img_bin, kernel)
    img_dilate = cv2.dilate(img_bin, kernel)
    img_open = cv2.morphologyEx(img_bin, cv2.MORPH_OPEN, kernel)
    img_close = cv2.morphologyEx(img_bin, cv2.MORPH_CLOSE, kernel)

    # 可视化
    titles = ["原始灰度", "二值图", "腐蚀", "膨胀", "开运算", "闭运算"]
    imgs = [img_gray, img_bin, img_erode, img_dilate, img_open, img_close]
    plt.figure(figsize=(12, 7))
    for i in range(6):
        plt.subplot(2, 3, i + 1)
        plt.imshow(imgs[i], cmap="gray")
        plt.title(titles[i])
        plt.axis("off")
    plt.suptitle("形态学变换结果")
    plt.tight_layout()
    plt.show()
    return img_bin

# ===================== 2.手写高斯滤波函数 gaussian_filter =====================
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

# ===================== 3.高斯金字塔（基于手写gaussian_filter） =====================
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
    plt.suptitle("高斯金字塔")
    plt.tight_layout()
    plt.show()
    return pyramid


if __name__ == "__main__":
    image_file = "blobs.png" # 修改成你的图片路径

    #任务1 形态学变换
    binary_img = morphology_demo(image_file)

    #任务2 高斯滤波测试
    blur_result = gaussian_filter(binary_img, kernel_size=5, sigma=2.0)
    plt.figure()
    plt.subplot(121),plt.imshow(binary_img,cmap="gray"),plt.title("原图"),plt.axis("off")
    plt.subplot(122),plt.imshow(blur_result,cmap="gray"),plt.title("高斯滤波"),plt.axis("off")
    plt.show()

    #任务3 高斯金字塔
    gaussian_pyramid(binary_img, level=4, kernel_size=5, sigma=2.0)
