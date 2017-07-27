#!/usr/bin/env python

from Pegasus.DAX3 import *
import sys
import os


# The name of the DAX file is the first argument
if len(sys.argv) != 2:
    sys.stderr.write("Usage: %s DAXFILE\n" % (sys.argv[0]))
    sys.exit(1)
daxfile = sys.argv[1]



# Create a abstract dag
alpine_tst_wf = ADAG("alpine-test-workflow")

# Add input file to the DAX-level replica catalog
#fin = File("fin")
#fin.addPFN(PFN("hdfs:///f.in", "catalyst"))
#spark_tst_wf.addFile(fin)


cur_dir = os.getcwd()


#t = Transformation("sprktest")
#e = Executable("sprktest",arch="x86_64",installed=True)
#e.addPFN(PFN("file://"+cur_dir+"/bin/spark-execute-script","catalyst"))
#t.uses(e)
#spark_tst_wf.addExecutable(e)
#spark_tst_wf.addTransformation(t)

actions_json = File("alpine_actions.json")
actions_json.addPFN(PFN("file:///g/g91/pandey1/newalpinetest/alpine/build-debug/examples/proxies/lulesh2.0.3/alpine_actions.json","catalyst"))

options_json = File("alpine_options.json")
options_json.addPFN(PFN("file:///g/g91/pandey1/newalpinetest/alpine/build-debug/examples/proxies/lulesh2.0.3/alpine_options.json","catalyst"))

lulesh_ser = File("lulesh_ser")
lulesh_ser.addPFN(PFN("file:///g/g91/pandey1/newalpinetest/alpine/build-debug/examples/proxies/lulesh2.0.3/lulesh_ser","catalyst"))


alpine_tst_wf.addFile(options_json)
alpine_tst_wf.addFile(actions_json)
alpine_tst_wf.addFile(lulesh_ser)
        
# Add executables to the DAX-level transformation catalog
# For submitting MPI jobs directly through condor without GRAM
# we need to refer to wrapper that calls mpiexec with 
# the mpi executable
#e_mpi_hw = Executable(namespace="pegasus", name="mpihw", os="linux", arch="x86_64", installed=True)
#e_mpi_hw.addPFN(PFN("file://" + os.getcwd() + "/mpi-hello-world-wrapper", "catalyst"))
#mpi_hw_wf.addExecutable(e_mpi_hw)


# Add the mpi hello world job
alpine_tst_job = Job(namespace="pegasus",name="alpine_ser")
#spark_jar = File("spark.jar")
#spark_jar.addPFN(PFN("file:///usr/tce/packages/spark/spark-2.1.0-bin-hadoop2.7/examples/src/main/python/wordcount.py","catalyst"))
#spark_tst_job.addArguments(spark_jar,"hdfs:///f.in")
#spark_tst_job.uses(fin, link=Link.INPUT)
alpine_tst_job.uses(actions_json, link=Link.INPUT)
alpine_tst_job.uses(options_json, link=Link.INPUT)
alpine_tst_job.uses(lulesh_ser, link=Link.INPUT)


alpine_tst_job.addProfile( Profile("pegasus", "runtime", "120"))
alpine_tst_wf.addJob(alpine_tst_job)



# Write the DAX to stdout
#mpi_hw_wf.writeXML(sys.stdout)
f = open(daxfile, "w")
alpine_tst_wf.writeXML(f)
f.close()
