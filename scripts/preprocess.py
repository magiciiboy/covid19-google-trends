import os
import pandas as pd
import config
from os import listdir

def union_CSSE_covid19_data_US():
    print('Joining CSSE COVID19 data ...')
    data_dir = config.COVID19_CSSE_DATA_DIR
    files = [f for f in listdir(data_dir) if os.path.isfile(os.path.join(data_dir, f)) and '.csv' in f]
    df = None
    for f in files:
        file_path = os.path.join(data_dir, f)
        date = f"{f[6:10]}-{f[0:2]}-{f[3:5]}"
        f_df = pd.read_csv(file_path)
        f_df["Date"] = date
        if df is None:
            df = f_df
        else:
            df = pd.concat([df, f_df])
    df.to_csv(os.path.join(data_dir, 'UTD.csv'), index=False)
    print('Done!')
    return df
