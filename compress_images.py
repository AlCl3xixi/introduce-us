import os
from PIL import Image

def compress_image(input_path, quality=60, max_size=512):
    try:
        img = Image.open(input_path)
        
        width, height = img.size
        if width > max_size or height > max_size:
            ratio = min(max_size / width, max_size / height)
            new_width = int(width * ratio)
            new_height = int(height * ratio)
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        if input_path.lower().endswith('.png'):
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
            img.save(input_path, 'PNG', optimize=True)
        else:
            if img.mode != 'RGB':
                img = img.convert('RGB')
            img.save(input_path, 'JPEG', quality=quality, optimize=True)
        
        return True
    except Exception as e:
        print(f"压缩失败 {input_path}: {e}")
        return False

def main():
    image_extensions = ('.jpg', '.jpeg', '.png', '.gif')
    count = 0
    
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.lower().endswith(image_extensions):
                filepath = os.path.join(root, file)
                if compress_image(filepath):
                    count += 1
                    print(f"已压缩: {filepath}")
    
    print(f"\n共压缩 {count} 张图片")

if __name__ == '__main__':
    main()