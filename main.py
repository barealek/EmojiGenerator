from PIL import Image, ImageDraw
import cairosvg
import requests
from io import BytesIO

from functions import get_dict_option_from_user, print_welcome, ensure_dir

import os
import time
import math

TRANSPARENCY = 0.25  # i procent
MASK_URL = "https://github.com/barealek/EmojiGenerator/blob/main/assets/mask.jpg?raw=true"

DIMENSIONS = (512, 512)
ICON_SIZE = 3 / 5
CALCULATED_ICON_SIZE = (int(DIMENSIONS[0] * ICON_SIZE), int(DIMENSIONS[0] * ICON_SIZE))  # 2/3 af billedet

COLORMAP = {
    "lime": (88, 240, 0),
    "grøn": (0, 224, 157),
    "grå": (60, 64, 72),
    "blå": (75, 201, 255),
    "pink": (255, 161, 251),
    "gul": (255, 230, 0),
    "rød": (255, 67, 78),
    "orange": (255, 125, 40),
    "brun": (194, 124, 14),
    "lilla": (90, 66, 210),
    "hvid": (240, 240, 240),
    "cyan": (0, 255, 255),
    "lys rød": (255, 92, 95),
    "beige": (255, 250, 200),
    "mørkegrå": (40, 40, 40)
}


def main():
    print_welcome()

    print("Vælg den farve som du vil generere emojierne i:")

    color_name, color = get_dict_option_from_user(COLORMAP)

    ensure_dir("in")

    print("Læg alle de SVG filer du vil konvertere ind i mappen 'in' og tryk enter.")
    input()

    print("Klargører basale assets...")

    out = Image.new("RGBA", DIMENSIONS)
    square = Image.new("RGBA", DIMENSIONS)
    square_draw = ImageDraw.Draw(square)

    print("Downloader mask fra alek's GitHub...")
    mask = Image.open(BytesIO(requests.get(MASK_URL).content)).convert("L")
    # mask = Image.open("assets/mask.jpg")
    mask = mask.resize(out.size)

    square_draw.rectangle((0, 0, *DIMENSIONS), fill=color + (int(255 * TRANSPARENCY),))

    # Draw the contents of square onto img using the mask
    out.paste(square, (0, 0), mask=mask)

    print("Mask og out-fil er klar")

    for icon_in in os.listdir("in"):
        print(f"Processerer {icon_in}...")
        _out = out.copy()

        # Generate a mask from the icon
        print(f"Konverterer {icon_in} til en PNG fil...")
        ensure_dir("temp")

        cairosvg.svg2png(url=f"in/{icon_in}", write_to="temp/icon.png", output_width=DIMENSIONS[0] / 2, output_height=DIMENSIONS[1] / 2)

        icon = Image.open("temp/icon.png")

        # Make the icon png all white
        print("Gør PNGen til en mask...")
        icon.putdata([(255, 255, 255, 255) if x[3] != 0 else (0, 0, 0) for x in icon.getdata()])
        icon = icon.resize(CALCULATED_ICON_SIZE)

        # Paste the icon onto the image
        print("Indsætter masken på billedet med den valgte farve...")
        icon_square = Image.new("RGB", CALCULATED_ICON_SIZE, color)
        _out.paste(icon_square, (
            int(DIMENSIONS[0] / 2 - CALCULATED_ICON_SIZE[0] / 2), int(DIMENSIONS[1] / 2 - CALCULATED_ICON_SIZE[1] / 2)),
                   mask=icon.convert('L'))

        ensure_dir(f"out/{color_name}/")
        print(f"Gemmer {icon_in}...")
        _out.resize((128, 128)).save(f"out/{color_name}/{icon_in.removesuffix('svg')}png")

    print("Rydder op...")
    os.remove("temp/icon.png")
    os.rmdir("temp")
    print("\nFærdig! Du kan finde dine emojis i mappen 'out'.")
    for i in range(5, 0, -1):
        print(f"Lukker om {i} sekunder...", end="\r")
        time.sleep(1)


main()
