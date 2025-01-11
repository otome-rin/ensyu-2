import tkinter as tk
from tkinter import messagebox
from tkinter import PhotoImage
import sounddevice as sd
import numpy as np
from record_audio import record_audio
from compare_audio import compare_audio
from compare_audio import rhythm_compare
import matplotlib.pyplot as plt
import soundfile as sf
from PIL import Image, ImageTk
from scipy.io import wavfile
import threading
import pygame
from matplotlib import rcParams
from matplotlib import font_manager

# 録音を保存するファイル名
recorded_file = r"C:\Users\tamur\OneDrive\デスクトップ\dio\recorded_audio.wav"  # 保存したいパスを指定
save_file = r"C:\Users\tamur\OneDrive\デスクトップ\dio\save_plot.png"  # 保存したいパスを指定



# 録音設定
duration = 5  # 録音時間 (秒)
sample_rate = 44100  # サンプリングレート

flag_c = 0
# メインウィンドウを作成
root = tk.Tk()
root.title("声真似録音アプリ")
root.geometry("800x600")

# ステータスメッセージ用ラベル
status_label = tk.Label(root, text="", font=("Arial", 30))
#status_label.place(x = 400,y = 350,anchor = "center")  # 適切な位置に配置

def doraemon_data():
    target_files = []
    target_files.append(r"C:\Users\tamur\OneDrive\デスクトップ\dio\doraemon01.wav")
    target_files.append(r"C:\Users\tamur\OneDrive\デスクトップ\dio\doraemon02.wav")
    target_files.append(r"C:\Users\tamur\OneDrive\デスクトップ\dio\doraemon03.wav")
    target_files.append(r"C:\Users\tamur\OneDrive\デスクトップ\dio\doraemon04.wav")
    target_files.append(r"C:\Users\tamur\OneDrive\デスクトップ\dio\doraemon05.wav")
    pitch_W = 30
    intonation_W = 20
    mfcc_W = 30
    rhythm_W = 10
    speed_W = 10
    Weights = [pitch_W, intonation_W, mfcc_W, rhythm_W, speed_W]
    wave_data = r"C:\Users\tamur\OneDrive\デスクトップ\dio_G\doraemon_wave.png"  # 保存したいパスを指定

    return target_files,Weights,wave_data

def anpanman_data():
    target_files = []
    target_files.append(r"C:\Users\tamur\OneDrive\デスクトップ\dio\anpanman01.wav")
    target_files.append(r"C:\Users\tamur\OneDrive\デスクトップ\dio\anpanman02.wav")
    target_files.append(r"C:\Users\tamur\OneDrive\デスクトップ\dio\anpanman03.wav")
    target_files.append(r"C:\Users\tamur\OneDrive\デスクトップ\dio\anpanman04.wav")
    target_files.append(r"C:\Users\tamur\OneDrive\デスクトップ\dio\anpanman05.wav")
    pitch_W = 30
    intonation_W = 20
    mfcc_W = 30
    rhythm_W = 10
    speed_W = 10
    Weights = [pitch_W, intonation_W, mfcc_W, rhythm_W, speed_W]
    wave_data = r"C:\Users\tamur\OneDrive\デスクトップ\dio_G\anpanman_wave.png"  # 保存したいパスを指定

    return target_files,Weights,wave_data

def sazae_data():
    target_files = []
    target_files.append(r"C:\Users\tamur\OneDrive\デスクトップ\dio\sazae01.wav")
    target_files.append(r"C:\Users\tamur\OneDrive\デスクトップ\dio\sazae02.wav")
    target_files.append(r"C:\Users\tamur\OneDrive\デスクトップ\dio\sazae03.wav")
    target_files.append(r"C:\Users\tamur\OneDrive\デスクトップ\dio\sazae04.wav")
    target_files.append(r"C:\Users\tamur\OneDrive\デスクトップ\dio\sazae05.wav")
    pitch_W = 30
    intonation_W = 20
    mfcc_W = 30
    rhythm_W = 10
    speed_W = 10
    Weights = [pitch_W, intonation_W, mfcc_W, rhythm_W, speed_W]
    wave_data = r"C:\Users\tamur\OneDrive\デスクトップ\dio_G\sazae_wave.png"  # 保存したいパスを指定

    return target_files,Weights,wave_data

