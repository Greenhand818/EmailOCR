import os
from PIL import Image, ImageFont, ImageDraw
import random

Parameters = {
    "target_path": "E:\GenerateImage\letters",
    "dict_path": "E:\GenerateImage\label_dict.txt",
    "ttf_path": r"E:\GenerateImage\ttf"
}

def generateLetter(target_path, dict_path):
    with open(dict_path, 'r') as f:
        lines = f.read()
        letters = lines.split()
        for letter in letters:
            path = os.listdir(Parameters["ttf_path"])
            params = [1 - float(random.randint(1, 2)) / 100,
                      0,
                      0,
                      0,
                      1 - float(random.randint(1, 10)) / 100,
                      float(random.randint(1, 2)) / 500,
                      0.001,
                      float(random.randint(1, 2)) / 500]
            if letter != '.':
                letter_path = os.path.join(target_path, letter.upper())
            else:
                letter_path = os.path.join(target_path, "dot")

            if letter >= 'a' and letter <= 'z':
                letter_path = os.path.join(letter_path, "lower")
            elif letter >= 'A' and letter <= 'Z':
                letter_path = os.path.join(letter_path, "capital")
            letter_p = os.listdir(letter_path)
            for lp in letter_p:
                os.remove(os.path.join(letter_path, lp))
            count = 0
            for ttf in path:
                for epoch in range(5):
                    img = Image.new("RGB", (50, 50), (255, 255, 255))
                    image = ImageDraw.Draw(img)
                    font = ImageFont.truetype(os.path.join("./ttf", ttf), 20)
                    area = (10, 10)
                    image.text(area, letter, font=font, fill="#000000")
                    img = img.rotate(random.randint(-5, 5))
                    img = img.transform((50, 50), Image.PERSPECTIVE, params)
                    img = img.crop([10, 10, 34, 50])
                    save_path = os.path.join(letter_path,  str(count + epoch) + ".jpg")
                    img.save(save_path)
                count += 1




if __name__ == "__main__":
    generateLetter(Parameters["target_path"], Parameters["dict_path"])