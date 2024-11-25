# macOS桌面创建「from」文件夹，待转换视频拖进去。
# pip install ffmpeg-python
# python ffmpeg.py
#
# Encoder hevc_videotoolbox [VideoToolbox H.265 Encoder]:
#    General capabilities: dr1 delay hardware
#    Threading capabilities: none
#    Supported hardware devices: videotoolbox
#    Supported pixel formats: videotoolbox_vld nv12 yuv420p bgra p010le
# hevc_videotoolbox AVOptions:
#  -profile           <int>        E..V....... Profile (from -99 to INT_MAX) (default -99)
#     main            1            E..V....... Main Profile
#     main10          2            E..V....... Main10 Profile
#  -alpha_quality     <double>     E..V....... Compression quality for the alpha channel (from 0 to 1) (default 0)
#  -constant_bit_rate <boolean>    E..V....... Require constant bit rate (macOS 13 or newer) (default false)
#  -allow_sw          <boolean>    E..V....... Allow software encoding (default false)
#  -require_sw        <boolean>    E..V....... Require software encoding (default false)
#  -realtime          <boolean>    E..V....... Hint that encoding should happen in real-time if not faster (e.g. capturing from camera). (default false)
#  -frames_before     <boolean>    E..V....... Other frames will come before the frames in this session. This helps smooth concatenation issues. (default false)
#  -frames_after      <boolean>    E..V....... Other frames will come after the frames in this session. This helps smooth concatenation issues. (default false)
#  -prio_speed        <boolean>    E..V....... prioritize encoding speed (default auto)
#  -power_efficient   <int>        E..V....... Set to 1 to enable more power-efficient encoding if supported. (from -1 to 1) (default -1)
#  -max_ref_frames    <int>        E..V....... Sets the maximum number of reference frames. This only has an effect when the value is less than the maximum allowed by the profile/level. (from 0 to INT_MAX) (default 0)

# ffmpeg -codecs | grep videotoolbox
# DEV.LS h264                 H.264 / AVC / MPEG-4 AVC / MPEG-4 part 10 (encoders: libx264 libx264rgb h264_videotoolbox)
# DEV.L. hevc                 H.265 / HEVC (High Efficiency Video Coding) (encoders: libx265 hevc_videotoolbox)
# DEVIL. prores               Apple ProRes (iCodec Pro) (encoders: prores prores_aw prores_ks prores_videotoolbox)

import os
import shutil
import subprocess
import time
from datetime import datetime


# 模式选择
# [1]：转换容器格式                               [对比时间：01s 测试大小/原大小：41.4MB/41.3MB]
# [2]：硬编码                                    [对比时间：22s 测试大小/原大小：80.6MB/41.3MB] 
# [3]：软编码                                    [对比时间：44s 测试大小/原大小：25.4MB/41.3MB]
# [4]：限制码率[码率限制964K-3856K，缓冲区2000K]    [对比时间：57s 测试大小/原大小：62.7MB/41.3MB]
# [5]：改变分辨率[默认1080P]
# [6]：提取音频
# [7]：裁剪视频
FFmpeg = 1

# 目标格式
target_ext = ".mp4"

# 原格式[FFmpeg]
source_ext = [
    '.3g2', '.3gp', '.amv', '.asf', '.avi', '.drc', '.f4a', '.f4b', '.f4p', '.f4v',
    '.flv', '.gif', '.gifv', '.m2v', '.m3u8', '.m4p', '.m4v', '.mkv', '.mng', '.mov',
    '.mp2', '.mp4', '.mpe', '.mpeg', '.mpg', '.mpv', '.mxf', '.nsv', '.ogg', '.ogv',
    '.qt', '.rm', '.rmvb', '.roq', '.svi', '.ts', '.vob', '.webm', '.wmv', '.yuv'
]

# 时间格式
start_time = time.time()
current_time = datetime.now().strftime("%H-%M-%S")
# Mac路径
desktop = os.path.join(os.path.expanduser('~'), 'Desktop')
from_folder = os.path.join(desktop, 'from')
to_folder = os.path.join(desktop, f'File[{FFmpeg}]{current_time}')


if not os.path.exists(to_folder):
    os.makedirs(to_folder)

def create_log():
    log_path = os.path.join(desktop, f'Log[{FFmpeg}]{current_time}.txt')
    with open(log_path, 'w') as log_file:
        log_file.write('## 本次运行信息\n成功：0\n失败：0\n跳过：0\n总数：0\n总时间：00H:00M:00S\n\n')
        log_file.write('## 成功转换的视频名称\n')
        log_file.write('## 失败转换的视频名称\n')
        log_file.write('## 跳过转换的视频名称\n')
    return log_path

def log_update(log_path, success_count, failure_count, skip_count, total_files, elapsed_time):
    with open(log_path, 'r+') as log_file:
        content = log_file.readlines()
        content[1] = f'成功：{success_count}\n'
        content[2] = f'失败：{failure_count}\n'
        content[3] = f'跳过：{skip_count}\n'
        content[4] = f'总数：{total_files}\n'
        content[5] = f'总时间：{elapsed_time}\n'
        log_file.seek(0)
        log_file.writelines(content)

def log_append_section(log_path, section, message):
    with open(log_path, 'r+') as log_file:
        content = log_file.readlines()
        index = content.index(f'## {section}\n') + 1
        while index < len(content) and not content[index].startswith('## '):
            index += 1
        content.insert(index, f'{message}\n')
        log_file.seek(0)
        log_file.writelines(content)

