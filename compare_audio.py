import librosa
import numpy as np
from fastdtw import fastdtw
from scipy.spatial.distance import cosine
from librosa.sequence import dtw
import whisper
import warnings
# 警告を無視
warnings.filterwarnings("ignore", category=UserWarning)


def compare_audio(audio_path1,audio_path2,Weights):

    #ピッチの得点
    pitch_score = compare_pitch(audio_path1, audio_path2) * Weights[0]

    # 抑揚の得点
    intonation_score = compare_intonation(audio_path1, audio_path2) * Weights[1]

    #mfccの得点
    mfcc_score = evaluate_similarity(audio_path1, audio_path2) * Weights[2]


    #速度の得点
    speed_score = speed_compare(audio_path1,audio_path2) * Weights[4]
    
    #総合得点の計算
    Score = pitch_score + intonation_score + mfcc_score + speed_score

    return pitch_score,intonation_score,mfcc_score,speed_score,Score

def compare_pitch(audio_path1, audio_path2):
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

    if len(f0_2) != 0:
      f0_1_s = f0_1 / np.max(f0_1)
      f0_2_s = f0_2 / np.max(f0_2)
    # fastdtwを使用して基本周波数の動的時間伸縮距離を計算
    distance1, path1 = fastdtw(f0_1, f0_2)
    distance2, _ = fastdtw(f0_1_s, f0_2_s)

    pitch_score = 0

    if distance1 >= 10000:
        pitch_score += 0
    elif distance1 <= 2000:
        pitch_score += 0.5
    else:
        pitch_score += 0.625 - distance1/16000

    if distance2 >= 10:
        pitch_score += 0
    elif distance2 <= 1:
        pitch_score += 0.5
    else:
        pitch_score += 5/9 - distance2/18

    if distance1 == 0:
      return False
    else:
      return pitch_score

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

    intonation_score = 0

    if distance >= 30:
        intonation_score = 0
    elif distance <= 5:
        intonation_score = 1
    else:
        intonation_score = 1.2 - distance/25
    return intonation_score

def extract_mfcc(file_path, n_mfcc=13):
    # 音声ファイルを読み込み
    y, sr = librosa.load(file_path, sr=None)

    # MFCC特徴量を抽出
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=n_mfcc)

    return mfcc

def dtw_distance(mfcc1, mfcc2):
    # DTWを計算
    D, wp = dtw(X=mfcc1, Y=mfcc2, metric='euclidean')

    # 最小コストを返す
    return D[-1, -1]

# 話者の類似性を評価する関数
def evaluate_similarity(file1, file2):
    # 2つの音声ファイルからMFCCを抽出
    mfcc1 = extract_mfcc(file1)
    mfcc2 = extract_mfcc(file2)

    # コサイン類似度を計算
    distance = dtw_distance(mfcc1, mfcc2)

    mfcc_score = 0

    if distance>= 90000:
        mfcc_score = 0
    elif distance <= 30000:
        mfcc_score = 1
    else:
        mfcc_score = 1.5 - distance/60000
    return mfcc_score

# 音声データをロードする関数
def load_audio(file_path, sr=22050):
    audio, _ = librosa.load(file_path, sr=sr)
    return audio

def rhythm_compare(audio_path1, audio_path2):
   # Whisperのモデルをロード
    model = whisper.load_model("turbo")
    
    # 音声ファイルをテキストに変換し、詳細情報を取得
    result1 = model.transcribe(audio_path1, language="ja", word_timestamps=True)
    result2 = model.transcribe(audio_path2, language="ja", word_timestamps=True)
    
    # 各セグメント（音声の区間）を取り出し、単語ごとの情報を取得
    word_durations1 = []
    for segment in result1['segments']:
        for word_info in segment['words']:
            word = word_info['word']
            duration = word_info['end'] - word_info['start']
            word_durations1.append((word, duration))
    
    word_durations2 = []
    for segment in result2['segments']:
        for word_info in segment['words']:
            word = word_info['word']
            duration = word_info['end'] - word_info['start']
            word_durations2.append((word, duration))

    # 合計発話時間
    total_duration1 = sum(duration for _, duration in word_durations1)
    total_duration2 = sum(duration for _, duration in word_durations2)

    # 発話時間の比率を計算
    duration_ratios1 = [(word, duration / total_duration1) for word, duration in word_durations1]
    duration_ratios2 = [(word, duration / total_duration2) for word, duration in word_durations2]
    
    # リズムスコアを計算
    def calculate_score(ratios1, ratios2):
        score = 0
        min_len = min(len(ratios1), len(ratios2))
        for i in range(min_len):
            ratio1 = ratios1[i][1]
            ratio2 = ratios2[i][1]
            score += 1.1* min(ratio1, ratio2) / max(ratio1, ratio2) / min_len
        return min(score, 1.0)  # スコアを最大1に制限

    return calculate_score(duration_ratios1, duration_ratios2)


def speed_compare(audio_path1, audio_path2):
    #喋る速さ測定
    audio1 = load_audio(audio_path1)
    audio2 = load_audio(audio_path2)

    sp=0
    if(len(audio1))>(len(audio2) - 22100):
      sp=1-(len(audio2) - 22100)/(len(audio1))
    if(len(audio2) - 22100)>=(len(audio1)):
      sp=1-(len(audio1))/(len(audio2) - 22100)

    sp_score = 0
    if sp >= 0.6:
       sp_score = 0
    elif sp <= 0.1:
       sp_score = 1
    else:
       sp_score = 1.2 - 2*sp
    return sp_score