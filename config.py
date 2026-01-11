import pygame

BASE_WIDTH = 184
BASE_HEIGHT = 24
INITIAL_SCALE = 4

PATH_HOTBAR = "assets/hotbar.png"
PATH_SELECTOR = "assets/selector.png"
PATH_ITEM = "assets/item.png"
PATH_FONT = "assets/minecraft_font.otf"
PATH_SOUND_SUCCESS = "assets/success.wav"
PATH_SOUND_ERROR = "assets/fail.wav"
CONFIG_FILE = "config.json"

TPS = 20
MS_PER_TICK = 1000 // TPS
DEFAULT_LIMIT_TICKS = -1

COLOR_EDITING = (255, 255, 0)
COLOR_TEXT = (255, 255, 255)
COLOR_SHADOW = (62, 62, 62)

DEFAULT_KEYS = [
    pygame.K_1, pygame.K_2, pygame.K_3,
    pygame.K_4, pygame.K_5, pygame.K_6,
    pygame.K_7, pygame.K_8, pygame.K_9
]