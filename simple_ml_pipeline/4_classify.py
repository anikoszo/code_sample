import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier

from defs import sqlite_connect
from sklearn.metrics import recall_score, precision_score

db_name = 'customer.sqlite'

test = pd.read_sql('''
                    SELECT *
                    FROM example_dat_2014''',
                   sqlite_connect(db_name))

train = pd.read_sql('''
                    SELECT *
                    FROM tr_dat_with_clusters_grouped
                    ''', sqlite_connect(db_name))

# add flags
train['flag'] = 'Train'
test['flag'] = 'Test'

print(len(train), len(test))
train['Clusters'] = train['Clusters'].astype(str)
test['Clusters'] = train['Clusters'].astype(str)
del test['counter']
del train['counter']
all_dat = pd.concat([train, test], axis=0)

cat_cols = ['amount',
            'purchase_day',
            'purchase_month',
            'purchase_year']

x_train = train[list(cat_cols)].values
y_train = train['Clusters'].values
x_validate = test[list(cat_cols)].values
y_validate = test['Clusters'].values
x_test = test[list(cat_cols)].values

# random.seed(100)

rf = GradientBoostingClassifier(n_estimators=100, random_state=1, learning_rate=0.5)
rf.fit(x_train, y_train)
tr_pred = rf.predict(x_train)
ts_pred = rf.predict(x_test)

recallt = recall_score(y_validate, ts_pred, pos_label='0')
recalltr = recall_score(tr_pred, y_train, pos_label='0')
prect = precision_score(y_validate, ts_pred, pos_label='0')
prectr = precision_score(tr_pred, y_train, pos_label='0')

print('Accuracy tr:', rf.score(X=x_train, y=y_train),
      "\nAccuracy test:", rf.score(X=x_validate, y=y_validate),
      "\nRecall t: %.2f%%" % (recallt * 100), "\n Prec t: %.2f%%" % (prect * 100),
      "\nRecall tr: %.2f%%" % (recalltr * 100), "\n Prec tr: %.2f%%" % (prectr * 100),
      "\nPrec t: %.2f%%" % (recallt * 100), "\n Prec t: %.2f%%" % (prect * 100),
      "\nPrec tr: %.2f%%" % (recalltr * 100), "\n Prec tr: %.2f%%" % (prectr * 100))

test = test[['purchase_year',
             'purchase_month',
             'purchase_day',
             'Clusters'
             ]]
test.to_sql('predictions_2014', index=False, if_exists='replace'
            , con=sqlite_connect(db_name))
