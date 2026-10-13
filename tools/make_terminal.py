from PIL import Image, ImageDraw
import os

R = 8                         # raio dos cantos
BORDER = 2                    # espessura da borda azul
M = 16                        # margem preta entre a borda da tela e a borda azul
LINE = (10, 132, 255, 255)    # azul da borda
FILL = (0, 0, 0, 255)         # preto opaco
SCALE = 4

H = M + R                     # tamanho de cada canto
size = 2 * H + 1
big = size * SCALE

# tudo preto opaco, com um retângulo azul arredondado recuado em M pixels
img = Image.new("RGBA", (big, big), FILL)
d = ImageDraw.Draw(img)
d.rounded_rectangle((M * SCALE, M * SCALE, big - 1 - M * SCALE, big - 1 - M * SCALE),
                    radius=R * SCALE, fill=FILL, outline=LINE, width=BORDER * SCALE)
img = img.resize((size, size), Image.LANCZOS)

pedacos = {
    "nw": (0, 0, H, H),        "n": (H, 0, H + 1, H),        "ne": (H + 1, 0, size, H),
    "w":  (0, H, H, H + 1),    "c": (H, H, H + 1, H + 1),    "e":  (H + 1, H, size, H + 1),
    "sw": (0, H + 1, H, size), "s": (H, H + 1, H + 1, size), "se": (H + 1, H + 1, size, size),
}

os.makedirs("terminal", exist_ok=True)
for nome, caixa in pedacos.items():
    img.crop(caixa).save(f"terminal/terminal_box_{nome}.png")
    print("criado:", nome)