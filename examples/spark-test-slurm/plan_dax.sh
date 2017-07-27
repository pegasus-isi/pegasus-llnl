#!/bin/bash

set -e

if [ $# -ne 1 ]; then
    echo "Usage: $0 DAXFILE"
    exit 1
fi

DAXFILE=$1
DIR=$(cd $(dirname $0) && pwd)

cat > $DIR/bin/spark-execute-script <<EOF
#!/bin/bash

# before launching the job switch to the directory that
# pegasus created for the workflow
#echo $PEGASUS_SCRATCH_DIR
#cd \$PEGASUS_SCRATCH_DIR
#pwd
#unset TMP
#unset TMPDIR
#unset TEMP
#export SPARK_HOME="/usr/tce/packages/spark/spark-2.1.0-bin-hadoop2.7"
source $PEGASUS_LLNL_WORK_HOME/my-job-env-pegasus
\$SPARK_HOME/bin/spark-submit --master yarn --deploy-mode cluster --driver-memory 1g --executor-memory 1g --executor-cores 4 --num-executors 2 "\$@"
EOF
chmod +x  $DIR/bin/spark-execute-script


# This environment variable is used in all of the catalogs to
# determine the paths to transformations, files, and input/output dirs
export WF_DIR=$(cd $(dirname $0) && pwd)
export CUR_DIR=$(pwd)
export PEGASUS_LLNL_WORK_HOME=$HOME/pegasus-llnl/ 
source $HOME/pegasus-llnl/bin/setup.sh

cat > $DIR/pegasus.properties << EOF
# This tells Pegasus where to find the Site Catalog
pegasus.catalog.site.file=$DIR/sites.xml

# This tells Pegasus where to find the Replica Catalog
pegasus.catalog.replica=File
pegasus.catalog.replica.file=$DIR/rc.dat

# This tells Pegasus where to find the Transformation Catalog
pegasus.catalog.transformation=Text
pegasus.catalog.transformation.file=$DIR/tc.txt

# This is the name of the application for analytics
pegasus.metrics.app=diamond-llnl

pegasus.gridstart.arguments= -f
EOF



pegasus-plan \
    --conf $DIR/pegasus.properties \
    --cleanup leaf \
    --dax $DAXFILE \
    --output-site catalyst \
    --sites catalyst
