###
#   Merges result files and outputs the resulting clusters.
###

import sys

original_file = sys.argv[1]
input_files = sys.argv[2:]

import pandas as pd
orig = pd.read_csv(original_file, sep = '\t', skiprows=3)
orig = orig[orig['#sample_index'] == 0]
orig['mutation_id'] = orig['character_index']
orig = orig.set_index('mutation_id')


for filename in input_files:
    df = pd.read_csv(filename, sep = '\t').set_index('mutation_id')
    df = df.join(orig, how = 'inner')
    
    
    for cluster in df['cluster_id'].unique():
        #print "------"
        #print filename
        print(";".join(map(str, df[df['cluster_id'] == cluster]['character_label'].unique())))

