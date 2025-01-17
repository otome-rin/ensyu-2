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

def split_data(data, n_parts):
    """時系列データを指定した部分数に分割"""
    length = len(data)
    split_size = length // n_parts
    splits = [data[i * split_size:(i + 1) * split_size] for i in range(n_parts - 1)]
    splits.append(data[(n_parts - 1) * split_size:])  # 残りを最後に追加
    return splits

def calculate_dtw_similarity(data1, data2):
    """DTW距離を計算"""
    distance, path = fastdtw(data1, data2)
    return distance, path

def split_data_by_dtw_path(path, n_parts, data2):
    """DTWの対応パスからdata2を分割"""
    path_points = [p[1] for p in path]  # data2のインデックスを抽出
    segment_size = len(path_points) // n_parts
    split_indices = [path_points[i * segment_size] for i in range(1, n_parts)]
    split_indices = sorted(set(split_indices))  # 重複を排除してソート

    segments = []
    start_idx = 0
    for idx in split_indices:
        segments.append(data2[start_idx:idx + 1])
        start_idx = idx + 1
    segments.append(data2[start_idx:])
    return segments

def calculate_similarity(distance, max_distance):
    """距離を類似度（0から1の範囲）に変換"""
    return max(0, 1 - (distance / max_distance))

def evaluate_segments(data1, data2, n_parts):
    """時系列データを分割して各部分の類似度を計算"""
    segments1 = split_data(data2, n_parts)

    # 全体のDTWパスを計算し、それを基にdata2を分割
    _, path = calculate_dtw_similarity(data1, data2)
    segments2 = split_data_by_dtw_path(path, n_parts, data2)

    results = []
    for i, (seg1, seg2) in enumerate(zip(segments1, segments2)):
        distance, path = calculate_dtw_similarity(seg1, seg2)
        results.append((i + 1, distance, path))
    return results

def segmented_pitch_and_intonation(audio_path1, audio_path2):
    # ピッチ（F0）とエネルギー（RMS）の変動を抽出
    y1, sr1 = librosa.load(audio_path1)
    y2, sr2 = librosa.load(audio_path2)

    rms_1 = librosa.feature.rms(y=y1)[0]
    rms_2 = librosa.feature.rms(y=y2)[0]

    Max_f0 = 500
    Min_f0 = 100
    f0_1, _, _ = librosa.pyin(y1, fmin = Min_f0, fmax = Max_f0)
    f0_2, _, _ = librosa.pyin(y2, fmin = Min_f0, fmax = Max_f0)

    # NaNを除去
    f0_1 = f0_1[~np.isnan(f0_1)]
    f0_2 = f0_2[~np.isnan(f0_2)]

    # 時系列データを3つに分割して評価
    n_parts = 3

    pitch_distances = []
    intonation_distances = []

    segments1_pitch = split_data(f0_1, n_parts) # Split pitch data
    segments1_intonation = split_data(rms_1, n_parts) # Split intonation data

    _, path_pitch = calculate_dtw_similarity(f0_1, f0_2)
    _, path_intonation = calculate_dtw_similarity(rms_1, rms_2)

    segments2_pitch = split_data_by_dtw_path(path_pitch, n_parts, f0_2)
    segments2_intonation = split_data_by_dtw_path(path_intonation, n_parts, rms_2)

    for i in range(n_parts):
        distance_pitch, _ = calculate_dtw_similarity(segments1_pitch[i], segments2_pitch[i])
        distance_intonation, _ = calculate_dtw_similarity(segments1_intonation[i], segments2_intonation[i])

        pitch_distances.append(distance_pitch)
        intonation_distances.append(distance_intonation)

    pitch_similarities = [calculate_similarity(d, max(pitch_distances)) for d in pitch_distances]
    intonation_similarities = [calculate_similarity(d, max(intonation_distances)) for d in intonation_distances]

    return pitch_similarities,intonation_similarities


    segments = ["序盤", "中盤", "終盤"]


    # --- Generate feedback ---
    min_pitch_index = pitch_similarities.index(min(pitch_similarities))
    min_intonation_index = intonation_similarities.index(min(intonation_similarities))

    min_pitch_similarity = min(pitch_similarities)
    min_intonation_similarity = min(intonation_similarities)

    if min_pitch_similarity > 0.9 and min_intonation_similarity > 0.9:
        print("ほぼ完璧です！")
    elif min_pitch_similarity > 0.7 and min_intonation_similarity > 0.7:
        print("かなり似ています！")
    elif min_pitch_similarity > 0.5 and min_intonation_similarity > 0.5:
        print("悪くないですね。")
    elif min_pitch_similarity > 0.3 and min_intonation_similarity > 0.3:
        print("あまり似ていません。")
    else:
        print("似ていません。")
    if min_pitch_similarity < min_intonation_similarity:
        print(f" 特に {segments[min_pitch_index]} の音高に修正が必要です。")
    else:
        print(f"特に {segments[min_intonation_index]} のボリュームに修正が必要です。")