#!/bin/bash

set -e

if [ $# -ne 1 ]; then
    echo "Usage: $0 DAXFILE"
    exit 1
fi

DAXFILE=$1

cat > bin/mpi-hello-world-wrapper <<EOF
#!/bin/bash

# before launching the job switch to the directory that
# pegasus created for the workflow
cd \$PEGASUS_SCRATCH_DIR
unset TMP
unset TMPDIR
unset TEMP
$PWD/bin/pegasus-mpi-hw "\$@"
EOF
chmod +x  ./bin/mpi-hello-world-wrapper



# This environment variable is used in all of the catalogs to
# determine the paths to transformations, files, and input/output dirs
export WF_DIR=$(cd $(dirname $0) && pwd)

pegasus-plan \
    --conf ./pegasus.properties \
    --cleanup leaf \
    --dax $DAXFILE \
    --output-site catalyst \
    --sites catalyst
