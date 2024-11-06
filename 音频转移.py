import os
import time
from moviepy.editor import VideoFileClip


def replace_audio(video_path, audio_source_path, output_folder):
    """
    将一个视频的音频替换为另一个视频的音频，并保存到指定输出文件夹，自动生成文件名。

    :param video_path: 需要替换音频的视频路径
    :param audio_source_path: 提供新音频的视频路径
    :param output_folder: 输出视频文件保存的文件夹路径
    """
    # 确保输出文件夹存在，如果不存在则创建
    os.makedirs(output_folder, exist_ok=True)

    # 基于当前时间戳生成唯一的文件名
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    output_filename = f"output_video_{timestamp}.mp4"

    # 构建完整的输出路径
    output_path = os.path.join(output_folder, output_filename)

    # 加载需要替换音频的视频
    video = VideoFileClip(video_path)

    # 加载提供新音频的视频
    audio_source = VideoFileClip(audio_source_path)

    # 提取提供新音频的视频的音轨
    new_audio = audio_source.audio

    # 将新音频替换到目标视频中
    video_with_new_audio = video.set_audio(new_audio)

    # 导出带有新音频的视频
    video_with_new_audio.write_videofile(output_path, codec="libx264", audio_codec="aac")

    print(f"视频已保存到: {output_path}")


def main():
    # 配置参数部分
    # 需要替换音频的视频的路径（相对或绝对路径）
    VIDEO_PATH = r"D:\sd-webui-aki-v4.8\outputs\frame-interpolation\ba_00001__1\ba_00001__FILM_x3.mp4"  # 请将此处替换为实际视频路径

    # 提供新音频的视频的路径（相对或绝对路径）
    AUDIO_SOURCE_PATH = r"D:\sc\2.mp4"  # 请将此处替换为实际音频来源视频路径

    # 输出保存的文件夹路径（相对或绝对路径）
    OUTPUT_FOLDER = r"D:\sd-webui-aki-v4.8\outputs\frame-interpolation\ba_00001__1"  # 请将此处替换为保存结果视频的文件夹路径

    # 执行音频替换操作
    replace_audio(VIDEO_PATH, AUDIO_SOURCE_PATH, OUTPUT_FOLDER)


if __name__ == "__main__":
    main()