target_files, Weights, wave_file = doraemon_data()
file_path = r"C:\Users\tamur\OneDrive\デスクトップ\dio\doraemon01.wav"

def play():    # Pygameの初期化
    pygame.init()
    pygame.mixer.init()

    # 音声ファイルをロード
    pygame.mixer.music.load(file_path)

    # 音声の再生
    pygame.mixer.music.play()

    # 再生が終了するまで待機
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)  # チェック間隔を調整（10msごと）

    # Pygameのリソースを解放
    pygame.mixer.quit()
    pygame.quit()

def update_status(text):
    status_label.config(text=text)
    root.update()  # 即時反映

# タイトル画面を表示する関数
def show_title_screen():
    # ステータスメッセージ用ラベル
    global status_label
    status_label = tk.Label(root, text="", font=("Arial", 30))
    clear_screen()
    label = tk.Label(root, text="声真似採点",font=("HGsoeikakupoptai", 80))
    label.pack(pady=30)
    button1 = tk.Button(root, text="スタート", font=("Arial", 24), width=15,command=show_select_screen)
    button1.pack(pady=20)
    button3 = tk.Button(root, text="アプリを終了", font=("Arial", 24), width=15,command=exit_app)
    button3.pack(pady=20)

def show_select_screen():
    clear_screen()
    label = tk.Label(root, text="キャラクターを選択", font=("HGsoeikakupoptai", 40))
    label.pack(pady=30)
    button4 = tk.Button(root, text="ドラえもん", font=("Arial", 24),width=15, command=set_doraemon)
    button4.pack(pady=20)
    button5 = tk.Button(root, text="アンパンマン", font=("Arial", 24),width=15, command=set_anpanman)
    button5.pack(pady=20)
    button6 = tk.Button(root, text="サザエさん", font=("Arial", 24),width=15, command=set_sazae)
    button6.pack(pady=20)
    button7 = tk.Button(root, text="戻る", font=("Arial", 24),width=15, command=show_title_screen)
    button7.pack(pady=20)

def set_doraemon():
    global target_files, Weights, wave_file,file_path
    target_files, Weights, wave_file = doraemon_data()
    file_path = r"C:\Users\tamur\OneDrive\デスクトップ\dio\doraemon01.wav"
  
    clear_screen()
    label = tk.Label(root, text="ドラえもん", font=("HGsoeikakupoptai", 40))
    label.pack(pady=30)

    button8 = tk.Button(root, text="音声を再生",width=15, font=("Arial", 24), command=play)
    button8.pack(pady=20)
    button9 = tk.Button(root, text="採点を始める",width=15, font=("Arial", 24), command = countdown)
    button9.pack(pady=20)
    button10 = tk.Button(root, text="戻る", font=("Arial", 24),width=15, command=show_select_screen)
    button10.pack(pady=20)

def set_anpanman():
    global target_files, Weights, wave_file, file_path
    target_files, Weights, wave_file = anpanman_data()
    file_path = r"C:\Users\tamur\OneDrive\デスクトップ\dio\anpanman01.wav"


    clear_screen()
    label = tk.Label(root, text="アンパンマン", font=("HGsoeikakupoptai", 40))
    label.pack(pady=30)

    button11 = tk.Button(root, text="音声を再生",width=15, font=("Arial", 24), command=play)
    button11.pack(pady=20)
    button12 = tk.Button(root, text="採点を始める",width=15, font=("Arial", 24), command = countdown)
    button12.pack(pady=20)
    button13 = tk.Button(root, text="戻る", font=("Arial", 24),width=15, command=show_select_screen)
    button13.pack(pady=20)

