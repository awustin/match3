import pygame
import json
import os
import sys


PROJECT_FOLDER = os.path.dirname(os.path.abspath(os.path.curdir))
CONFIG_FOLDER = os.path.join(PROJECT_FOLDER, 'config')
sys.path.insert(0, CONFIG_FOLDER)
try:
    import globales
except Exception as e:
    print(e)
    raise


SPR_CONFIG_FILE = os.path.join(CONFIG_FOLDER, 'chips_config.json')
SPRITES = {}


def init_sprite_data():
    global SPRITES
    if len(SPRITES) == 0:
        with open(SPR_CONFIG_FILE) as c_file:
            SPRITES = json.load(c_file)
        for item in SPRITES:
            sprite_data = SpriteData(SPRITES[item])
            SPRITES[item] = sprite_data


def get_animation_frames(key='default'):
    global SPRITES
    if len(SPRITES) == 0:
        print('No sprites data')
        return None
    key = str(key)
    return SPRITES[key].get_animation_frames()


def get_num_frames(key='default'):
    global SPRITES
    if len(SPRITES) == 0:
        print('No sprites data')
        return None
    key = str(key)
    return SPRITES[key].get_num_frames()


def get_anim_speed(key='default'):
    global SPRITES
    if len(SPRITES) == 0:
        print('No sprites data')
        return None
    key = str(key)
    return SPRITES[key].get_anim_speed()


class SpriteData(object):
    def __init__(self, spr_object):
        self.__surface = None
        self.__frames = []
        self.__path = os.path.normpath(spr_object['path'])
        self.__num_frames = spr_object['num_frames']
        self.__width = spr_object['width_px']
        self.__height = spr_object['height_px']
        self.__anim_speed = spr_object['anim_speed']
        self.__load_surface()
        self.__create_frames()

    def __load_surface(self):
        load_from = os.path.join(globales.ROOT_DIR, self.__path)
        self.__surface = pygame.image.load(load_from).convert_alpha()

    def __create_frames(self):
        for i in range(self.__num_frames):
            xpos = i * self.__width
            frame = self.__surface.subsurface(xpos, 0,
                                              self.__width,
                                              self.__height)
            self.__frames.append(frame)

    def get_animation_frames(self):
        return self.__frames

    def get_num_frames(self):
        return self.__num_frames

    def get_anim_speed(self):
        return self.__anim_speed

    def get_path(self):
        return self.__path
