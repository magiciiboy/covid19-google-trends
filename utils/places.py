import os
import pandas as pd


def getPlaces(data_dir):
    data_file = '%s/places.csv'
    df = pd.read_csv(data_file)
    return df
