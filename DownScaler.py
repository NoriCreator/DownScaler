import numpy as np
from PIL import Image
from collections import Counter
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox

def DownScale_Dot_Image(image, down_scale):
    """ドット絵向けダウンスケーラー"""
    src = np.array(image)
    h, w, c = src.shape
    nh, nw = down_scale

    # 拡大の場合はNEARESTでシンプルに拡大
    if nh > h or nw > w:
        return image.resize((nw, nh), resample=Image.NEAREST)

    # 最頻値法
    block_h = h / nh
    block_w = w / nw
    result = np.zeros((nh, nw, c), dtype=np.uint8)

    for i in range(nh):
        for j in range(nw):
            y0, y1 = int(i * block_h), int((i + 1) * block_h)
            x0, x1 = int(j * block_w), int((j + 1) * block_w)
            block = src[y0:y1, x0:x1]

            # RGBまとめて最頻値
            pixels = [tuple(px) for row in block for px in row]
            most_common_color = Counter(pixels).most_common(1)[0][0]

            result[i, j] = most_common_color

    return Image.fromarray(result)

def main():
    root = tk.Tk()
    root.withdraw()

    # 入力ファイル選択
    filepath = filedialog.askopenfilename(
        title="ダウンスケールしたい画像を選んでください",
        filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp")]
    )
    if not filepath:
        return

    # 出力サイズの入力
    new_w = simpledialog.askinteger("入力", "出力画像の横ピクセル数を入力してください")
    new_h = simpledialog.askinteger("入力", "出力画像の縦ピクセル数を入力してください")
    if not new_w or not new_h:
        messagebox.showinfo("中断", "サイズ入力がキャンセルされました")
        return

    # 画像読み込み
    img = Image.open(filepath).convert("RGB")

    # ドット絵向けダウンスケール
    resized = DownScale_Dot_Image(img, (new_h, new_w))

    # 保存先選択
    savepath = filedialog.asksaveasfilename(
        title="保存先を指定してください",
        defaultextension=".png",
        filetypes=[("PNG Image", "*.png")] # JPEGは非可逆圧縮のため、ドット絵が劣化する可能性によりPNG出力
    )
    if not savepath:
        messagebox.showinfo("中断", "保存がキャンセルされました")
        return

    # 保存
    resized.save(savepath)
    messagebox.showinfo("完了", f"保存しました: {savepath}")

if __name__ == "__main__":
    main()
