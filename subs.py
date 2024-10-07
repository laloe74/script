# pip isntall pysubs2 chardet opencc
# 调整字幕时间
# 转换繁体转简体

import pysubs2
import os
import chardet  # 用于自动检测文件编码
from opencc import OpenCC  # 用于繁体转换为简体

# 设置时间调整值（负值表示提前，单位为秒）
time_adjustment = 0.5

# 初始化 OpenCC，用于繁体转换为简体
cc = OpenCC('t2s')  # 't2s' 表示繁体转简体

# 获取输入的字幕文件目录
subtitle_directory = input("输入路径（直接将待处理的文件夹拖进来）：").strip()

# 处理可能的路径格式问题（去除两端引号）
subtitle_directory = subtitle_directory.strip('"').strip("'")

# 进一步处理路径中的转义字符（将路径中的 `\` 去掉）
subtitle_directory = subtitle_directory.replace('\\ ', ' ').replace('\\(', '(').replace('\\)', ')')

# 打印调试信息，确认处理后的路径
print(f"正在处理目录：{subtitle_directory}")

# 检查目录是否存在
if not os.path.isdir(subtitle_directory):
    print(f"目录 {subtitle_directory} 不存在，请检查路径是否正确。")
    exit()

# 获取指定目录下所有 .srt 文件
for filename in os.listdir(subtitle_directory):
    if filename.endswith(".srt"):
        file_path = os.path.join(subtitle_directory, filename)

        # 自动检测字幕文件编码格式
        with open(file_path, 'rb') as file:
            raw_data = file.read()
            result = chardet.detect(raw_data)
            detected_encoding = result['encoding']
            print(f"检测到文件 {file_path} 的编码格式为：{detected_encoding}")

        # 加载字幕文件，并使用检测到的编码格式
        try:
            subs = pysubs2.load(file_path, encoding=detected_encoding)
        except UnicodeDecodeError:
            print(f"使用检测到的编码格式 {detected_encoding} 读取失败，跳过该文件：{file_path}")
            continue

        # 调整每个事件的时间，并将繁体内容转换为简体
        for line in subs:
            line.start += int(time_adjustment * 1000)  # 将秒转换为毫秒
            line.end += int(time_adjustment * 1000)
            
            # 繁体转换为简体
            line.text = cc.convert(line.text)

        # 直接替换原始文件，强制使用 UTF-8 编码保存
        subs.save(file_path, encoding="utf-8")  # 强制使用 UTF-8 编码保存，替换原文件
        print(f"处理完成并替换原始文件：{file_path}")