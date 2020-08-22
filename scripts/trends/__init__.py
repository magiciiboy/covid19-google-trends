import numpy as np
import config

def get_group_queries(group):
    default_queries = config.TRENDS_DATA_GROUPS.get(group, [])
    extended_queries = config.TRENDS_DATA_GROUPS_EXTENDED_QUERIES.get(group, [])
    return sorted(list(np.unique(default_queries + extended_queries)))

def get_data_dir(group):
    return "%s/%s" % (config.TRENDS_DATA_DIR, group)

def get_data_filename(group, query, country="US", state=None, full=False):
    filename = f"{country}_{'All' if not state else state}_{query.lower().replace(' ', '_')}"
    if full:
        data_dir = get_data_dir(group)
        return "%s/%s.csv" % (data_dir, filename)
    else:
        return filename