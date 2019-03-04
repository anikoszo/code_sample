import sqlite3
import pandas as pd
import numpy as np
import itertools as it


def sqlite_connect(name):
    """
     create or connect to database
     :param name: database name
     :return: connection to database
     or create the database
    """
    conn = sqlite3.connect(name)
    return conn


def write_to_db(df, table_name, conn):
    df.to_sql(table_name, conn, if_exists='replace')


def aggregate_by_column(column, data_frame, measure):
    return data_frame.groupby(by=column)[
        measure].sum().reset_index().rename(
        columns={column: 'Analysis'})


def combine_cols(df, i):
    df['Analysis'] = df[i].astype(
        str).apply(
        lambda x: ' - '.join(x),
        axis=1)


def to_crosstab(category, df, measure):
    return pd.crosstab(columns=[df[x] for x in category],
                       index=df[category[0]],
                       aggfunc=np.sum,
                       values=df[measure],
                       margins=True, margins_name=measure,
                       dropna=False)


def autom_analyse(df, category_cols, measure, dependencies=None):
    """combined analysis for main cols"""
    categories = []
    for col in category_cols:
        if df[col].dtype == 'object':
            categories.append(col)

    combinations = it.combinations(categories, 2)

    combined_dfs = []
    for i in combinations:
        df_comb = to_crosstab(i, df, measure).T.reset_index().fillna(
            0)
        combine_cols(df_comb, list(i))
        df_comb = df_comb[['Analysis', measure]].reset_index(
            drop=True)
        combined_dfs.append(df_comb)

    df_comb = pd.concat(combined_dfs).drop_duplicates()

    """own analysis for main columns"""
    df_main_list = []
    for col in category_cols:
        df_main_list.append(
            aggregate_by_column(column=col, data_frame=df,
                                measure=measure))
    # concat all created df-s
    df_main = pd.concat(df_main_list)

    # analysis for dependent columns pairs
    if dependencies is not None:
        df_dep_list = []
        for i in [[k, v] for k, v in dependencies.items()]:
            df_dep = to_crosstab(i, df,
                                 measure).T.reset_index().fillna(0)
            combine_cols(df_dep, i)
            df_dep_list.append(df_dep)

        df_dep = pd.concat(df_dep_list, sort=False)
        df_dep = df_dep[['Analysis', measure]].reset_index(drop=True)
        df_dep = df_dep[:-1]
    else:
        df_dep = None

    # concatenate all generated df-s
    df_all = pd.concat([df_comb, df_main, df_dep]).reset_index(
        drop=True).set_index('Analysis').sort_values(by=measure)

    print(f'df analysis\n', df_all)
    return df_all
