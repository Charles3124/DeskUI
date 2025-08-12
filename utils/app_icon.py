from PIL import Image

def make_square(im: Image.Image, min_size: int = 256, fill_color: tuple[int, int, int, int] = (255,255,255,0)) -> Image.Image:
    x, y = im.size
    size = max(min_size, x, y)
    new_im = Image.new('RGBA', (size, size), fill_color)
    new_im.paste(im, ((size - x) // 2, (size - y) // 2))
    return new_im

img = Image.open('data/icon_cropped.png').convert('RGBA')
img = make_square(img, 256)
img.save('data/app_icon.ico', format='ICO', sizes=[(256,256), (128,128), (64,64), (32,32), (16,16)])
