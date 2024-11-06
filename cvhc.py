import os
from pathlib import Path
from moviepy.editor import ImageSequenceClip, AudioFileClip, VideoFileClip
from PIL import Image


def resize_images(frames, target_size):
    """
    调整所有图像的尺寸到 target_size。

    :param frames: 图像路径列表。
    :param target_size: 目标尺寸 (宽度, 高度)。
    :return: 调整后的图像路径列表。
    """
    resized_frames = []
    for frame_path in frames:
        img = Image.open(frame_path)
        if img.size != target_size:
            img = img.resize(target_size, Image.ANTIALIAS)
            resized_path = frame_path.parent / f"resized_{frame_path.name}"
            img.save(resized_path)
            resized_frames.append(str(resized_path))
        else:
            resized_frames.append(str(frame_path))
    return resized_frames


def frames_to_video(frames_dir, output_video_path, frame_rate=30, audio_path=None):
    """
    将图像帧合成为视频，并添加音频（可选）。

    :param frames_dir: 包含图像帧的文件夹路径（相对路径或绝对路径）。
    :param output_video_path: 输出视频的保存路径（包含文件名和扩展名，如 output.mp4）。
    :param frame_rate: 视频的帧率（FPS）。
    :param audio_path: 音频文件的路径。如果指向视频文件，则从中提取音频。
    """
    frames_dir = Path(frames_dir).resolve()
    output_video_path = Path(output_video_path).resolve()

    # 检查帧文件夹是否存在
    if not frames_dir.exists() or not frames_dir.is_dir():
        print(f"错误: 帧文件夹不存在或不是文件夹: {frames_dir}")
        return

    # 收集所有图像帧，支持常见图片格式
    image_extensions = ['.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.gif']
    frames = sorted([
        frame for frame in frames_dir.iterdir()
        if frame.suffix.lower() in image_extensions
    ])

    if not frames:
        print(f"错误: 在文件夹 '{frames_dir}' 中未找到支持的图像帧。")
        return

    print(f"找到 {len(frames)} 张图片帧，开始合成视频...")

    # 确保所有图像尺寸一致
    # 以第一张图像的尺寸为基准
    with Image.open(frames[0]) as img:
        target_size = img.size

    # 调整图像尺寸
    frames = resize_images(frames, target_size)

    # 创建视频剪辑
    clip = ImageSequenceClip(frames, fps=frame_rate)

    # 处理音频
    if audio_path:
        audio_path = Path(audio_path).resolve()
        if not audio_path.exists():
            print(f"错误: 音频文件不存在: {audio_path}")
            return

        if audio_path.suffix.lower() in ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv']:
            # 音频路径指向视频文件，提取音频
            print(f"音频路径指向视频文件，正在从 '{audio_path}' 提取音频...")
            try:
                video_clip = VideoFileClip(str(audio_path))
                if video_clip.audio:
                    audio_clip = video_clip.audio
                    clip = clip.set_audio(audio_clip)
                    print("音频已添加到视频剪辑。")
                else:
                    print(f"警告: 视频文件 '{audio_path}' 不包含音频。")
            except Exception as e:
                print(f"错误: 从视频文件中提取音频失败: {e}")
        elif audio_path.suffix.lower() in ['.mp3', '.wav', '.aac', '.flac', '.ogg', '.m4a']:
            # 音频路径指向音频文件
            print(f"音频路径指向音频文件，正在加载音频 '{audio_path}'...")
            try:
                audio_clip = AudioFileClip(str(audio_path))
                clip = clip.set_audio(audio_clip)
                print("音频已添加到视频剪辑。")
            except Exception as e:
                print(f"错误: 加载音频文件失败: {e}")
        else:
            print(f"错误: 不支持的音频文件格式: {audio_path.suffix}")
            return

    # 导出视频
    try:
        print(f"正在导出视频到 '{output_video_path}'...")
        clip.write_videofile(
            str(output_video_path),
            codec='libx264',
            audio_codec='aac' if audio_path else None
        )
        print(f"视频已成功保存到: {output_video_path}")
    except Exception as e:
        print(f"错误: 导出视频失败: {e}")


def main():
    # 配置参数部分
    # 设置图像帧文件夹的路径（相对于脚本文件夹或绝对路径）
    FRAMES_DIR =  r"D:\sd-webui-aki-v4.8\outputs\frame-interpolation\00004_1\interpolated_frames_film_00004"  # 请将此处替换为实际帧文件夹路径

    # 设置输出视频的路径（包含文件名和扩展名）
    OUTPUT_VIDEO_PATH = r"E:\aivideo\cp\video.mp4"  # 请将此处替换为实际输出视频路径

    # 设置帧率（FPS）
    FRAME_RATE = 30  # 例如，设为30表示每秒30帧

    # 设置音频路径（可选）
    AUDIO_PATH = r"G:\sucai\1.mp4"  # 请将此处替换为实际音频或视频路径，或设为 None

    # 执行合成
    frames_to_video(FRAMES_DIR, OUTPUT_VIDEO_PATH, FRAME_RATE, AUDIO_PATH)


if __name__ == "__main__":
    main()

def main():
    # 配置参数部分
    # 设置图像帧文件夹的路径（相对于脚本文件夹或绝对路径）
    FRAMES_DIR = r"D:\sd-webui-aki-v4.8\outputs\frame-interpolation\00004_1\interpolated_frames_film_00004"  # 请将此处替换为实际帧文件夹路径

    # 设置输出视频的路径（包含文件名和扩展名）
    OUTPUT_VIDEO_PATH = r"E:\aivideo\cp\video.mp4"  # 请将此处替换为实际输出视频路径

    # 设置帧率（FPS）
    FRAME_RATE = 30  # 例如，设为30表示每秒30帧

    # 设置音频路径（可选）
    # 如果音频路径指向视频文件，将从中提取音频
    # 如果指向音频文件，将直接使用该音频
    # 如果不需要添加音频，设为 None
    AUDIO_PATH = r"G:\sucai\1.mp4"  # 请将此处替换为实际音频或视频路径，或设为 None

    # 执行合成
    frames_to_video(FRAMES_DIR, OUTPUT_VIDEO_PATH, FRAME_RATE, AUDIO_PATH)

