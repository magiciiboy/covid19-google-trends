import os
from utils.places import load_places

ROOT_DIR = os.getcwd()

DATA_DIR = "%s/data" % ROOT_DIR
COVID19_DATA_SOURCE = 'CSSE'
COVID19_NYT_DATA_DIR = "%s/covid-19-data" % DATA_DIR
COVID19_CSSE_DATA_DIR = '%s/COVID-19/csse_covid_19_data/csse_covid_19_daily_reports_us/' % DATA_DIR

TRENDS_DATA_DIR = "%s/trends" % DATA_DIR

PLACES = load_places(DATA_DIR)

# Plots
FIGURES_DIR = "%s/figures" % ROOT_DIR
LINE_COLOR = 'rgb(130, 130, 130)'

LINE_COLOR_BEFORE = '#2375B3'
LINE_COLOR_AFTER = '#9D433C'

LINE_COLOR_ACTIVE_BEFORE = '#1365B3'
LINE_COLOR_ACTIVE_AFTER = '#95C623'