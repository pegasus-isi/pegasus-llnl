import os
import subprocess
import time

#WORK_HOME = raw_input("Please provide the path to PEGASUS_LLNL_WORK_HOME:\n ")
WORK_HOME = subprocess.check_output(["pwd"])
WORK_HOME = WORK_HOME.strip('\n')
if not os.path.isdir(WORK_HOME):
  print "Provided PEGASUS_LLNL_WORK_HOME is not a directory"

HOME = os.environ['HOME']
os.chdir(WORK_HOME)
os.system('cp -rf service.py '+HOME+'/.pegasus/')
if os.path.isfile(HOME+'/.pegasus/workflow.db'):
  os.system('rm '+HOME+'/.pegasus/workflow.db')

os.environ['PEGASUS_LLNL_WORK_HOME']=WORK_HOME

os.chdir(WORK_HOME)
os.system('source bin/setup.sh')

os.chdir(WORK_HOME+"/magpie")
print "Submitted job"
job = subprocess.check_output(["sbatch","--ip-isolate=yes","magpie.sbatch-srun-spark-with-hdfs-pegasus"])
job = job.strip('\n')

jobid = job[20:len(job)]
slurm_file = "slurm-"+jobid+".out"
print "Slurm file is "+slurm_file
print "Waiting for nodes to be allocated"

if os.path.isfile(WORK_HOME+"/my-job-env-pegasus"):
  os.system("rm "+WORK_HOME+"/my-job-env-pegasus")

if os.path.exists(WORK_HOME+"/alpine-pegasus/alpinempi/"):
  os.system("rm -rf "+WORK_HOME+"/alpine-pegasus/alpinempi/")

if os.path.exists(WORK_HOME+"/spark-pegasus/workflows/"):
  os.system("rm -rf "+WORK_HOME+"/spark-pegasus/workflows/*")

while not os.path.isfile(WORK_HOME+"/magpie/"+slurm_file):
  print "Waiting more for nodes to be allocated"
  time.sleep(30)

while not os.path.isfile(WORK_HOME+"/my-job-env-pegasus"):
  print "Waiting for some moments..."
  time.sleep(30)

time.sleep(10)
print "Setup done... Custom script"+WORK_HOME+"/magpie/magpie-setup-pegasus is being executed"


