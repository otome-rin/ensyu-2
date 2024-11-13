import librosa
import numpy as np
from fastdtw import fastdtw
from scipy.signal import correlate
from scipy.spatial.distance import euclidean
import matplotlib.pyplot as plt
from scipy.spatial.distance import cosine

def compare_doraemon(audio_path1,audio_path2):

    compare_f0(audio_path1, audio_path2)
    print("A")
        # 基本周波数の類似度
    pitch_similarity = compare_f0(audio_path1, audio_path2)
    print(f"Pitch Similarity (F0): {pitch_similarity}")

    # 抑揚の類似度
    intonation_similarity = compare_intonation(audio_path1, audio_path2)
    print(f"Intonation Similarity (Energy): {intonation_similarity}")

    similarity_score00 = evaluate_similarity(audio_path1, audio_path2)
    print(f"Similarity Score: {similarity_score00}")

    ry,similarity = rhythm_compare(audio_path1,audio_path2)
    print(f"リズムの類似度: {ry}")
    print(f"リズムの類似度？: {similarity}")

def compare_f0(audio_path1, audio_path2):
    # 音声の基本周波数（F0）を抽出
    y1, sr1 = librosa.load(audio_path1)
    y2, sr2 = librosa.load(audio_path2)
    Max_f0 = 500
    Min_f0 = 100
    f0_1, _, _ = librosa.pyin(y1, fmin = Min_f0, fmax = Max_f0)
    f0_2, _, _ = librosa.pyin(y2, fmin = Min_f0, fmax = Max_f0)

    # NaNを除去
    f0_1 = f0_1[~np.isnan(f0_1)]
    f0_2 = f0_2[~np.isnan(f0_2)]
    # fastdtwを使用して基本周波数の動的時間伸縮距離を計算
    distance, _ = fastdtw(f0_1, f0_2)
    if distance == 0:
      return False
    else:
      return distance

# 抑揚（ピッチとエネルギー変動）の類似度を計算する関数
def compare_intonation(audio_path1, audio_path2):
    # ピッチ（F0）とエネルギー（RMS）の変動を抽出
    y1, sr1 = librosa.load(audio_path1)
    y2, sr2 = librosa.load(audio_path2)

    rms_1 = librosa.feature.rms(y=y1)[0]
    rms_2 = librosa.feature.rms(y=y2)[0]

    if len(rms_2) != 0:
      rms_1 = rms_1 / np.max(rms_1)
      rms_2 = rms_2 / np.max(rms_2)
    # fastdtwを使用して抑揚の動的時間伸縮距離を計算
    distance, _ = fastdtw(rms_1, rms_2)
    return distance

def extract_mfcc(file_path, n_mfcc=13):
    # 音声ファイルを読み込み
    y, sr = librosa.load(file_path, sr=None)

    # MFCC特徴量を抽出
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=n_mfcc)

    # フレームごとの平均値を計算して特徴ベクトルを生成
    mfcc_mean = np.mean(mfcc.T, axis=0)
    return mfcc_mean

# コサイン類似度を計算する関数
def cosine_similarity(vec1, vec2):
    return 1 - cosine(vec1, vec2)

# 話者の類似性を評価する関数
def evaluate_similarity(file1, file2):
    # 2つの音声ファイルからMFCCを抽出
    mfcc1 = extract_mfcc(file1)
    mfcc2 = extract_mfcc(file2)

    # コサイン類似度を計算
    similarity = cosine_similarity(mfcc1, mfcc2)

    return similarity

# 音声データをロードする関数
def load_audio(file_path, sr=22050):
    audio, _ = librosa.load(file_path, sr=sr)
    return audio

# ゼロクロス率を計算する関数
def compute_zero_crossing_rate(audio, frame_length=2048, hop_length=512):
    return librosa.feature.zero_crossing_rate(audio, frame_length=frame_length, hop_length=hop_length)

# テンポ（BPM）を計算する関数
def compute_tempo(audio, sr=22050):
    onset_env = librosa.onset.onset_strength(y=audio, sr=sr)
    tempo, _ = librosa.beat.beat_track(onset_envelope=onset_env, sr=sr)
    return tempo

# ゼロクロス率の類似度を計算する関数
def zero_crossing_rate_similarity(zcr1, zcr2):
    # ゼロクロス率の平均を比較
    zcr1_mean = np.mean(zcr1)
    zcr2_mean = np.mean(zcr2)
    return 1 - np.abs(zcr1_mean - zcr2_mean) / max(zcr1_mean, zcr2_mean)

# テンポの類似度を計算する関数
def tempo_similarity(tempo1, tempo2):
    return 1 - np.abs(tempo1 - tempo2) / max(tempo1, tempo2)


# リズムの類似度を計算
def rhythm_similarity(correlation):
    # 最大相互相関値を取る位置を特定
    max_correlation = np.max(np.abs(correlation))
    # 類似度（最大相互相関値を基準にする）
    similarity = max_correlation
    return similarity
def calculate_cross_correlation(wave1, wave2):
    # 相互相関を計算
    correlation = correlate(wave1, wave2, mode='full')
    return correlation
def rhythm_compare(audio_path1, audio_path2):
    audio1 = load_audio(audio_path1)
    audio2 = load_audio(audio_path2)
    Max_f0 = 500
    Min_f0 = 100
    f1, _, _ = librosa.pyin(audio1, fmin = Min_f0, fmax = Max_f0)
    f2, _, _ = librosa.pyin(audio2, fmin = Min_f0, fmax = Max_f0)

    # NaNを除去
    f1 = f1[~np.isnan(f1)]
    f2 = f2[~np.isnan(f2)]
    # fastdtwを使用して基本周波数の動的時間伸縮距離を計算
    _,F=fastdtw(f1,f2)
    if(len(F)==0):
      print("False")
      return "False"
     #テンポの類似性
    ry=0
    for i in range(len(F)-1):
      ry+=abs(F[i+1][0]-F[i][0]-F[i+1][1]+F[i][1])
    ry=ry/len(F)
    # 波1と波2の相互相関を計算
    correlation = calculate_cross_correlation(audio1, audio2)
    # リズムの類似度を計算
    similarity = rhythm_similarity(correlation)
    return ry, similarity