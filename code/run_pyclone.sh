
profile=$1
out_dir=$2
filelist=$3

files=`grep $profile $filelist`
samples=`echo $files | xargs -n 1 basename | cut -f 2  -d "."`
echo $samples
echo $files

PyClone setup_analysis --in_files $files --samples $samples --working_dir $out_dir/$profile --num_iters 10000 --init_method connected --config_extras_file config/pyclone_config_extras_1.5.yaml
PyClone run_analysis --config_file $out_dir/$profile/config.yaml --seed 1
PyClone build_table --config_file $out_dir/$profile/config.yaml --out_file $out_dir/$profile/result.txt --table_type loci

