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
CHIP_DATA = {}


def init_score_data():
    global CHIP_DATA
    if len(CHIP_DATA) == 0:
        with open(SPR_CONFIG_FILE) as c_file:
            CHIP_DATA = json.load(c_file)
        for item in CHIP_DATA:
            CHIP_DATA[item] = ScoreData(CHIP_DATA[item]['score_data'])


def get_base_value(key='default'):
    global CHIP_DATA
    if len(CHIP_DATA) == 0:
        print('No score data')
        return None
    key = str(key)
    return CHIP_DATA[key].get_base_value()


def get_fruity(key='default'):
    global CHIP_DATA
    if len(CHIP_DATA) == 0:
        print('No score data')
        return None
    key = str(key)
    return CHIP_DATA[key].get_fruity()


def get_bitter(key='default'):
    global CHIP_DATA
    if len(CHIP_DATA) == 0:
        print('No score data')
        return None
    key = str(key)
    return CHIP_DATA[key].get_bitter()


def get_rotten(key='default'):
    global CHIP_DATA
    if len(CHIP_DATA) == 0:
        print('No score data')
        return None
    key = str(key)
    return CHIP_DATA[key].get_rotten()


class ScoreData():
    def __init__(self, read_object):
        self.__base_value = read_object['base_value']
        self.__frutiy = read_object['fruity']
        self.__bitter = read_object['bitter']
        self.__rotten = read_object['rotten']

    def get_base_value(self):
        return self.__base_value

    def get_fruity(self):
        return self.__frutiy

    def get_bitter(self):
        return self.__bitter

    def get_rotten(self):
        return self.__rotten
