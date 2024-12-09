#!/usr/bin/env python

# -- coding: utf-8 --
# @Time : 2024/6/26 下午5:08
# @Author : Genesis Ai
# @File : geometry_calculator.py

import tkinter as tk
from tkinter import ttk, messagebox
import math
from datetime import datetime

# 添加历史记录列表
calculation_history = []

# 添加样式设置
def setup_styles():
    style = ttk.Style()
    style.configure("TButton", padding=6, relief="flat", background="#ccc", font=('Arial', 10))
    style.configure("TLabel", padding=5, font=('Arial', 10))
    style.configure("TCombobox", padding=5, font=('Arial', 10))

# 添加历史记录功能
def save_calculation(shape, calculation_type, params, result):
    calculation_history.append({
        "时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "图形": shape,
        "计算类型": calculation_type,
        "参数": params,
        "结果": result
    })

# 显示历史记录
def show_history():
    history_window = tk.Toplevel(root)
    history_window.title("计算历史")
    history_window.geometry("400x300")
    
    history_text = tk.Text(history_window, wrap=tk.WORD)
    history_text.pack(fill=tk.BOTH, expand=True)
    
    for record in calculation_history:
        history_text.insert(tk.END, 
            f"时间: {record['时间']}\n"
            f"图形: {record['图形']}\n"
            f"计算类型: {record['计算类型']}\n"
            f"参数: {record['参数']}\n"
            f"结果: {record['结果']}\n"
            f"{'-'*40}\n"
        )
    history_text.config(state=tk.DISABLED)

# 更新参数输入框提示
def update_parameter_labels(event=None):
    shape = shape_var.get()
    if shape == "正方形":
        entry1_label.config(text="请输入边长（单位：厘米）:")
        entry2_label.pack_forget()
        entry2.pack_forget()
        entry3_label.pack_forget()
        entry3.pack_forget()
    elif shape == "长方形":
        entry1_label.config(text="请输入长（单位：厘米）:")
        entry2_label.config(text="请输入宽（单位：厘米）:")
        entry2_label.pack()
        entry2.pack()
        entry3_label.pack_forget()
        entry3.pack_forget()
    # ... 其他图形的参数提示 ...

# 添加图形预览功能
def show_shape_preview(event=None):
    shape = shape_var.get()
    canvas.delete("all")
    
    if shape == "正方形":
        canvas.create_rectangle(50, 50, 150, 150)
    elif shape == "长方形":
        canvas.create_rectangle(30, 50, 170, 120)
    elif shape == "圆形":
        canvas.create_oval(50, 50, 150, 150)
    # ... 其他图形的预览 ...

# 主窗口设置
root = tk.Tk()
root.title("几何计算器")
root.geometry("600x800")  # 设置窗口大小

# 设置样式
setup_styles()

# 创建预览画布
canvas = tk.Canvas(root, width=200, height=200, bg="white")
canvas.pack(pady=10)

# 添加历史记录按钮
history_button = ttk.Button(root, text="查看历史记录", command=show_history)
history_button.pack(pady=5)

# 定义计算函数
def calculate_square():
    try:
        a = float(entry1.get())
        choice = var.get()
        params = f"边长: {a}厘米"
        
        if choice == "周长":
            result = 4 * a
            result_text = f"正方形的周长是: {result:.4f} 厘米"
        elif choice == "面积":
            result = a * a
            result_text = f"正方形的面积是: {result:.4f} 平方厘米"
        else:
            messagebox.showerror("错误", "无效的计算类型")
            return
            
        result_label.config(text=result_text)
        save_calculation("正方形", choice, params, result_text)
    except ValueError:
        messagebox.showerror("错误", "请输入有效的数字")

def calculate_rectangle():
    try:
        a = float(entry1.get())
        b = float(entry2.get())
        choice = var.get()
        params = f"长: {a}厘米, 宽: {b}厘米"
        
        if choice == "周长":
            result = 2 * (a + b)
            result_text = f"长方形的周长是: {result:.4f} 厘米"
        elif choice == "面积":
            result = a * b
            result_text = f"长方形的面积是: {result:.4f} 平方厘米"
        else:
            messagebox.showerror("错误", "无效的计算类型")
            return
            
        result_label.config(text=result_text)
        save_calculation("长方形", choice, params, result_text)
    except ValueError:
        messagebox.showerror("错误", "请输入有效的数字")

def calculate_circle():
    try:
        r = float(entry1.get())
        choice = var.get()
        params = f"半径: {r}厘米"
        
        if choice == "周长":
            result = 2 * math.pi * r
            result_text = f"圆的周长是: {result:.4f} 厘米"
        elif choice == "面积":
            result = math.pi * r * r
            result_text = f"圆的面积是: {result:.4f} 平方厘米"
        else:
            messagebox.showerror("错误", "无效的计算类型")
            return
            
        result_label.config(text=result_text)
        save_calculation("圆形", choice, params, result_text)
    except ValueError:
        messagebox.showerror("错误", "请输入有效的数字")

