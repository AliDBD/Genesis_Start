#!/usr/bin/env python

# -- coding: utf-8 --
# @Time : 2024/6/26 下午5:08
# @Author : Genesis Ai
# @File : geometry_calculator.py

import tkinter as tk
from tkinter import ttk, messagebox
import math

# 定义计算函数
def calculate_square():
    try:
        a = float(entry1.get())
        choice = var.get()
        if choice == "周长":
            result = 4 * a
            result_label.config(text=f"正方形的周长是: {result:.4f} 厘米")
        elif choice == "面积":
            result = a * a
            result_label.config(text=f"正方形的面积是: {result:.4f} 平方厘米")
        else:
            messagebox.showerror("错误", "无效的计算类型")
    except ValueError:
        messagebox.showerror("错误", "请输入有效的数字")

def calculate_rectangle():
    try:
        a = float(entry1.get())
        b = float(entry2.get())
        choice = var.get()
        if choice == "周长":
            result = 2 * (a + b)
            result_label.config(text=f"长方形的周长是: {result:.4f} 厘米")
        elif choice == "面积":
            result = a * b
            result_label.config(text=f"长方形的面积是: {result:.4f} 平方厘米")
        else:
            messagebox.showerror("错误", "无效的计算类型")
    except ValueError:
        messagebox.showerror("错误", "请输入有效的数字")

def calculate_circle():
    try:
        r = float(entry1.get())
        choice = var.get()
        if choice == "周长":
            result = 2 * math.pi * r
            result_label.config(text=f"圆的周长是: {result:.4f} 厘米")
        elif choice == "面积":
            result = math.pi * r * r
            result_label.config(text=f"圆的面积是: {result:.4f} 平方厘米")
        else:
            messagebox.showerror("错误", "无效的计算类型")
    except ValueError:
        messagebox.showerror("错误", "请输入有效的数字")

def calculate_cube():
    try:
        a = float(entry1.get())
        choice = var.get()
        if choice == "表面积":
            result = 6 * a * a
            result_label.config(text=f"立方体的表面积是: {result:.4f} 平方厘米")
        elif choice == "体积":
            result = a * a * a
            result_label.config(text=f"立方体的体积是: {result:.4f} 立方厘米")
        else:
            messagebox.showerror("错误", "无效的计算类型")
    except ValueError:
        messagebox.showerror("错误", "请输入有效的数字")

def calculate_rectangular_prism():
    try:
        a = float(entry1.get())
        b = float(entry2.get())
        c = float(entry3.get())
        choice = var.get()
        if choice == "表面积":
            result = 2 * (a * b + b * c + a * c)
            result_label.config(text=f"长方体的表面积是: {result:.4f} 平方厘米")
        elif choice == "体积":
            result = a * b * c
            result_label.config(text=f"长方体的体积是: {result:.4f} 立方厘米")
        else:
            messagebox.showerror("错误", "无效的计算类型")
    except ValueError:
        messagebox.showerror("错误", "请输入有效的数字")

def calculate_cylinder():
    try:
        r = float(entry1.get())
        h = float(entry2.get())
        choice = var.get()
        if choice == "表面积":
            result = 2 * math.pi * r * (h + r)
            result_label.config(text=f"圆柱体的表面积是: {result:.4f} 平方厘米")
        elif choice == "体积":
            result = math.pi * r * r * h
            result_label.config(text=f"圆柱体的体积是: {result:.4f} 立方厘米")
        else:
            messagebox.showerror("错误", "无效的计算类型")
    except ValueError:
        messagebox.showerror("错误", "请输入有效的数字")

def calculate_ellipse():
    try:
        a = float(entry1.get())
        b = float(entry2.get())
        choice = var.get()
        if choice == "周长":
            result = math.pi * (3 * (a + b) - math.sqrt((3 * a + b) * (a + 3 * b)))  # 公式套用计算
            result_label.config(text=f"椭圆的周长（近似）是: {result:.4f} 厘米")
        elif choice == "面积":
            result = math.pi * a * b
            result_label.config(text=f"椭圆的面积是: {result:.4f} 平方厘米")
        else:
            messagebox.showerror("错误", "无效的计算类型")
    except ValueError:
        messagebox.showerror("错误", "请输入有效的数字")

