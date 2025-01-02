"""
pip install pandas openpyxl tabulate
"""

import pandas as pd
import os
from datetime import datetime

# 定义文件路径，使用 os.path.expanduser() 将路径中的 ~ 替换为绝对路径
input_file = os.path.expanduser('~/Desktop/marks.xlsx') 
output_excel = os.path.expanduser('~/Desktop/film.xlsx') 
output_markdown = os.path.expanduser('/Users/keo/Project/keooq/content/pages/film.md')  # 直接更新博客文件

# 读取指定的分表「看过」
df = pd.read_excel(input_file, sheet_name='看过')

# 将“创建时间”列转换为日期类型
df['创建时间'] = pd.to_datetime(df['创建时间'], errors='coerce')

# 筛选出电影内容，排除剧集（根据 NeoDB链接 前缀）
df = df[df['NeoDB链接'].str.contains('https://neodb.social/movie/')]

# 创建新的数据框，并按照要求格式化
df_new = pd.DataFrame()
# 去除名称列中感叹号 !，修改为 []() 格式
df_new['名称'] = df.apply(lambda row: f"[{row['标题']}]({row['NeoDB链接']})", axis=1)
df_new['时间'] = df['创建时间'].apply(lambda x: x.strftime('%Y/%m/%d') if pd.notnull(x) else '')  # 格式化时间为 年/月/日
df_new['评分'] = df['我的评分'].apply(lambda x: '★' * int(x) + '☆' * (5 - int(x)) if pd.notnull(x) and x != '' else '-')

# 按时间倒序排序
df_new = df_new.sort_values(by='时间', ascending=False)

# 统计评分数据
total_count = len(df_new)  # 总数
five_star_count = (df_new['评分'] == '★★★★★').sum()  # 5星数量
four_star_count = (df_new['评分'] == '★★★★☆').sum()  # 4星数量
three_star_count = (df_new['评分'] == '★★★☆☆').sum()  # 3星数量
two_star_count = (df_new['评分'] == '★★☆☆☆').sum()  # 2星数量
one_star_count = (df_new['评分'] == '★☆☆☆☆').sum()  # 1星数量

# 创建汇总统计表格（总数、5星、4星、3星、2星、1星）
summary_header = pd.DataFrame([['总数', '5星', '4星', '3星', '2星', '1星']])
summary_data = pd.DataFrame([[total_count, five_star_count, four_star_count, three_star_count, two_star_count, one_star_count]])

# 创建数据表头（名称、时间、评分）
data_header = pd.DataFrame([['名称', '时间', '评分']], columns=[0, 1, 2])

# 创建一个空的 DataFrame，用于填充前面的空行
empty_rows = pd.DataFrame([[''] * 6], index=[0])  # 空行占据 6 列

# 将汇总表格、空行、数据表头和数据内容组合成一个完整的表格
final_table = pd.concat([summary_header, summary_data, empty_rows, data_header], ignore_index=True)

# 将原数据表插入到最终表格的第5行（A5开始）
for idx, row in df_new.iterrows():
    final_table.at[idx + 4, 0] = row['名称']  # 名称列（A列，从 A5 开始）
    final_table.at[idx + 4, 1] = row['时间']  # 时间列（B列，从 B5 开始）
    final_table.at[idx + 4, 2] = row['评分']  # 评分列（C列，从 C5 开始）

# 去除所有 NaN 值，替换为空字符串
final_table = final_table.fillna('')

# 保存到新的 Excel 文件中，禁用 header 和 index
with pd.ExcelWriter(output_excel) as writer:
    final_table.to_excel(writer, index=False, header=False)

# 手动创建Markdown内容
markdown_lines = []

# 添加Markdown文件的前置内容
markdown_lines.append('---')
markdown_lines.append('title: Film - 电影')
markdown_lines.append('url: film')
markdown_lines.append('---')
markdown_lines.append('')  # 添加一个空行
markdown_lines.append('')  # 再添加一个空行
markdown_lines.append('### 电影')

# 第一部分：生成汇总统计表的Markdown内容
summary_table_header = '|总数|五星|四星|三星|二星|一星|'
summary_table_divider = '|:----|:----|:----|:----|:----|:----|'
summary_table_content = '|{}|{}|{}|{}|{}|{}|'.format(total_count, five_star_count, four_star_count, three_star_count, two_star_count, one_star_count)
markdown_lines.append(summary_table_header)
markdown_lines.append(summary_table_divider)
markdown_lines.append(summary_table_content)

# 添加分隔符，前后各有空行
markdown_lines.append('')
markdown_lines.append('---')
markdown_lines.append('')

# 第二部分：生成数据表头和内容的Markdown内容
data_table_header = '|名称|时间|评分|'
data_table_divider = '|:----|:----|:----|'
markdown_lines.append(data_table_header)
markdown_lines.append(data_table_divider)

# 遍历每一行，将其转换为Markdown格式的表格语法
for index, row in df_new.iterrows():
    # 将每行转换为 Markdown 表格格式
    row_data = '|{}|{}|{}|'.format(str(row['名称']).strip(), str(row['时间']).strip(), str(row['评分']).strip())
    markdown_lines.append(row_data)

# 将所有行组合成Markdown内容
markdown_content = '\n'.join(markdown_lines)

# 将Markdown内容写入文件，确保路径有效
with open(output_markdown, 'w', encoding='utf-8') as md_file:
    md_file.write(markdown_content)

print("\nfilm.py 执行完成")