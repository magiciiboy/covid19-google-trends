import os
from utils.places import load_places

ROOT_DIR = os.getcwd()

DATA_DIR = "%s/data" % ROOT_DIR
COVID19_DATA_SOURCE = "MERGE" #  NYT, CSSE, or MERGE
COVID19_NYT_DATA_DIR = "%s/covid-19-data" % DATA_DIR
COVID19_CSSE_DATA_DIR = "%s/COVID-19/csse_covid_19_data/csse_covid_19_daily_reports_us/" % DATA_DIR

PLACES = load_places(DATA_DIR)

# Plots
FIGURES_DIR = "%s/figures" % ROOT_DIR
LINE_COLOR = "rgb(130, 130, 130)"

LINE_COLOR_BEFORE = "#2375B3"
LINE_COLOR_AFTER = "#9D433C"

LINE_COLOR_ACTIVE_BEFORE = "#1365B3"
LINE_COLOR_ACTIVE_AFTER = "#95C623"

# Trends
TRENDS_DATA_DIR = "%s/trends" % DATA_DIR
TRENDS_DATA_GROUPS = {
    'job': ['employment', 'unemployment'],
    'anxiety': ['agitated', 'dread', 'overwhelming', 'sweat', 'anxiety', 'fear',
                'fatigue', 'panic', 'sweaty', 'anxious', 'headache', 'phobia', 
                'worry', 'back pain', 'insomnia', 'restless', 'worst', 'death', 
                'lightheadedness', 'sensitive', 'distress', 'muscle tension', 
                'sleep disorder', 'dizziness', 'nervous', 'stomach pain', 'anxious'],
    'disorder': ['anxiety', 'disorder', 'phobia', 'ptsd', 'anxiety disorder', 
                 'panic disorder', 'phobias', 'sleeping disorder'],
    'medication': ['antidepresant', 'klonopin', 'prozac', 'ssris', 'xanax', 'benzo', 
                   'lexapro', 'ssri', 'valium', 'zoloft'],
    'suicide': ['alcohol', 'drug', 'gun', 'reckless', 'unbearable', 
               'death', 'drugs', 'hopeless', 'suicide prevention', 'suicide methods'],
    'crypto': [],
    'memory': [],
    'opioid': ['opioid', 'drug', 'heroin', 'fentanyl', 'pain relievers', 'hydrocodone', 'codeine',
               'oxycodone', 'morphine']
}

FORCE_RELOAD_GROUPS = {
    'job': False,
    'anxiety': False,
    'disorder': False,
    'medication': False,
    'suicide': False,
    'crypto': False,
    'memory': False,
    'opioid': False,
}

TRENDS_DATA_GROUPS_MAIN_TERM = {
    'job': 'job',
    'anxiety': 'anxiety',
    'disorder': 'disorder',
    'medication': 'anxiety medication',
    'suicide': 'suicide',
    'crypto': 'crypto',
    'memory': 'memory',
    'opioid': 'opioid',
}

TRENDS_DATA_GROUPS_EXCLUDED_QUERIES = {
    'job': ['btc', 'bmw', 'benz', 'binance', 'apple', 'job lot'],
    'anxiety': ['dog anxiety'],
    'disorder': [],
    'medication': ['depression', 'depression and anxiety', 'anxiety disorder', 'dog anxiety'],
    'suicide': ['suicide squad', 'the suicide squad', 'suicide boys', 'suicide squad 2', 'joker', 
                'joker suicide squad', 'suicide lyrics', 'suicide squad cast', 
                'epstein suicide', 'harley quinn', 'suicide number', 'epstein', 
                'harley quinn suicide squad', 'suicidal'],
    'crypto': [],
    'memory': [],
    'opioid': [],
}

TRENDS_DATA_GROUPS_REPLACED_QUERIES = {
    'job': {},
    'anxiety': {
        'symptoms': 'anxiety symptoms',
    },
    'disorder': {
        'symptoms': 'disorder symptoms',
    },
    'medication': {},
    'suicide': [],
    'crypto': [],
    'memory': [],
    'opioid': [],
}


TRENDS_DATA_GROUPS_EXTENDED_QUERIES = {
    'job': [],
    'anxiety': [],
    'disorder': [],
    'medication': [],
    'suicide': [],
    'crypto': [],
    'memory': [],
    'opioid': [],
}

FORCE_REDOWNLOAD_RELATED_TOPICS = False
FORCE_REDOWNLOAD_TRENDS = False