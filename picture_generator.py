import io

from PIL import Image
from PIL import ImageDraw


def create_picture(quests):
    font_size = 20
    y = 10
    indent = 10
    width = 640
    height = 480
    i = Image.new(mode="RGB", size=(width, height))
    Im = ImageDraw.Draw(i)
    for q in quests:
        Im.text((indent, y), q['title'] + ' : ' + q['quest_type'],
                font_size=font_size, fill=(255, 255, 255))
        y += font_size
        Im.text((2 * indent, y), q['description'],
                font_size=font_size, fill=(255, 255, 255))
        y += font_size
        Im.text((2 * indent, y),
                q['current_step'] * '#' + (q['number_of_steps'] - q['current_step']) * '-',
                font_size=font_size, fill=(255, 255, 255))
        y += font_size + indent
    img_byte_arr = io.BytesIO()
    i.save(img_byte_arr, format='PNG')
    return img_byte_arr.getvalue()
