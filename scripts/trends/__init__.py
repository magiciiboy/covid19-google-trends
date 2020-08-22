import config

def get_data_dir(group):
    return "%s/%s" % (config.TRENDS_DATA_DIR, group)

def get_data_filename(group, query, country="US", state=None, full=False):
    filename = f"{country}_{'All' if not state else state}_{query.lower().replace(' ', '_')}"
    if full:
        data_dir = get_data_dir(group)
        return "%s/%s" % (data_dir, filename)
    else:
        return filename