from plotly.subplots import make_subplots
import plotly.graph_objects as go
from datetime import datetime

import config

def plot_covid19_cases(df_all, country="US", level="state", start_date=None, end_date=None):
    all_places = config.PLACES
    places = {k:all_places[k] for k in config.PLACES if all_places[k]["Country"]==country}
    places_keys = sorted(places.keys())
    places_names = [places[k]["State"] for k in places]

    df_all = df_all[(df_all["Country_Region"]==country) & (df_all["Province_State"].isin(places_names))]
    if start_date:
        df_all = df_all[df_all["Date"] >= start_date]
    if end_date:
        df_all = df_all[df_all["Date"] <= end_date]

    n_places = len(places_keys)
    n_cols = 1
    n_rows = int(n_places / n_cols) + (1 if n_places % n_cols else 0)
    max_cases = df_all["Confirmed"].max()
    min_date = df_all["Date"].min()
    max_date = df_all["Date"].max()

    # Initialize figure with subplots
    subplot_titles = [f"<b>{places[k]['State']}</b><br>Population={places[k]['Population']:,}" for k in places]
    fig = make_subplots(
        rows=n_rows, cols=n_cols, subplot_titles=subplot_titles,
        shared_yaxes=True, 
        shared_xaxes=True
    )

    for idx, place_key in enumerate(places_keys):
        place = places[place_key]
        place_name = place["State"]
        close_date = place["ClosedFrom"]
        open_date = place["ClosedTo"]

        row = int(idx / n_cols) + 1
        col = idx % n_cols + 1

        df = df_all[df_all["Province_State"] == place_name]
        # Process
        df_before = df[(df["Date"] < close_date)]
        df_after = df[(df["Date"] >= close_date)]
        close_date_data = df[df["Date"]==close_date]["Confirmed"].unique()
        close_date_cases = close_date_data[0] if close_date_data else 0

        # Horizontal line
        shape_close_date_line = go.layout.Shape(**{"type": "line",
                    "y0": 0,"y1": 0.9 * max_cases,"x0":close_date, "x1":close_date,
                    "line": {"color": "red","width": 1.5, "dash": "dot"}})
        shape_open_date_line = go.layout.Shape(**{"type": "line",
                    "y0": 0,"y1": 0.9 * max_cases,"x0":open_date, "x1":open_date,
                    "line": {"color": "green","width": 1.5, "dash": "dot"}})
        fig.add_shape(shape_close_date_line, row=row, col=col)
        fig.add_shape(shape_open_date_line, row=row, col=col)

        close_date_anno = go.layout.Annotation(showarrow=False, text=f"{close_date}",
            xanchor="right", x=close_date, yanchor="middle", y=max_cases/2, yshift=0, textangle=-90)
        close_date_cases_anno = go.layout.Annotation(showarrow=False, text=f"{place['OrderType']}<br>n = {close_date_cases}",
            xanchor="left", x=close_date, yanchor="middle", y=max_cases/2, yshift=0, textangle=-90)
        fig.add_annotation(close_date_anno, row=row, col=col)
        fig.add_annotation(close_date_cases_anno, row=row, col=col)

        open_date_anno = go.layout.Annotation(showarrow=False, text=f"{open_date}",
            xanchor="right", x=open_date, yanchor="middle", y=max_cases/2, yshift=0, textangle=-90)
        open_date_cases_anno = go.layout.Annotation(showarrow=False, text=f"Reopen",
            xanchor="left", x=open_date, yanchor="middle", y=max_cases/2, yshift=0, textangle=-90)
        fig.add_annotation(open_date_anno, row=row, col=col)
        fig.add_annotation(open_date_cases_anno, row=row, col=col)

        # Plot
        subplot_confirmed_before = go.Scatter(x=df_before["Date"], y=df_before["Confirmed"], 
                            mode="lines",
                            line=dict(width=1, color=config.LINE_COLOR_BEFORE), 
                            line_shape="linear") # linear or spline 
        subplot_confirmed_after = go.Scatter(x=df_after["Date"], y=df_after["Confirmed"], 
                            mode="lines",
                            line=dict(width=1.5, color=config.LINE_COLOR_AFTER), 
                            line_shape="linear") # linear or spline 
        
        subplot_active_before = go.Scatter(x=df_before["Date"], y=df_before["Active"], 
                            mode="lines",
                            line=dict(width=1, color=config.LINE_COLOR_ACTIVE_BEFORE), 
                            line_shape="linear") # linear or spline 
        subplot_active_after = go.Scatter(x=df_after["Date"], y=df_after["Active"], 
                            mode="lines",
                            line=dict(width=1.5, color=config.LINE_COLOR_ACTIVE_AFTER), 
                            line_shape="linear") # linear or spline 

        fig.add_trace(subplot_confirmed_before, row=row, col=col)
        fig.add_trace(subplot_confirmed_after, row=row, col=col)
        fig.add_trace(subplot_active_before, row=row, col=col)
        fig.add_trace(subplot_active_after, row=row, col=col)

    # Layout
    fig.update_layout(title={"text": "COVID19 - %s" % (country), "x":0.5, "xanchor": "center"}, 
                    height=n_rows * 375, width=800 * n_cols, coloraxis=dict(colorscale="Bluered_r"), 
                    showlegend=False, plot_bgcolor="white", titlefont={"size": 30},
                    margin={"t": 200}
                    )
    fig.update_xaxes(showgrid=False, showticklabels=True, showline=True, linecolor='grey', range=[min_date, max_date])
    fig.update_yaxes(showgrid=False, showticklabels=True, showline=True, linecolor='grey', range=[0, max_cases])

    # Save
    # fig.write_image("%s/%s/All/covid19.png" % (config.FIGURES_DIR, country))

    # Show
    fig.show()

