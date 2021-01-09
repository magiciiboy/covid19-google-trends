
from math import sqrt
from scipy.stats import t
from scipy.stats import ttest_ind
from statistics import mean, stdev
import pandas as pd
from scripts.trends import get_data_filename, get_group_queries

group = 'suicide'
query_terms = get_group_queries(group, only_root=True)
country = 'US'
state = None

LOCKDOWN_DATE = "2020-03-16"
REOPEN_DATE = "2020-06-09" # 2020-06-09 https://www.nytimes.com/interactive/2020/us/states-reopen-map-coronavirus.html
ENDSTUDY_DATE = "2020-08-31"

print(query_terms, len(query_terms))

def compute_MoE(N1, N2, mean1, mean2, std1, std2, CI=0.95):
    df = (N1 + N2 - 2)
    std_N1N2 = sqrt( ((N1 - 1)*(std1)**2 + (N2 - 1)*(std2)**2) / df) 

    diff_mean = mean1 - mean2
    MoE = t.ppf(CI, df) * std_N1N2 * sqrt(1/N1 + 1/N2)
    return MoE

def compare_ttest(d1, d2, group1="Group 1", group2="Group 2"):
    CI = 0.95
    N1 = len(d1)
    N2 = len(d2)
    mean1 = round(mean(d1), 3)
    mean2 = round(mean(d2), 3)
    stdev1 = round(stdev(d1), 3)
    stdev2 = round(stdev(d2), 3)
    t, p = ttest_ind(d1, d2, equal_var=False)
    MoE = compute_MoE(N1, N2, mean1, mean2, stdev1, stdev2, CI=CI)
    diff_mean = mean2 - mean1

    print(f"* Testing {group1} [x̅={mean1}, s={stdev1}] vs {group2} [x̅={mean2}, s={stdev2}]")
    print("* Difference between {} vs {}: {:3.2f} [{:.0f}% CI ({:3.2f}, {:3.2f})]".format(group2, group1, diff_mean, CI * 100, diff_mean - MoE, diff_mean + MoE))
    print(f"\tP-value = {p}")
    if p < 0.05:
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
    df2019_P2Late = df[(df['date'] >= '2019-06-09') & (df['date'] <= '2019-08-31')]

    df2020_P1 = df[(df['date'] >= '2020-01-01') & (df['date'] <= LOCKDOWN_DATE)]
    df2020_P2 = df[(df['date'] > LOCKDOWN_DATE) & (df['date'] <= ENDSTUDY_DATE)]

    df2020_P2Early = df[(df['date'] > LOCKDOWN_DATE) & (df['date'] <= REOPEN_DATE)]
    df2020_P2Late = df[(df['date'] > REOPEN_DATE) & (df['date'] <= ENDSTUDY_DATE)]

    print(f"\nT-test of `{query}`:")
    l2019 = df2019[query]
    l2019_P2Late = df2019_P2Late[query]

    l2020_P1 = df2020_P1[query]
    l2020_P2 = df2020_P2[query]
    l2020_P2Early = df2020_P2Early[query]
    l2020_P2Late = df2020_P2Late[query]

    # print(l2019, l2020_P1, l2020_P2)

    # compare_ttest(l2019, l2020_P2, group1="2019", group2="2020")
    # compare_ttest(l2020_P1, l2020_P2, group1="Before Lockdown", group2="After Lockdown")
    # compare_ttest(l2020_P2Early, l2020_P2Late, group1="Early Lockdown", group2="Later Lockdown")

    compare_ttest(l2019_P2Late, l2020_P2Late, group1="2019 P2Late", group2="2020 P2Late")
    
    # break