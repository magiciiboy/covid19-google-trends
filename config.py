import os
from .utils.places import getPlaces

ROOT_DIR = os.getcwd()
DATA_DIR = '%s/data' % ROOT_DIR

PLACES = getPlaces(DATA_DIR)