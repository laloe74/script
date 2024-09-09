import os

# 清除空格
def clean_whitespace(text):
    """
    清除空格：
    1. 清除只有空格的行中的所有空格。
    2. 删除每行末尾的多余空格。
    """
    lines = text.split('\n')
    cleaned_lines = []

    for line in lines:
        # 移除行尾空格
        line = line.rstrip()
        # 若行内只有空格，则清除空格
        if line.strip() == '':
            cleaned_lines.append('')
        else:
            cleaned_lines.append(line)

    return '\n'.join(cleaned_lines)

# 版面控制
def format_layout(text):
    """
    控制版面
        标题处理：
            - 第一个标题上只保留两个空行。
            - 其余标题上保留三个空行。
        作者处理：
            - 标题下紧跟作者
            - 若标题下没有紧跟作者，以「作者」替代。
            - 确保作者和内容之间有且仅有一个空行。
        诗歌内容处理：
            - 内容内部若存在连续多个空行，只保留一个空行。
        整体处理：
            - 确保最后一行有文字的内容就是整个文件的最后一行。
    """

    lines = text.split('\n')
    formatted_lines = []
    i = 0
    first_title_found = False

    # 处理每一行
    while i < len(lines):
        line = lines[i]  # 保留行首空格

        # 标题处理
        if line.startswith('### '):
            # 处理第一个标题
            if not first_title_found:
                first_title_found = True
                # 在第一个标题上方只保留两个空行
                while len(formatted_lines) > 0 and formatted_lines[-1].strip() == '':
                    formatted_lines.pop()
                formatted_lines.extend(['', ''])
            else:
                # 其余标题上方保留三个空行
                while len(formatted_lines) > 0 and formatted_lines[-1].strip() == '':
                    formatted_lines.pop()
                formatted_lines.extend(['', '', ''])

            # 添加标题行
            formatted_lines.append(line)

            # 作者处理
            if i + 1 < len(lines) and lines[i + 1].strip() != '' and not lines[i + 1].startswith('### '):
                # 如果标题下面的行存在且不是下一个标题，则认为是作者行
                formatted_lines.append(lines[i + 1])
                i += 1
            else:
                # 否则添加默认作者行
                formatted_lines.append('作者')

        # 诗歌内容处理
        else:
            # 直接添加，不做其他处理
            formatted_lines.append(line)

        i += 1

    # 整体处理
    # 删除末尾所有空行，确保最后一行有文字的内容
    while len(formatted_lines) > 0 and formatted_lines[-1].strip() == '':
        formatted_lines.pop()

    # 返回结果
    return '\n'.join(formatted_lines)

# Hugo 格式
def add_spaces(text):
    """
    处理空格要求：
    1. 除了标题行外（###开头），每个有内容的行后面加两个空格。
    2. 每个空行（除了第一个标题上面的两个空行）里加上一个全角空格然后再加两个空格。
    """
    lines = text.split('\n')
    processed_lines = []
    first_title_found = False
    empty_line_count = 0

    for line in lines:
        # 处理第一个标题上面的空行
        if not first_title_found:
            if line.startswith('### '):
                first_title_found = True
            processed_lines.append(line)
            continue

        # 处理有内容的行（除标题行外）
        if line.strip() != '':
            if not line.startswith('### '):
                processed_lines.append(line + '  ')  # 非标题行的内容行后面加两个空格
            else:
                processed_lines.append(line)  # 标题行保持不变
        else:
            # 处理空行，排除第一个标题上面的两个空行
            processed_lines.append('　  ')  # 每个空行里加上一个全角空格再加两个空格

    return '\n'.join(processed_lines)

# 模式控制
def process_files(input_folder, output_folder):
    """
    处理输入文件夹中的所有 Markdown 文件，将结果保存到输出文件夹。
    """
    # 设置模式变量：
    # - 1：清除空格
    # - 2：清除空格+版面控制
    # - 3：Hugo格式
    mode = int(input("请输入处理模式（1, 2, 3）："))

    for filename in os.listdir(input_folder):
        if filename.endswith('.md'):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)

            # 读取文件内容
            with open(input_path, 'r', encoding='utf-8') as file:
                content = file.read()
           
            while True:
                if mode == 1:
                    print("执行模式-1: 清除空格")
                    final_content = clean_whitespace(content)
                    break

                elif mode == 2:
                    print("执行模式-2: 清除空格+版面控制")
                    clean_content = clean_whitespace(content)
                    final_content = format_layout(clean_content)
                    break

                elif mode == 3:
                    print("执行模式-3: Hugo格式")
                    clean_content = clean_whitespace(content)
                    formatted_content = format_layout(clean_content)
                    final_content = add_spaces(formatted_content)
                    break
                else:
                    print("没有选择模式")
                    mode = int(input("请再次输入模式（1, 2, 3）："))

            # 保存处理后的文件
            with open(output_path, 'w', encoding='utf-8') as file:
                file.write(final_content)

            print(f"Processed file: {filename}")


# 定义输入和输出文件夹路径
input_folder = os.path.expanduser("~/Desktop/from")
output_folder = os.path.expanduser("~/Desktop")

# 处理文件
process_files(input_folder, output_folder)