import os
import shutil
from pathlib import Path


def get_image_files(directory):
    """获取指定目录中的所有图片文件，支持常见图片格式。"""
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff']
    return sorted([
        f for f in os.listdir(directory)
        if Path(f).suffix.lower() in image_extensions
    ])


def rename_images(source_dir, target_dir, output_dir):
    # 检查源文件夹和目标文件夹是否存在
    if not os.path.isdir(source_dir):
        print(f"源文件夹不存在: {source_dir}")
        return
    if not os.path.isdir(target_dir):
        print(f"目标文件夹不存在: {target_dir}")
        return

    # 创建输出文件夹（如果不存在）
    os.makedirs(output_dir, exist_ok=True)

    # 获取源文件夹和目标文件夹中的图片文件
    source_images = get_image_files(source_dir)
    target_images = get_image_files(target_dir)

    # 检查图片数量是否一致
    if len(source_images) != len(target_images):
        print("源文件夹和目标文件夹中的图片数量不一致。")
        print(f"源文件夹图片数量: {len(source_images)}")
        print(f"目标文件夹图片数量: {len(target_images)}")
        return

    # 逐一重命名并复制图片
    for src, tgt in zip(source_images, target_images):
        src_path = os.path.join(source_dir, src)
        tgt_name = tgt  # 包含扩展名
        output_path = os.path.join(output_dir, tgt_name)

        # 检查目标文件是否已存在，避免覆盖
        if os.path.exists(output_path):
            print(f"目标文件已存在，跳过: {output_path}")
            continue

        # 复制并重命名
        shutil.copy2(src_path, output_path)
        print(f"已复制: {src} -> {tgt_name}")

    print("重命名完成。")

if __name__ == "__main__":
    # 示例使用，可以根据需要修改路径
    source_directory = r"D:\ComfyUI-aki-v1.3\ComfyUI-aki-v1.3\output\key"  # 源文件夹路径
    target_directory = r"E:\aivideo\x\key"  # 目标文件夹路径
    output_directory = r"E:\aivideo\x\imkey"  # 输出文件夹路径

    rename_images(source_directory, target_directory, output_directory)


