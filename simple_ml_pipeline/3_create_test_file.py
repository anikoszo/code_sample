import pandas as pd
import datetime
import sqlite3

conn = sqlite3.connect('customer.sqlite')
cur = conn.cursor()
start = datetime.datetime.now()

example = pd.DataFrame()
date_2014 = datetime.date(2014, 1, 1)
example['purchase_date'] = [i for i in range(0, 365)]
example['purchase_date'] = example['purchase_date'] \
    .apply(lambda x: date_2014 +
                     datetime.timedelta(
                         x))

tr_dat_with_clust_gr = pd.read_sql('''
                                    SELECT purchase_month,
                                           purchase_day,
                                           avg(counter) AS counter,
                                           avg(amount) AS amount
                                    FROM tr_dat_with_clusters_grouped
                                    GROUP BY purchase_month,
                                             purchase_day
                                    ''',
                                   con=conn)
print(tr_dat_with_clust_gr)
example['purchase_year'] = pd.DatetimeIndex(example['purchase_date']).year
example['purchase_month'] = pd.DatetimeIndex(example['purchase_date']).month
example['purchase_day'] = pd.DatetimeIndex(example['purchase_date']).weekday
example['Clusters'] = '?'

del example['purchase_date']

example = pd.merge(example, tr_dat_with_clust_gr,
                   on=['purchase_month', 'purchase_day'],
                   how='left')

example = example.drop_duplicates()
example.to_sql('example_dat_2014',
               if_exists='replace',
               index=False,
               con=conn
               )


