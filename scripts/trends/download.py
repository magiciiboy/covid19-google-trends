import time
import os
import pandas as pd 
import numpy as np                       
from pytrends.request import TrendReq
import config
from scripts.trends import get_data_dir, get_data_filename, get_group_queries
from utils.io import mkdir_if_not_exist

def download_topics():
    for idx, group in enumerate(DATA_GROUPS.keys()):
        main_term = DATA_GROUPS_MAIN_TERM[group]
        pytrend.build_payload(kw_list=[main_term], timeframe='today 12-m', geo = 'US')
        print('Group: %s' % group)
        
        # Related topics
        df_topics_top = None
        df_topics_rising = None
        if not os.path.isfile('%s/topics/%s_top.csv' % (DATA_DIR, group)) or FORCE_REDOWNLOAD_RELATED_TOPICS \
            or FORCE_RELOAD_GROUPS[group]:
            print('- Fetching related topics data...')
            related_topic = pytrend.related_topics()
            df_topics_top = related_topic[main_term]['top']
            df_topics_rising = related_topic[main_term]['rising']

            df_topics_top.to_csv('%s/topics/%s_top.csv' % (DATA_DIR, group), index=False)
            df_topics_rising.to_csv('%s/topics/%s_rising.csv' % (DATA_DIR, group), index=False)
            print('- Saved!')
        else:
            print('- Related topics files existed.')
            df_topics_top = pd.read_csv('%s/topics/%s_top.csv' % (DATA_DIR, group))
            df_topics_rising = pd.read_csv('%s/topics/%s_rising.csv' % (DATA_DIR, group))

        # Related queries
        df_queries_top = None
        df_queries_rising = None
        if not os.path.isfile('%s/queries/%s_top.csv' % (DATA_DIR, group)) or FORCE_REDOWNLOAD_RELATED_TOPICS:
            print('- Fetching related queries data...')
            related_querie = pytrend.related_queries()
            df_queries_top = related_querie[main_term]['top']
            df_queries_rising = related_querie[main_term]['rising']

            df_queries_top.to_csv('%s/queries/%s_top.csv' % (DATA_DIR, group), index=False)
            df_queries_rising.to_csv('%s/queries/%s_rising.csv' % (DATA_DIR, group), index=False)
            print('- Saved!')
        else:
            print('- Related queries files existed.')
            df_queries_top = pd.read_csv('%s/queries/%s_top.csv' % (DATA_DIR, group))
            df_queries_rising = pd.read_csv('%s/queries/%s_rising.csv' % (DATA_DIR, group))

        # Select queries
        for q in df_queries_top['query']:
            if q in DATA_GROUPS_EXCLUDED_QUERIES[group]:
                continue
            if q in DATA_GROUPS_REPLACED_QUERIES[group]:
                q = DATA_GROUPS_REPLACED_QUERIES[group][q]
            DATA_GROUPS_EXTENDED_QUERIES[group] += [q]
            
        # Reduce downloading freq
        time.sleep(1)


def download_trends(country="US", state=None, timeframe="2019-01-01 2020-08-31"):
    pytrend = TrendReq()
    for group in config.TRENDS_DATA_GROUPS:
        group_queries = get_group_queries(group)
        delay = False
        for query in group_queries:
            query_file_name = get_data_filename(group, query, country=country, state=state)
            query_dir = get_data_dir(group)
            query_file_path = '%s/%s.csv' % (query_dir, query_file_name)
            if os.path.isfile(query_file_path) and not config.TRENDS_FORCE_REDOWNLOAD_TRENDS \
                and not config.TRENDS_FORCE_RELOAD_GROUPS.get(group):
                print('- File existed at %s' % query_file_path)
            else:
                delay = True
                mkdir_if_not_exist(query_dir)
                geo = country if not state else "%s-%s" % (country, state)
                pytrend.build_payload(kw_list=[query], timeframe=timeframe, geo = geo, ) # "today 5-y"
                df = pytrend.interest_over_time()
                df['date'] = df.index
                df.to_csv(query_file_path, index=False)
                print('- Saved: %s' % query_file_path)
        # Reduce downloading freq
        if delay:
            time.sleep(config.TRENDS_DOWNLOAD_DELAY_SECONDS)