def calculate_parallelogram():
    try:
        a = float(entry1.get())
        b = float(entry2.get())
        h = float(entry3.get())
        choice = var.get()
        if choice == "周长":
            result = 2 * (a + b)
            result_label.config(text=f"平行四边形的周长是: {result:.4f} 厘米")
        elif choice == "面积":
            result = a * h
            result_label.config(text=f"平行四边形的面积是: {result:.4f} 平方厘米")
        else:
            messagebox.showerror("错误", "无效的计算类型")
    except ValueError:
        messagebox.showerror("错误", "请输入有效的数字")

def calculate_cone():
    try:
        r = float(entry1.get())
        h = float(entry2.get())
        choice = var.get()
        if choice == "表面积":
            result = math.pi * r * (r + math.sqrt(h**2 + r**2))
            result_label.config(text=f"圆锥体的表面积是: {result:.4f} 平方厘米")
        elif choice == "体积":
            result = (1/3) * math.pi * r**2 * h
            result_label.config(text=f"圆锥体的体积是: {result:.4f} 立方厘米")
        else:
            messagebox.showerror("错误", "无效的计算类型")
    except ValueError:
        messagebox.showerror("错误", "请输入有效的数字")

def calculate_triangle():
    try:
        a = float(entry1.get())
        b = float(entry2.get())
        c = float(entry3.get())
        choice = var.get()
        if choice == "周长":
            result = a + b + c
            result_label.config(text=f"三角形的周长是: {result:.4f} 厘米")
        elif choice == "面积":
            s = (a + b + c) / 2
            result = math.sqrt(s * (s - a) * (s - b) * (s - c))
            result_label.config(text=f"三角形的面积是: {result:.4f} 平方厘米")
        else:
            messagebox.showerror("错误", "无效的计算类型")
    except ValueError:
        messagebox.showerror("错误", "请输入有效的数字")

# 创建主窗口
root = tk.Tk()
root.title("几何计算器")

# 创建下拉菜单选择几何形状
shapes = {
    "正方形": calculate_square,
    "长方形": calculate_rectangle,
    "圆形": calculate_circle,
    "立方体": calculate_cube,
    "长方体": calculate_rectangular_prism,
    "圆柱体": calculate_cylinder,
    "椭圆": calculate_ellipse,
    "平行四边形": calculate_parallelogram,
    "圆锥体": calculate_cone,
    "三角形": calculate_triangle
}

shape_label = tk.Label(root, text="请选择几何形状:")
shape_label.pack()

shape_var = tk.StringVar(root)
shape_var.set("正方形")  # 默认值

shape_menu = ttk.Combobox(root, textvariable=shape_var, values=list(shapes.keys()))
shape_menu.pack()

# 创建下拉菜单选择计算类型
var = tk.StringVar()
var.set("周长")  # 默认值

type_label = tk.Label(root, text="请选择计算类型:")
type_label.pack()

type_menu = ttk.Combobox(root, textvariable=var, values=["周长", "面积", "表面积", "体积"])
type_menu.pack()

# 创建输入框
entry1_label = tk.Label(root, text="请输入第一个参数（单位：厘米）:")
entry1_label.pack()
entry1 = tk.Entry(root)
entry1.pack()

entry2_label = tk.Label(root, text="请输入第二个参数（单位：厘米）:")
entry2_label.pack()
entry2 = tk.Entry(root)
entry2.pack()

entry3_label = tk.Label(root, text="请输入第三个参数（单位：厘米）:")
entry3_label.pack()
entry3 = tk.Entry(root)
entry3.pack()

# 创建计算按钮
def calculate():
    shape = shape_var.get()
    if shape in shapes:
        shapes[shape]()
    else:
        messagebox.showerror("错误", "无效的几何形状")

calculate_button = tk.Button(root, text="计算", command=calculate)
calculate_button.pack()

# 创建结果显示标签
result_label = tk.Label(root, text="")
result_label.pack()

# 运行主循环
root.mainloop()
