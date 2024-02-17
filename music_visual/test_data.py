# -*- coding: utf-8 -*-
"""
Created on Sat Jan 27 16:30:00 2024

@author: Administrator
"""
from keras.models import save_model, load_model
import librosa
import numpy as np

# %%
def extract_feature_song(f):
    y, sr = librosa.load(f, sr= 8000)  # 加载音频文件，并获取采样率

    mfcc = librosa.feature.mfcc(y=y, sr=sr)  # 使用采样率作为参数
    mfcc /= np.amax(np.absolute(mfcc))
    # 调整特征向量的形状以匹配模型的输入
    # 假设模型的输入形状是 (1, num_features)
    mfcc = np.expand_dims(mfcc, axis=0)
    mfcc = mfcc[:, :27]  # 保留前 27 个特征
    return mfcc
    # return np.ndarray.flatten(mfcc)[:27]

# %%
def extract_feature_song1(songname):
        data_set = []
        hop_length = 512
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
        return data_set

# 加载模型
loaded_model = load_model('music_genre_classifier.h5')
# path = r'dataset\genres\classical\classical.00025.wav'
path = r'苗族芦笙云.mp3'

X_new = extract_feature_song1(path)


# %%
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X = np.array(X_new, dtype = float)
print(X.shape)

# 使用加载的模型对新数据进行预测
# 假设你有一些新的音频特征数据X_new，你可以使用加载的模型进行预测
predictions = loaded_model.predict(X)
print(predictions.shape)
print(predictions[0])
genres = ['blues' 'classical', 'country', 'disco', 'hiphop', 'jazz', 'metal', 'pop', 'reggae', 'rock']
i = np.argmax(predictions[0])
print(i)
print(genres[i-1])
