"""
仅能显示一个窗口，选择RGB图或深度图来查看，保存也只能存一个，初始测试，已弃用
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


# 获取RGB图, 保持Kinect获取的原始尺寸 1920x1080
def get_last_rgb():
    frame = kinect.get_last_color_frame()
    # 获取RGB数据 (忽略Alpha通道)
    rgb_frame = frame.reshape((1080, 1920, 4))[:, :, 0:3]  # 原始尺寸1920x1080
    return rgb_frame


# 初始化Kinect，选择运行模式为获取深度图和RGB图
kinect = PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Depth | PyKinectV2.FrameSourceTypes_Color)

# 设置显示模式，'rgb' 或 'depth'
# frame_type = 'rgb'
frame_type = 'depth'

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
    # 只处理最新的帧数据，避免重复处理相同帧
    if frame_type == 'rgb' and kinect.has_new_color_frame():
        last_rgb_frame = get_last_rgb()  # 获取 RGB 图像
        cv2.imshow('Kinect RGB Frame', last_rgb_frame)  # 显示 RGB 图像
    elif frame_type == 'depth' and kinect.has_new_depth_frame():
        last_depth_frame, last_depth_display = get_last_depth()  # 获取深度图像
        cv2.imshow('Kinect Depth Frame', last_depth_display)  # 显示深度图像

    # 处理按键输入
    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):
        break
    elif key == ord('s'):
        # 按 's' 键保存当前帧
        if frame_type == 'rgb' and 'last_rgb_frame' in locals():
            # 保存RGB图像
            rgb_filename = f"{rgb_output_dir}/rgb_image_{image_count:04d}.png"
            cv2.imwrite(rgb_filename, last_rgb_frame)
            print(f"RGB图像已保存: {rgb_filename}")
        elif frame_type == 'depth' and 'last_depth_frame' in locals():
            # 保存深度图像 (原始深度数据和可视化图像)
            depth_filename = f"{depth_output_dir}/depth_image_{image_count:04d}.png"
            depth_display_filename = f"{depth_output_dir}/depth_display_{image_count:04d}.png"
            cv2.imwrite(depth_filename, last_depth_frame)  # 保存16位深度图像
            cv2.imwrite(depth_display_filename, last_depth_display)  # 保存可视化的8位深度图像
            print(f"深度图像已保存: {depth_filename}")
            print(f"可视化深度图像已保存: {depth_display_filename}")

        # 更新图像计数器
        image_count += 1

# 关闭Kinect传感器
kinect.close()
cv2.destroyAllWindows()
