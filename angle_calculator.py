# -*- coding: utf-8 -*-
"""
模块名称: angle_calculator.py
负责人: 同学 B / 同学 C
功能: 输入平面上三个点的坐标(A, B, C)，计算以B为顶点的夹角∠ABC (角度制值)
"""
import numpy as np

def calculate_angle(a, b, c):
    """
    计算三点组成的夹角值（以点 b 为顶点）
    :param a: 数组点 A 的坐标 [x, y]
    :param b: 核心顶点 B 的坐标 [x, y] (如膝关节)
    :param c: 数组点 C 的坐标 [x, y]
    :return: 角度值 (float, 范围 0 到 180 度)
    """
    a = np.array(a)  # 节点 A (例如：髋关节)
    b = np.array(b)  # 节点 B (例如：膝关节，作为顶点)
    c = np.array(c)  # 节点 C (例如：踝关节)

    # 创建 B->A 和 B->C 的向量
    ba = a - b
    bc = c - b

    # 计算余弦值: cos(θ) = (ba · bc) / (|ba| * |bc|)
    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    
    # 剪裁值域防止数值误差导致 acos 报错 (-1.0 到 1.0 之间)
    cosine_angle = np.clip(cosine_angle, -1.0, 1.0)
    
    # 转换为角度制
    angle = np.arccos(cosine_angle)
    return np.degrees(angle)