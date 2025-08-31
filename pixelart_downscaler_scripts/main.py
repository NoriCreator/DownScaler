import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
from PIL import Image
from downscaler.downscaler import DotImageDownScaler

def main():
    # メインウィンドウを非表示
    root = tk.Tk()
    root.withdraw()

    # 入力画像選択
    filepath = filedialog.askopenfilename(
        title="ダウンスケールする画像を選択してください",
        filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp")]
    )
    if not filepath:
        messagebox.showinfo("中断", "入力画像が選択されませんでした。")
        return

    # 出力サイズ入力
    new_w = simpledialog.askinteger("出力サイズ", "出力画像の横⇔ピクセル数を入力してください")
    new_h = simpledialog.askinteger("出力サイズ", "出力画像の縦⇕ピクセル数を入力してください")
    if not new_w or not new_h:
        messagebox.showinfo("中断", "サイズ入力がキャンセルされました。")
        return

    # 画像読み込み & ダウンスケール
    img = Image.open(filepath).convert("RGB")
    scaler = DotImageDownScaler(method="mode")
    resized = scaler.downscale(img, (new_h, new_w))

    # 保存先選択
    savepath = filedialog.asksaveasfilename(
        title="保存先を選択してください",
        defaultextension=".png",
        filetypes=[("PNG Image", "*.png")]
    )
    if not savepath:
        messagebox.showinfo("中断", "保存がキャンセルされました。")
        return

    # 保存
    resized.save(savepath)
    messagebox.showinfo("完了", f"保存しました: {savepath}")


if __name__ == "__main__":
    main()
