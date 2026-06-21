import os
import math
import random
from PIL import Image, ImageDraw, ImageFilter

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_DIR = os.path.join(BASE_DIR, "images", "covers")
OUTPUT_DIR = os.path.join(BASE_DIR, "images", "puzzle")

# 配置：每张图切几块
PUZZLE_CONFIG = {
    "mudan.jpg": 3,
    "fenghuang.jpg": 4,
    "long.jpg": 5,
}

IMG_SIZE = 400       # 原图尺寸
TAB_SIZE = 30        # 拼图齿大小（凸起/凹陷的尺寸）
TAB_COUNT = 3        # 每条分割线上有几个拼图齿


def generate_split_line(x_base, img_h, tab_size, tab_count, seed=None):
    """
    生成一条垂直分割线的 y->x 偏移。
    返回一个列表，每个元素是对应 y 坐标的 x 偏移量。
    """
    if seed is not None:
        random.seed(seed)

    # 每个拼图齿的位置和方向（凸=1，凹=-1）
    tab_positions = []
    spacing = img_h / (tab_count + 1)
    for i in range(tab_count):
        y_center = spacing * (i + 1) + random.uniform(-spacing * 0.2, spacing * 0.2)
        direction = random.choice([-1, 1])  # -1=凹, 1=凸
        tab_positions.append((y_center, direction))

    # 为每个 y 计算 x 偏移
    offsets = []
    for y in range(img_h):
        offset = 0
        for y_center, direction in tab_positions:
            # 每个齿的影响范围（半高）
            half_h = tab_size * 1.2
            dy = y - y_center
            if abs(dy) < half_h:
                # 用余弦曲线做平滑的凸起/凹陷
                t = (dy / half_h) * math.pi
                offset += direction * tab_size * 0.5 * (1 + math.cos(t)) * (-1)
        offsets.append(x_base + offset)

    return offsets, tab_positions


def create_puzzle_pieces(img_path, num_pieces, output_prefix):
    """
    把一张图切成 num_pieces 块不规则拼图，保存为 PNG。
    """
    img = Image.open(img_path).convert("RGBA")
    w, h = img.size

    # 生成分割线
    piece_w = w / num_pieces
    lines = []
    tab_info = []

    for i in range(num_pieces - 1):
        x_base = piece_w * (i + 1)
        # 用确定性种子，保证同一张图的切割结果一致
        seed = hash(output_prefix + str(i)) & 0x7FFFFFFF
        offsets, tabs = generate_split_line(x_base, h, TAB_SIZE, TAB_COUNT, seed)
        lines.append(offsets)
        tab_info.append(tabs)

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # 切割每一块
    for piece_idx in range(num_pieces):
        # 创建 mask
        mask = Image.new("L", (w, h), 0)
        draw = ImageDraw.Draw(mask)

        # 构建多边形路径
        points = []

        # 左边缘
        if piece_idx == 0:
            left_xs = [0] * h
        else:
            left_xs = lines[piece_idx - 1]

        # 右边缘
        if piece_idx == num_pieces - 1:
            right_xs = [w - 1] * h
        else:
            right_xs = lines[piece_idx]

        # 上边缘：从左到右
        # 找到左右两边 y=0 时的 x
        points.append((left_xs[0], 0))
        points.append((right_xs[0], 0))

        # 右边缘：从上到下
        for y in range(1, h):
            points.append((right_xs[y], y))

        # 下边缘：从右到左
        points.append((right_xs[h - 1], h - 1))
        points.append((left_xs[h - 1], h - 1))

        # 左边缘：从下到上
        for y in range(h - 2, -1, -1):
            points.append((left_xs[y], y))

        # 填充 mask
        draw.polygon(points, fill=255)

        # 轻微模糊边缘，让拼接更自然
        mask = mask.filter(ImageFilter.SMOOTH)

        # 应用 mask
        piece = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        piece.paste(img, (0, 0), mask)

        # 裁剪到实际内容区域（减小文件体积）
        bbox = piece.getbbox()
        if bbox:
            piece = piece.crop(bbox)

        # 保存
        out_path = os.path.join(OUTPUT_DIR, f"{output_prefix}-{piece_idx + 1}.png")
        piece.save(out_path, "PNG", optimize=True)

        size_kb = os.path.getsize(out_path) / 1024
        print(f"  {output_prefix}-{piece_idx + 1}.png: {piece.size[0]}x{piece.size[1]}, {size_kb:.1f}KB")

    # 保存一张完整的小预览图
    preview = img.copy()
    preview.thumbnail((200, 200))
    preview_path = os.path.join(OUTPUT_DIR, f"{output_prefix}-preview.jpg")
    preview.convert("RGB").save(preview_path, "JPEG", quality=80)
    print(f"  {output_prefix}-preview.jpg: 预览图")


def main():
    print("开始切割拼图素材...\n")

    for filename, num_pieces in PUZZLE_CONFIG.items():
        input_path = os.path.join(INPUT_DIR, filename)
        if not os.path.exists(input_path):
            print(f"跳过 {filename}：文件不存在")
            continue

        prefix = filename.replace(".jpg", "")
        print(f"【{prefix}】切成 {num_pieces} 块：")
        create_puzzle_pieces(input_path, num_pieces, prefix)
        print()

    print("完成！输出目录:", OUTPUT_DIR)


if __name__ == "__main__":
    main()
