# 将ass转换成srt
# 调整字幕时间
# 繁体转简体

# pip install pysubs2 chardet opencc-python-reimplemented
import pysubs2
import os
import chardet  # 用于自动检测文件编码
from opencc import OpenCC  # 用于繁体转换为简体

# 设置时间调整值（负值表示提前，单位为秒）
time_adjustment = 0

# 初始化 OpenCC，用于繁体转换为简体
cc = OpenCC('t2s')  # 't2s' 表示繁体转简体

# 获取输入的字幕文件目录
subtitle_directory = input("\n输入路径（直接将待处理的文件夹拖进来）\n---------------------：").strip()

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

# 遍历指定目录下所有 .ass 和 .srt 文件
for filename in os.listdir(subtitle_directory):
    # 只处理 .srt 或 .ass 文件
    if filename.endswith(".srt") or filename.endswith(".ass"):
        file_path = os.path.join(subtitle_directory, filename)

        # 检测文件编码格式
        with open(file_path, 'rb') as file:
            raw_data = file.read()
            result = chardet.detect(raw_data)
            detected_encoding = result['encoding']
            print(f"检测到文件 {file_path} 的编码格式为：{detected_encoding}")

        # 如果是 .ass 文件，先转换为 .srt 格式
        if filename.endswith(".ass"):
            print(f"正在将 .ass 文件转换为 .srt 文件：{file_path}")
            try:
                # 加载 .ass 文件并转换为 .srt 格式
                subs = pysubs2.load(file_path, encoding=detected_encoding)
                # 转换后的文件路径（使用 .srt 作为后缀）
                srt_file_path = os.path.join(subtitle_directory, f"{os.path.splitext(filename)[0]}.srt")
                subs.save(srt_file_path, encoding="utf-8")
                print(f"转换完成：{file_path} -> {srt_file_path}")
                
                # 删除原始 .ass 文件
                os.remove(file_path)
                print(f"已删除原 .ass 文件：{file_path}")
                
                # 将 file_path 修改为转换后的 .srt 文件路径，继续处理
                file_path = srt_file_path
            except UnicodeDecodeError:
                print(f"使用检测到的编码格式 {detected_encoding} 读取 .ass 文件失败，跳过该文件：{file_path}")
                continue

        # 读取转换后的 .srt 文件（或原始的 .srt 文件）
        try:
            subs = pysubs2.load(file_path, encoding="utf-8")  # 使用 UTF-8 加载 .srt 文件
        except UnicodeDecodeError:
            print(f"使用 UTF-8 编码读取文件失败，跳过该文件：{file_path}")
            continue

        # 调整每个事件的时间，并将繁体内容转换为简体
        for line in subs:
            line.start += int(time_adjustment * 1000)  # 将秒转换为毫秒
            line.end += int(time_adjustment * 1000)
            
            # 繁体转换为简体
            line.text = cc.convert(line.text)

        # 直接替换原始文件，强制使用 UTF-8 编码保存（替换原始 .srt 文件）
        subs.save(file_path, encoding="utf-8")
        print(f"处理完成并替换原始文件：{file_path}")