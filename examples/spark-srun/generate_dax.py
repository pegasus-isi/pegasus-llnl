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
spark_tst_wf = ADAG("spark-test-workflow")

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

spark_jar = File("wordcount.py")
spark_jar.addPFN(PFN("file:///usr/tce/packages/spark/spark-2.1.0-bin-hadoop2.7/examples/src/main/python/wordcount.py","catalyst"))
spark_tst_wf.addFile(spark_jar)
        
# Add executables to the DAX-level transformation catalog
# For submitting MPI jobs directly through condor without GRAM
# we need to refer to wrapper that calls mpiexec with 
# the mpi executable
#e_mpi_hw = Executable(namespace="pegasus", name="mpihw", os="linux", arch="x86_64", installed=True)
#e_mpi_hw.addPFN(PFN("file://" + os.getcwd() + "/mpi-hello-world-wrapper", "catalyst"))
#mpi_hw_wf.addExecutable(e_mpi_hw)


# Add the mpi hello world job
spark_tst_job = Job(namespace="pegasus",name="sprktest")
#spark_jar = File("spark.jar")
#spark_jar.addPFN(PFN("file:///usr/tce/packages/spark/spark-2.1.0-bin-hadoop2.7/examples/src/main/python/wordcount.py","catalyst"))
spark_tst_job.addArguments("-n 3 -N 3 -c 1",os.getcwd()+"/bin/spark-test-wrapper",spark_jar,"hdfs:///f.in")
#spark_tst_job.uses(fin, link=Link.INPUT)
spark_tst_job.uses(spark_jar, link=Link.INPUT)


spark_tst_job.addProfile( Profile("pegasus", "runtime", "120"))
spark_tst_wf.addJob(spark_tst_job)



# Write the DAX to stdout
#mpi_hw_wf.writeXML(sys.stdout)
f = open(daxfile, "w")
spark_tst_wf.writeXML(f)
f.close()
