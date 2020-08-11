import pandas as pd
import config

def load_NYT_data():
    data_file = "%s/us-states.csv" % config.COVID19_NYT_DATA_DIR
    df = pd.read_csv(data_file)
    df["Country_Region"] = "US"
    df["Active"] = None
    df = df.rename(columns={"state": "Province_State", "date": "Date", "cases": "Confirmed"})
    return df

def load_CSSE_data():
    data_file = "%s/UTD.csv" % config.COVID19_CSSE_DATA_DIR
    df = pd.read_csv(data_file)
    df = df.sort_values("Date")
    # Clean
    invalid_data = df[df["Active"] > df["Confirmed"]][["Date", "Province_State", "Active", "Confirmed"]]
    for idx in invalid_data.index:
        df.loc[idx, ["Active"]] = df.loc[idx, ["Confirmed"]]
    return df

def load_data_states(source="NYT"):
    df = None
    if source == "NYT":
        df = load_NYT_data()
    elif source == "CSSE":
        df = load_CSSE_data()
    elif source == "MERGE":
        # As data of CSSE is from April 12
        # We merge data of NYT before April 12 to CSSE data
        # In NYT data, there is no information of Active cases
        # Our assumption is Active = Confirmed on these dates before April 12
        columns = ["Country_Region", "Province_State", "Date", "Confirmed", "Active"]
        df_NYT = load_NYT_data()[columns]
        df_CSSE = load_CSSE_data()[columns]

        min_date = df_CSSE["Date"].min()
        df_NYT_filtered = df_NYT[df_NYT["Date"] < min_date]
        df_NYT_filtered["Active"] = df_NYT_filtered["Confirmed"]
        df = pd.concat([df_NYT_filtered, df_CSSE])
    else:
        raise Exception("Unknown source. Got: %s. Accepted: NYT, CSSE" % source)

    assert "Country_Region" in df.columns, "Missing `Country_Region` column"
    assert "Province_State" in df.columns, "Missing `Province_State` column"
    assert "Date" in df.columns, "Missing `Date` column"
    assert "Confirmed" in df.columns, "Missing `Confirmed` column"
    assert "Active" in df.columns, "Missing `Active` column"
    return df

    
