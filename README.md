# Sparse Frequency Clustering

## Overview

This code paritions mutations according to the samples that they are present in, runs a clustering algoritm on each partition,
then merges the resulting set of clusters. 

## Requirements
- snakemake
- python2
- pyclone

## Basic example

A full example can be found in the `example` directory.
Input data is provided as `example/input.tsv`.

To run the example:

    ```
    cd code
    snakemake --configfile ../example/example.config --cores 30
    ```

This will produce an output file `example/results/cluster_assignments.txt`. 

## Basic usage

The clustering pipeline is run using snakemake. To begin, `cd` into the `code/` directory. 
Required parameters:

- `input`: The input file in SPRUCE format
- `outdir`: The output directory. This directory will be created if one does not exist. This directory should be unique for
            each separate dataset. 


These parameters can be provided via command line,

`snakemake --config input='../example/input.tsv' outdir='../example/results'`

or using a configration file,

`snakemake --configfile ../example/example.config`

The output of the pipeline is `{outdir}/cluster_assignments.txt`. Here, each line will correspond to a cluster, and 
the semi-colon separated entries of each line correspond to charcter names provided in the input file. 
