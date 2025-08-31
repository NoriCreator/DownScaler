import numpy as np

def split_into_blocks(src: np.ndarray, nh: int, nw: int):
    """
    入力画像を nh x nw のブロックに分割するジェネレータ
    """
    h, w, _ = src.shape
    block_h = h / nh
    block_w = w / nw

    for i in range(nh):
        for j in range(nw):
            y0, y1 = int(i * block_h), int((i + 1) * block_h)
            x0, x1 = int(j * block_w), int((j + 1) * block_w)
            block = src[y0:y1, x0:x1]
            yield i, j, block
