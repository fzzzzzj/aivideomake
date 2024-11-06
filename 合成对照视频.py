from moviepy.editor import VideoFileClip, clips_array


def merge_videos_left_right(video_path1, video_path2, output_path):
    """
    将两个视频合成为一左一右的单个视频，并保存到指定路径。

    :param video_path1: 左侧视频路径
    :param video_path2: 右侧视频路径
    :param output_path: 输出视频的保存路径
    """
    # 加载两个视频
    video1 = VideoFileClip(video_path1)
    video2 = VideoFileClip(video_path2)

    # 确保两个视频的高度相同，如果不同则调整
    if video1.h != video2.h:
        video2 = video2.resize(height=video1.h)

    # 水平拼接两个视频
    final_video = clips_array([[video1, video2]])

    # 导出合成后的新视频
    final_video.write_videofile(output_path, codec="libx264", audio_codec="aac")

    print(f"视频已保存到: {output_path}")


def main():
    # 配置参数部分
    # 左侧视频的路径（相对或绝对路径）
    VIDEO_PATH1 = r"E:\剧\抖音-记录美好生活_4.mp4"  # 请将此处替换为左侧视频路径

    # 右侧视频的路径（相对或绝对路径）
    VIDEO_PATH2 = r"D:\sd-webui-aki-v4.8\outputs\frame-interpolation\short_00002_\short_00002__FILM_x3.mp4"  # 请将此处替换为右侧视频路径

    # 输出保存的路径（相对或绝对路径）
    OUTPUT_PATH = r"D:\sc\xxn.mp4"  # 请将此处替换为保存结果视频的路径

    # 执行视频合并操作
    merge_videos_left_right(VIDEO_PATH1, VIDEO_PATH2, OUTPUT_PATH)


if __name__ == "__main__":
    main()
