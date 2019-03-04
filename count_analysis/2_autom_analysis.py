import pandas as pd
import glob
import datetime

from count_analysis.defs.defs import sqlite_connect, autom_analyse, write_to_db

start = datetime.datetime.now()
print(f'Start at: ', start)

db_path = glob.glob('*.sqlite')
conn = sqlite_connect(db_path[0])

data = pd.read_sql("""
                SELECT *
                FROM
                test_new_table
                """, con=conn)

# generate variables
test_df = data
test_df['All_sales($)'] = test_df['Unit Price'] * test_df.Quantity

analysis = autom_analyse(test_df,
                         measure='All_sales($)',
                         category_cols=['Location', 'Product'],
                         dependencies={'Product': 'Color'})
write_to_db(analysis, 'Quantity_unknown_cols', conn)
