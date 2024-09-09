# 邻女 余怒
# 鸵鸟的四维鸟瞰（节选） 余怒

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
    3. 若以半角空格开头，每两个半角空格替换为一个全角空格。
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

        # 处理以半角空格开头的行
        if line.startswith(' '):
            # 将每两个半角空格替换为一个全角空格
            while '  ' in line:
                line = line.replace('  ', '　')

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

# 检验排版
def validate_layout(text, mode):
    """
    检验排版是否符合以下规则：
    模式3 (Hugo格式)：
        1. 查找第二个 '---' 行，然后检查其下方的第3行是否为标题行。
        2. 以 '###' 开头的标题行末尾不存在任何空格。
        3. 以 '###' 开头的标题下方第一行（作者行）有内容，并且该行以两个空格结尾。
        4. 以 '###' 开头的标题下方第二行为「　 」（一个全角空格和两个半角空格）。
        5. 内容行以两个空格结尾。
        6. 其余的标题行上方三行为「　 」（每行一个全角空格和两个半角空格）。
        7. 文件的最后一行是非空行。
    模式2 (清除空格+版面控制)：
        1. 查找第二个 '---' 行，然后检查其下方的第3行是否为标题行。
        2. 以 '###' 开头的标题行末尾不存在任何空格。
        3. 以 '###' 开头的标题下方第一行（作者行）有内容。
        4. 以 '###' 开头的标题下方第二行为空行。
        5. 内容末尾没有空格。
        6. 其余的标题行上方三行为3个空行。
        7. 文件的最后一行是非空行。
    """

    if mode == 1:
        print("排版检测: 跳过")
        return

    lines = text.split('\n')
    errors = []
    total_lines = len(lines)
    inside_delimiters = False  # 用于跟踪是否在 --- 包裹内部
    first_title_found = False  # 用于标记第一个标题是否已找到

    # 查找第二个 '---' 行的位置
    delimiter_count = 0
    second_delimiter_index = -1

    for i, line in enumerate(lines):
        if line.strip() == '---':
            delimiter_count += 1
            if delimiter_count == 2:
                second_delimiter_index = i
                break

    # 1. 检查第二个 '---' 行后的格式（其下方的第3行应为标题行）
    if second_delimiter_index != -1 and second_delimiter_index + 3 < total_lines:
        if not lines[second_delimiter_index + 3].startswith('### '):
            errors.append("格式错误：第二个 '---' 行下方的第3行应为标题行")

    for i, line in enumerate(lines):
        # 检查是否进入或离开 --- 包裹部分
        if line.strip() == '---':
            inside_delimiters = not inside_delimiters
            continue  # 跳过对 '---' 行的进一步检查

        # 如果在 --- 包裹部分内，跳过检查
        if inside_delimiters:
            continue

        # 2. 检查标题行末尾空格
        if line.startswith('### ') and line.rstrip() != line:
            errors.append(f"第 {i + 1} 行：标题行末尾存在空格")

        # 处理第一个标题行的逻辑
        if line.startswith('### ') and not first_title_found:
            first_title_found = True  # 标记已经找到第一个标题行
            continue  # 跳过第一个标题行的其他检查

        # 模式3的特定检查
        if mode == 3:
            # 3. 检查标题下方的作者行
            if line.startswith('### '):
                if i + 1 < total_lines:
                    author_line = lines[i + 1]
                    if author_line.strip() == '' or not author_line.endswith('  '):
                        errors.append(f"第 {i + 2} 行：作者行格式不正确，必须有内容并以两个空格结尾")

                # 4. 检查标题下方的第二行（应为「　 」，一个全角空格和两个半角空格）
                if i + 2 < total_lines:
                    second_line = lines[i + 2]
                    if second_line != '　  ':
                        errors.append(f"第 {i + 3} 行：标题下方的第二行应为「　 」（一个全角空格和两个半角空格）")

            # 5. 检查内容行结尾空格
            if line.strip() != '' and not line.startswith('### ') and not line.endswith('  '):
                errors.append(f"第 {i + 1} 行：内容行应以两个空格结尾（模式3）")

            # 6. 检查其他标题行前的空行（不处理第一个标题）
            if line.startswith('### ') and first_title_found:
                if i > 2 and not (lines[i - 1] == '　  ' and lines[i - 2] == '　  ' and lines[i - 3] == '　  '):
                    errors.append(f"第 {i + 1} 行：其他标题行前应为三行「　 」（每行一个全角空格和两个半角空格）")

        # 模式2的特定检查
        elif mode == 2:
            # 3. 检查标题下方的作者行
            if line.startswith('### '):
                if i + 1 < total_lines:
                    author_line = lines[i + 1]
                    if author_line.strip() == '':
                        errors.append(f"第 {i + 2} 行：作者行格式不正确，必须有内容")

                # 4. 检查标题下方的第二行（应为空行）
                if i + 2 < total_lines:
                    second_line = lines[i + 2]
                    if second_line.strip() != '':
                        errors.append(f"第 {i + 3} 行：标题下方的第二行应为空行")

            # 5. 检查内容行末尾不应有空格
            if line.strip() != '' and not line.startswith('### ') and line.rstrip() != line:
                errors.append(f"第 {i + 1} 行：内容行末尾不应有空格（模式2）")

            # 6. 检查其他标题行前的空行（不处理第一个标题）
            if line.startswith('### ') and first_title_found:
                if i > 2 and not (lines[i - 1].strip() == '' and lines[i - 2].strip() == '' and lines[i - 3].strip() == ''):
                    errors.append(f"第 {i + 1} 行：其他标题行前应为三行空行")

    # 7. 检查最后一行是非空行
    if total_lines > 0 and lines[-1].strip() == '':
        errors.append("最后一行不应为空")

    # 输出错误信息
    if errors:
        print("排版检查: 错误")
        for error in errors:
            print(error)
    else:
        print("排版检查: 通过")


# 文件处理
def process_files(input_folder, output_folder):
    """
    处理输入文件夹中的所有 Markdown 文件，将结果保存到输出文件夹。
    """
    # 设置模式变量：
    # - 1：清除空格
    # - 2：清除空格+版面控制
    # - 3：Hugo格式
    mode = int(input("输入处理模式 1/2/3：    "))

    for filename in os.listdir(input_folder):
        if filename.endswith('.md'):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)

            # 读取文件内容
            with open(input_path, 'r', encoding='utf-8') as file:
                content = file.read()
           
            while True:
                if mode == 1:
                    print("\n模式:1     清除空格")
                    final_content = clean_whitespace(content)
                    break

                elif mode == 2:
                    print("\n模式:2     清除空格+版面控制")
                    clean_content = clean_whitespace(content)
                    final_content = format_layout(clean_content)
                    break

                elif mode == 3:
                    print("\n模式:3     Hugo格式")
                    clean_content = clean_whitespace(content)
                    formatted_content = format_layout(clean_content)
                    final_content = add_spaces(formatted_content)
                    break
                else:
                    print("您没有选择模式")
                    mode = int(input("请再次输入处理模式 1/2/3：    "))

            # 检验排版，根据当前模式
            validate_layout(final_content, mode)

            # 保存处理后的文件
            with open(output_path, 'w', encoding='utf-8') as file:
                file.write(final_content)

            print(f"\n处理完成: {filename}\n")


# 定义输入和输出文件夹路径
input_folder = os.path.expanduser("~/Desktop/from")
output_folder = os.path.expanduser("~/Desktop")

# 处理文件
process_files(input_folder, output_folder)