#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = '蔡琳娜'
import pandas as pd
data=pd.read_excel(io=r'G:\大三下数据可视化\excel面试分析\测试题目相关数据-20210312.xlsx', 
                   sheet_name=2)
print(data)