def set_sazae():
    global target_files, Weights, wave_file, file_path
    target_files, Weights, wave_file = sazae_data()
    file_path = r"C:\Users\tamur\OneDrive\デスクトップ\dio\sazae01.wav"


    clear_screen()
    label = tk.Label(root, text="サザエさん", font=("HGsoeikakupoptai", 40))
    label.pack(pady=30)

    button11 = tk.Button(root, text="音声を再生",width=15, font=("Arial", 24), command=play)
    button11.pack(pady=20)
    button12 = tk.Button(root, text="採点を始める",width=15, font=("Arial", 24), command = countdown)
    button12.pack(pady=20)
    button13 = tk.Button(root, text="戻る", font=("Arial", 24),width=15, command=show_select_screen)
    button13.pack(pady=20)

def countdown(count=3):
    clear_screen()
    status_label.pack(pady=20)
    if count > 0:
        update_status(f"{count}")
        root.after(1000, countdown, count - 1)  # 1秒後に数字を減らして再度呼び出し
    else:
        #update_status("録音中…")
        start_in_thread()

def start_in_thread():
    clear_screen()
    def display_image():
        image = Image.open(wave_file)
        image = image.resize((600, 240))
        photo = ImageTk.PhotoImage(image)
        label = tk.Label(root, image=photo)
        label.photo = photo  # 参照を保持
        label.pack(pady=20)

    threading.Thread(target=display_image).start()
    root.after(0, start_record)

def start_record():
    clear_screen()
    def recording_process():
        update_status("録音中…")
        record_audio(recorded_file)
        root.after(0, post_recording)  # 録音後にメインスレッドで後続処理を実行

    threading.Thread(target=recording_process).start()

def post_recording():
    update_status("録音完了！採点中...")
    scores, plot_labels, plot_range,sum_score = compare(target_files, Weights)
    update_status("採点終了！")
    plot_radar_chart(scores, plot_labels,plot_range, save_file)
    root.after(500, result(scores,sum_score))

def compare(target_files, Weights):
    pitch_scores = []
    intonation_scores = []
    voice_quality_scores = []
    speed_scores = []
    for target_file in target_files: 
        p,i,v,sp,sc =compare_audio(target_file, recorded_file,Weights)
        pitch_scores.append(p)
        intonation_scores.append(i)
        voice_quality_scores.append(v)
        speed_scores.append(sp)

    pitch_max = max(pitch_scores)
    intonation_max = max(intonation_scores)
    voice_quality_max = max(voice_quality_scores)
    speed_max = max(speed_scores)
    rhythm_score = rhythm_compare(target_files[0],recorded_file)
    Score = pitch_max + intonation_max + voice_quality_max + rhythm_score + speed_max
    '''
    print(f"Pitch Score: {round(pitch_max,3)} / {Weights[0]}")
    print(f"Volume Score: {round(intonation_max,3)} / {Weights[1]}")
    print(f"Voice Characteristic Score: {voice_quality_max:.3f} / {Weights[2]}")
    print(f"Rhythm Score: {round(rhythm_max,3)} / {Weights[3]}")
    print(f"Speed Score: {round(speed_max,3)} / {Weights[4]}")
    print(f"Score: {round(Score,3)} / 100")
    '''

    # レーダーチャートを描画
    plot_labels = ["高さ", "音量", "声質", "リズム", "スピード"]
    scores = [
        pitch_max,
        intonation_max,
        voice_quality_max,
        rhythm_score,
        speed_max
    ]
    plot_range = [
        (0,Weights[0]),
        (0,Weights[1]),
        (0,Weights[2]),
        (0,Weights[3]),
        (0,Weights[4])
    ]
    return scores, plot_labels,plot_range,Score

def set_japanese_font():
    # 適切な日本語フォントを指定（例: Noto Sans JP）
    font_path = "C:/Windows/Fonts/meiryo.ttc" # 環境に応じて変更
    font = font_manager.FontProperties(fname=font_path)
    rcParams["font.family"] = font.get_name()


