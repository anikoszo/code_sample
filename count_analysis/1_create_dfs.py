import datetime
from count_analysis.defs.defs import *

start = datetime.datetime.now()
print(f'Start at: ', start)

db_name = 'test_db.sqlite'
conn = sqlite_connect(db_name)

# predefine  data
data_1 = {'Location': ['Chicago', 'Los Angeles', 'Los Angeles', 'Los Angeles', 'San Francisco', 'San Francisco']
    , 'Product': ['iPhone', 'iPhone', 'Mac Book',
                  'Mac Book', 'Mac Book', 'iPhone']
    , 'Quantity': [1, 1, 1, 1, 2, 3, ]
    , 'Unit Price': [1000, 1000, 2000, 2000, 2000, 1000]}

data_2 = {'Location': ['Chicago', 'Los Angeles', 'Los Angeles', 'Los Angeles', 'San Francisco', 'San Francisco']
    , 'Product': ['iPhone', 'iPhone', 'Mac Book',
                  'Mac Book', 'Mac Book', 'iPhone']
    , 'Color': ['black', 'black', 'black', 'black', 'black', 'blue']
    , 'Quantity': [1, 1, 1, 1, 2, 3, ]
    , 'Unit Price': [1000, 1000, 2000, 2000, 2000, 1000]}

# make dataFrame
test_df = pd.DataFrame(data=data_1)
test_df2 = pd.DataFrame(data=data_2)

# push data to sqlite db
test_df.to_sql('test_table', if_exists='replace', con=conn)
test_df2.to_sql('test_new_table', if_exists='replace', con=conn)

end = datetime.datetime.now()
print(f'End at: ', end)
