# main.py
from record_audio import record_audio
from compare_doraemon import compare_doraemon

# 音声を録音して保存
recorded_file = "recorded_audio.mp3"
record_audio(recorded_file, duration=2)

# 他の音声ファイルと比較
other_file = 'doraemon.mp3'  # 比較したい別の音声ファイル
compare_doraemon(recorded_file, other_file)