import pandas as pd


def preprocess_data(df):
    # ✅ DEBUG (remove later)
    print("Columns before preprocess:", df.columns.tolist())

    # ✅ Convert datetime properly (fix warning too)
    df['trans_date_trans_time'] = pd.to_datetime(
        df['trans_date_trans_time'],
        format="%d-%m-%Y %H:%M"
    )

    df['dob'] = pd.to_datetime(
        df['dob'],
        format="%d-%m-%Y"
    )

    # ✅ Sort BEFORE using/dropping
    df = df.sort_values('trans_date_trans_time')

    # ❌ DO NOT DROP datetime columns here
    # Only drop unnecessary columns
    df = df.drop(columns=['first', 'last', 'street', 'trans_num'], errors='ignore')

    return df