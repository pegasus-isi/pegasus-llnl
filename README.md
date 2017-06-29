This allows you to setup a Pegasus and a HTCondor pool via Magpie on a SLRUM job provisioned by Magpie using sbatch

Instructions:

1) set environment varilable PEGASUS_LLNL_WORK_HOME to the directory where you checked out the pegasus-llnl repo
   cd pegasus-llnl
   export PEGASUS_LLNL_WORK_HOME=`pwd`

2) Source a setup script to have Pegasus and HTCondor in your path
   source bin/setup.sh

3) Submit a Magpie job
   cd magpie
   sbatch --ip-isolate=yes  magpie.sbatch-srun-spark-with-hdfs-pegasus


4) Wait till the slurm job output says starting up condor
   At this time this file will also be created
   ${PEGASUS_LLNL_WORK_HOME}/my-job-env-pegasus

5) we need to create an evnironment setup script to to be able to setup experiment by
   logging on the mapgpie master node
   setup_slurm_env.sh slurm-2507934.out

6) figure out the magpie master node
    grep SPARK_MASTER_NODE ${PEGASUS_LLNL_WORK_HOME}/my-job-env-pegasus 
    For example:
    grep SPARK_MASTER_NODE ${PEGASUS_LLNL_WORK_HOME}/my-job-env-pegasus
    export SPARK_MASTER_NODE="catalyst115"


8) Now open up a new terminal and logon to catalyst.llnl.gov.  All steps going forward are to
   be done in the second terminal you open

9) Logon to the magpie master node as identified in Step 6
   

Experiment Setup in Second Terminal
======================================
10) set environment varilable PEGASUS_LLNL_WORK_HOME to the directory where you checked out the pegasus-llnl repo
   cd pegasus-llnl
   export PEGASUS_LLNL_WORK_HOME=`pwd`

11) Source a setup script to have Pegasus and HTCondor in your path
   source bin/setup.sh

12) Check condor is up and running
    condor_q
    condor_status

13) source the environment file written out in step 5
    For example:
    source magpie/slurm-2507934.env  

14) Now we are set to submit a pegasus example workflow
    cd $PEGASUS_LLNL_WORK_HOME/examples/mpi-hw-slurm/

15) compile the sample mpi program
    cd bin
    make

16) generate the dax and submit workflow
    cd ..
    ./generate_dax.py mpi-hw.dax 
    ./plan_dax.sh mpi-hw.dax
    Run pegasus-run on the invocation

17) Once experiment is done. 
    Shutdown the condor

    condor_stop