import os
from utils.places import load_places

ROOT_DIR = os.getcwd()

DATA_DIR = "%s/data" % ROOT_DIR
FIGURES_DIR = "%s/figures" % ROOT_DIR
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
TRENDS_FIGURES_DIR = "%s/trends" % FIGURES_DIR
TRENDS_DATA_GROUPS = {
    'anxiety': ['anxiety', 'anxious', 'fearful', 'frighten', 'hypervigilant', 'nervous', 'panic', 'phobia',
                'phobic', 'scared', 'stress', 'tense', 'worried'],
    'depression': ['depressed', 'depressive', 'dysphoric', 'dysthymic', 'sad', 'tearful'],
    'suicide': ['suicide', 'suicidal', 'suicidality', 'suicide prevention', 'suicide methods'],
    'psychosis': ['psychotic', 'psychosis', 'hallucination', 'delusion', 'paranoid', 'paranoia', 
                'hallucinate', 'hallucinated', 'delusional'],
    'violence': ['psychosis', 'violence', 'violent']
}

TRENDS_FORCE_RELOAD_GROUPS = {
    'anxiety': False,
}

TRENDS_DATA_GROUPS_MAIN_TERM = {
    'anxiety': 'anxiety',
}

TRENDS_DATA_GROUPS_EXCLUDED_QUERIES = {
}

TRENDS_DATA_GROUPS_REPLACED_QUERIES = {
    'anxiety': {
        'symptoms': 'anxiety symptoms',
    },
    'disorder': {
        'symptoms': 'disorder symptoms',
    }
}


TRENDS_DATA_GROUPS_EXTENDED_QUERIES = {
    'anxiety': [],
    'depression': ['quarantine depression'],
    # https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6747463/
    'suicide': ['suicide', 'suicidal', 'suicide methods', 'how to commit suicide',       # Root terms
                'commit suicide', 'i want to die', 'suicidality', 'suicide attempt',     # Tran et al. 
                'suicide forum', 'suicidal ideation', 'suicidal thoughts',
                'suicide hotline', 'how to hang yourself', 'how to kill yourself',
                'feeling down', 'crisis text line',
                'painless suicide', 'suicide by jumping',  # https://sci-hub.tw/10.1371/journal.pone.0183149
                'suicide help', 'suicide hotline', 'how to overdose',
                'online suicide', 'suicide chat', 'suicide method'
    ]
}

TRENDS_FORCE_REDOWNLOAD_RELATED_TOPICS = False
TRENDS_FORCE_REDOWNLOAD_TRENDS = False
TRENDS_DOWNLOAD_DELAY_SECONDS = 2
TRENDS_EXPORT_FIGURES = True

TRENDS_APPLY_NORMALIZATION = True