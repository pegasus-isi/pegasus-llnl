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
mpi_hw_wf = ADAG("mpi-hello-world")

# Add input file to the DAX-level replica catalog
fin = File("fin")
fin.addPFN(PFN("file://" + os.getcwd() + "/input/f.in", "catalyst"))
mpi_hw_wf.addFile(fin)
        
# Add executables to the DAX-level transformation catalog
# For submitting MPI jobs directly through condor without GRAM
# we need to refer to wrapper that calls mpiexec with 
# the mpi executable
#e_mpi_hw = Executable(namespace="pegasus", name="mpihw", os="linux", arch="x86_64", installed=True)
#e_mpi_hw.addPFN(PFN("file://" + os.getcwd() + "/mpi-hello-world-wrapper", "catalyst"))
#mpi_hw_wf.addExecutable(e_mpi_hw)


# Add the mpi hello world job
mpi_hw_job = Job(namespace="pegasus", name="mpihw" )
fout = File("f.out")
mpi_hw_job.addArguments("-n 3 -N 3 -c 1 ", os.getcwd() + "/bin/mpi-hello-world-wrapper", "-o", fout )
mpi_hw_job.uses(fin, link=Link.INPUT)
mpi_hw_job.uses(fout, link=Link.OUTPUT)


mpi_hw_job.addProfile( Profile("pegasus", "runtime", "120"))
mpi_hw_wf.addJob(mpi_hw_job)



# Write the DAX to stdout
#mpi_hw_wf.writeXML(sys.stdout)
f = open(daxfile, "w")
mpi_hw_wf.writeXML(f)
f.close()
