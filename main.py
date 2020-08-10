import argparse
import config
from utils.covid19 import load_data_states
from scripts.plot import plot_covid19_cases
from scripts.preprocess import union_CSSE_covid19_data_US

if __name__ == "__main__":
    app_parser = argparse.ArgumentParser()
    app_parser.version = "1.0"
    app_parser.add_argument("-d", "--download", action="store_true", help="Download data")
    app_parser.add_argument("-p", "--preprocess", action="store_true", help="Preprocess data")
    app_parser.add_argument("-f", "--plotfigures", action="store_true", help="Plot figures")
    app_parser.add_argument("-v", action="version")
    args = app_parser.parse_args()

    if args.plotfigures:
        print("Plot figures")
        df = load_data_states(source=config.COVID19_DATA_SOURCE)
        plot_covid19_cases(df)

    if args.preprocess:
        df = union_CSSE_covid19_data_US()
