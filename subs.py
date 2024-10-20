# 将ass转换成srt
# 调整字幕时间
# 繁体转简体

# pip install pysubs2 chardet opencc-python-reimplemented
import pysubs2
import os
import chardet  # 用于自动检测文件编码
from opencc import OpenCC  # 用于繁体转换为简体

# 设置时间调整值（负值表示提前，单位为秒）
time_adjustment = 46

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

# 过滤特效字幕函数（根据样式、位置等条件）
def is_effect_subtitle(event):
    # 过滤条件1: 判断是否是特效字幕（通过样式名判断）
    effect_styles = ["top", "scroll", "move", "notice", "tip"]  # 样式名称中包含这些关键字的被认为是特效字幕
    if any(style in event.style.lower() for style in effect_styles):
        return True

    # 过滤条件2: 判断是否包含特殊的 ASS 标签控制（如滚动、移动、位置）
    special_tags = ["\\move", "\\pos", "\\fade", "\\an"]  # 包含这些标签的认为是特效字幕
    if any(tag in event.text for tag in special_tags):
        return True

    # 过滤条件3: 判断是否包含特定的滚动字幕文本（如广告语句）
    special_texts = ["仅供学习使用", "请于24小时内删除", "更多资源请访问"]  # 包含这些文字的认为是特效字幕
    if any(text in event.text for text in special_texts):
        return True

    # 如果都不符合，认为是正常字幕
    return False

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
                
                # 移除特效字幕，只保留正常字幕事件
                subs.events = [event for event in subs.events if not is_effect_subtitle(event)]
                
                # 转换后的文件路径（使用 .srt 作为后缀）
                srt_file_path = os.path.join(subtitle_directory, f"{os.path.splitext(filename)[0]}.srt")
                subs.save(srt_file_path, encoding="utf-8")
                print(f"转换完成并过滤特效字幕：{file_path} -> {srt_file_path}")
                
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