import os
from PIL import Image, ImageDraw

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_DIR = os.path.join(BASE_DIR, "images", "covers")
OUTPUT_DIR = os.path.join(BASE_DIR, "images", "puzzle")

BOARD_SIZE = 180  # 拼图板尺寸
THUMB_HEIGHT = 60  # 缩略图高度

def cut_mudan(img):
    """牡丹：3块横向切割（左、中、右），mask方式输出180×180透明背景"""
    w, h = img.size
    pieces = []
    
    mask1 = Image.new("L", (w, h), 0)
    draw1 = ImageDraw.Draw(mask1)
    draw1.rectangle([(0, 0), (int(w * 0.333), h)], fill=255)
    piece1 = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    piece1.paste(img, (0, 0), mask1)
    pieces.append(piece1)
    
    mask2 = Image.new("L", (w, h), 0)
    draw2 = ImageDraw.Draw(mask2)
    draw2.rectangle([(int(w * 0.333), 0), (int(w * 0.667), h)], fill=255)
    piece2 = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    piece2.paste(img, (0, 0), mask2)
    pieces.append(piece2)
    
    mask3 = Image.new("L", (w, h), 0)
    draw3 = ImageDraw.Draw(mask3)
    draw3.rectangle([(int(w * 0.667), 0), (w, h)], fill=255)
    piece3 = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    piece3.paste(img, (0, 0), mask3)
    pieces.append(piece3)
    
    return pieces

def cut_fenghuang(img):
    """凤凰：两条对角线切成4个三角形"""
    w, h = img.size
    pieces = []
    cx, cy = w / 2, h / 2
    
    mask1 = Image.new("L", (w, h), 0)
    draw1 = ImageDraw.Draw(mask1)
    draw1.polygon([(0, 0), (cx, cy), (0, h)], fill=255)
    piece1 = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    piece1.paste(img, (0, 0), mask1)
    pieces.append(piece1)
    
    mask2 = Image.new("L", (w, h), 0)
    draw2 = ImageDraw.Draw(mask2)
    draw2.polygon([(w, 0), (cx, cy), (0, 0)], fill=255)
    piece2 = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    piece2.paste(img, (0, 0), mask2)
    pieces.append(piece2)
    
    mask3 = Image.new("L", (w, h), 0)
    draw3 = ImageDraw.Draw(mask3)
    draw3.polygon([(w, h), (cx, cy), (w, 0)], fill=255)
    piece3 = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    piece3.paste(img, (0, 0), mask3)
    pieces.append(piece3)
    
    mask4 = Image.new("L", (w, h), 0)
    draw4 = ImageDraw.Draw(mask4)
    draw4.polygon([(0, h), (cx, cy), (w, h)], fill=255)
    piece4 = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    piece4.paste(img, (0, 0), mask4)
    pieces.append(piece4)
    
    return pieces

