import whisper
import warnings

# 警告を無視
warnings.filterwarnings("ignore", category=UserWarning)

# 音声ファイルのパス
audio_file1 = r"C:\Users\tamur\Onedrive\デスクトップ\dio\dora_hiro.wav"
audio_file2 = r"C:\Users\tamur\Onedrive\デスクトップ\dio\doraemon01.wav"

def comparerhythm(audio_file1, audio_file2):
    # Whisperのモデルをロード
    model = whisper.load_model("turbo")
    
    # 音声ファイルをテキストに変換し、詳細情報を取得
    result1 = model.transcribe(audio_file1, language="ja", word_timestamps=True)
    result2 = model.transcribe(audio_file2, language="ja", word_timestamps=True)
    
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

    score = calculate_score(duration_ratios1, duration_ratios2)
    print(f"リズムスコア: {score:.4f}")

    # 単語と比率を表示
    print("ファイル1の単語比率:")
    for word, ratio in duration_ratios1:
        print(f"単語: {word}, 発話時間比率: {ratio:.4f}")
    
    print("ファイル2の単語比率:")
    for word, ratio in duration_ratios2:
        print(f"単語: {word}, 発話時間比率: {ratio:.4f}")

# 実行
comparerhythm(audio_file1, audio_file2)
