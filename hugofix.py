import os

# 设置模式变量：1：普通格式；2：Hugo格式
mode = 2

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


def format_layout(text):
    """
    控制版面格式：
    1. 确保标题下紧跟作者名称。
    2. 确保作者和内容之间有且仅有一个空行。
    3. 确保最后一个标题的最后一行内容就是文件的最后一行内容。
    4. 确保第一个###标题上和---之间保持两个空行。
    5. 内容内部，连续空行最多保持1行。
    6. 如果某一行有内容，但是是以空格开头，则删除空格，让其以内容开头。
    """
    lines = text.split('\n')
    formatted_lines = []
    i = 0
    first_title_found = False

    while i < len(lines):
        line = lines[i]
        
        # 删除行首的空格
        line = line.lstrip()

        # 添加标题
        if line.startswith('### '):
            if not first_title_found:
                first_title_found = True
                # 在第一个标题上方确保保留两个空行
                while len(formatted_lines) > 0 and formatted_lines[-1].strip() == '':
                    formatted_lines.pop()
                formatted_lines.extend([''] * 2)

            else:
                # 在非第一个标题上方保留三个空行
                while len(formatted_lines) > 0 and formatted_lines[-1].strip() == '':
                    formatted_lines.pop()
                formatted_lines.extend([''] * 3)
            
            formatted_lines.append(line)
            
            # 确保标题下一行为作者
            if i + 1 < len(lines) and lines[i + 1].strip() != '':
                formatted_lines.append(lines[i + 1].strip())
                i += 1
            else:
                formatted_lines.append('作者')  # 默认添加作者行
            
            # 添加作者和内容之间的一个空行
            formatted_lines.append('')
        
        # 处理其他内容
        else:
            if line.strip() == '':
                # 跳过多余空行，仅保留一个空行
                if len(formatted_lines) > 0 and formatted_lines[-1] == '':
                    i += 1
                    continue
            formatted_lines.append(line)
        
        i += 1

    # 删除末尾所有空行，确保文件以最后一行内容结尾
    while len(formatted_lines) > 0 and formatted_lines[-1].strip() == '':
        formatted_lines.pop()

    return '\n'.join(formatted_lines)


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


def process_files(input_folder, output_folder):
    """
    处理输入文件夹中的所有 Markdown 文件，将结果保存到输出文件夹。
    """
    for filename in os.listdir(input_folder):
        if filename.endswith('.md'):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)

            # 读取文件内容
            with open(input_path, 'r', encoding='utf-8') as file:
                content = file.read()

            # 清除空格
            content = clean_whitespace(content)

            # 控制版面
            formatted_content = format_layout(content)

            # 根据 mode 设置决定是否添加额外的空格处理
            if mode == 2:
                # 添加空格
                final_content = add_spaces(formatted_content)
            else:
                # 不进行额外的空格处理
                final_content = formatted_content

            # 保存处理后的文件
            with open(output_path, 'w', encoding='utf-8') as file:
                file.write(final_content)

            print(f"Processed file: {filename}")


# 定义输入和输出文件夹路径
input_folder = os.path.expanduser("~/Desktop/from")
output_folder = os.path.expanduser("~/Desktop")

# 处理文件
process_files(input_folder, output_folder)