#!/usr/bin/env python

from Pegasus.DAX3 import *
import sys
import os
import json
import subprocess

# The name of the DAX file is the first argument
if len(sys.argv) != 4:
    sys.stderr.write("Usage: %s DAXFILE SPARK_CYCLE_NUMBER CONFIG_FILE\n" % (sys.argv[0]))
    sys.exit(1)
daxfile = sys.argv[1]
spark_cycle_num = int(sys.argv[2])
configfile = sys.argv[3]

data = None
with open(configfile) as data_file:
    data = json.load(data_file)

ridx = data["event-dir"].rfind("/")
scratchdir = data["event-dir"][0:ridx]
dirs = subprocess.check_output(["find",scratchdir,"-name","tout_lulesh.cycle_*"+str(spark_cycle_num)])
dirs = dirs.split('\n')
dirs = dirs[0:len(dirs)-1]
totaldirs = ' '.join(dirs)

#total_files = []
#for each_dir in dirs:
#    each_dir = each_dir.strip('.')
#    files = subprocess.check_output(["find",each_dir,"-name","*.hdf5"])
#    files = files.split('\n')
#    files = files[0:len(files)-1]
#    total_files.append(files)


#filesargs = ""
#for each_file in total_files:
#    files = ' '.join(each_file)
#    filesargs += files
#    filesargs += " "

# Create a abstract dag
spark_tst_wf = ADAG("spark-test-workflow")
cur_dir = os.getcwd()
spark_jar = File("wordcount.py")
spark_jar.addPFN(PFN("file:///usr/tce/packages/spark/spark-2.1.0-bin-hadoop2.7/examples/src/main/python/wordcount.py","catalyst"))
spark_tst_wf.addFile(spark_jar)


hdfs_cpy_job = Job(namespace="pegasus",name="hdfscpy")
hdfs_cpy_job.addArguments("dfs","-copyFromLocal",totaldirs,"/")
spark_tst_wf.addJob(hdfs_cpy_job)
        
# Add the mpi hello world job
spark_tst_job = Job(namespace="pegasus",name="sprktest")
spark_tst_job.addArguments(spark_jar,"hdfs:///f.in")
#spark_tst_job.uses(fin, link=Link.INPUT)
spark_tst_job.uses(spark_jar, link=Link.INPUT)
spark_tst_job.invoke('at_end',  "/usr/workspace/wsb/alemm/pegasus/pegasus/share/pegasus/notification/email --to surajp@hawaii.edu")

spark_tst_job.addProfile( Profile("pegasus", "runtime", "120"))
spark_tst_wf.addJob(spark_tst_job)

spark_tst_wf.addDependency(Dependency(parent=hdfs_cpy_job,child=spark_tst_job))

# Write the DAX to stdout
#mpi_hw_wf.writeXML(sys.stdout)
f = open(daxfile, "w")
spark_tst_wf.writeXML(f)
f.close()
