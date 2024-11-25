#!/bin/bash

# 设置桌面路径
desktop_path="$HOME/Desktop"
output_folder="$desktop_path/converted_docs"

# 创建保存转换文件的文件夹（如果不存在）
mkdir -p "$output_folder"

# 切换到桌面目录
cd "$desktop_path"

# 查找所有 PDF 文件并进行转换
for pdf_file in *.pdf; do
    # 提取文件名（去掉扩展名）
    filename="${pdf_file%.*}"
    
    # 使用 pdf2docx 正确转换 PDF 为 DOCX，存储到 output_folder
    pdf2docx convert "$pdf_file" "$output_folder/${filename}.docx"

    echo "已转换 $pdf_file 为 $output_folder/${filename}.docx"
done