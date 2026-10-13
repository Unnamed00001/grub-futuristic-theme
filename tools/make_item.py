from PIL import Image
import glob
import os

for f in glob.glob("menu/selected_*.png"):
    img = Image.open(f)
    nome = os.path.basename(f).replace("selected_", "item_")
    Image.new("RGBA", img.size, (0, 0, 0, 0)).save(f"menu/{nome}")
    print("criado:", nome, img.size)