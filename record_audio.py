import sounddevice as sd
from scipy.io.wavfile import write

def record_audio(filename, duration = 5, sample_rate = 44100):
    # 録音開始
    print("Recording...")
    audio_data = sd.rec(int(sample_rate * duration), samplerate=sample_rate, channels=2)
    sd.wait()  # 録音が終了するまで待機
    print("Recording finished")

    # 音声データをWAVファイルとして保存
    write(filename, sample_rate, audio_data)
    print(f"Recording finished and saved as {filename}")

    # 録音した音声を再生
    #print("Playing the recorded audio...")
    #sd.play(audio_data, samplerate=sample_rate)
    #sd.wait()  # 再生が終了するまで待機
    #print("Playback finished")