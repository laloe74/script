import os
import subprocess

# 定义输入文件夹和输出文件夹路径
input_folder = r'F:\Download'
output_folder = r'F:\Music'

# 确保输出文件夹存在，如果不存在则创建它
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 遍历输入文件夹中的所有文件
for filename in os.listdir(input_folder):
    if filename.endswith(('.mp4', '.mkv')):
        input_file = os.path.join(input_folder, filename)
        output_file = os.path.join(output_folder, f'{os.path.splitext(filename)[0]}.mp3')
        # 使用 ffmpeg 提取音频，并设置编码质量
        subprocess.run(['ffmpeg', '-i', input_file, '-vn', '-codec:a', 'libmp3lame', '-q:a', '0', output_file], check=True)