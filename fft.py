import numpy as np  # 数値計算用のライブラリ
import matplotlib.pyplot as plt  # グラフ描画用のライブラリ
from scipy.io import wavfile  # WAVファイル読み込み用のライブラリ
from scipy.fft import fft  # FFT（高速フーリエ変換）計算用のライブラリ

# 1. WAVファイルを読み込む
sample_rate, data = wavfile.read('./wav2/rec_20240930_182942.wav')  # 'sample.wav' を読み込み、サンプリングレートとデータを取得
print(f"サンプリングレート: {sample_rate} Hz")

# 2. データのサイズ確認とモノラル化（ステレオの場合）
if data.ndim > 1:
    data = data.mean(axis=1)  # ステレオ（2チャンネル）なら平均をとってモノラル化

# 3. FFT（高速フーリエ変換）を行う
fft_result = fft(data)  # FFT計算
N = len(data)  # データのサンプル数
frequencies = np.fft.fftfreq(N, d=1/sample_rate)  # 周波数軸の計算

# 4. FFT結果をプロットする
plt.figure(figsize=(12, 6))  # グラフのサイズを指定
plt.plot(frequencies[:N//2], np.abs(fft_result)[:N//2])  # 周波数と対応するFFT振幅をプロット（正の周波数成分のみ）
plt.xlabel('周波数 (Hz)')  # x軸のラベル
plt.ylabel('振幅')  # y軸のラベル
plt.title('FFT結果')  # グラフタイトル
plt.grid()  # グリッドを表示
plt.show()  # グラフを表示
