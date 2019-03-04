import pandas as pd
from defs import del_cols, sqlite_connect

db_name = 'customer.sqlite'

tr_dat = pd.read_sql('''
                    SELECT * 
                    FROM tr_data_with_variables 
                    ''', con=sqlite_connect(db_name))

list_for_del = ['quantity', 'sales_amount', 'product_id']
tr_dat = del_cols(tr_dat, list_for_del)

cluster_dat = pd.read_sql('''
                            SELECT * 
                            FROM training_with_clusters
                            ''', con=sqlite_connect(db_name))
print(cluster_dat.describe())
print(cluster_dat.corr())

list_for_del_clust = ['amount', 'counter']
cluster = del_cols(cluster_dat, list_for_del_clust)
print(cluster.dtypes)
tr_dat_with_clust = pd.merge(tr_dat,
                             cluster,
                             on=['contact_id',
                                 'purchase_year',
                                 'purchase_month',
                                 'purchase_day'],
                             how='left', )

tr_dat_with_clust.to_sql('tr_dat_with_clusters',
                         if_exists='replace',
                         index=False,
                         con=sqlite_connect(db_name)
                         )

list_for_del_merged = ['contact_id', 'purchase_id', 'purchase_date', 'product_price']

tr_dat_with_clust = del_cols(tr_dat_with_clust, list_for_del_merged)

tr_dat_with_clust_gr = tr_dat_with_clust.groupby(
    by=['purchase_year', 'purchase_month', 'purchase_day', 'Clusters']
    , axis=0).sum().reset_index()

tr_dat_with_clust_gr.to_sql('tr_dat_with_clusters_grouped',
                            if_exists='replace',
                            index=False,
                            con=sqlite_connect(db_name)
                            )
