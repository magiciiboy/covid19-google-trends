import config
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from datetime import datetime

from scripts.trends import get_data_filename, get_group_queries
from utils.io import mkdir_if_not_exist

# COVID_START_DATE = "2020-01-11"
COVID_START_DATE = "2020-01-12"
DATA_START_DATE = "2019-08-21"
DATA_END_DATE = "2020-08-21"
SOCIAL_DISTANCE_ORDER_DATE = "2020-03-16"


def plot_trends(group, country="US", state=None, place=None):
    print(f"* Plotting Google Trends of `{group}` for {country} - {state or 'All'}")
    group_queries = get_group_queries(group)

    n_queries = len(group_queries)
    n_cols = 5
    n_rows = int(n_queries / n_cols) + (1 if n_queries % n_cols else 0)

    # Initialize figure with subplots
    subplot_titles = ["%s..." % t[:22] if len(t) >= 22 else t for t in group_queries]
    fig = make_subplots(
        rows=n_rows, cols=n_cols, subplot_titles=subplot_titles,
        shared_yaxes=True
    )

    # Marked Dates
    covid_start_date = COVID_START_DATE
    data_start_date = DATA_START_DATE
    data_end_date = DATA_END_DATE

    for idx, query in enumerate(group_queries):
        row = int(idx / n_cols) + 1
        col = idx % n_cols + 1

        query_file_path = get_data_filename(group, query, country=country, state=state, full=True)
        df = pd.read_csv(query_file_path)
        count = df["date"].count()
        
        # No data
        if count == 0:
            continue

        # Process
        stayhome_order_date = place.get("ClosedFrom") if place else SOCIAL_DISTANCE_ORDER_DATE

        df = df[(df["date"] >= data_start_date) & (df["date"] <= data_end_date)]
        df_before = df[(df["date"] <= covid_start_date)]
        df_after = df[(df["date"] >= covid_start_date)]

        # Normalize
        if config.TRENDS_APPLY_NORMALIZATION:
            max_value = df[query].max()
            baseline = df_before[query].median()
            df["value"] = df[query].apply(lambda x: (x - baseline) / max_value)
            df_before["value"] = df_before[query].apply(lambda x: (x - baseline) / max_value)
            df_after["value"] = df_after[query].apply(lambda x: (x - baseline) / max_value)
        else:
            df["value"] = df[query]
            df_before["value"] = df_before[query]
            df_after["value"] = df_after[query]

        # Horizontal line 
        shape = go.layout.Shape(**{"type": "line","y0":0,"y1": 0,"x0":str(df["date"].values[0]), 
                    "x1":str(df["date"].values[-1]),"xref":"x1","yref":"y1",
                    "line": {"color": "rgb(200, 200, 200)","width": 1.5}})
        fig.add_shape(shape, row=row, col=col)

        # Stay home order
        if stayhome_order_date:
            shape_stayhome_order = go.layout.Shape(**{"type": "line","y0":-0.25,"y1": 0.25,"x0":stayhome_order_date, 
                    "x1":stayhome_order_date,"xref":"x1","yref":"y1",
                    "line": {"color": "blue","width": 1.5, "dash": "dot"}})
            fig.add_shape(shape_stayhome_order, row=row, col=col)

        # Plot
        subplot_before = go.Scatter(x=df_before["date"], y=df_before["value"], 
                            mode="lines",
                            line=dict(width=1, color=config.LINE_COLOR_BEFORE), 
                            line_shape="linear") # linear or spline 
        subplot_after = go.Scatter(x=df_after["date"], y=df_after["value"], 
                            mode="lines",
                            line=dict(width=1.5, color=config.LINE_COLOR_AFTER), 
                            line_shape="linear") # linear or spline 
        fig.add_trace(subplot_before, row=row, col=col)
        fig.add_trace(subplot_after, row=row, col=col)

    # Caption
    # caption = go.layout.Annotation(
    #     showarrow=False,
    #     text="",
    #     xanchor="center",
    #     x=0.5,
    #     yanchor="top",
    #     y=0.0,
    #     yshift=0,
    # )

    # Layout
    fig.update_layout(title={"text": f"Term: {group}<br> ({data_start_date} - {data_end_date})", "x":0.5, "xanchor": "center"}, 
                    height=300 + n_rows * 175, width=250 * n_cols, coloraxis=dict(colorscale="Bluered_r"), 
                    showlegend=False, plot_bgcolor="rgb(255,255,255)", titlefont={"size": 30},
                    margin={"t": 200}
                    # annotations=[caption]
                    )
    fig.update_xaxes(showgrid=False, showticklabels=False, showline=False)
    fig.update_yaxes(showgrid=False, showticklabels=False, showline=False, range=[-1, 1])

    if config.TRENDS_EXPORT_FIGURES:
        # Save
        mkdir_if_not_exist(config.TRENDS_FIGURES_DIR)
        fig.write_image("%s/%s_%s_%s.jpg" % (config.TRENDS_FIGURES_DIR, country, state or "All", group))
        # fig.show()
    else:
        # Show
        fig.show()