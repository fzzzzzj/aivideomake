from pathlib import Path
import tiqu
import cv2


def video_to_frames(video_path, output_dir, frame_rate=None):
    """
    将视频拆分为帧并保存为图像文件。

    :param video_path: 视频文件的路径（相对路径或绝对路径）。
    :param output_dir: 输出文件夹的路径，用于保存拆分的帧。
    :param frame_rate: 每秒提取的帧数（可选）。如果为 None，则提取视频的所有帧。
    """
    # 检查视频文件是否存在
    video_path = Path(video_path)
    if not video_path.exists():
        print(f"错误: 视频文件不存在: {video_path}")
        return

    # 创建输出文件夹（如果不存在）
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # 打开视频文件
    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        print(f"错误: 无法打开视频文件: {video_path}")
        return

    # 获取视频的基本信息
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    duration = total_frames / fps if fps else 0

    print(f"视频信息：")
    print(f"路径: {video_path}")
    print(f"总帧数: {total_frames}")
    print(f"帧率 (FPS): {fps}")
    print(f"时长 (秒): {duration:.2f}")

    # 计算提取帧的间隔
    if frame_rate:
        frame_interval = int(round(fps / frame_rate)) if fps else 1
        print(f"设定的提取帧率: {frame_rate} FPS")
        print(f"每 {frame_interval} 帧提取一次")
    else:
        frame_interval = 1  # 提取所有帧

    current_frame = 0
    saved_frames = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if current_frame % frame_interval == 0:
            # 生成帧的文件名
            frame_filename = output_dir / f"frame_{saved_frames:06d}.png"
            # 保存帧为图像文件
            cv2.imwrite(str(frame_filename), frame)
            print(f"已保存: {frame_filename}")
            saved_frames += 1

        current_frame += 1

    cap.release()
    print(f"拆分完成，共保存 {saved_frames} 帧。")

def main():
    # 配置参数部分

    # 设置视频文件的路径（相对于脚本文件夹或绝对路径）
    VIDEO_PATH = r"G:\sucai\video\你的老父亲的抖音 - 抖音.mp4"# 请将此处替换为实际视频路径

    # 设置输出文件夹的路径（相对于脚本文件夹或绝对路径）
    OUTPUT_DIR = r"G:\sucai\video\gcly"    # 请将此处替换为实际输出路径

    # 设置每秒提取的帧数（可选）
    FRAME_RATE = None  # 例如，设为1表示每秒提取1帧；设为None则提取所有帧

    # 执行拆分
    video_to_frames(VIDEO_PATH, OUTPUT_DIR, FRAME_RATE)

    SOURCE_DIR = OUTPUT_DIR  # 请将此处替换为实际源文件夹路径

    # 设置目标文件夹路径（相对或绝对路径）
    TARGET_DIR = r"G:\sucai\video\sd\keytemp"  # 请将此处替换为实际目标文件夹路径

    # 设置提取间隔，如每隔 3 张提取一张
    INTERVAL = 3

    # 执行提取操作
    tiqu.extract_frames(SOURCE_DIR, TARGET_DIR, INTERVAL)
if __name__ == "__main__":
    main()
