import tkinter as tk
from tkinter import messagebox

# タイトル画面を表示する関数
def show_title_screen():
    # 既存のウィジェットを削除
    clear_screen()

    # タイトル画面のウィジェットを作成
    label = tk.Label(root, text="タイトル画面", font=("Arial", 24))
    label.pack(pady=20)

    button1 = tk.Button(root, text="次の画面へ", font=("Arial", 14), command=show_next_screen)
    button1.pack(pady=10)

    button2 = tk.Button(root, text="メッセージを表示", font=("Arial", 14), command=show_message)
    button2.pack(pady=10)

    button3 = tk.Button(root, text="アプリを終了", font=("Arial", 14), command=exit_app)
    button3.pack(pady=10)

# 次の画面を表示する関数
def show_next_screen():
    # 既存のウィジェットを削除
    clear_screen()

    # 次の画面のウィジェットを作成
    label = tk.Label(root, text="次の画面へようこそ！", font=("Arial", 24))
    label.pack(pady=20)

    button = tk.Button(root, text="戻る", font=("Arial", 14), command=show_title_screen)
    button.pack(pady=10)

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
root.title("画面遷移のサンプル")
root.geometry("400x300")

# 初期画面をタイトル画面に設定
show_title_screen()

# アプリケーションのメインループ
root.mainloop()
