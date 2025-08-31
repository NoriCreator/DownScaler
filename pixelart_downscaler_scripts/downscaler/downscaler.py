import numpy as np
from PIL import Image
from collections import Counter
from downscaler.block_utils import split_into_blocks

class DotImageDownScaler:
    """ドット絵向けの高精度ダウンスケーラー"""

    def __init__(self, method: str = "mode"):
        """
        Args:
            method (str): ダウンスケール方式 ("mode": 最頻値)
        """
        self.method = method

    def downscale(self, image: Image.Image, new_size: tuple[int, int]) -> Image.Image:
        """ドット絵向けダウンスケール"""
        src = np.array(image.convert("RGB"))
        h, w, c = src.shape
        nh, nw = new_size

        # 拡大はNEARESTで対応
        if nh > h or nw > w:
            return image.resize((nw, nh), resample=Image.NEAREST)

        result = np.zeros((nh, nw, c), dtype=np.uint8)

        for i, j, block in split_into_blocks(src, nh, nw):
            if self.method == "mode":
                pixels = [tuple(px) for row in block for px in row]
                most_common_color = Counter(pixels).most_common(1)[0][0]
                result[i, j] = most_common_color
            else:
                raise NotImplementedError(f"Unknown method: {self.method}")

        return Image.fromarray(result)
