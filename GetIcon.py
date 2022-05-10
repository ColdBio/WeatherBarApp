import os
import json
import rumps
import requests
from PIL import Image as PImage

def return_icon(url):
    url = url.split("/")

    dayornight = url[-2]
    icon_name = url[-1]

    img = f'{dayornight}/{icon_name}'
    return img