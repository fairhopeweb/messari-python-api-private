"""This module is dedicated to helpers for the Upshot class"""


import pandas as pd


def format_df(df_in: pd.DataFrame) -> pd.DataFrame:
    """format a typical DF from Upshot, replace date & drop duplicates

    Parameters
    ----------
       df_in: pd.DataFrame
           input DataFrame

    Returns
    -------
       DataFrame
           formated pandas DataFrame
    """

    # set date to index
    df_new = df_in
    if 'timestamp' in df_in.columns:
        df_new.set_index('timestamp', inplace=True)
        df_new.index = pd.to_datetime(df_new.index, unit='s', origin='unix')
        df_new.index = df_new.index.date

    # drop duplicates
    df_new = df_new[~df_new.index.duplicated(keep='last')]
    return df_new