def plot_radar_chart(scores, labels, ranges, savefile):
    # スコアを正規化（0から1の範囲にスケーリング）
    set_japanese_font()
    normalized_scores = [
        (score - min_val) / (max_val - min_val)
        for score, (min_val, max_val) in zip(scores, ranges)
    ]
    normalized_scores.append(normalized_scores[0])  # データを閉じるために最初の値を追加

    # プロットする角度を生成
    angles = np.linspace(0, 2 * np.pi, len(labels) + 1, endpoint=True)

    # プロット設定
    fig = plt.figure(facecolor="w", figsize=(6, 6))
    ax = fig.add_subplot(1, 1, 1, polar=True)

    # レーダーチャートの線と塗りつぶし
    ax.plot(angles, normalized_scores, color="blue", linewidth=2)
    ax.fill(angles, normalized_scores, color="lightblue", alpha=0.2)

    # 項目ラベルの表示
    ax.set_thetagrids(angles[:-1] * 180 / np.pi, labels)

    # 始点を上(北)に変更し、時計回りに設定
    ax.set_theta_zero_location("N")
    ax.set_theta_direction(-1)

    # 円形目盛り線を消去
    ax.grid(False)  # グリッド全体を消去

    # 多角形の目盛線を描画
    for level in np.linspace(0, 1, 5):
        ax.plot(angles, [level] * len(angles), color="gray", linewidth=0.5)

    # 各項目ごとのメモリ値を描画
    for i, (min_val, max_val) in enumerate(ranges):
        # 5段階のメモリを生成
        grid_values = np.linspace(min_val, max_val, 5)
        grid_norm = (grid_values - min_val) / (max_val - min_val)  # 正規化
        for value, norm in zip(grid_values, grid_norm):
            ax.text(
                x=angles[i],
                y=norm,
                s=f"{value:.0f}",
                fontsize=8,
                color="gray",
                ha="center",
                va="bottom",
            )
        # 放射線を描画
        ax.plot([angles[i], angles[i]], [0, 1], color="gray", linewidth=0.5)

    # rの範囲を固定
    ax.set_rlim([0, 1])

    ax.set_yticklabels([])

    # 一番外側の円を消去
    ax.spines["polar"].set_visible(False)

    # 保存して閉じる
    plt.tight_layout()
    plt.savefig(savefile, dpi=300)
    plt.close()

def result(scores,sum_score):
    clear_screen()
    status_label.destroy()
    sum_score_r = round(sum_score, 3)
    score_r = [round(i, 3) for i in scores]
# 左側のフレーム (点数を表示)
    left_frame = tk.Frame(root)
    left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # 右側のフレーム (画像を表示)
    right_frame = tk.Frame(root)
    right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    # スコアを左側に表示
    total_score_label = tk.Label(
        left_frame,
        text=f"{sum_score_r} / 100",
        font=("HGsoeikakupoptai", 40),  # 大きなフォントサイズ
    )
    total_score_label.pack(pady=30)

    # 他のスコアを表示
    other_scores_label = tk.Label(
        left_frame,
        text=f"高さ: {score_r[0]}\n\n"
             f"音量: {score_r[1]}\n\n"
             f"声質: {score_r[2]}\n\n"
             f"リズム: {score_r[3]}\n\n"
             f"スピード {score_r[4]}",
        font=("HGsoeikakupoptai", 20),  # 小さめのフォントサイズ
        justify=tk.LEFT,
    )
    other_scores_label.pack(pady=20, anchor="w")

    # 画像を右側に表示
    def display_radar():
        image = Image.open(save_file)
        image = image.resize((400, 400))  # サイズ調整
        photo = ImageTk.PhotoImage(image)
        radar_label = tk.Label(right_frame, image=photo)
        radar_label.photo = photo  # 参照を保持
        radar_label.pack(pady=30)

        next_button = tk.Button(
                right_frame,
                text="タイトル画面へ",
                font=("Arial", 16),
                command=show_title_screen
            )
        next_button.pack(pady=10)
    threading.Thread(target=display_radar).start()

# アプリケーションを終了する関数
def exit_app():
    root.destroy()

# 現在の画面をクリアする関数
def clear_screen():
    for widget in root.winfo_children():
        if widget != status_label:  # ステータスラベルは削除しない
            widget.destroy()

# 初期画面をタイトル画面に設定
show_title_screen()

# アプリケーションのメインループ
root.mainloop()
