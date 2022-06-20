import json

from .globals import window


def draw_sprite(spr, frame, x, y):
    window.blit(spr, (x, y), frame)


def draw_text(font, x, y, text, color):
    window.blit(font.render(text, True, color), (x, y))


def json_write(path, data):
    json.dump(data, open(path, "w"))


def json_read(path):
    return json.loads(open(path, "r").read())
