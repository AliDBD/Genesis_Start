#!/usr/bin/env python

# -- coding: utf-8 --
# @Time : 2024/6/26 下午4:22
# @Author : Genesis Ai
# @File : 几何运算.py

import math

def calculate_square():
    a = float(input("请输入正方形的边长（单位：厘米）: "))
    choice = input("请选择计算类型（周长或面积）: ").strip()
    if choice == "周长":
        result = 4 * a
        print(f"正方形的周长是: {result:.4f} 厘米")
    elif choice == "面积":
        result = a * a
        print(f"正方形的面积是: {result:.4f} 平方厘米")
    else:
        print("无效的计算类型")

def calculate_rectangle():
    a = float(input("请输入长方形的长（单位：厘米）: "))
    b = float(input("请输入长方形的宽（单位：厘米）: "))
    choice = input("请选择计算类型（周长或面积）: ").strip()
    if choice == "周长":
        result = 2 * (a + b)
        print(f"长方形的周长是: {result:.4f} 厘米")
    elif choice == "面积":
        result = a * b
        print(f"长方形的面积是: {result:.4f} 平方厘米")
    else:
        print("无效的计算类型")

def calculate_circle():
    r = float(input("请输入圆的半径（单位：厘米）: "))
    choice = input("请选择计算类型（周长或面积）: ").strip()
    if choice == "周长":
        result = 2 * math.pi * r
        print(f"圆的周长是: {result:.4f} 厘米")
    elif choice == "面积":
        result = math.pi * r * r
        print(f"圆的面积是: {result:.4f} 平方厘米")
    else:
        print("无效的计算类型")

def calculate_cube():
    a = float(input("请输入立方体的边长（单位：厘米）: "))
    choice = input("请选择计算类型（表面积或体积）: ").strip()
    if choice == "表面积":
        result = 6 * a * a
        print(f"立方体的表面积是: {result:.4f} 平方厘米")
    elif choice == "体积":
        result = a * a * a
        print(f"立方体的体积是: {result:.4f} 立方厘米")
    else:
        print("无效的计算类型")

def calculate_rectangular_prism():
    a = float(input("请输入长方体的长（单位：厘米）: "))
    b = float(input("请输入长方体的宽（单位：厘米）: "))
    c = float(input("请输入长方体的高（单位：厘米）: "))
    choice = input("请选择计算类型（表面积或体积）: ").strip()
    if choice == "表面积":
        result = 2 * (a * b + b * c + a * c)
        print(f"长方体的表面积是: {result:.4f} 平方厘米")
    elif choice == "体积":
        result = a * b * c
        print(f"长方体的体积是: {result:.4f} 立方厘米")
    else:
        print("无效的计算类型")

def calculate_cylinder():
    r = float(input("请输入圆柱体的半径（单位：厘米）: "))
    h = float(input("请输入圆柱体的高（单位：厘米）: "))
    choice = input("请选择计算类型（表面积或体积）: ").strip()
    if choice == "表面积":
        result = 2 * math.pi * r * (h + r)
        print(f"圆柱体的表面积是: {result:.4f} 平方厘米")
    elif choice == "体积":
        result = math.pi * r * r * h
        print(f"圆柱体的体积是: {result:.4f} 立方厘米")
    else:
        print("无效的计算类型")

def calculate_ellipse():
    a = float(input("请输入椭圆的长轴半径（单位：厘米）: "))
    b = float(input("请输入椭圆的短轴半径（单位：厘米）: "))
    choice = input("请选择计算类型（周长或面积）: ").strip()
    if choice == "周长":
        result = math.pi * (3 * (a + b) - math.sqrt((3 * a + b) * (a + 3 * b)))  # 近似公式
        print(f"椭圆的周长（近似）是: {result:.4f} 厘米")
    elif choice == "面积":
        result = math.pi * a * b
        print(f"椭圆的面积是: {result:.4f} 平方厘米")
    else:
        print("无效的计算类型")

def calculate_parallelogram():
    a = float(input("请输入平行四边形的底边长度（单位：厘米）: "))
    b = float(input("请输入平行四边形的另一边长度（单位：厘米）: "))
    h = float(input("请输入平行四边形的高（单位：厘米）: "))
    choice = input("请选择计算类型（周长或面积）: ").strip()
    if choice == "周长":
        result = 2 * (a + b)
        print(f"平行四边形的周长是: {result:.4f} 厘米")
    elif choice == "面积":
        result = a * h
        print(f"平行四边形的面积是: {result:.4f} 平方厘米")
    else:
        print("无效的计算类型")

def calculate_cone():
    r = float(input("请输入圆锥体的底面半径（单位：厘米）: "))
    h = float(input("请输入圆锥体的高（单位：厘米）: "))
    choice = input("请选择计算类型（表面积或体积）: ").strip()
    if choice == "表面积":
        result = math.pi * r * (r + math.sqrt(h**2 + r**2))
        print(f"圆锥体的表面积是: {result:.4f} 平方厘米")
    elif choice == "体积":
        result = (1/3) * math.pi * r**2 * h
        print(f"圆锥体的体积是: {result:.4f} 立方厘米")
    else:
        print("无效的计算类型")

def calculate_triangle():
    a = float(input("请输入三角形的第一条边（单位：厘米）: "))
    b = float(input("请输入三角形的第二条边（单位：厘米）: "))
    c = float(input("请输入三角形的第三条边（单位：厘米）: "))
    choice = input("请选择计算类型（周长或面积）: ").strip()
    if choice == "周长":
        result = a + b + c
        print(f"三角形的周长是: {result:.4f} 厘米")
    elif choice == "面积":
        s = (a + b + c) / 2
        result = math.sqrt(s * (s - a) * (s - b) * (s - c))
        print(f"三角形的面积是: {result:.4f} 平方厘米")
    else:
        print("无效的计算类型")

def main():
    shapes = {
        1: ("正方形", calculate_square),
        2: ("长方形", calculate_rectangle),
        3: ("圆形", calculate_circle),
        4: ("立方体", calculate_cube),
        5: ("长方体", calculate_rectangular_prism),
        6: ("圆柱体", calculate_cylinder),
        7: ("椭圆", calculate_ellipse),
        8: ("平行四边形", calculate_parallelogram),
        9: ("圆锥体", calculate_cone),
        10: ("三角形", calculate_triangle)
    }

    print("请选择几何形状:")
    for key, value in shapes.items():
        print(f"{key}: {value[0]}")

    choice = int(input("请输入几何形状的编号: ").strip())
    if choice in shapes:
        shapes[choice][1]()
    else:
        print("无效的几何形状编号")

if __name__ == "__main__":
    main()
