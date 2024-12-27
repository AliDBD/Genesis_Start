#!/usr/bin/env python

# -- coding: utf-8 --
# @Time : 2024/12/25 18:51
# @Author : Genesis Ai
# @File : platfrom_excel.py


import pandas as pd

# 1. 为了在控制台打印时不省略列、也不截断单元格内容
pd.set_option('display.max_columns', None)   # 显示所有列
pd.set_option('display.max_rows', None)      # 显示所有行（若数据非常多，请谨慎使用）
pd.set_option('display.max_colwidth', 5000)  # 单元格内容的最大打印宽度
pd.set_option('display.width', 5000)         # 输出时控制台一次可容纳的字符宽度

# 2. 读取 Excel 文件（注意在字符串前面加 r，避免转义字符问题）
excel_file = r"E:\tmp\zhongrui.xlsx"
df = pd.read_excel(excel_file)

# 3. 打印查看所有列名，确认是否存在 'Description' 等字段
print("=== 打印查看所有列名，确认是否存在 'Description' 等字段 ===")
print(df.columns.tolist())

# 4. 打印整个 DataFrame 数据（此时不会再省略列或截断内容）
print("\n=== Full DataFrame Preview ===")
print(df)

# 5. 如果需要验证某个字段(如 'Description')是否读取正确，可以单独打印这一列
if 'Description' in df.columns:
    print("\n=== 'Description' Column Preview ===")
    print(df['Description'])
else:
    print("\n[警告] 未找到列名 'Description'，请检查表头或拼写是否正确。")

# 6. 将数据转换成 list[dict] 格式，缓存到变量 data_cache 以供后续使用
data_cache = df.to_dict(orient='records')

# 7. 打印缓存数据（可能较长，酌情使用）
print("\n=== data_cache (list of dict) Preview ===")
for row in data_cache[:5]:  # 只示例打印前5行，避免控制台太长
    print(row)

# 8. 示例：若要在后续把 data_cache 写回新的 Excel 或 CSV，可以执行：
# pd.DataFrame(data_cache).to_excel('new_data.xlsx', index=False)
# pd.DataFrame(data_cache).to_csv('new_data.csv', index=False)