log_path = create_log()
total_files = sum([len([file for file in files if file.endswith(tuple(source_ext))]) for _, _, files in os.walk(from_folder)])
success_count = 0
failure_count = 0
skip_count = 0

def convert_video(input_path, output_path):
    try:
        # 模式处理
        if FFmpeg == 1:
            command = ['ffmpeg', '-i', input_path, '-c', 'copy', output_path]
        elif FFmpeg == 2:
            command = ['ffmpeg', '-i', input_path, '-c:v', 'hevc_videotoolbox', output_path]
        elif FFmpeg == 3:
            command = ['ffmpeg', '-i', input_path, '-c:v', 'libx265', '-crf', '28', '-preset', 'ultrafast', '-c:a', 'aac', '-b:a', '128k', output_path]
        elif FFmpeg == 4:
            command = ['ffmpeg', '-i', input_path, '-minrate', '964K', '-maxrate', '3856K', '-bufsize', '2000K', output_path]
        elif FFmpeg == 5:
            command = ['ffmpeg', '-i', input_path, '-vf', 'scale=1080:-1', output_path]
        elif FFmpeg == 6:
            command = ['ffmpeg', '-i', input_path, '-vn', '-c:a', 'copy', output_path]
        elif FFmpeg == 7:
            command = ['ffmpeg', '-ss', '[start]','-i', input_path, '-to', '[end]', '-c', 'copy', output_path]  # 00:01:50


        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        duration = None
        for line in process.stderr:
            if 'Duration' in line:
                duration_str = line.split('Duration: ')[1].split(', ')[0]
                h, m, s = duration_str.split(':')
                duration = int(h) * 3600 + int(m) * 60 + float(s)
            if 'time=' in line and duration:
                time_str = line.split('time=')[1].split(' ')[0]
                time_parts = time_str.split(':')
                if len(time_parts) == 3:
                    h, m, s = time_parts
                    current_time = int(h) * 3600 + int(m) * 60 + float(s)
                    progress = int(current_time / duration * 100)
                    bar = f"[{'█' * int(progress // 5)}{' ' * (20 - int(progress // 5))}]"
                    elapsed_time = format_time(time.time() - start_time)
                    filename = os.path.basename(input_path)
                    display_name = f'{os.path.splitext(filename)[0][:20]}..{os.path.splitext(filename)[1]}'
                    print(f"\r运行中[{elapsed_time}]: {success_count}/{failure_count}/{skip_count}/{total_files} {progress}% {bar} -- {display_name}", end='\n', flush=True)
        process.wait()
        if process.returncode != 0:
            raise subprocess.CalledProcessError(process.returncode, command)
        return True
    except subprocess.CalledProcessError:
        return False

def format_time(seconds):
    time_struct = time.gmtime(seconds)
    return time.strftime("%H", time_struct) + "H:" + time.strftime("%M", time_struct) + "M:" + time.strftime("%S", time_struct) + "S"

def process_videos():
    global success_count, failure_count, skip_count
    processed_files = 0
    for root, _, files in os.walk(from_folder):
        for file in files:
            if not file.endswith(tuple(source_ext)):
                continue
            input_path = os.path.join(root, file)
            relative_path = os.path.relpath(root, from_folder)
            output_dir = os.path.join(to_folder, relative_path)
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            output_path = os.path.join(output_dir, f"[{FFmpeg}]" + os.path.splitext(file)[0] + target_ext)
            processed_files += 1

            # 原扩展名和目标扩展名一样 且 模式设置为1、2、3则跳过处理
            if os.path.splitext(file)[-1] == target_ext and FFmpeg in [1, 2, 3]:
                shutil.copy(input_path, output_path)
                skip_count += 1
                log_append_section(log_path, '跳过转换的视频名称', file)
                print(f"\r跳过[{format_time(time.time() - start_time)}]: {success_count}/{failure_count}/{skip_count}/{total_files} 0% |        | -- {os.path.splitext(file)[0][:20]}..{os.path.splitext(file)[1]}", end='\n', flush=True)
                continue
            
            result = convert_video(input_path, output_path)
            if result:
                success_count += 1
                log_append_section(log_path, '成功转换的视频名称', file)
            else:
                failure_count += 1
                log_append_section(log_path, '失败转换的视频名称', f'{file} -- 转换失败')
                print(f"\n[失败] 转换失败 -- {file}", flush=True)
                continue
            
            progress = processed_files / total_files * 100
            bar = f"[{'█' * int(progress // 5)}{' ' * (20 - int(progress // 5))}]"
            print(f"\r运行中[{format_time(time.time() - start_time)}]: {success_count}/{failure_count}/{skip_count}/{total_files} {int(progress)}% {bar} -- {os.path.splitext(file)[0][:20]}..{os.path.splitext(file)[1]}", end='\n', flush=True)

            log_update(log_path, success_count, failure_count, skip_count, total_files, format_time(time.time() - start_time))

process_videos()

total_time = time.time() - start_time
log_update(log_path, success_count, failure_count, skip_count, total_files, format_time(total_time))

with open(log_path, 'r') as log_file:
    content = log_file.readlines()
    basic_info = content[1:6]
    print("\n\n" + "".join(basic_info))

print(f"处理完成，详情请在桌面查看日志文件-> Log[{FFmpeg}]{current_time}.txt")