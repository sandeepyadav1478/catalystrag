import pandas as pd

loc = "client_data/kaggle_Finance_data.csv"

# Load CSV file
def upload_data(location=loc) -> object:
    return pd.read_csv(location)