def calculate_cube():
    try:
        a = float(entry1.get())
        choice = var.get()
        params = f"边长: {a}厘米"
        
        if choice == "表面积":
            result = 6 * a * a
            result_text = f"立方体的表面积是: {result:.4f} 平方厘米"
        elif choice == "体积":
            result = a * a * a
            result_text = f"立方体的体积是: {result:.4f} 立方厘米"
        else:
            messagebox.showerror("错误", "无效的计算类型")
            return
            
        result_label.config(text=result_text)
        save_calculation("立方体", choice, params, result_text)
    except ValueError:
        messagebox.showerror("错误", "请输入有效的数字")

def calculate_rectangular_prism():
    try:
        a = float(entry1.get())
        b = float(entry2.get())
        c = float(entry3.get())
        choice = var.get()
        params = f"长: {a}厘米, 宽: {b}厘米, 高: {c}厘米"
        
        if choice == "表面积":
            result = 2 * (a * b + b * c + a * c)
            result_text = f"长方体的表面积是: {result:.4f} 平方厘米"
        elif choice == "体积":
            result = a * b * c
            result_text = f"长方体的体积是: {result:.4f} 立方厘米"
        else:
            messagebox.showerror("错误", "无效的计算类型")
            return
            
        result_label.config(text=result_text)
        save_calculation("长方体", choice, params, result_text)
    except ValueError:
        messagebox.showerror("错误", "请输入有效的数字")

def calculate_cylinder():
    try:
        r = float(entry1.get())
        h = float(entry2.get())
        choice = var.get()
        params = f"半径: {r}厘米, 高: {h}厘米"
        
        if choice == "表面积":
            result = 2 * math.pi * r * (h + r)
            result_text = f"圆柱体的表面积是: {result:.4f} 平方厘米"
        elif choice == "体积":
            result = math.pi * r * r * h
            result_text = f"圆柱体的体积是: {result:.4f} 立方厘米"
        else:
            messagebox.showerror("错误", "无效的计算类型")
            return
            
        result_label.config(text=result_text)
        save_calculation("圆柱体", choice, params, result_text)
    except ValueError:
        messagebox.showerror("错误", "请输入有效的数字")

def calculate_ellipse():
    try:
        a = float(entry1.get())
        b = float(entry2.get())
        choice = var.get()
        params = f"长轴: {a}厘米, 短轴: {b}厘米"
        
        if choice == "周长":
            result = math.pi * (3 * (a + b) - math.sqrt((3 * a + b) * (a + 3 * b)))  # 公式套用计算
            result_text = f"椭圆的周长（近似）是: {result:.4f} 厘米"
        elif choice == "面积":
            result = math.pi * a * b
            result_text = f"椭圆的面积是: {result:.4f} 平方厘米"
        else:
            messagebox.showerror("错误", "无效的计算类型")
            return
            
        result_label.config(text=result_text)
        save_calculation("椭圆", choice, params, result_text)
    except ValueError:
        messagebox.showerror("错误", "请输入有效的数字")

def calculate_parallelogram():
    try:
        a = float(entry1.get())
        b = float(entry2.get())
        h = float(entry3.get())
        choice = var.get()
        params = f"边长: {a}厘米, 高: {h}厘米"
        
        if choice == "周长":
            result = 2 * (a + b)
            result_text = f"平行四边形的周长是: {result:.4f} 厘米"
        elif choice == "面积":
            result = a * h
            result_text = f"平行四边形的面积是: {result:.4f} 平方厘米"
        else:
            messagebox.showerror("错误", "无效的计算类型")
            return
            
        result_label.config(text=result_text)
        save_calculation("平行四边形", choice, params, result_text)
    except ValueError:
        messagebox.showerror("错误", "请输入有效的数字")

def calculate_cone():
    try:
        r = float(entry1.get())
        h = float(entry2.get())
        choice = var.get()
        params = f"半径: {r}厘米, 高: {h}厘米"
        
        if choice == "表面积":
            result = math.pi * r * (r + math.sqrt(h**2 + r**2))
            result_text = f"圆锥体的表面积是: {result:.4f} 平方厘米"
        elif choice == "体积":
            result = (1/3) * math.pi * r**2 * h
            result_text = f"圆锥体的体积是: {result:.4f} 立方厘米"
        else:
            messagebox.showerror("错误", "无效的计算类型")
            return
            
        result_label.config(text=result_text)
        save_calculation("圆锥体", choice, params, result_text)
    except ValueError:
        messagebox.showerror("错误", "请输入有效的数字")

def calculate_triangle():
    try:
        a = float(entry1.get())
        b = float(entry2.get())
        c = float(entry3.get())
        choice = var.get()
        params = f"边长: {a}厘米, 边长: {b}厘米, 边长: {c}厘米"
        
        if choice == "周长":
            result = a + b + c
            result_text = f"三角形的周长是: {result:.4f} 厘米"
        elif choice == "面积":
            s = (a + b + c) / 2
            result = math.sqrt(s * (s - a) * (s - b) * (s - c))
            result_text = f"三角形的面积是: {result:.4f} 平方厘米"
        else:
            messagebox.showerror("错误", "无效的计算类型")
            return
            
        result_label.config(text=result_text)
        save_calculation("三角形", choice, params, result_text)
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

# 绑定图形选择事件
shape_menu.bind('<<ComboboxSelected>>', lambda e: (update_parameter_labels(), show_shape_preview()))

# 运行主循环
root.mainloop()
