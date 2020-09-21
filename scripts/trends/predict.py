import numpy as np
import scipy.stats
from statsmodels.tsa.arima.model import ARIMA
from pmdarima.arima.utils import ndiffs
from pmdarima.arima import auto_arima
from pandas import datetime

def mean_confidence_interval(data, confidence=0.95):
    a = 1.0 * np.array(data)
    n = len(a)
    m, se = np.mean(a), scipy.stats.sem(a)
    h = se * scipy.stats.t.ppf((1 + confidence) / 2., n-1)
    return m, m-h, m+h

def get_best_arima(y):
    d_kpss = ndiffs(y, test="kpss")
    d_adf = ndiffs(y, test="adf")
    d_pp = ndiffs(y, test="pp")

    d_min = min([d_kpss, d_adf, d_pp])
    d_max = min([d_kpss, d_adf, d_pp])
    
    # Params from Tran et al. works
    # p = 0:4
    # d = 0:1
    # q = 0:2
    # P = 0:1
    # D = 0:1
    # Q = 0:1

    model = auto_arima(y, 
            start_p=0, max_p=4, 
            d=None, max_d=1, 
            start_q=0, max_q=5,
            start_P=0, max_P=1, 
            D=None, max_D=1,
            start_Q=0, max_Q=1,
            # seasonal=False, m=52,
            maxiter=100,
            n_jobs=1)
    print("Model order:", model.get_params()["order"])
    return model


def arima_predict(df, from_date, value_col="value", date_col="date", num_predictions=None, period="week",
                order=(1,0,0)):
    new_df = df
    # print("Columns:", df.columns)
    history_df = df[df[date_col] <= from_date]
    future_df = df[df[date_col] > from_date]

    if num_predictions is not None:
        assert future_df[date_col].count() >= num_predictions
    else:
        num_predictions = int(future_df[date_col].count())

    history = list(history_df[value_col].to_numpy())
    history_len = len(history)
    future = list(future_df[value_col].to_numpy())
    predictions = []

    # Fit model
    # for i in range(0, num_predictions):
    #     model = ARIMA(history, order=order)
    #     model_fit = model.fit()
    #     # print(model_fit.summary())
    #     output = model_fit.forecast()
    #     yhat = output[0]
    #     predictions.append(yhat)
    #     # history.append(future[i])
    #     history.append(yhat)

    # Fit model
    model = get_best_arima(history)
    new_values = list(model.predict(n_periods=num_predictions))
    predictions += new_values

    # Mark row has been predicted
    series_predictions = [0 for i in range(0, history_len)] + predictions + [0 for i in range(0, len(future) - num_predictions)]
    series_is_predicted = [0 for i in range(0, history_len)] + [1 for i in range(0, num_predictions)] + [0 for i in range(0, len(future) - num_predictions)]

    new_df["prediction"] = series_predictions
    new_df["is_predicted"] = series_is_predicted
    # print(predictions)
    return new_df, model