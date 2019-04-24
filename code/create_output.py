
def apply_clustering(datafile, cluster_assignments, outfile):
    data = {}
    sample_info = {}
    anatomical_site_info = {}
    with open(datafile, "r") as f:
        a = f.readline().split()[0] # number of anatomical sites
        m = f.readline().split()[0] # number of samples
        n = f.readline().split()[0] # number of mutations
        header = f.readline().split() # header
        for line in f:
            tkns = line.split()
            sample_idx = int(tkns[0])
            sample_label = tkns[1]
            site_idx = tkns[2]
            site_label = tkns[3]
            # Store information about each sample
            sample_info[sample_idx] = sample_label, site_idx, site_label

            mut = tkns[-3]
            ref = int(tkns[-2])
            var = int(tkns[-1])
            data[sample_idx, mut] = ref, var

    cluster_to_muts = {} # map from cluster index to list of mutations
    idx = 0
    with open(cluster_assignments, "r") as f:
        for line in f:
            tkns = line.strip().split(';')
            assert idx not in cluster_to_muts
            cluster_to_muts[idx] = tkns
            idx += 1

    # Create output file
    rows = []
    rows.append([a + " # anatomical sites"])
    rows.append([m + " # samples"])
    rows.append([n + " # mutations"])
    rows.append(header)
    for sample_idx in range(int(m)):
        sample_label, site_idx, site_label = sample_info[sample_idx]
        for cl_idx in range(idx):
            total_ref = sum([data[sample_idx, x][0] for x in cluster_to_muts[cl_idx]])
            total_var = sum([data[sample_idx, x][1] for x in cluster_to_muts[cl_idx]])
            myrow = [sample_idx, sample_label, site_idx, site_label, cl_idx, ";".join(cluster_to_muts[cl_idx]), total_ref, total_var]
            rows.append([str(x) for x in myrow])

    with open(outfile, "w") as f:
        f.write('\n'.join(['\t'.join(row) for row in rows]))

if __name__ == "__main__":
    import sys
    datafile = sys.argv[1]
    cluster_assignments = sys.argv[2]
    outfile = sys.argv[3]
    apply_clustering(datafile, cluster_assignments, outfile)
