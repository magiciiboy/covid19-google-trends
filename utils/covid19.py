import pandas as pd
import config


def load_data_states(source="NYT"):
    df = None
    if source == "NYT":
        data_file = "%s/us-states.csv" % config.COVID19_NYT_DATA_DIR
        df = pd.read_csv(data_file)
        df["Country_Region"] = "US"
        df["Active"] = None
        df = df.rename(columns={"state": "Province_State", "date": "Date", "cases": "Confirmed"})
    elif source == "CSSE":
        data_file = "%s/UTD.csv" % config.COVID19_CSSE_DATA_DIR
        df = pd.read_csv(data_file)
        df = df.sort_values("Date")
    else:
        raise Exception("Unknown source. Got: %s. Accepted: NYT, CSSE" % source)

    assert "Country_Region" in df.columns, "Missing `Country_Region` column"
    assert "Province_State" in df.columns, "Missing `Province_State` column"
    assert "Date" in df.columns, "Missing `Date` column"
    assert "Confirmed" in df.columns, "Missing `Confirmed` column"
    assert "Active" in df.columns, "Missing `Active` column"
    return df

    
