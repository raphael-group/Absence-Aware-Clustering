import sys

if len(sys.argv) != 6:
    print(sys.argv)
    print("Usage: {} [Input File] [Profile file] [Profile] [Sample] [Output Directory]".format(sys.argv[0]))
    exit(1)


input_file = sys.argv[1]
profile_file = sys.argv[2]
profile = str(sys.argv[3])
sample = int(sys.argv[4])
out_dir = sys.argv[5]


profile_strip = profile.split('-')[-1]

if profile_strip[sample] == '0':
    exit()

output_filename = "{}/{}/input.{}.tsv".format(out_dir, profile, sample)

print("CLUSTERING INPUT -- Reading in data from:", input_file)
print("CLUSTERING INPUT -- Reading in profiles from:", input_file)
print("CLUSTERING INPUT -- Profile:", profile)
print("CLUSTERING INPUT -- Sample:", sample)

import pandas as pd

df = pd.read_csv(input_file, sep = '\t', skiprows = 3)
profs = pd.read_csv(profile_file, sep = '\t')

df = df[df['#sample_index'] == sample].set_index('character_index')
profs = profs[profs['profile'] == profile].set_index('character_index')
df = df.join(profs, how = 'inner')
df['mutation_id'] = df.index
df['ref_counts'] = df['ref']
df['var_counts'] = df['var']
df['normal_cn'] = 2
df['major_cn'] = 1
df['minor_cn'] = 1

df_out = df[['mutation_id', 'ref_counts', 'var_counts', 'normal_cn', 'major_cn', 'minor_cn']]

print("CLUSTERING INPUT -- Writing file to:", output_filename)
df_out.to_csv(output_filename, sep = '\t', index = False)












