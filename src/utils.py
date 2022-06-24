import json
import pygame

from .globals import window


def draw_sprite(spr, frame, x, y):
    window.blit(spr, (x, y), frame)


def draw_text(font, x, y, text, color):
    window.blit(font.render(text, True, color), (x, y))


def json_write(path, data):
    json.dump(data, open(path, "w"))


def json_read(path):
    return json.loads(open(path, "r").read())


def ninepatch(surface: pygame.Surface, rect: tuple):
    rect = pygame.Rect(rect)
    result = pygame.Surface(rect.size, pygame.SRCALPHA)
    subsurf_w = surface.get_width() // 3
    subsurf_h = surface.get_height() // 3
    a1 = surface.subsurface(0, 0, subsurf_w, subsurf_h)
    a2 = surface.subsurface(subsurf_w, 0, subsurf_w, subsurf_h)
    a3 = surface.subsurface(2 * subsurf_w, 0, subsurf_w, subsurf_h)
    b1 = surface.subsurface(0, subsurf_h, subsurf_w, subsurf_h)
    b2 = surface.subsurface(subsurf_w, subsurf_h, subsurf_w, subsurf_h)
    b3 = surface.subsurface(2 * subsurf_w, subsurf_h, subsurf_w, subsurf_h)
    c1 = surface.subsurface(0, 2 * subsurf_h, subsurf_w, subsurf_h)
    c2 = surface.subsurface(subsurf_w, 2 * subsurf_h, subsurf_w, subsurf_h)
    c3 = surface.subsurface(2 * subsurf_w, 2 * subsurf_h, subsurf_w, subsurf_h)

    result.blit(a1, (0, 0))
    result.blit(pygame.transform.scale(a2, (rect.w - 2 * subsurf_w, subsurf_h)), (subsurf_w, 0))
    result.blit(a3, (rect.w - subsurf_w, 0))
    result.blit(pygame.transform.scale(b1, (subsurf_w, rect.h - 2 * subsurf_h)), (0, subsurf_h))
    result.blit(
        pygame.transform.scale(b2, (rect.w - 2 * subsurf_w, rect.h - 2 * subsurf_h)),
        (subsurf_w, subsurf_h),
    )
    result.blit(
        pygame.transform.scale(b3, (subsurf_w, rect.h - 2 * subsurf_h)),
        (rect.w - subsurf_w, subsurf_h),
    )
    result.blit(c1, (0, rect.h - subsurf_h))
    result.blit(
        pygame.transform.scale(c2, (rect.w - 2 * subsurf_w, subsurf_h)),
        (subsurf_w, rect.h - subsurf_h),
    )
    result.blit(c3, (rect.w - subsurf_w, rect.h - subsurf_h))

    return result

################### Effects #########################

