import argparse
import config
from utils.covid19 import load_data_states
from scripts.plot import plot_covid19_cases
from scripts.preprocess import union_CSSE_covid19_data_US
from scripts.trends.download import download_trends
from scripts.trends.plot import plot_trends

if __name__ == "__main__":
    app_parser = argparse.ArgumentParser()
    app_parser.version = "1.0"
    app_parser.add_argument("-d", "--download", action="store_true", help="Download data")
    app_parser.add_argument("-p", "--preprocess", action="store_true", help="Preprocess data")
    app_parser.add_argument("-f", "--plotfigures", action="store_true", help="Plot figures")
    app_parser.add_argument("-v", action="version")
    args = app_parser.parse_args()

    if args.download:
        print("Download Google Trends data")
        countries = []
        for place_key in config.PLACES:
            place = config.PLACES[place_key]
            place_country = place["Country"]
            place_state = place["Abbrev"]
            print(f"* {place_country} - {place_state}")
            download_trends(country=place_country, state=place_state)
            if place_country not in countries:
                download_trends(country=place_country)
                countries.append(place_country)
            break
        print("Done!")

    if args.plotfigures:
        print("Plot figures")
        data_type = 't'
        if data_type == 'c':
            df = load_data_states(source=config.COVID19_DATA_SOURCE)
            plot_covid19_cases(df)
        elif data_type == 't':
            for group in config.TRENDS_DATA_GROUPS:
                countries = []
                for place_key in config.PLACES:
                    place = config.PLACES[place_key]
                    place_country = place["Country"]
                    place_state = place["Abbrev"]
                    plot_trends(group, country=place_country, state=place_state, place=place)
                    if place_country not in countries:
                        plot_trends(group, country=place_country)
                        countries.append(place_country)
                    break

    if args.preprocess:
        df = union_CSSE_covid19_data_US()
