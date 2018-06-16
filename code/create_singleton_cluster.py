import sys

if len(sys.argv) < 4:
    print "Usage: {} [Output Directory] [Profile] [List of Input Files]"
    exit(1)

out_dir = sys.argv[1]
profile = sys.argv[2]
input_files = sys.argv[3:]



import pandas as pd

try:
    df = pd.read_csv(input_files[0], sep = '\t')
except:
    exit()

df['sample_id'] = 0
df['cluster_id'] = 0
df['cellular_prevalence'] = 0
df['cellular_prevalence_std'] = 0
df['variant_allele_frequency'] = 0

df = df[['mutation_id', 'sample_id', 'cluster_id', 'cellular_prevalence', 'cellular_prevalence_std', 'variant_allele_frequency']]


output_filename = "{}/{}/results.txt".format(out_dir, profile)

print "SINGLETON CLUSTERING -- Writing file to:", output_filename
df.to_csv(output_filename, sep = '\t', index = False)












