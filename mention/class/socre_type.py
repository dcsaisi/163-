# -*- coding: utf-8 -*-
"""
Created on Mon Jan 22 13:46:07 2024

@author: Administrator
"""

import pandas as pd
from snownlp import SnowNLP

# 读取CSV文件
input_file = 'all_data.xls'  # 替换为你的CSV文件路径
output_file = 'pos_score.xls'  # 输出情感分析结果的文件路径


# 读取CSV文件中的评论数据
df = pd.read_excel(input_file)
df.head()

def type_class(text):
    if text > 0.65:
        text = '积极'
    elif text >= 0.4 and text <= 0.65:
        text = '中性'
    else:
        text = '消极'
    return text
df['sentiments'] = df['comment'].apply(lambda x: SnowNLP(x).sentiments)
df['type'] = df['sentiments'].apply(lambda x: type_class(x))

# 将带有情感分析结果的DataFrame保存为新的CSV文件
df.to_excel(output_file, index=False, engine='openpyxl')

print(f"情感分析结果已保存到 {output_file}")
