import os
import sys
from pathlib import Path


def get_image_files(directory):
    """
    获取指定目录中的所有图片文件，支持常见图片格式，并按名称排序。
    """
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff']
    return sorted([
        f for f in os.listdir(directory)
        if Path(f).suffix.lower() in image_extensions
    ])


def rename_images(path, batch_name):
    """
    按照指定格式重命名图片文件。
    """
    # 解析路径
    directory = Path(path).resolve()

    # 检查路径是否存在且为目录
    if not directory.exists():
        print(f"错误: 路径不存在: {directory}")
        sys.exit(1)
    if not directory.is_dir():
        print(f"错误: 不是一个文件夹: {directory}")
        sys.exit(1)

    # 获取图片文件
    image_files = get_image_files(directory)

    if not image_files:
        print(f"在文件夹 '{directory}' 中未找到图片文件。")
        sys.exit(1)

    print(f"找到 {len(image_files)} 张图片，开始重命名...")

    # 重命名
    for idx, filename in enumerate(image_files, start=1):
        src_path = directory / filename
        # 生成新文件名
        new_filename = f"{batch_name}_{idx:09d}.png"
        dest_path = directory / new_filename

        # 检查目标文件是否已存在，避免覆盖
        if dest_path.exists():
            print(f"警告: 目标文件已存在，跳过: {dest_path}")
            continue

        # 重命名文件
        try:
            src_path.rename(dest_path)
            print(f"已重命名: {filename} -> {new_filename}")
        except Exception as e:
            print(f"错误: 无法重命名 {filename} -> {new_filename}: {e}")

    print("重命名完成。")


def main():
    # 配置参数部分
    # 设置图片文件夹的路径（相对于 webui 文件夹的路径或绝对路径）
    IMAGE_FOLDER_PATH = r"D:\sd-webui-aki-v4.8\outputs\frame-interpolation\ba_000000001\interpolated_frames_film_ba_000000001"  # 请将此处替换为实际路径

    # 设置批次名称，用于替换文件名中的前缀部分
    BATCH_NAME = "ba"  # 请将此处替换为实际的批次名称

    # 执行重命名
    rename_images(IMAGE_FOLDER_PATH, BATCH_NAME)


if __name__ == "__main__":
    main()
