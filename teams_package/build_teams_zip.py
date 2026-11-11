import os
import zipfile
from pathlib import Path

PKG_DIR = Path(__file__).resolve().parent

def generate_icons():
    color_file = PKG_DIR / "color.png"
    outline_file = PKG_DIR / "outline.png"
    
    # If icons already exist, no need for PIL
    if color_file.exists() and outline_file.exists():
        return

    try:
        from PIL import Image, ImageDraw
    except ImportError:
        print("[Notice] Pillow not installed, but icons already exist. Skipping icon generation.")
        return

    # 1. Color icon: 192x192 PNG
    color_img = Image.new("RGBA", (192, 192), (91, 95, 199, 255))
    draw = ImageDraw.Draw(color_img)
    draw.ellipse((24, 24, 168, 168), fill=(255, 255, 255, 230))
    draw.polygon([(96, 40), (60, 110), (96, 110), (84, 155), (135, 95), (105, 95)], fill=(91, 95, 199, 255))
    color_img.save(color_file, "PNG")

    # 2. Outline icon: 32x32 PNG with transparent background
    outline_img = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
    d2 = ImageDraw.Draw(outline_img)
    d2.polygon([(16, 4), (8, 18), (16, 18), (14, 28), (24, 15), (18, 15)], fill=(255, 255, 255, 255))
    outline_img.save(outline_file, "PNG")

def create_teams_zip():
    generate_icons()
    zip_path = PKG_DIR / "teams_365_agent.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        z.write(PKG_DIR / "manifest.json", "manifest.json")
        z.write(PKG_DIR / "color.png", "color.png")
        z.write(PKG_DIR / "outline.png", "outline.png")
    print(f"Created official Teams App Package: {zip_path} ({os.path.getsize(zip_path)} bytes)")

if __name__ == "__main__":
    create_teams_zip()
