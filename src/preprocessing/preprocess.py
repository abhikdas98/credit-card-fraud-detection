import pandas as pd


def preprocess_data(df):
    df['trans_date_trans_time'] = pd.to_datetime(df['trans_date_trans_time'])
    df['dob'] = pd.to_datetime(df['dob'])

    df = df.drop(columns=['first', 'last', 'street', 'trans_num'])

    df = df.sort_values('trans_date_trans_time')

    return df