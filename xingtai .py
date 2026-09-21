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


if __name__ == "__main__":
    image_file = "blobs.png" # 修改成你的图片路径

    #任务1 形态学变换
    binary_img = morphology_demo(image_file)
