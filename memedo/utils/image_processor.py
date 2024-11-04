import os, sys
import traceback

from PIL import Image, ImageDraw, ImageFont
font_path = "memedo/static/fonts/Arial.ttf"

import textwrap



def wrap(text, width):
    new_text = ""

    wrapper = textwrap.TextWrapper(width=width)
    text = wrapper.wrap(text=text)

    for ii in text[:-1]:
        new_text = new_text + ii + "\n"
    new_text += text[-1]

    return new_text


class Image_Manager:
    def __init__(self):
        print("Image manager create")

    @staticmethod
    def add_text(
        base,
        text,
        position,
        font_size,
        text_color="black",
        text_width_proportion=4,
        wrapped_width=None,
        rotate_degrees=None,
    ):

        try:
            overlay_image = Image.new("RGBA", base.size, (0, 0, 0, 0))
            if wrapped_width is not None:
                text = wrap(text, wrapped_width)

            font = ImageFont.truetype(font_path, font_size)
            draw = ImageDraw.Draw(overlay_image)
            fill = (0, 0, 0, 255)
            if text_color == "white":
                fill = (255, 255, 255, 255)
            draw.text(position, text, font=font, fill=fill)
            if rotate_degrees is not None:
                overlay_image = overlay_image.rotate(rotate_degrees)

            return overlay_image
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print(traceback.format_exc())
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(f"error: {e}")
            print(f"line: {exc_tb.tb_lineno}")
            print(f"file: {fname}")
            return "error"
