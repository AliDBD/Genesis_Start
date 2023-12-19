#!/usr/bin/env python

# -- coding: utf-8 --
# @Time : 2023/12/19 16:54
# @Author : Genesis Ai
# @File : app.py

# 导入Flask模块和其他必要库
from flask import Flask, request, redirect, url_for
import os
import json
# 创建Flask应用实例
from xhs.id提取 import extract_ids_to_excel

app = Flask(__name__)

# 定义一个路由，处理上传到'/upload'路径的POST请求
@app.route('/upload', methods=['POST'])
def upload_file():
    # 检查请求中是否有文件部分
    if 'file' not in request.files:
        return 'No file part'

    # 获取请求中的文件
    file = request.files['file']

    # 如果没有选择文件，文件名为空
    if file.filename == '':
        return 'No selected file'

    # 检查文件是否允许上传（基于文件名）
    if file and allowed_file(file.filename):
        # 拼接文件保存路径
        filename = os.path.join('path/to/save', file.filename)

        # 保存文件到服务器
        file.save(filename)

        # 调用函数处理文件
        extract_ids_to_excel(filename)

        # 返回成功消息
        return 'File uploaded and processed successfully'
    else:
        # 如果文件类型不允许，返回错误消息
        return 'Invalid file type'

# 辅助函数，用于检查文件的扩展名是否允许
def allowed_file(filename):
    # 检查文件名中是否有点号，并且扩展名是否是'txt'
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() == 'txt'

# 运行Flask应用
if __name__ == '__main__':
    app.run(debug=True)
