from PIL import Image, ImageDraw
import os

R = 8                         # Corner radius
BORDER = 2                    # Blue border thickness
M = 16                        # Black margin between the screen edge and the blue border
LINE = (10, 132, 255, 255)    # Border blue color
FILL = (0, 0, 0, 255)         # Opaque black
SCALE = 4

H = M + R                     # Size of each corner
size = 2 * H + 1
big = size * SCALE

# Solid opaque black background with a rounded blue rectangle inset by M pixels
img = Image.new("RGBA", (big, big), FILL)
d = ImageDraw.Draw(img)
d.rounded_rectangle(
    (M * SCALE, M * SCALE, big - 1 - M * SCALE, big - 1 - M * SCALE),
    radius=R * SCALE,
    fill=FILL,
    outline=LINE,
    width=BORDER * SCALE
)
img = img.resize((size, size), Image.LANCZOS)

pieces = {
    "nw": (0, 0, H, H),
    "n":  (H, 0, H + 1, H),
    "ne": (H + 1, 0, size, H),
    "w":  (0, H, H, H + 1),
    "c":  (H, H, H + 1, H + 1),
    "e":  (H + 1, H, size, H + 1),
    "sw": (0, H + 1, H, size),
    "s":  (H, H + 1, H + 1, size),
    "se": (H + 1, H + 1, size, size),
}

os.makedirs("terminal", exist_ok=True)

for name, box in pieces.items():
    img.crop(box).save(f"terminal/terminal_box_{name}.png")
    print("Created:", name)