import numpy as np
import config
import requests, json 

def get_group_queries(group, only_root=False):
    root_queries = config.TRENDS_DATA_GROUPS.get(group, [])
    extended_queries = config.TRENDS_DATA_GROUPS_EXTENDED_QUERIES.get(group, [])
    if only_root:
        return sorted(list(np.unique(root_queries)))
    else:
        return sorted(list(np.unique(root_queries + extended_queries)))

def get_data_dir(group):
    return "%s/%s" % (config.TRENDS_DATA_DIR, group)

def get_data_filename(group, query, country="US", state=None, full=False):
    filename = f"{country}_{'All' if not state else state}_{query.lower().replace(' ', '_')}"
    if full:
        data_dir = get_data_dir(group)
        return "%s/%s.csv" % (data_dir, filename)
    else:
        return filename

def get_suggestion_terms(term):
    URL="http://suggestqueries.google.com/complete/search?client=firefox&q=%s" % term 
    headers = {'User-agent':'Mozilla/5.0'} 
    response = requests.get(URL, headers=headers) 
    result = json.loads(response.content.decode('utf-8')) 
    return result