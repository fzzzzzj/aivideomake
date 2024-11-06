import os
import shutil
from pathlib import Path


def extract_frames(source_dir, target_dir, interval):
    """
    从源文件夹中每隔几张图片提取一张保存到目标文件夹。

    :param source_dir: 源图片文件夹路径
    :param target_dir: 目标文件夹路径
    :param interval: 每隔多少张图片提取一张
    """
    # 将路径转换为绝对路径
    source_dir = Path(source_dir).resolve()
    target_dir = Path(target_dir).resolve()

    # 检查源文件夹是否存在
    if not source_dir.exists() or not source_dir.is_dir():
        print(f"错误: 源文件夹不存在或不是文件夹: {source_dir}")
        return

    # 如果目标文件夹不存在，创建它
    target_dir.mkdir(parents=True, exist_ok=True)

    # 获取源文件夹中的所有图片文件（支持的格式）
    image_extensions = ['.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.gif']
    images = sorted([f for f in source_dir.iterdir() if f.suffix.lower() in image_extensions])

    if not images:
        print(f"错误: 在文件夹 '{source_dir}' 中未找到支持的图像文件。")
        return

    print(f"找到 {len(images)} 张图片，每隔 {interval} 张提取一张。")

    # 开始提取图片
    extracted_count = 0
    for idx, image_path in enumerate(images):
        # 仅在满足间隔时提取图片
        if idx % interval == 0:
            # 生成目标路径
            target_image_path = target_dir / image_path.name
            # 复制图片到目标文件夹
            shutil.copy(image_path, target_image_path)
            print(f"提取图片: {image_path.name} -> {target_image_path}")
            extracted_count += 1

    print(f"提取完成，共提取 {extracted_count} 张图片到 '{target_dir}' 文件夹中。")


def main():
    # 配置参数部分
    # 设置源图片文件夹路径（相对或绝对路径）
    SOURCE_DIR = r"G:\sucai\video\temp"  # 请将此处替换为实际源文件夹路径

    # 设置目标文件夹路径（相对或绝对路径）
    TARGET_DIR = r"G:\sucai\video\keytemp"  # 请将此处替换为实际目标文件夹路径

    # 设置提取间隔，如每隔 3 张提取一张
    INTERVAL = 3

    # 执行提取操作
    extract_frames(SOURCE_DIR, TARGET_DIR, INTERVAL)


if __name__ == "__main__":
    main()
