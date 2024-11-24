# main.py
from record_audio import record_audio
from compare_doraemon import compare_doraemon, weight_doraemon
from mutagen.mp3 import MP3
#比較元の音声ファイル
target_files = []
target_files.append(r"C:\Users\rinri\OneDrive - NITech\デスクトップ\メディア系演習Ⅱ\doraemon01.mp3")
target_files.append(r"C:\Users\rinri\OneDrive - NITech\デスクトップ\メディア系演習Ⅱ\doraemon02.mp3")
target_files.append(r"C:\Users\rinri\OneDrive - NITech\デスクトップ\メディア系演習Ⅱ\doraemon03.mp3")
target_files.append(r"C:\Users\rinri\OneDrive - NITech\デスクトップ\メディア系演習Ⅱ\doraemon04.mp3")
target_files.append(r"C:\Users\rinri\OneDrive - NITech\デスクトップ\メディア系演習Ⅱ\doraemon05.mp3")


recorded_file = r"C:\Users\rinri\OneDrive - NITech\デスクトップ\メディア系演習Ⅱ\recorded_audio.mp3"  # 保存したいパスを指定
record_audio(recorded_file)

#比較、結果の出力
pitch_scores = []
intonation_scores = []
voice_quality_scores = []
rhythm_scores = []
speed_scores = []
pitch_W, intonation_W, mfcc_W, rhythm_W, speed_W = weight_doraemon()

for target_file in target_files: 
    p,i,v,r,sp,sc =compare_doraemon(target_file, recorded_file)
    pitch_scores.append(p)
    intonation_scores.append(i)
    voice_quality_scores.append(v)
    rhythm_scores.append(r)
    speed_scores.append(sp)

pitch_ave = sum(pitch_scores)/len(pitch_scores)
intonation_ave = sum(intonation_scores)/len(intonation_scores)
voice_quality_ave = sum(voice_quality_scores)/len(voice_quality_scores)
rhythm_ave = sum(rhythm_scores)/len(rhythm_scores)
speed_ave = sum(speed_scores)/len(speed_scores)
Score = pitch_ave + intonation_ave + voice_quality_ave + rhythm_ave + speed_ave

print(f"Pitch Score: {round(pitch_ave,3)} / {pitch_W}")
print(f"Intonation Score: {round(intonation_ave,3)} / {intonation_W}")
print(f"Voice Quality Score: {voice_quality_ave:.3f} / {mfcc_W}")
print(f"Rhythm Score: {round(rhythm_ave,3)} / {rhythm_W}")
print(f"Speed Score: {round(speed_ave,3)} / {speed_W}")
print(f"Score: {round(Score,3)} / 100")