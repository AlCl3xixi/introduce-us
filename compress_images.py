import os
from PIL import Image

def compress_png_aggressive(input_path, output_path):
    try:
        img = Image.open(input_path)
        
        original_size = os.path.getsize(input_path)
        
        if img.mode == 'RGBA':
            palette_size = len(set(img.getdata()))
            if palette_size <= 256:
                img = img.convert('P', palette=Image.ADAPTIVE)
            else:
                img = img.convert('RGBA')
        else:
            palette_size = len(set(img.getdata()))
            if palette_size <= 256:
                img = img.convert('P', palette=Image.ADAPTIVE)
        
        img.save(output_path, 'PNG', optimize=True, compress_level=9)
        
        compressed_size = os.path.getsize(output_path)
        ratio = (1 - compressed_size / original_size) * 100
        
        print(f"{os.path.basename(input_path):<30} {original_size/1024:>7.1f}KB -> {compressed_size/1024:>7.1f}KB ({ratio:>5.1f}% saved)")
        return True
    except Exception as e:
        print(f"压缩失败 {input_path}: {e}")
        return False

def convert_to_webp(input_path, output_path, quality=70):
    try:
        img = Image.open(input_path)
        
        original_size = os.path.getsize(input_path)
        
        if img.mode == 'RGBA':
            img.save(output_path.replace('.png', '.webp'), 'WEBP', quality=quality, lossless=False)
        else:
            img = img.convert('RGB')
            img.save(output_path.replace('.png', '.webp'), 'WEBP', quality=quality, lossless=False)
        
        compressed_size = os.path.getsize(output_path.replace('.png', '.webp'))
        ratio = (1 - compressed_size / original_size) * 100
        
        print(f"{os.path.basename(input_path):<30} {original_size/1024:>7.1f}KB -> {compressed_size/1024:>7.1f}KB ({ratio:>5.1f}% saved) [WebP]")
        return True
    except Exception as e:
        print(f"转换失败 {input_path}: {e}")
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
    print("游戏图片压缩脚本")
    print("=" * 70)
    
    total_original = 0
    total_compressed = 0
    count = 0
    
    ceramic_dir = 'game/images/ceramic'
    print("\n【瓷片图片压缩 - 转换为 WebP】")
    print("-" * 70)
    for filename in os.listdir(ceramic_dir):
        if filename.endswith('.png'):
            input_path = os.path.join(ceramic_dir, filename)
            output_path = os.path.join(ceramic_dir, filename.replace('.png', '.webp'))
            total_original += os.path.getsize(input_path)
            if convert_to_webp(input_path, output_path, quality=65):
                total_compressed += os.path.getsize(output_path)
                count += 1
    
    puzzle_dir = 'game/images/puzzle'
    print("\n【拼图图片压缩】")
    print("-" * 70)
    for filename in os.listdir(puzzle_dir):
        if filename.endswith('.png') and '-delineate' in filename:
            input_path = os.path.join(puzzle_dir, filename)
            output_path = os.path.join(puzzle_dir, filename.replace('.png', '.webp'))
            total_original += os.path.getsize(input_path)
            if convert_to_webp(input_path, output_path, quality=60):
                total_compressed += os.path.getsize(output_path)
                count += 1
        elif filename.endswith('.png'):
            input_path = os.path.join(puzzle_dir, filename)
            total_original += os.path.getsize(input_path)
            if compress_png_aggressive(input_path, input_path):
                total_compressed += os.path.getsize(input_path)
                count += 1
        elif filename.endswith('.jpg'):
            input_path = os.path.join(puzzle_dir, filename)
            total_original += os.path.getsize(input_path)
            if compress_jpg(input_path, input_path, quality=65):
                total_compressed += os.path.getsize(input_path)
                count += 1
    
    covers_dir = 'game/images/covers'
    print("\n【封面图片压缩】")
    print("-" * 70)
    for filename in os.listdir(covers_dir):
        if filename.endswith('.jpg'):
            input_path = os.path.join(covers_dir, filename)
            total_original += os.path.getsize(input_path)
            if compress_jpg(input_path, input_path, quality=70):
                total_compressed += os.path.getsize(input_path)
                count += 1
    
    print("\n" + "=" * 70)
    total_saved = total_original - total_compressed
    ratio = (total_saved / total_original) * 100 if total_original > 0 else 0
    print(f"总计: {count} 张图片")
    print(f"原始大小: {total_original/1024:.1f} KB")
    print(f"压缩后:   {total_compressed/1024:.1f} KB")
    print(f"节省空间: {total_saved/1024:.1f} KB ({ratio:.1f}%)")
    print("=" * 70)
    print("\n注意：已将部分 PNG 转换为 WebP 格式，需要更新 HTML/JS 中的图片引用")

if __name__ == '__main__':
    main()
