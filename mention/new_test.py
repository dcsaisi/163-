# import matplotlib in line
import pandas as pd
import numpy as np
import re
import jieba.posseg as psg
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import pandas as pd
import os
import jieba.analyse
import matplotlib as mpl

# 加载评论数据
reviews = pd.read_excel('pos_score.xls')
# 统计重复数据
reviews[['comment', 'type']].duplicated().sum()
# 评论去重
reviews = reviews[['comment', 'type']].drop_duplicates()
# 重置索引
reviews.reset_index(drop=True, inplace=True)

# 去掉评论中的数字、字母，以及“京东”“京东商城”“美的”“热水器”“电热水器"
content = reviews['comment']
# 编译匹配模式
pattern = re.compile('[a-zA-Z0-9]|苗族|牛|版')
# re.sub用于替换字符串中的匹配项
content = content.apply(lambda x : pattern.sub('',x))
# 自定义简单的分词函数
worker = lambda s : [[x.word,x.flag] for x in psg.cut(s)]   # 单词与词性
seg_word = content.apply(worker)

# 将词语转化为数据框形式，一列是词，一列是词语所在的句子id，最后一列是词语在该句子中的位置
 # 每一评论中词的个数
n_word = seg_word.apply(lambda x: len(x))
# 构造词语所在的句子id
n_content = [[x+1]*y for x,y in zip(list(seg_word.index), list(n_word))]
# 将嵌套的列表展开，作为词所在评论的id
index_content = sum(n_content, [])

seg_word = sum(seg_word,[])
# 词
word = [x[0] for x in seg_word]
# 词性
nature = [x[1] for x in seg_word]
# content_type评论类型
content_type = [[x]*y for x,y in zip(list(reviews['type']),list(n_word))]
content_type = sum(content_type,[])

# 构造数据框
result = pd.DataFrame({'index_content': index_content,
                      'word' : word,
                      'nature': nature,
                      'content_type' : content_type})
# 删除标点符号(x的词性为标点符号     )
result = result[result['nature'] != 'x']

# 删除停用词
# 加载停用词
stop_path = open('./class/hit_stopwords.txt','r', encoding='utf-8')
stop = [x.replace('\n','') for x in stop_path.readlines()]
# 得到非停用词序列
word = list(set(word) - set(stop))
# 判断表格中的单词列是否在非停用词列中
result = result[result['word'].isin(word)]

# 构造各词在评论中的位置列
n_word = list(result.groupby(by=['index_content'])['index_content'].count())
index_word = [list(np.arange(0,x)) for x in n_word]
index_word = sum(index_word,[])
result['index_word'] = index_word
result.reset_index(drop=True,inplace=True)


# # 提取含名词的评论的句子id
# ind = result[[x == 'n' for x in result['nature']]]['index_content'].unique()
# # 提取评论
# result = result[result['index_content'].isin(ind)]
#
# # 重置索引
# result.reset_index(drop=True,inplace=True)

# 提取含名词的评论的句子id
ind = result[[x == 'n' for x in result['nature']]]['index_content'].unique()

# 提取评论
result_with_noun = result[(result['index_content'].isin(ind))]

# 重置索引
result_with_noun.reset_index(drop=True, inplace=True)




# 按word分组统计数目
frequencies = result.groupby(by = ['word'])['word'].count()
# 按数目降序排序
frequencies = frequencies.sort_values(ascending = False)
# 从文件中将图像读取为数组
# backgroud_Image=plt.imread('data/pl.jpg')
wordcloud = WordCloud(font_path="C:\Windows\Fonts\simsun.ttc",# 这里的字体要与自己电脑中的对应
                      max_words=100,            # 选择前100词
                      # background_color='white',  # 背景颜色为白色
                      # mask=backgroud_Image
                      )
my_wordcloud = wordcloud.fit_words(frequencies)
# 将数据展示到二维图像上
plt.imshow(my_wordcloud)
# 关掉x,y轴
plt.axis('off')
plt.show()

# 将结果写出
result.to_csv("word.csv", index = False, encoding = 'utf-8')


# 读入评论词表
word = pd.read_csv('word.csv',header=0)
# 读入正面、负面情感评价词
pos_comment = pd.read_csv("./data/正面评价词语（中文）.txt", header=None,sep="\n",
                           encoding='GBK', engine='python')
neg_comment = pd.read_csv("./data/负面评价词语（中文）.txt", header=None,sep="\n",
                           encoding='GBK', engine='python')
pos_emotion = pd.read_csv("./data/正面情感词语（中文）.txt", header=None,sep="\n",
                           encoding='GBK', engine='python')
neg_emotion = pd.read_csv("./data/负面情感词语（中文）.txt", header=None,sep="\n",
                           encoding='GBK', engine='python')
