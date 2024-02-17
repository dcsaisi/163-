# 横轴：接近1情感为好  接近0情感为差
#纵轴：情感分布

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_excel('../mention/pos_score.xls')


sentiments_list = []
for score in df['sentiments']:
    sentiments_list.append(score)

plt.hist(sentiments_list, bins = np.arange(0, 1, 0.01), facecolor = 'r')
plt.xlabel('Sentiments Probability')
plt.ylabel('Quantity')
plt.title('Analysis of Sentiments')
plt.show()
