"""
app_icon.py

功能: 制作程序图标
时间: 2025/12/04
版本: 1.0
"""

from PIL import Image


def make_square(
    im: Image.Image,
    min_size: int = 256,
    fill_color: tuple[int, int, int, int] = (255, 255, 255, 0)
) -> Image.Image:
    """将图片调整为方形"""
    x, y = im.size
    size = max(min_size, x, y)
    new_im = Image.new("RGBA", (size, size), fill_color)
    new_im.paste(im, ((size - x) // 2, (size - y) // 2))
    return new_im


if __name__ == "__main__":
    img = Image.open("data/icon_cropped.png").convert("RGBA")
    img = make_square(img)
    img.save(
        im="data/app_icon.ico",
        format="ICO",
        sizes=[(256, 256), (128, 128), (64, 64), (32, 32), (16, 16)]
    )
