from PIL import Image, ImageDraw
import os

R = 6                        # Corner radius (rounding and frame height)
PAD_X = 10                   # Extra margin on the sides (left and right)
BORDER = 2
FILL = (4, 22, 58, 255)
LINE = (10, 132, 255, 255)
SCALE = 4

# Draws the bar with extra width: each side gains PAD_X pixels
W = 2 * (R + PAD_X) + 1
Hh = 2 * R + 1
big_w, big_h = W * SCALE, Hh * SCALE

img = Image.new("RGBA", (big_w, big_h), (0, 0, 0, 0))
d = ImageDraw.Draw(img)
d.rounded_rectangle(
    (0, 0, big_w - 1, big_h - 1),
    radius=R * SCALE,
    fill=LINE
)
b = BORDER * SCALE
d.rounded_rectangle(
    (b, b, big_w - 1 - b, big_h - 1 - b),
    radius=(R - BORDER) * SCALE,
    fill=FILL
)
img = img.resize((W, Hh), Image.LANCZOS)

L = R + PAD_X                # Width of the left and right pieces
pieces = {
    "nw": (0, 0, L, R),          "n": (L, 0, L + 1, R),          "ne": (L + 1, 0, W, R),
    "w":  (0, R, L, R + 1),      "c": (L, R, L + 1, R + 1),      "e":  (L + 1, R, W, R + 1),
    "sw": (0, R + 1, L, Hh),     "s": (L, R + 1, L + 1, Hh),     "se": (L + 1, R + 1, W, Hh),
}

os.makedirs("menu", exist_ok=True)

for name, box in pieces.items():
    img.crop(box).save(f"menu/selected_{name}.png")
    print("Created:", name, box)