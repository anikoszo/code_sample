import pandas as pd
from sklearn.cluster import KMeans
import datetime


from defs import del_cols, sqlite_connect

'''
create local database for handling files 
during the analysis
'''

db_name = 'customer.sqlite'

start = datetime.datetime.now()

print(f'start:', start)
# read the training file
tr_dat = pd.read_csv('training.csv', delimiter=',',
                     converters={'order_id': str,
                                 'contact_id': str,
                                 'product_id': str,
                                 })

# some descriptive statistics about data
print(tr_dat.tail(10))
print('Len dataset:\n', len(tr_dat))
print('Simple description:\n', tr_dat.describe())
print('Unique values count:\n', tr_dat.apply(lambda x: len(x.unique())))
print('Len dataset:\n', len(tr_dat))
print('Data types:\n', tr_dat.dtypes)

# calculate additional variables to enrich data
tr_dat['amount'] = tr_dat.quantity * tr_dat.sales_amount
tr_dat['purchase_year'] = pd.DatetimeIndex(tr_dat['purchase_date']).year
tr_dat['counter'] = 1
tr_dat['product_price'] = tr_dat.sales_amount / tr_dat.quantity
tr_dat['purchase_month'] = pd.DatetimeIndex(tr_dat['purchase_date']).month
tr_dat['purchase_day'] = pd.DatetimeIndex(tr_dat['purchase_date']).weekday

print('Sum spend:', tr_dat['amount'].sum())

# write the new dataset to my local database
tr_dat.to_sql('tr_data_with_variables',
              if_exists='replace',
              index=False,
              con=sqlite_connect(name=db_name))

# define correlation between variables
tr_dat = pd.read_sql_query('''
                            SELECT *
                            FROM tr_data_with_variables
                            ''', con=sqlite_connect(db_name))

# create clusters with aggregate to contacts by time
list_of_del = ['sales_amount', 'quantity', 'purchase_id', 'product_price']

tr_dat = del_cols(tr_dat, list_of_del)

tr_dat = tr_dat.groupby(by=['contact_id',
                            'purchase_year',
                            'purchase_month',
                            'purchase_day']
                        , axis=0).sum().reset_index()

tr_dat.to_sql('grouped_contacts',
              if_exists='replace',
              index=False,
              con=sqlite_connect(db_name)
              )

correlation = tr_dat.corr()
correlation.to_sql('correlation_matrix',
                   if_exists='replace',
                   index=True,
                   con=sqlite_connect(db_name)
                   )
km = KMeans(random_state=0,n_clusters=2)
tr_new = tr_dat._get_numeric_data().dropna(axis=1)
km.fit(tr_new)
predict = km.predict(tr_new)
print(len(tr_dat))
tr_dat['Clusters'] = pd.Series(predict, index=tr_dat.index)

# tr_dat.to_csv('training_with_clusters.csv', index=False)
tr_dat.to_sql('training_with_clusters',
              if_exists='replace',
              index=False,
              con=sqlite_connect(db_name)
              )
end = datetime.datetime.now()
print('end:', end)
print('duration:', end - start)
