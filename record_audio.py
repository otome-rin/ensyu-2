import sounddevice as sd
from scipy.io.wavfile import write
import pyaudio
import numpy as np
import time
from scipy.signal import lfilter
import wave

# 設定
FORMAT = pyaudio.paInt16  # 音声フォーマット
CHANNELS = 1             # モノラル
RATE = 44100             # サンプルレート
CHUNK = 1024             # フレームサイズ
THRESHOLD = 1000         # 音声の検出閾値
RECORD_SECONDS = 10      # 最大録音時間
SILENCE_DURATION = 0.5

def is_above_threshold(data, threshold):
    """データが閾値を超えているか判定"""
    return np.max(np.abs(data)) > threshold

def record_audio(output_path):
    """音声を検出して録音を開始"""
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
    print("音声を待機中...")

    frames = []
    recording = False
    frames = []
    silent_chunks = 0  # 無音フレームの数
    max_silent_chunks = int(SILENCE_DURATION * RATE / CHUNK)

    for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        # 音声データを取得
        data = stream.read(CHUNK, exception_on_overflow=False)
        np_data = np.frombuffer(data, dtype=np.int16)

        if not recording and is_above_threshold(np_data, THRESHOLD):
            print("音声を検出、録音を開始...")
            recording = True

        if recording:
            frames.append(data)

                    # 無音判定
        if recording and is_above_threshold(np_data, THRESHOLD):
            silent_chunks = 0
        else:
            silent_chunks += 1

        # 無音が指定時間続いたら停止
        if recording and silent_chunks > max_silent_chunks:
            print("無音を検出しました。録音終了。")
            break


    # 録音終了
    stream.stop_stream()
    stream.close()
    audio.terminate()

    if frames:
        # ファイルに保存
        with wave.open(output_path, 'wb') as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(audio.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))
        print(f"録音を {output_path} に保存しました。")
    else:
        print("音声が検出されませんでした。")


'''
def record_audio(filename, duration = 5, sample_rate = 44100):
    # 録音開始
    countdown_seconds = 3
    for i in range(countdown_seconds, 0, -1):
        print(i)
        time.sleep(1)

    print("Recording...")
    audio_data = sd.rec(int(sample_rate * duration), samplerate=sample_rate, channels=2)
    sd.wait()  # 録音が終了するまで待機
    print("Recording finished")

    # 音声データをWAVファイルとして保存
    write(filename, sample_rate, audio_data)
    print(f"Recording finished and saved as {filename}")
    '''

    # 録音した音声を再生
    #print("Playing the recorded audio...")
    #sd.play(audio_data, samplerate=sample_rate)
    #sd.wait()  # 再生が終了するまで待機
    #print("Playback finished")