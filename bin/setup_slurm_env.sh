#!/bin/bash

set -e

#sanity check on arguments
if [ $# -lt 1 ] ; then
    echo "setup_slurm_env requires slurm job output file as input"
    exit 1
fi


slurm_job_output=$1
slurm_job_env=`echo $slurm_job_output | sed 's/\.out//'`.env
rm -f $slurm_job_env
touch $slurm_job_env
echo "#!/bin/bash" >> $slurm_job_env

#for env_var in `grep SLURM_ $slurm_job_output`; do
#    echo $env_var
#    key=`echo $env_var | sed 's/=.*//'`
#    var=`echo $env_var | sed 's/.*=//'`
#    echo "export $key=\"$var\"" >> $slurm_job_env
#done

filename=${PEGASUS_LLNL_WORK_HOME}/magpie.env
while read -r env_var
do
    echo $env_var
    if [[ $env_var == BASH_FUNC_module* ]]; then
	# hack to break as we don't need any variables
	# after that
	break
    fi
    key=`echo $env_var | sed 's/=.*//'`
    var=`echo $env_var | sed 's/.*=//'`
    echo "export $key=\"$var\"" >> $slurm_job_env
done < "$filename"

echo "Written out slurm environment variables to $slurm_job_env"
