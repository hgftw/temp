import cv2
import os

def images_to_video(image_folder, video_name, fps):
    # 获取文件夹中的所有图片文件并排序
    images = [img for img in os.listdir(image_folder) if img.endswith(".png")]
    images.sort(key=lambda x: int(os.path.splitext(x)[0]))

    if not images:
        print("No images found in the specified folder.")
        return

    # 读取第一张图片以获取视频帧的尺寸
    first_image_path = os.path.join(image_folder, images[0])
    first_image = cv2.imread(first_image_path)

    if first_image is None:
        print(f"Failed to read the first image from path: {first_image_path}")
        return

    height, width, layers = first_image.shape

    # 打印当前工作目录和目标文件路径
    print(f"Current working directory: {os.getcwd()}")
    print(f"Video will be saved to: {os.path.abspath(video_name)}")

    # 尝试初始化VideoWriter对象
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(video_name, fourcc, fps, (width, height))

    if not video.isOpened():
        print("Failed to initialize VideoWriter")
        return

    for image in images:
        image_path = os.path.join(image_folder, image)
        frame = cv2.imread(image_path)
        if frame is None:
            print(f"Failed to read image: {image_path}")
            continue
        video.write(frame)

    # 释放VideoWriter对象
    video.release()

    print(f"Video saved as {video_name}")
    print(f"Video absolute path: {os.path.abspath(video_name)}")

# 定义参数
image_folder = '05_22_2024_test_crop/output_05222024rightdown_crop'  # 图像文件夹路径
video_name = '5222024rightdown_crop.mp4'        # 输出视频文件名
fps = 20                                        # 每秒帧数

# 将图像转换为视频
images_to_video(image_folder, video_name, fps)
