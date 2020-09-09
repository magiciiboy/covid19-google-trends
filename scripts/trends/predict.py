from statsmodels.tsa.arima.model import ARIMA
from pandas import datetime

def arima_predict(df, from_date, value_col="value", date_col="date", num_predictions=None, period="week",
                order=(1,1,0)):
    new_df = df
    # print("Columns:", df.columns)
    history_df = df[df[date_col] <= from_date]
    future_df = df[df[date_col] > from_date]

    if num_predictions is not None:
        assert future_df[date_col].count() >= num_predictions
    else:
        num_predictions = future_df[date_col].count()

    history = list(history_df[value_col].to_numpy())
    history_len = len(history)
    future = list(future_df[value_col].to_numpy())
    predictions = []

    for i in range(0, num_predictions):
        model = ARIMA(history, order=order)
        model_fit = model.fit()
        # print(model_fit.summary())
        output = model_fit.forecast()
        yhat = output[0]
        predictions.append(yhat)
        # history.append(future[i])
        history.append(yhat)

    series_predictions = [0 for i in range(0, history_len)] + predictions + [0 for i in range(0, len(future) - num_predictions)]
    series_is_predicted = [0 for i in range(0, history_len)] + [1 for i in range(0, num_predictions)] + [0 for i in range(0, len(future) - num_predictions)]

    new_df["prediction"] = series_predictions
    new_df["is_predicted"] = series_is_predicted
    # print(predictions)
    return new_df