def cut_long(img):
    """神龙：赵爽弦图 5块（连接四边中点）"""
    w, h = img.size
    pieces = []
    cx, cy = w // 2, h // 2
    
    mask1 = Image.new("L", (w, h), 0)
    draw1 = ImageDraw.Draw(mask1)
    draw1.polygon([(cx, 0), (w, 0), (w, cy)], fill=255)
    piece1 = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    piece1.paste(img, (0, 0), mask1)
    pieces.append(piece1)
    
    mask2 = Image.new("L", (w, h), 0)
    draw2 = ImageDraw.Draw(mask2)
    draw2.polygon([(0, 0), (cx, 0), (0, cy)], fill=255)
    piece2 = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    piece2.paste(img, (0, 0), mask2)
    pieces.append(piece2)
    
    mask3 = Image.new("L", (w, h), 0)
    draw3 = ImageDraw.Draw(mask3)
    draw3.polygon([(0, cy), (0, h), (cx, h)], fill=255)
    piece3 = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    piece3.paste(img, (0, 0), mask3)
    pieces.append(piece3)
    
    mask4 = Image.new("L", (w, h), 0)
    draw4 = ImageDraw.Draw(mask4)
    draw4.polygon([(cx, h), (w, h), (w, cy)], fill=255)
    piece4 = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    piece4.paste(img, (0, 0), mask4)
    pieces.append(piece4)
    
    mask5 = Image.new("L", (w, h), 0)
    draw5 = ImageDraw.Draw(mask5)
    draw5.polygon([(cx, 0), (w, cy), (cx, h), (0, cy)], fill=255)
    piece5 = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    piece5.paste(img, (0, 0), mask5)
    pieces.append(piece5)
    
    return pieces

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # 牡丹
    img_path = os.path.join(INPUT_DIR, "mudan.jpg")
    if os.path.exists(img_path):
        img = Image.open(img_path).convert("RGBA")
        img = img.resize((BOARD_SIZE, BOARD_SIZE), Image.LANCZOS)
        img.convert("RGB").save(os.path.join(OUTPUT_DIR, "mudan-full.jpg"), "JPEG", quality=90)
        print(f"mudan-full.jpg: {img.size[0]}x{img.size[1]}")
        pieces = cut_mudan(img)
        for i, piece in enumerate(pieces):
            out_path = os.path.join(OUTPUT_DIR, f"mudan-{i+1}.png")
            piece.save(out_path, "PNG", optimize=True)
            print(f"mudan-{i+1}.png: {piece.size[0]}x{piece.size[1]}")
            
            thumb = piece.copy()
            thumb_ratio = THUMB_HEIGHT / thumb.size[1]
            thumb = thumb.resize((int(thumb.size[0] * thumb_ratio), THUMB_HEIGHT), Image.LANCZOS)
            thumb_path = os.path.join(OUTPUT_DIR, f"mudan-{i+1}-s.png")
            thumb.save(thumb_path, "PNG", optimize=True)
            print(f"mudan-{i+1}-s.png: {thumb.size[0]}x{thumb.size[1]}")
        
        preview = img.copy()
        preview.thumbnail((80, 80))
        preview.convert("RGB").save(os.path.join(OUTPUT_DIR, "mudan-preview.jpg"), "JPEG", quality=85)
    
    # 凤凰
    img_path = os.path.join(INPUT_DIR, "fenghuang.jpg")
    if os.path.exists(img_path):
        img = Image.open(img_path).convert("RGBA")
        img = img.resize((BOARD_SIZE, BOARD_SIZE), Image.LANCZOS)
        pieces = cut_fenghuang(img)
        for i, piece in enumerate(pieces):
            out_path = os.path.join(OUTPUT_DIR, f"fenghuang-{i+1}.png")
            piece.save(out_path, "PNG", optimize=True)
            print(f"fenghuang-{i+1}.png: {piece.size[0]}x{piece.size[1]}")
            
            thumb = piece.copy()
            thumb_ratio = THUMB_HEIGHT / thumb.size[1]
            thumb = thumb.resize((int(thumb.size[0] * thumb_ratio), THUMB_HEIGHT), Image.LANCZOS)
            thumb_path = os.path.join(OUTPUT_DIR, f"fenghuang-{i+1}-s.png")
            thumb.save(thumb_path, "PNG", optimize=True)
            print(f"fenghuang-{i+1}-s.png: {thumb.size[0]}x{thumb.size[1]}")
        
        preview = img.copy()
        preview.thumbnail((80, 80))
        preview.convert("RGB").save(os.path.join(OUTPUT_DIR, "fenghuang-preview.jpg"), "JPEG", quality=85)
    
    # 神龙
    img_path = os.path.join(INPUT_DIR, "long.jpg")
    if os.path.exists(img_path):
        img = Image.open(img_path).convert("RGBA")
        img = img.resize((BOARD_SIZE, BOARD_SIZE), Image.LANCZOS)
        pieces = cut_long(img)
        for i, piece in enumerate(pieces):
            out_path = os.path.join(OUTPUT_DIR, f"long-{i+1}.png")
            piece.save(out_path, "PNG", optimize=True)
            print(f"long-{i+1}.png: {piece.size[0]}x{piece.size[1]}")
            
            thumb = piece.copy()
            thumb_ratio = THUMB_HEIGHT / thumb.size[1]
            thumb = thumb.resize((int(thumb.size[0] * thumb_ratio), THUMB_HEIGHT), Image.LANCZOS)
            thumb_path = os.path.join(OUTPUT_DIR, f"long-{i+1}-s.png")
            thumb.save(thumb_path, "PNG", optimize=True)
            print(f"long-{i+1}-s.png: {thumb.size[0]}x{thumb.size[1]}")
        
        preview = img.copy()
        preview.thumbnail((80, 80))
        preview.convert("RGB").save(os.path.join(OUTPUT_DIR, "long-preview.jpg"), "JPEG", quality=85)
    
    print("\n切割完成！")

if __name__ == "__main__":
    main()
