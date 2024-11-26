import tkinter as tk
from tkinter import messagebox
import sounddevice as sd
import numpy as np
import wave

# 録音を保存するファイル名
recording_file = "recording.wav"

# 録音設定
duration = 5  # 録音時間 (秒)
sample_rate = 44100  # サンプリングレート

# 録音を開始する関数
def start_recording():
    # 録音中のメッセージを表示
    messagebox.showinfo("録音中", "録音を開始します。5秒間お待ちください...")
    
    try:
        # 音声を録音
        audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=2, dtype='int16')
        sd.wait()  # 録音が終了するまで待つ

        # 録音データを保存
        save_audio(audio_data)
        messagebox.showinfo("録音完了", f"録音が完了しました！\nファイル: {recording_file}")
    except Exception as e:
        messagebox.showerror("エラー", f"録音中にエラーが発生しました: {e}")

# 音声データを保存する関数
def save_audio(audio_data):
    with wave.open(recording_file, 'wb') as wf:
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
    button4 = tk.Button(root, text="ドラえもん", font=("Arial", 14), command=start_recording)
    button4.pack(pady=10)
    button5 = tk.Button(root, text="サザエさん", font=("Arial", 14), command=start_recording)
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
