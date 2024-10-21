"""
RGB图像缩放到与深度图一致，但因为不是等比缩放，导致得到图像会失真，已弃用
"""
from pykinect2 import PyKinectV2
from pykinect2 import PyKinectRuntime
import cv2
import numpy as np
import os

# 获取深度图, 保持Kinect获取的原始尺寸 512x424
def get_last_depth():
    frame = kinect.get_last_depth_frame()
    # 保持Kinect的原始深度数据
    dep_frame = frame.astype(np.uint16).reshape((424, 512))  # 原始尺寸512x424
    # 归一化深度值以便显示
    dep_frame_display = cv2.convertScaleAbs(dep_frame, alpha=0.05)
    return dep_frame, dep_frame_display

# 获取RGB图，并将其缩放到512x424
def get_last_rgb():
    frame = kinect.get_last_color_frame()
    # 获取RGB数据 (忽略Alpha通道)
    rgb_frame = frame.reshape((1080, 1920, 4))[:, :, 0:3]  # 原始尺寸1920x1080
    # 缩放到与深度图像相同的分辨率 (512x424)
    rgb_frame_resized = cv2.resize(rgb_frame, (512, 424))
    return rgb_frame_resized

# 初始化Kinect，选择运行模式为获取深度图和RGB图
kinect = PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Depth | PyKinectV2.FrameSourceTypes_Color)

# 设置RGB图像和深度图像保存路径
rgb_output_dir = "output_images/rgb"
depth_output_dir = "output_images/depth"

# 创建保存目录
if not os.path.exists(rgb_output_dir):
    os.makedirs(rgb_output_dir)
if not os.path.exists(depth_output_dir):
    os.makedirs(depth_output_dir)

# 图像计数器，用于生成唯一的文件名
image_count = 0

while True:
    # 只处理最新的RGB和深度帧
    if kinect.has_new_color_frame() and kinect.has_new_depth_frame():
        # 获取最新的RGB和深度图像
        rgb_frame = get_last_rgb()  # 缩放后的RGB图像
        depth_frame, depth_display = get_last_depth()  # 深度图像

        # 显示RGB图像
        cv2.imshow('Kinect RGB Frame', rgb_frame)
        # 显示深度图像 (经过归一化处理)
        cv2.imshow('Kinect Depth Frame', depth_display)

    # 处理按键输入
    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):
        break
    elif key == ord('s'):
        # 按 's' 键保存当前帧
        rgb_filename = f"{rgb_output_dir}/rgb_image_{image_count:04d}.png"
        depth_filename = f"{depth_output_dir}/depth_image_{image_count:04d}.png"
        depth_display_filename = f"{depth_output_dir}/depth_display_{image_count:04d}.png"

        # 保存缩放后的RGB图像
        cv2.imwrite(rgb_filename, rgb_frame)
        # 保存深度图像 (原始深度数据和可视化图像)
        cv2.imwrite(depth_filename, depth_frame)  # 保存16位深度图像
        cv2.imwrite(depth_display_filename, depth_display)  # 保存可视化的8位深度图像

        print(f"RGB图像已保存: {rgb_filename}")
        print(f"深度图像已保存: {depth_filename}")
        print(f"可视化深度图像已保存: {depth_display_filename}")

        # 更新图像计数器
        image_count += 1

# 关闭Kinect传感器
kinect.close()
cv2.destroyAllWindows()
