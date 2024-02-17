# -*- coding: utf-8 -*-
"""
Created on Fri Jan 12 19:21:57 2024

@author: Administrator
"""

## 加载数据到内存

#%%

import librosa
import numpy as np
import os
genres = 'blues classical country disco hiphop jazz metal pop reggae rock'.split()
data_set = []
label_set = []
label2id = {genre:i for i,genre in enumerate(genres)}
id2label = {i:genre for i,genre in enumerate(genres)}
print(label2id)

hop_length = 512
for g in genres:
    print(g)
    for filename in os.listdir(f'dataset/genres/{g}/'):
        songname = f'dataset/genres/{g}/{filename}'
        y, sr = librosa.load(songname, mono=True, duration=30)
        chroma_stft = librosa.feature.chroma_stft(y=y, sr=sr)
        # y换成 s 即频谱图会更准确
        S, phase = librosa.magphase(librosa.stft(y))
        rmse = librosa.feature.rms(S=S)

        spec_cent = librosa.feature.spectral_centroid(y=y, sr=sr)
        spec_bw = librosa.feature.spectral_bandwidth(y=y, sr=sr)
        rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
        zcr = librosa.feature.zero_crossing_rate(y)
        mfcc = librosa.feature.mfcc(y=y, sr=sr)

        # 计算节奏信息
        # Compute local onset autocorrelation
        oenv = librosa.onset.onset_strength(y=y, sr=sr, hop_length=hop_length)
        tempogram = librosa.feature.tempogram(onset_envelope=oenv, sr=sr,
                                       hop_length=hop_length)
        # Compute global onset autocorrelation
        ac_global = librosa.autocorrelate(oenv, max_size=tempogram.shape[0])
        ac_global = librosa.util.normalize(ac_global)

        to_append = f'{np.mean(chroma_stft)} {np.mean(rmse)} {np.mean(spec_cent)} {np.mean(spec_bw)} {np.mean(rolloff)} {np.mean(zcr)} {np.mean(ac_global)}'
        for e in mfcc:
            to_append += f' {np.mean(e)}'
        data_set.append([float(i) for i in to_append.split(" ")])
        label_set.append(label2id[g])

#%% md

### 手动打乱数据集

# 通过`get_state()`保存状态，`set_state()`重新载入状态，可以使得两个数组在保证对应关系不变的情况下，完成随机打乱。

#%%

state = np.random.get_state()
np.random.shuffle(data_set)
np.random.set_state(state)
np.random.shuffle(label_set)

#%% md

## 创建数据集

#%%

from sklearn.preprocessing import StandardScaler
from keras.utils import to_categorical
scaler = StandardScaler()
X = scaler.fit_transform(np.array(data_set, dtype = float))
y = to_categorical(np.array(label_set))

#%%

print("X.shape: ", X.shape, " Y.shape:", y.shape)

#%% md

### 将测试集和训练集分隔

#%%

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

#%% md

## 创建模型

#%%

from keras import models
from keras.layers import Dense, Dropout
from keras import regularizers
def create_model():
    model = models.Sequential()
    model.add(Dense(256, activation='relu', input_shape=(X_train.shape[1],), kernel_regularizer=regularizers.l2(0.003)))
    model.add(Dense(128, activation='relu', kernel_regularizer=regularizers.l2(0.003)))
    model.add(Dense(64, activation='relu', kernel_regularizer=regularizers.l2(0.003)))
    model.add(Dropout(0.5))
    model.add(Dense(10, activation='softmax'))
    return model
model = create_model()

#%% md

# 这里创建了一个包含三个隐藏层的神经网络，最后一层输出的是分类层，因为是10类，所以最后一层是10个单元。（这里增加了一层Dropout减少数据过拟合）

#%% md

## 编译模型

# 这里是一个分类问题，所以使用类别交叉熵函数`categorical_crossentropy`，然后优化器选择`Adam`，评价指标选择正确率。

#%%

from keras import optimizers
adam = optimizers.Adam(lr=0.001,beta_1=0.9,beta_2=0.999,epsilon=1e-8)
model.compile(optimizer=adam,
              loss='categorical_crossentropy',
              metrics=['accuracy'])

#%% md

## 训练与评估

# 接下来使用`fit`方法进行训练，训练70轮。

#%%

model.fit(X_train, y_train, epochs=70, batch_size=128)

#%% md

# 使用`evaluate`方法进行评估。

#%%

test_loss, test_acc = model.evaluate(X_test,y_test)
print('test_acc: ',test_acc)

#预测值和打印出来第一个值
prediction = model.predict(X_test)
prediction.shape

prediction[0]
np.argmax(prediction[0])#取最大

#%%

from keras.models import save_model, load_model


# 保存模型
model.save('music_genre_classifier.h5')
