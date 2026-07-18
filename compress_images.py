import os
from PIL import Image

def convert_to_webp(input_path, output_path, quality=70, lossless=False):
    try:
        img = Image.open(input_path)
        original_size = os.path.getsize(input_path)
        
        if img.mode == 'RGBA':
            img.save(output_path.replace('.png', '.webp'), 'WEBP', quality=quality, lossless=lossless)
        else:
            img = img.convert('RGB')
            img.save(output_path.replace('.png', '.webp'), 'WEBP', quality=quality, lossless=lossless)
        
        compressed_size = os.path.getsize(output_path.replace('.png', '.webp'))
        ratio = (1 - compressed_size / original_size) * 100
        mode = 'lossless' if lossless else ''
        print(f"{os.path.basename(input_path):<30} {original_size/1024:>7.1f}KB -> {compressed_size/1024:>7.1f}KB ({ratio:>5.1f}% saved) [WebP{mode}]")
        return True
    except Exception as e:
        print(f"转换失败 {input_path}: {e}")
        return False

def generate_placeholder(input_path, output_path, quality=20, scale=0.1):
    try:
        img = Image.open(input_path)
        w, h = img.size
        placeholder = img.resize((int(w * scale), int(h * scale)), Image.Resampling.LANCZOS)
        placeholder.save(output_path, 'WEBP', quality=quality, lossless=False)
        print(f"{os.path.basename(input_path):<30} -> placeholder: {os.path.getsize(output_path)/1024:.1f}KB")
        return True
    except Exception as e:
        print(f"生成占位图失败 {input_path}: {e}")
        return False

def create_sprite_sheet(images, output_path, cols=6):
    try:
        if not images:
            return False
        
        first_img = Image.open(images[0])
        img_w, img_h = first_img.size
        
        rows = (len(images) + cols - 1) // cols
        sheet_w = img_w * cols
        sheet_h = img_h * rows
        
        sheet = Image.new('RGBA', (sheet_w, sheet_h), (0, 0, 0, 0))
        
        for i, img_path in enumerate(images):
            img = Image.open(img_path)
            row = i // cols
            col = i % cols
            sheet.paste(img, (col * img_w, row * img_h))
        
        sheet.save(output_path, 'WEBP', quality=75, lossless=False)
        print(f"雪碧图: {output_path} ({sheet_w}x{sheet_h}), {os.path.getsize(output_path)/1024:.1f}KB")
        return True
    except Exception as e:
        print(f"生成雪碧图失败: {e}")
        return False

def compress_jpg(input_path, output_path, quality=70):
    try:
        img = Image.open(input_path)
        original_size = os.path.getsize(input_path)
        
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        img.save(output_path, 'JPEG', quality=quality, optimize=True)
        compressed_size = os.path.getsize(output_path)
        ratio = (1 - compressed_size / original_size) * 100
        print(f"{os.path.basename(input_path):<30} {original_size/1024:>7.1f}KB -> {compressed_size/1024:>7.1f}KB ({ratio:>5.1f}% saved)")
        return True
    except Exception as e:
        print(f"压缩失败 {input_path}: {e}")
        return False

def main():
    print("=" * 70)
    print("游戏图片优化脚本")
    print("=" * 70)
    
    ceramic_dir = 'game/images/ceramic'
    puzzle_dir = 'game/images/puzzle'
    covers_dir = 'game/images/covers'
    
    print("\n【1. 生成瓷片占位图 (低质量预览)】")
    print("-" * 70)
    for filename in os.listdir(ceramic_dir):
        if filename.endswith('.png'):
            input_path = os.path.join(ceramic_dir, filename)
            placeholder_path = os.path.join(ceramic_dir, filename.replace('.png', '-placeholder.webp'))
            generate_placeholder(input_path, placeholder_path)
    
    print("\n【2. 生成瓷片 WebP 图片】")
    print("-" * 70)
    for filename in os.listdir(ceramic_dir):
        if filename.endswith('.png') and '-placeholder' not in filename:
            input_path = os.path.join(ceramic_dir, filename)
            output_path = os.path.join(ceramic_dir, filename.replace('.png', '.webp'))
            convert_to_webp(input_path, output_path, quality=65)
    
    print("\n【3. 生成瓷片雪碧图】")
    print("-" * 70)
    ceramic_images = sorted([
        os.path.join(ceramic_dir, f) 
        for f in os.listdir(ceramic_dir) 
        if f.endswith('.webp') and '-placeholder' not in f
    ])
    if ceramic_images:
        create_sprite_sheet(ceramic_images, os.path.join(ceramic_dir, 'ceramic-sprite.webp'), cols=6)
    
    print("\n【4. 生成轮廓图片 WebP】")
    print("-" * 70)
    for filename in os.listdir(puzzle_dir):
        if filename.endswith('-delineate.png'):
            input_path = os.path.join(puzzle_dir, filename)
            output_path = os.path.join(puzzle_dir, filename.replace('.png', '.webp'))
            convert_to_webp(input_path, output_path, quality=60)
    
    print("\n【5. 压缩封面图片】")
    print("-" * 70)
    for filename in os.listdir(covers_dir):
        if filename.endswith('.jpg'):
            input_path = os.path.join(covers_dir, filename)
            compress_jpg(input_path, input_path, quality=75)
    
    print("\n【6. 压缩拼图预览图片】")
    print("-" * 70)
    for filename in os.listdir(puzzle_dir):
        if filename.endswith('-preview.jpg'):
            input_path = os.path.join(puzzle_dir, filename)
            compress_jpg(input_path, input_path, quality=70)
    
    print("\n" + "=" * 70)
    print("优化完成！")
    print("=" * 70)

if __name__ == '__main__':
    main()
