import sys


if len(sys.argv) != 5:
    print("Usage: {} [Input File] [Partition File] [Profile] [Output Directory]".format(sys.argv[0]))
    exit(1)


input_file = sys.argv[1]
partition_file = sys.argv[2]
profile = str(sys.argv[3])
out_dir = sys.argv[4]

profile_strip = profile.split('-')[-1]


print("ALL-0 INPUT -- Reading in data from:", input_file)
print("ALL-0 INPUT -- Reading in profiles from:", input_file)
print("ALL-0 INPUT -- Profile:", profile)

import pandas as pd

df = pd.read_csv(input_file, sep = '\t', skiprows = 3)
profs = pd.read_csv(partition_file, sep = '\t')

df = df.set_index('character_index')
profs = profs[profs['profile'] == profile].set_index('character_index')
df = df.join(profs, how = 'inner')
df['mutation_id'] = df.index
df['ref_counts'] = df['ref']
df['var_counts'] = df['var']
df['normal_cn'] = 2
df['major_cn'] = 1
df['minor_cn'] = 1
df = df[df['#sample_index'] == df['#sample_index'].unique()[0]]
df = df[['mutation_id', 'ref_counts', 'var_counts', 'normal_cn', 'major_cn', 'minor_cn']]
df['sample_id'] = 0
df['cluster_id'] = 0
df['cellular_prevalence'] = 0
df['cellular_prevalence_std'] = 0
df['variant_allele_frequency'] = 0

df = df[['mutation_id', 'sample_id', 'cluster_id', 'cellular_prevalence', 'cellular_prevalence_std', 'variant_allele_frequency']]


output_filename = "{}/{}/results.txt".format(out_dir, profile)

print("ALL-0 CLUSTERING -- Writing file to:", output_filename)
df.to_csv(output_filename, sep = '\t', index = False)












