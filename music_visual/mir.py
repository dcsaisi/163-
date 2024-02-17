# -*- coding: utf-8 -*-
"""
Created on Fri Jan 12 19:26:29 2024

@author: Administrator
"""
#%%

# !python --version

#%%

import librosa

#%% md

# 加载音乐

#%%

x, sr = librosa.load('Subwoofer Lullaby.mp3', sr= 8000)
print(x.shape, sr)

#%% md

# 这里`x`是音频信号的数字信息，可以看到是一维的，`sr`是采样频率，用8000就好了

# 接下来查看这首歌在时域上的波形

#%%

# %matplotlib inline
import matplotlib.pyplot as plt
import librosa.display
plt.figure(figsize=(14, 5))
librosa.display.waveshow(x, sr=sr)

#%% md

# 横轴为时间，纵轴为振幅，这是音乐在时域上的信息

# 接下来对音乐在频域上的信息进行分析，首先是时变的频谱图(Spectogram)

#%%

X = librosa.stft(x)
Xdb = librosa.amplitude_to_db(abs(X))   # 把幅度转成分贝格式
plt.figure(figsize=(14, 5))
librosa.display.specshow(Xdb, sr=sr, x_axis='time', y_axis='hz')
plt.colorbar()

#%% md

# 这里横轴是时间，纵轴是频率，颜色则代表分贝（声音的响度），可以看到越红的地方信号音量越大

#%% md

## 音乐信息的特征提取

#%% md

### 过零率（Zero Crossing Rate）

# 过零率(Zero Crossing Rate,ZCR)是指在每帧中,语音信号通过零点(从正变为负或从负变为正)的次数。这个特征已在语音识别和音乐信息检索领域得到广泛使用，是金属声音和摇滚乐的关键特征。

# 回到时域图，在时间上放大



#%%

n0 = 9000
n1 = 9100
plt.figure(figsize=(14, 5))
plt.plot(x[n0:n1])
plt.grid()

#%% md

# 这里有13个过零点，可以通过下面的方法进行计算

#%%

zero_crossings = librosa.zero_crossings(x[n0:n1], pad=False)
print(sum(zero_crossings))

#%% md

### 频谱中心（Spectral Centroid）
# 频谱中心代表声音的“质心”，又称为频谱一阶距。频谱中心的值越小，表明越多的频谱能量集中在低频范围内。

#%%

#spectral centroid -- centre of mass -- weighted mean of the frequencies present in the sound
import sklearn
spectral_centroids = librosa.feature.spectral_centroid(y=x[:80000], sr=sr)[0]
# Computing the time variable for visualization
frames = range(len(spectral_centroids))
t = librosa.frames_to_time(frames, sr=8000)
# Normalising the spectral centroid for visualisation
def normalize(x, axis=0):
    return sklearn.preprocessing.minmax_scale(x, axis=axis)
#Plotting the Spectral Centroid along the waveform
librosa.display.waveshow(x[:80000], sr=sr, alpha=0.4)
plt.plot(t, normalize(spectral_centroids), color='r')

#%% md

# 这里用`x[:80000]`表示音乐的前10秒

# `.spectral_centroid`来计算每一帧的频谱中心。

# `.frames_to_time`将帧转换为时间，`time[i] == frame[i]`【因为stft是一个窗口(帧)一个窗口取的，和采样频率并不对应，所以有个转换】

# 为了更好的可视化，对频谱中心进行了归一化

#%% md

### 频谱滚降点（Spectral Rolloff）

# 频谱滚降点的意思大概是：比该频率低的频率的所有能量大于一定比例的整个频谱的能量，通常这个比例为0.85。

# 参考以下公式：

# (img)[http://nladuo.github.io/2019/08/31/%E4%BD%BF%E7%94%A8Python%E5%AF%B9%E9%9F%B3%E9%A2%91%E8%BF%9B%E8%A1%8C%E7%89%B9%E5%BE%81%E6%8F%90%E5%8F%96/rolloff.png]


#%%

spectral_rolloff = librosa.feature.spectral_rolloff(y=x, sr=sr)[0]
librosa.display.waveshow(y=x, sr=sr, alpha=0.4)
plt.plot(t, normalize(spectral_rolloff), color='r')




#%% md

### MFCC (梅尔频率倒谱系数)
# MFCC是音频信号特征中最重要的一个，基本上处理音频信号就会用到

# 信号的MFCC参数是一个小集合的特征（一般10-20个），它能够简洁的表示频谱的包络

#%%

mfccs = librosa.feature.mfcc(y=x, sr=sr)
print(mfccs.shape)
#Displaying  the MFCCs:
librosa.display.specshow(mfccs, sr=sr, x_axis='time')

#%% md

# `.mfcc` 用来计算信号的MFCC参数。

# 通过打印`mfccs.shape`，可以看看每一帧里面有多少维的MFCC特征。第一个参数是mfcc参数的维度，第二个参数是帧数。

# 这里一共3260帧，每一帧有20维特征。

#%%



#%%

n0 = 9000
n1 = 9100
plt.figure(figsize=(14, 5))
plt.plot(x[n0:n1])
plt.grid()