# 去掉每个词后面的空格
pos_comment[0] = pos_comment[0].str.rstrip()
pos_emotion[0] = pos_emotion[0].str.rstrip()
neg_comment[0] = neg_comment[0].str.rstrip()
neg_emotion[0] = neg_emotion[0].str.rstrip()
# 合并情感词与评价词
positive = set(pos_comment.iloc[:,0])|set(pos_emotion.iloc[:,0])
negative = set(neg_comment.iloc[:,0])|set(neg_emotion.iloc[:,0])
# 正负面情感词表中相同的词语
intersection = positive & negative
# 去掉相同的词
positive = list(positive - intersection)
negative = list(negative - intersection)

# 正面词语赋予初始权重1，负面词语赋予初始权重-1
positive = pd.DataFrame({"word":positive,
                         "weight":[1]*len(positive)})
negative = pd.DataFrame({"word":negative,
                         "weight":[-1]*len(negative)})
posneg = positive.append(negative)
# 将分词结果与正负面情感词表合并，定位情感词
data_posneg = pd.merge(left=word,right=posneg,on='word',how='left')
# 先按评论id排序，再按在评论中的位置排序
data_posneg = data_posneg.sort_values(by = ['index_content','index_word'])



# 根据情感词前面两个位置的词语是否存在否定词或双层否定词对情感值进行修正
# 载入否定词表
notdict = pd.read_csv("./data/not.csv", encoding='GBK')
# 处理否定修饰词
# 构造新列，作为经过否定词修正后的情感值
data_posneg['amend_weight'] = data_posneg['weight']
data_posneg['id'] = np.arange(0, len(data_posneg))
# 只保留有情感值的词语
only_inclination = data_posneg.dropna()
# 修改索引
only_inclination.index = np.arange(0, len(only_inclination))


index = only_inclination['id']
for i in np.arange(0, len(only_inclination)):
    # 提取第i个情感词所在的评论
    review = data_posneg[data_posneg['index_content'] == only_inclination['index_content'][i]]
    # 修改索引
    review.index = np.arange(0, len(review))
    # 第i个情感值在该文档的位置
    affective = only_inclination['index_word'][i]
    if affective == 1:
        # 情感词前面的单词是否在否定词表
        ne = sum([i in notdict['term'] for i in review['word'][affective - 1]])
        if ne == 1:
            data_posneg['amend_weight'][index[i]] = -data_posneg['weight'][index[i]]
    elif affective > 1:
        # 情感词前面两个位置的词语是否在否定词，存在一个调整成相反的情感权重，存在两个就不调整
        ne = sum([i in notdict['term'] for i in review['word'][[affective - 1, affective - 2]]])
        if ne == 1:
            data_posneg['amend_weight'][index[i]] = -data_posneg['weight'][index[i]]


# 计算每条评论的情感值
emotional_value = only_inclination.groupby(['index_content'],as_index=False)['amend_weight'].sum()
# 去除情感值为0的评论
emotional_value = emotional_value[emotional_value['amend_weight'] != 0]
emotional_value.reset_index(drop=True,inplace=True)


# 给情感值大于0的赋予评论类型pos，小于0的赋予neg
emotional_value['a_type'] = ''
emotional_value['a_type'][emotional_value['amend_weight'] > 0] = 'pos'
emotional_value['a_type'][emotional_value['amend_weight'] < 0] = 'neg'
# 查看情感分析的结果
result = pd.merge(left=word,right=emotional_value,on='index_content',how='right')
# 去重
result = result[['index_content','content_type', 'a_type']].drop_duplicates()

# 混淆矩阵-交叉表
confusion_matrix = pd.crosstab(result['content_type'],result['a_type'],margins=True)

# print(confusion_matrix)
# # 准确率
# print((confusion_matrix.iloc[1,0] + confusion_matrix.iloc[2,1])/confusion_matrix.iloc[3,2])

# 提取正负面评论信息
# 得到正面评论与负面评论对应的索引
ind_pos = list(emotional_value[emotional_value['a_type'] == 'pos']['index_content'])
ind_neg = list(emotional_value[emotional_value['a_type'] == 'neg']['index_content'])
# 得到正面评论与负面评论
posdata = word[[i in ind_pos for i in word['index_content']]]
negdata = word[[i in ind_neg for i in word['index_content']]]

# 绘制正面情感词云
# 正面情感词词云
freq_pos = posdata.groupby(by = ['word'])['word'].count()
freq_pos = freq_pos.sort_values(ascending = False)
# backgroud_Image=plt.imread('data/pl.jpg')
wordcloud = WordCloud(font_path="C:\Windows\Fonts\simsun.ttc",
                      max_words=100,
                      background_color='white',
                      # mask=backgroud_Image
                      )
pos_wordcloud = wordcloud.fit_words(freq_pos)
plt.imshow(pos_wordcloud)
plt.axis('off')
plt.show()


# 绘制负面评论词云
freq_neg = negdata.groupby(by = ['word'])['word'].count()
freq_neg = freq_neg.sort_values(ascending = False)
neg_wordcloud = wordcloud.fit_words(freq_neg)
plt.imshow(neg_wordcloud)
plt.axis('off')
plt.show()

# 将结果写出,每条评论作为一行
posdata.to_csv("posdata.csv", index = False, encoding = 'utf-8')
negdata.to_csv("negdata.csv", index = False, encoding = 'utf-8')




