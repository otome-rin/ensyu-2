import tkinter as tk
from tkinter import messagebox
import sounddevice as sd
import numpy as np
import wave
from record_audio import record_audio
from compare_doraemon import compare_doraemon, doraemon_data


# 録音を保存するファイル名
recorded_file = r"C:\Users\rinri\OneDrive - NITech\デスクトップ\メディア系演習Ⅱ\録音データ\recorded_audio.mp3"  # 保存したいパスを指定


# 録音設定
duration = 5  # 録音時間 (秒)
sample_rate = 44100  # サンプリングレート

def doraemon_D():
    target_files,Weights = doraemon_data()
    return target_files,Weights

def compare(target_files, Weights):
    pitch_scores = []
    intonation_scores = []
    voice_quality_scores = []
    rhythm_scores = []
    speed_scores = []
    for target_file in target_files: 
        p,i,v,r,sp,sc =compare_doraemon(target_file, recorded_file,Weights)
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

    print(f"Pitch Score: {round(pitch_ave,3)} / {Weights[0]}")
    print(f"Intonation Score: {round(intonation_ave,3)} / {Weights[1]}")
    print(f"Voice Quality Score: {voice_quality_ave:.3f} / {Weights[2]}")
    print(f"Rhythm Score: {round(rhythm_ave,3)} / {Weights[3]}")
    print(f"Speed Score: {round(speed_ave,3)} / {Weights[4]}")
    print(f"Score: {round(Score,3)} / 100")

# 録音を開始する関数
def start_doraemon():
    record_audio(recorded_file)
    target_files, Weights = doraemon_D()
    compare(target_files,Weights)


def start_sazaesan():
    record_audio(recorded_file)


# 音声データを保存する関数
def save_audio(audio_data):
    with wave.open(recorded_file, 'wb') as wf:
        wf.setnchannels(2)  # ステレオ
        wf.setsampwidth(2)  # 16ビット
        wf.setframerate(sample_rate)
        wf.writeframes(audio_data.tobytes())

# タイトル画面を表示する関数
def show_title_screen():
    clear_screen()
    label = tk.Label(root, text="タイトル画面", font=("Arial", 24))
    label.pack(pady=20)
    button1 = tk.Button(root, text="声真似を採点", font=("Arial", 14), command=show_next_screen)
    button1.pack(pady=10)
    button2 = tk.Button(root, text="使い方", font=("Arial", 14), command=show_message)
    button2.pack(pady=10)
    button3 = tk.Button(root, text="アプリを終了", font=("Arial", 14), command=exit_app)
    button3.pack(pady=10)

# 次の画面を表示する関数
def show_next_screen():
    clear_screen()
    label = tk.Label(root, text="キャラクターを選択", font=("Arial", 24))
    label.pack(pady=20)
    button4 = tk.Button(root, text="ドラえもん", font=("Arial", 14), command=start_doraemon)
    button4.pack(pady=10)
    button5 = tk.Button(root, text="サザエさん", font=("Arial", 14), command=start_sazaesan)
    button5.pack(pady=10)
    button6 = tk.Button(root, text="戻る", font=("Arial", 14), command=show_title_screen)
    button6.pack(pady=10)

# メッセージを表示する関数
def show_message():
    messagebox.showinfo("メッセージ", "こんにちは！これはタイトル画面のメッセージです。")

# アプリケーションを終了する関数
def exit_app():
    root.destroy()

# 現在の画面をクリアする関数
def clear_screen():
    for widget in root.winfo_children():
        widget.destroy()

# メインウィンドウを作成
root = tk.Tk()
root.title("声真似録音アプリ")
root.geometry("400x300")

# 初期画面をタイトル画面に設定
show_title_screen()

# アプリケーションのメインループ
root.mainloop()
