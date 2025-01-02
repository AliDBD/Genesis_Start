#!/usr/bin/env python
# -- coding: utf-8 --
# @Time : 2024/12/25 16:25
# @Author : Genesis Ai
# @File : excel_leng_pdf.py
"""
***优化代码写入问题
"""
import os
from PyPDF2 import PdfReader, PdfWriter
import pandas as pd


def load_excel_data(excel_file: str):
    """
    从 Excel 文件加载数据。
    :param excel_file: Excel 文件路径
    :return: list[dict] 格式的数据缓存
    """
    # 读取 Excel 文件
    df = pd.read_excel(excel_file)

    # 打印列名
    print("Excel 列名:", df.columns.tolist())

    # 转换为字典列表
    data_cache = df.to_dict(orient="records")
    print(f"加载了 {len(data_cache)} 条记录。")
    return data_cache


def fill_pdf_with_pypdf2(pdf_template: str, data: dict, output_path: str):
    """
    使用 PyPDF2 填充 PDF 表单字段，并保留所有页面内容。
    :param pdf_template: PDF 模板文件路径
    :param data: 字典数据，每条记录的字段键值对
    :param output_path: 填充后 PDF 输出路径
    """
    # 加载 PDF 模板
    reader = PdfReader(pdf_template)
    writer = PdfWriter()

    # 表单字段数据
    form_data = {
        " Description of Merchandise": f"{data.get('Product_Code', '')} {data.get('Description', '')}",
        #" Description of Merchandise": data.get('Description', '').strip(),
        "11 HTSUS NUMBER no dashessymbolsRow1": data.get('Tariff_Number', ''),
        "13 ARTICLECOMPONENT OF ARTICLERow1": data.get('Description', ''),
        "14 PLANT SCIENTIFIC NAME Genus SpeciesRow1": data.get('Genus', ''),
        "14 PLANT SCIENTIFIC NAME Genus SpeciesRow1_2": data.get('Species', ''),
        "15 COUNTRY OF HARVESTRow1": data.get('Country', ''),
        "16 QUANTITY OF PLANT MATERIALRow1": data.get('QUANTITY_OF_PLANT_MATERIAL（KGS）', '')
    }

    # 遍历所有页面并写入
    for page_num, page in enumerate(reader.pages):
        if page_num == 0:  # 仅修改第一页
            writer.update_page_form_field_values(page, form_data)
            print(f"[DEBUG] 填充第一页字段：{form_data}")
        writer.add_page(page)

    # 保存到新文件
    with open(output_path, "wb") as output_pdf:
        writer.write(output_pdf)

    print(f"生成 PDF 文件：{output_path}")


def main():
    # 输入文件路径
    excel_path = r"E:\tmp\20250102.xlsx"  # Excel 文件路径
    pdf_template = r"E:\tmp\pdfmoban.pdf"  # PDF 模板路径
    output_dir = r"E:\tmp\20250102"   # 输出文件夹路径

    # 创建输出目录（如不存在）
    os.makedirs(output_dir, exist_ok=True)

    # 从 Excel 加载数据
    all_data = load_excel_data(excel_path)

    # 遍历每条记录并生成 PDF
    for row in all_data:
        # 使用 Product_Code 作为文件名
        product_code = row.get('Product_Code', 'Unknown').strip()
        if not product_code:
            print(f"[警告] 缺少 Product_Code，跳过此记录。")
            continue

        output_file = os.path.join(output_dir, f"{product_code}.pdf")
        fill_pdf_with_pypdf2(pdf_template, row, output_file)

    print("[INFO] 所有 PDF 已成功生成。")


if __name__ == "__main__":
    main()
