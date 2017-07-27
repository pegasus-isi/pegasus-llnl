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
cur_dir = os.getcwd()

actions_json = File("alpine_actions.json")
actions_json.addPFN(PFN("file:///g/g91/pandey1/pegasus-llnl/llnl-pegasus/alpine/alpine_actions.json","catalyst"))

options_json = File("alpine_options.json")
options_json.addPFN(PFN("file:///g/g91/pandey1/pegasus-llnl/llnl-pegasus/alpine/alpine_options.json","catalyst"))

lulesh_par = File("lulesh_par")
lulesh_par.addPFN(PFN("file:///g/g91/pandey1/pegasus-llnl/llnl-pegasus/alpine/lulesh_par","catalyst"))


alpine_tst_wf.addFile(options_json)
alpine_tst_wf.addFile(actions_json)
alpine_tst_wf.addFile(lulesh_par)
        
alpine_tst_job = Job(namespace="pegasus",name="alpine_par")
alpine_tst_job.uses(actions_json, link=Link.INPUT)
alpine_tst_job.uses(options_json, link=Link.INPUT)
alpine_tst_job.uses(lulesh_par, link=Link.INPUT)

alpine_tst_job.addProfile( Profile("pegasus", "runtime", "120"))
alpine_tst_wf.addJob(alpine_tst_job)

f = open(daxfile, "w")
alpine_tst_wf.writeXML(f)
f.close()
