
from scipy.stats import ttest_ind
from statistics import mean, stdev
import pandas as pd
from scripts.trends import get_data_filename, get_group_queries

ROOT_TERMS = ['suicidal', 'suicide methods', 'how to commit suicide',                    # Root terms
                'commit suicide', 'i want to die', 'suicidality', 'suicide attempt',     # Tran et al. 
                'suicide forum', 'suicidal ideation', 'suicidal thoughts',
                'suicide hotline', 'how to hang yourself', 'how to kill yourself',]

group = 'suicide'
query_terms = get_group_queries(group)
query_terms = [t for t in query_terms if t in ROOT_TERMS]
country = 'US'
state = None

print(query_terms, len(query_terms))

def compare_ttest(d1, d2, group1="Group 1", group2="Group 2"):
    mean1 = round(mean(d1), 3)
    mean2 = round(mean(d2), 3)
    stdev1 = round(stdev(d1), 3)
    stdev2 = round(stdev(d2), 3)
    t, p = ttest_ind(d1, d2, equal_var=False)
    print(f"* Testing {group1} [{mean1}, {stdev1}] vs {group2} [{mean2}, {stdev2}]")
    print(f"\tP-value = {p}")
    if p < 0.1:
        sign = "slightly"
        if p < 0.01:
            sign = "significant"
        trend = f"{group1} > {group2}" if mean1 > mean2 else f"{group2} > {group1}"
        print(f"\t => {trend} ({sign})")
    else:
        print(f"\t => No significant difference")


for query in query_terms:
    query_file_path = get_data_filename(group, query, country=country, state=state, full=True)
    df = pd.read_csv(query_file_path, parse_dates=True)
    count = df["date"].count()
    # print(f"Total {count} data points of {round(count*7/375)} years")

    df2019 = df[(df['date'] >= '2019-03-15') & (df['date'] <= '2019-08-31')]
    df2020_P1 = df[(df['date'] >= '2020-01-01') & (df['date'] < '2020-03-15')]
    df2020_P2 = df[(df['date'] >= '2020-03-15') & (df['date'] <= '2020-08-31')]

    df2020_P2Early = df[(df['date'] >= '2020-03-15') & (df['date'] < '2020-06-01')]
    df2020_P2Late = df[(df['date'] >= '2020-06-01') & (df['date'] <= '2020-08-31')]

    print(f"\nT-test of `{query}`:")
    l2019 = df2019[query]
    l2020_P1 = df2020_P1[query]
    l2020_P2 = df2020_P2[query]
    l2020_P2Early = df2020_P2Early[query]
    l2020_P2Late = df2020_P2Late[query]

    # print(l2019, l2020_P1, l2020_P2)

    compare_ttest(l2019, l2020_P2, group1="2019", group2="2020")
    compare_ttest(l2020_P1, l2020_P2, group1="Before Lockdown", group2="After Lockdown")
    compare_ttest(l2020_P2Early, l2020_P2Late, group1="Early Lockdown", group2="Later Lockdown")
    
    # break



# # Term: suicide helpline
# print(f"T-test of `sucide helpline`:`")
# l2019 = [68, 77, 69, 73, 63, 68, 71, 67, 69, 68, 72, 77, 63, 71, 77, 61, 66, 56, 64, 54, 63, 66, 62, 72]
# l2020_P1 = [70, 75, 67, 72, 79, 76, 79, 73, 68, 69]
# l2020_P2 = [66, 69, 64, 72, 73, 80, 75, 74, 75, 76, 63, 66, 84, 80, 84, 79, 79, 87, 71, 68, 78, 76, 73, 93]

# t, p = ttest_ind(l2019, l2020_P2, equal_var=False)
# print(f"* P-value (2019 vs 2020 for Mar 15 - Aug 31): {p}")

# t, p = ttest_ind(l2020_P1, l2020_P2, equal_var=False)
# print(f"* P-value (Before vs After COVID19): {p}")

# # Term: commit suicide
# print(f"T-test of `commit suicide`:`")
# l2019 = [78, 80, 65, 59, 62, 65, 76, 67, 65, 69, 62, 69, 64, 61, 65, 54, 56, 58, 54, 59, 80, 89, 63, 64]
# l2020_P1 = [54, 69, 69, 68, 89, 66, 87, 72, 68, 69]
# l2020_P2 = [49, 55, 59, 59, 61, 62, 82, 63, 67, 56, 62, 100, 64, 83, 76, 76, 71, 76, 69, 65, 59, 52, 56, 54, 66]

# t, p = ttest_ind(l2019, l2020_P2, equal_var=False)
# print(f"* P-value (2019 vs 2020 for Mar 15 - Aug 31): {p}")

# t, p = ttest_ind(l2020_P1, l2020_P2, equal_var=False)
# print(f"* P-value (Before vs After COVID19): {p}")

# # Term: suicide methods
# print(f"T-test of `suicide methods`:`")
# l2019 = [74, 69, 63, 74, 54, 54, 42, 32, 65, 61, 72, 48, 49, 65, 45, 45, 76, 49, 62, 78, 60, 86, 53, 46]
# l2020_P1 = [48, 69, 71, 47, 65, 65, 60, 58, 66, 22]
# l2020_P2 = [26, 43, 25, 38, 58, 24, 53, 45, 34, 60, 48, 59, 30, 77, 100, 56, 56, 79, 52, 56, 42, 37, 37, 36, 57]

# t, p = ttest_ind(l2019, l2020_P2, equal_var=False)
# print(f"* P-value (2019 vs 2020 for Mar 15 - Aug 31): {p}")

# t, p = ttest_ind(l2020_P1, l2020_P2, equal_var=False)
# print(f"* P-value (Before vs After COVID19): {p}")

