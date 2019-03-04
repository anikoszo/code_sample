import os

try:
    os.system('python 1_Index_table_creator\\test_defs.py')
    print('\nFIRST STEP: Enrich data,define Clusters')
    os.system('python 1_define_clusters.py')
    print('\nSECOND STEP: Group train data')
    os.system('python 2_group_train_data.py')
    print('\nTHIRD STEP: Test file creation')
    os.system('python 3_create_test_file.py')
    print('\nFOURTH STEP: Decision Tree')
    os.system('python 4_classify.py')

    print('\nAll the created files is on the local .sqlite database\n'
          ' you can check it with opensource http://sqlitebrowser.org')

except ValueError():
    print('It seems to be IMPOSSIBLE')
