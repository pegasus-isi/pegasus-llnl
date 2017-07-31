Phase 1:
Pegasus and Big Data Workflows on LLNL
--------------------------------------------

This allows you to setup a Pegasus and a HTCondor pool via Magpie on a SLRUM job provisioned by Magpie using sbatch . This is an experimental research setup, for creating and running large HPC and Big Data In-situ worklfows that run on catalyst.

In this approach, we use Magpie a LLNL tool to create and setup environment for Big Data analysis, to provision nodes from the SLURM cluster. On the Magpie master node, a pegasus setup script is executed to start HTCondor workflow submit node. Once HTCondor is setup, the user is required to login to the Magpie master node and setup their environment to reflect to mimic the environment that is setup by sbatch when it runs the Magpie job.This allows us to ensure that any Pegasus workflows submitted on the master node, are run on the same set of nodes as provisioned for the Magpie job. The compute jobs in the Pegasus workflows need to be submitted via srun . An example workflow that illustrates this can be found in the examples/mpi-hw-slurm directory. 

Instructions
------------

## Submit a Magpie job and start HTCondor and Pegasus on Magpie master node
 
1. set environment varilable PEGASUS_LLNL_WORK_HOME to the directory where you checked out the pegasus-llnl repo
   ```shell
   cd pegasus-llnl
   export PEGASUS_LLNL_WORK_HOME=`pwd`
   ```

2. Source a setup script to have Pegasus and HTCondor in your path
   ```shell
   source bin/setup.sh
   ```

3. Submit a Magpie job
   ```shell
   cd magpie
   sbatch --ip-isolate=yes  magpie.sbatch-srun-spark-with-hdfs-pegasus
   ```

4. Wait till the slurm job output says starting up condor
   At this time this file will also be created
   ${PEGASUS_LLNL_WORK_HOME}/my-job-env-pegasus

5. we need to create an evnironment setup script to to be able to setup experiment by
   logging on the mapgpie master node
   ```shell
   setup_slurm_env.sh slurm-2507934.out
   ```
6. figure out the magpie master node
    ```shell
    grep SPARK_MASTER_NODE ${PEGASUS_LLNL_WORK_HOME}/my-job-env-pegasus 
    ```
    For example:
    ```shell
    grep SPARK_MASTER_NODE ${PEGASUS_LLNL_WORK_HOME}/my-job-env-pegasus
    export SPARK_MASTER_NODE="catalyst115"
    ```

8. Now open up a new terminal and logon to catalyst.llnl.gov.  All steps going forward are to
   be done in the second terminal you open

9. Logon to the magpie master node as identified in Step 6
   

## Experiment Setup on Magpie Master 
**The steps listed below should be done in a new terminal**

10. set environment varilable PEGASUS_LLNL_WORK_HOME to the directory where you checked out the pegasus-llnl repo
   ```shell    
   cd pegasus-llnl
   export PEGASUS_LLNL_WORK_HOME=`pwd`
   ```

11. Source a setup script to have Pegasus and HTCondor in your path
    ```shell
    source bin/setup.sh
    ```

12. Check condor is up and running
    ```shell
    condor_q
    condor_status
    ```

13. source the environment file written out in step 5
    For example:
    ```shell
    source magpie/slurm-2507934.env  
    ```

14. Now we are set to submit a pegasus example workflow
    ```shell
    cd $PEGASUS_LLNL_WORK_HOME/examples/mpi-hw-slurm/
    ````

15. compile the sample mpi program
    ```shell
    cd bin
    make
    ```

16. generate the dax and submit workflow
    ```shell
    cd ..
    ./generate_dax.py mpi-hw.dax 
    ./plan_dax.sh mpi-hw.dax
    Run pegasus-run on the invocation
    ```

17. Once experiment is done. 
   
    Shutdown the condor
    ```shell
    condor_stop
    ```

![Alt text](llnl-pegasus/projectflow.png?raw=true "Overall project flow diagram")


Phase 2:
Instructions
--------------------------------------------
llnl-pegasus directory has all required folders to run an alpine MPI workflow and an example spark workflow on catalyst using magpie.
Go to llnl-pegasus directory
   ``` shell
   cd llnl-pegasus
   ```
Files to be modified
--------------------------------------------
There are several files and folders. 
**Inside magpie** 
1. Modify magpie.sbatch-surn-spark-with-hdfs-pegasus to edit SLURM variables as per your need.
2. magpie-set-pegasus is the custom script that gets executed in Magpie Master.

**service.py**
This file has the configuration for Ensemble Mangager. 
``` shell
    EV_INTERVAL = 1
```
Setting the value of this variable to 1 will tell Ensemble Manager to check for the event triggers in every 1 seconds

**Inisde config**
1. event-config is the configuration file in JSON that tells Ensemble Manager where to look for the events. An example is given below:
``` json
   {
     "event-dir":"/p/lscratchd/pandey1/alpinempi/trigger_files",
     "event-content":"*",
     "event-type":"file-dir",
     "event-cycle":200,
     "event-size":0,
     "event-numfiles":1,
     "pegasus-args": "/g/g91/pandey1/llnl-pegasus/spark-pegasus/plan_dax.sh",
     "event-script": "/g/g91/pandey1/llnl-pegasus/spark-pegasus/dax_generator.sh",
     "event-dax-dir": "/g/g91/pandey1/llnl-pegasus/spark-pegasus/workflows"
    }

```
   event-dir tells where to look for the trigger files, event-content tells to look for any file names, event-type tells whether the content to watch over is directory or a file, event-size is the size of the trigger files, event-numfiles is the number of files after which trigger will occur. pegasus-args, event-script and event-dax-dir are the pegasus related variables.
   
**Inside alpine**
This directory is the place where pre-built executables of lulesh_par and their input files are kept. This directory can be anywhere but if placed at any other place the absolute path of the lulesh_par and the input files must be mentioned in the alpine dax generator python script which is inside alpine-pegasus folder.

**Inside alpine-pegasus**
This directory includes the pegasus files to create and submit an alpine MPI workflow.

**Inside spark-pegasus**
This directory includes the pegasus files to create and submit a spark workflow. Each time a new dax is created for a new spark simulation job. The dax is inside workflows directory. dax_generator.sh is a script that was mentioned in event-config that generates the dax for every new spark analysis jobs.


**How to run**
```python
   python setup_experiment.py
```

Output obtained from the above run:

![Alt text](llnl-pegasus/setup_experiment_output.png?raw=true "Setup experiment output")

Once the setup is done, you can ssh to the Master node to check if everything is working:

**Find out which one is the Master node**
```shell
   grep SPARK_MASTER_NODE ./my-job-env-pegasus
```

**SSH to the Master node**
```shell
   ssh catalystX
```

**Check if MPI job is running**
```shell
   export PEGASUS_LLNL_WORK_HOME=`pwd`
   source bin/setup.sh
   pegasus-em workflows a
```









  
   
   
   



