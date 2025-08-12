from PIL import Image

def crop_and_resize_image(input_path: str, output_path: str, size: int = 60) -> None:
    img = Image.open(input_path)

    # 居中裁剪为正方形
    width, height = img.size
    side = min(width, height)
    left = (width - side) // 2
    top = (height - side) // 2
    right = left + side
    bottom = top + side
    img_cropped = img.crop((left, top, right, bottom))

    # 缩放为指定大小
    img_resized = img_cropped.resize((size, size), Image.LANCZOS)

    # 保存结果
    img_resized.save(output_path)
    print(f"处理完成，保存为：{output_path}")

crop_and_resize_image("data/icon.png", "data/icon_cropped.png", size=60)
