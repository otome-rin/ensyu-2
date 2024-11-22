# main.py
from record_audio import record_audio
from compare_doraemon import compare_doraemon
from pydub.utils import mediainfo

#比較元の音声ファイル
target_file = 'doraemon.mp3'
# mediainfoで情報を取得
info = mediainfo(target_file)
duration = float(info['duration'])  # 秒数を取得
# 音声を録音して保存
recorded_file = "recorded_audio.mp3"
record_audio(recorded_file, duration + 2)

#比較、結果の出力
compare_doraemon(target_file, recorded_file)