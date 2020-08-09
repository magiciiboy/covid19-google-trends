import pandas as pd
import config


def load_data_states():
    data_file = "%s/us-states.csv" % config.COVID19_DATA_DIR
    df = pd.read_csv(data_file)
    df['country'] = 'US'
    return df
