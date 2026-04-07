import pandas as pd

def create_features(df):
    df['hour'] = df['trans_date_trans_time'].dt.hour
    df['day_of_week'] = df['trans_date_trans_time'].dt.dayofweek
    df['age'] = (df['trans_date_trans_time'] - df['dob']).dt.days // 365

    return df


def encode_data(train, test):
    low_card_cols = ['category', 'gender', 'state']
    high_card_cols = ['merchant', 'city', 'job']

    train = pd.get_dummies(train, columns=low_card_cols, drop_first=True)
    test = pd.get_dummies(test, columns=low_card_cols, drop_first=True)

    train, test = train.align(test, join='left', axis=1, fill_value=0)

    encoding_maps = {}

    for col in high_card_cols:
        freq = train[col].value_counts(normalize=True)
        encoding_maps[col] = freq.to_dict()

        train[col] = train[col].map(freq)
        test[col] = test[col].map(freq).fillna(0)

    return train, test, encoding_maps


# ✅ NEW FUNCTION (for inference)
def encode_single(df, encoding_maps):
    low_card_cols = ['category', 'gender', 'state']
    high_card_cols = ['merchant', 'city', 'job']

    df = pd.get_dummies(df, columns=low_card_cols, drop_first=True)

    for col in high_card_cols:
        freq_map = encoding_maps.get(col, {})
        df[col] = df[col].map(freq_map).fillna(0)

    return df