import librosa  # 音声処理ライブラリ
import librosa.display  # メル周波数スペクトログラムの表示用
import matplotlib.pyplot as plt  # グラフ描画用ライブラリ
import numpy as np

# 1. 音声ファイルを読み込む
file_path = './wav2/rec_20240930_183330.wav'  # 対象のWAVファイルのパス
y, sr = librosa.load(file_path, sr=None)  # 音声ファイルを読み込み、信号（y）とサンプリングレート（sr）を取得

# 2. メル周波数スペクトログラムを作成する
n_fft = 2048  # フレームサイズ（FFTのサイズ）
hop_length = 512  # フレーム間のシフトサイズ
n_mels = 128  # メルフィルタバンクの数
mel_spectrogram = librosa.feature.melspectrogram(y=y, sr=sr, n_fft=n_fft, hop_length=hop_length, n_mels=n_mels)

# 3. メルスペクトログラムを対数スケールに変換する
log_mel_spectrogram = librosa.power_to_db(mel_spectrogram, ref=np.max)  # 振幅を対数スケール（dB）に変換

print(type(log_mel_spectrogram))
print(log_mel_spectrogram.shape)

#  TSV ファイルに配列を保存する
np.savetxt('output.tsv', log_mel_spectrogram, delimiter='\t', fmt='%.2f', comments='')

# 4. メル周波数スペクトログラムをプロットする
plt.figure(figsize=(12, 8))  # グラフのサイズを指定
librosa.display.specshow(log_mel_spectrogram, sr=sr, hop_length=hop_length, x_axis='time', y_axis='mel')  # スペクトログラムを表示
plt.colorbar(format='%+2.0f dB')  # カラーバーを追加
plt.title('メル周波数スペクトログラム')  # グラフのタイトル
plt.xlabel('時間 (s)')  # x軸のラベル
plt.ylabel('周波数 (Hz)')  # y軸のラベル
plt.show()  # グラフを表示
