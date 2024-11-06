import os
from datetime import datetime
from PIL import Image
from moviepy.editor import ImageSequenceClip, VideoFileClip, AudioFileClip

# -------------------- 配置部分 --------------------

# 输入文件夹路径
folder_a =r"G:\sucai\video\gcly"   # 第一组图片
folder_b = r"G:\sucai\video\gcly\temp"  # 第二组图片
folder_mask = r"E:\comfui\ComfyUI-aki-v1.4\output\mask\jcly"  # 遮罩图片

# 输出文件夹路径
output_folder = r"G:\sucai\final\jcly"

# 视频和音频配置
audio_video_path = r"G:\sucai\video\你的老父亲的抖音 - 抖音.mp4"  # 指向包含音频的mp4文件

# 视频帧率
fps = 30  # 你可以根据需要调整帧率

# 自动生成视频文件名
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_video_path = os.path.join(output_folder, f"final_output_video_{timestamp}.mp4")

# ---------------------------------------------------

def ensure_folder_exists(folder):
    """确保输出文件夹存在，不存在则创建。"""
    if not os.path.exists(folder):
        os.makedirs(folder)
        print(f"创建文件夹: {folder}")

def get_sorted_filenames(folder):
    """
    获取文件夹中所有文件的排序列表。
    假设文件名按数字顺序排列，例如 00001.png, 00002.png, ...
    """
    return sorted(
        [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))],
        key=lambda x: os.path.splitext(x)[0]
    )

def composite_images(folder_a, folder_b, folder_mask, output_folder):
    """
    合成图片：将folder_a中的图片通过mask合成到folder_b中的图片上。
    """
    ensure_folder_exists(output_folder)

    filenames_a = get_sorted_filenames(folder_a)
    filenames_b = get_sorted_filenames(folder_b)
    filenames_mask = get_sorted_filenames(folder_mask)

    num_a = len(filenames_a)
    num_b = len(filenames_b)
    num_mask = len(filenames_mask)

    # 检查文件数量是否一致
    if num_a != num_b:
        raise ValueError(f"folder_A 和 folder_B 中的文件数量不一致：{num_a} vs {num_b}")

    if num_mask < num_a:
        raise ValueError(f"遮罩文件数量不足：需要至少 {num_a} 个，实际有 {num_mask} 个")

    output_filenames = []

    for index in range(num_a):
        filename_a = filenames_a[index]
        filename_b = filenames_b[index]
        filename_mask = filenames_mask[index]

        path_a = os.path.join(folder_a, filename_a)
        path_b = os.path.join(folder_b, filename_b)
        path_mask = os.path.join(folder_mask, filename_mask)
        path_out = os.path.join(output_folder, filename_a)  # 输出文件使用folder_a的文件名

        # 检查遮罩文件是否存在
        if not os.path.exists(path_mask):
            raise FileNotFoundError(f"遮罩文件未找到: {path_mask}")

        # 打开图片
        img_a = Image.open(path_a).convert("RGBA")
        img_b = Image.open(path_b).convert("RGBA")
        mask = Image.open(path_mask).convert("L")  # 转为灰度图

        # 将第二组图片等比例缩放到第一组图片的大小
        if img_b.size != img_a.size:
            img_b = img_b.resize(img_a.size, Image.LANCZOS)
            print(f"调整图片大小: {filename_b} 到 {img_a.size}")

        # 调整遮罩大小以匹配图片
        if mask.size != img_a.size:
            mask = mask.resize(img_a.size, Image.LANCZOS)
            print(f"调整遮罩大小: {filename_mask} 到 {img_a.size}")

        # 合成图片
        composite = Image.composite(img_a, img_b, mask)
        composite.save(path_out)

        output_filenames.append(path_out)
        print(f"合成并保存: {path_out}")

    return output_filenames

def create_video(image_files, audio_video_path, output_video_path, fps):
    """
    将合成后的图片序列生成视频，并添加音频。
    """
    if not image_files:
        raise ValueError("没有图片文件可用于生成视频。")

    # 创建视频剪辑
    clip = ImageSequenceClip(image_files, fps=fps)

    # 提取音频
    audio_clip = VideoFileClip(audio_video_path).audio
    if audio_clip is None:
        raise ValueError("无法从指定的mp4文件中提取音频。")

    # 确保音频长度与视频长度一致
    audio_clip = audio_clip.set_duration(clip.duration)

    # 添加音频到视频
    clip = clip.set_audio(audio_clip)

    # 写出最终视频
    clip.write_videofile(output_video_path, codec="libx264", audio_codec="aac")
    print(f"视频已保存到: {output_video_path}")

def main():
    try:
        # 合成图片
        print("开始合成图片...")
        output_images = composite_images(folder_a, folder_b, folder_mask, output_folder)
        print("图片合成完成。")

        # 创建视频
        print("开始生成视频...")
        create_video(output_images, audio_video_path, output_video_path, fps)
        print("视频生成完成。")

    except Exception as e:
        print(f"发生错误: {e}")

if __name__ == "__main__":
    main()
