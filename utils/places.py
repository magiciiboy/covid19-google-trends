import os
import pandas as pd

def load_places(data_dir):
    data_file = "%s/places.csv" % data_dir
    df = pd.read_csv(data_file)
    places = {}
    columns = df.columns
    for i in range(0, df['State'].count()):
        code = '%s:%s' % (df.iloc[i,0], df.iloc[i,1].replace(' ', '_'))
        place = {}
        for idx, c in enumerate(columns):
            place[c] = df.iloc[i, idx]
        places[code] = place
    return places
