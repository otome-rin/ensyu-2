import sounddevice as sd
from scipy.io.wavfile import write

# 設定
sample_rate = 44100  # サンプリングレート（Hz）
duration = 5  # 録音時間（秒）

# 録音開始
print("Recording...")
audio_data = sd.rec(int(sample_rate * duration), samplerate=sample_rate, channels=2)
sd.wait()  # 録音が終了するまで待機
print("Recording finished")

# 音声データをWAVファイルとして保存
write("output.wav", sample_rate, audio_data)
print("Audio saved as output.wav")

# 録音した音声を再生
print("Playing the recorded audio...")
sd.play(audio_data, samplerate=sample_rate)
sd.wait()  # 再生が終了するまで待機
print("Playback finished")