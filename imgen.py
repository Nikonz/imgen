#!/usr/bin/python

import argparse
import os
import random

from PIL import Image, ImageDraw, ImageFont

DATA_DIR = 'data'
FONTS_DIR = 'fonts'

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def generate_text_image(text, image_size=(256, 256), background_path=None,
            background_color=WHITE, font='Arial.ttf', font_size=40,
            text_pos=(0.5, 0.5)):
    if background_path is None:
        image = Image.new('RGBA', image_size, WHITE)
    else:
        image = Image.open(path).convert('RGBA')

    fnt = ImageFont.truetype('fonts/' + font, font_size)
    d = ImageDraw.Draw(image)

    tpos = (text_pos[0] * (image_size[0] - font_size * len(text) * 0.6),
            text_pos[1] * (image_size[1] - font_size))
    d.text(tpos, text, font=fnt, fill=BLACK)

    return image

def load_text(path):
    with open(path, 'r') as f:
        return [line[:-1] for line in f]

def load_letters():
    lcase = [chr(c) for c in range(ord('a'), ord('z') + 1)]
    ucase = [chr(c) for c in range(ord('A'), ord('Z') + 1)]
    return lcase + ucase

def load_words():
    return load_text(DATA_DIR + '/1000words.txt')

def load_data(n_samples, dtype):
    raw_data = []
    if dtype == 'letters':
        raw_data = load_letters()
    elif dtype == 'words':
        raw_data = load_words()
    else:
        raise('Unknown data type')
    random.shuffle(raw_data)

    data = [raw_data[i % len(raw_data)] for i in range(n_samples)]
    return data

def load_fonts(font_types):
    if font_types == 'mono':
        return ['FreeMono.ttf', 'FreeMonoBold.ttf']
    elif font_types == 'arial':
        return ['Arial.ttf']
    elif font_types == 'all':
        return os.listdir(FONTS_DIR)
    else:
        raise('Unknown font type')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Image generator')
    parser.add_argument('n_samples', type=int, help='number of samples')
    parser.add_argument('--dtype', type=str, default='letters',
            help='input data type (letters/words), letters by default')
    parser.add_argument('--font_types', type=str, default='all',
            help='font type (mono/arial/all), all by default')
    parser.add_argument('--font_size', type=int, default=40,
            help='font size, 40 by default')
    parser.add_argument('--image_size', type=int, nargs=2, default=[256, 256],
            help='output image size [w h], default 256x256')
    parser.add_argument('--output_path', type=str, default='images',
            help='path to the output folder')
    parser.add_argument('--start_index', type=int, default=0,
            help='number of the first output image, 0 by default')

    args = parser.parse_args()
    print(args.n_samples, args.dtype, args.image_size, args.font_types, args.font_size)

    data = load_data(args.n_samples, args.dtype)
    fonts = load_fonts(args.font_types)

    for idx, sample in enumerate(data):
        image = generate_text_image(sample, image_size=args.image_size,
                font=random.choice(fonts), font_size=args.font_size)
        #image.show()
        os.makedirs(args.output_path, exist_ok=True)
        image.save(args.output_path + "/%03d.png" % (args.start_index + idx), "PNG")
