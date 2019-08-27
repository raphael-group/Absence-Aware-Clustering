import sys

def pr_x(X, V, T, lam, eps):
    """
    Calculate the probability of X = x
    given V
    """
    if X == 0:
        return (1-lam)*binom.pmf(V,T, eps)
    elif X == 1:
        b = binom_coeff(T,V)
        
        if b == float('inf'): return float('inf')
        #bt = beta(1+V, 1+T-V)
        #print b, bt
        return lam * binom_coeff(T,V) * beta(1+V, 1+T-V)
    else:
        raise ValueError("X must be 0 or 1.")

def norm_pr_x(v, depth, lam, eps):
    """
    Calculate the normalized probability of x.
    Returns a tuple corresponding to the probability that x = 1,
    and the probablity that x = 0
    """

    p0 = pr_x(0, v, depth, lam, eps)
    p1 = pr_x(1, v, depth, lam, eps)

    if p1 == float('inf'):
        return 0, 1
    return p0/(p0 + p1), p1/(p0 + p1)

def partition_data(df, lam, eps, samples):
    probs = ['prob_{}'.format(i) for i in samples]


    # Input dataframe has 1 row per mutation & sample
    df['prob'] = df.apply(lambda x: norm_pr_x(x['var'], x['ref'] + x['var'], lam, eps)[1], axis = 1)
    df['prob_bin'] = (df['prob'] > 0.95).map(int).map(str)

    # Output is just in terms of mutations
    df_output = df[df['#sample_index'] == 0]
    #print df.groupby('character_index').sum()['prob_bin'].head()

    def get_profile(x):
        cid = x['character_index']
        profile = "".join(list(df[df['character_index'] == cid].sort_values(by='#sample_index')['prob_bin']))
        return "p-"+profile

    
   
    
    df_output['profile'] = df_output.apply(get_profile, axis=1)
    
    return df_output[['character_index', 'profile']]

if len(sys.argv) != 3:
    print("Usage: {} [Input File] [Output Directory]")


input_file = sys.argv[1]
output_filename = sys.argv[2]

print("Reading in data from:", input_file)

import pandas as pd
from scipy.stats import binom
from scipy.special import binom as binom_coeff
from scipy.special import beta

###
#  Parameters
###
#TODO: Pull these out as parameters
lam = 0.5
#eps = 0.0001
eps = 0.001


df = pd.read_csv(input_file, sep = '\t', skiprows = 3)
samples = df['#sample_index'].unique()
print("PARTITION -- Found {} samples: {}".format(len(samples), samples))
df = partition_data(df, lam, eps, samples) 
profiles = df['profile'].unique()
print("PARTITION -- Found {} profiles: {}".format(len(profiles), profiles))
print("PARTITION -- Writing out binary assignments to:", output_filename)
df.to_csv(output_filename, sep = '\t', index = False)



