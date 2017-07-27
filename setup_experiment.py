import os
import subprocess
import time

WORK_HOME = raw_input("Please provide the path to PEGASUS_LLNL_WORK_HOME:\n ")
if not os.path.isdir(WORK_HOME):
  print "Provided PEGASUS_LLNL_WORK_HOME is not a directory"

HOME = os.environ['HOME']
print HOME

os.environ['PEGASUS_LLNL_WORK_HOME']=WORK_HOME


os.chdir(WORK_HOME)
os.system('source bin/setup.sh')

os.chdir(WORK_HOME+"/magpie")
print "Submitted job"
job = subprocess.check_output(["sbatch","--ip-isolate=yes","magpie.sbatch-srun-spark-with-hdfs-pegasus"])
job = job.strip('\n')
#job = "submitted batch job 2594286"

jobid = job[20:len(job)]
slurm_file = "slurm-"+jobid+".out"
print "Slurm file is "+slurm_file
print "Waiting for nodes to be allocated"

if os.path.isfile(WORK_HOME+"/my-job-env-pegasus"):
  os.system("rm "+WORK_HOME+"/my-job-env-pegasus")

while not os.path.isfile(WORK_HOME+"/magpie/"+slurm_file):
  print "Waiting more for nodes to be allocated"
  time.sleep(30)

while not os.path.isfile(WORK_HOME+"/my-job-env-pegasus"):
  print "Waiting for some moments..."
  time.sleep(30)

os.chdir(WORK_HOME)
os.system('bin/setup_slurm_env.sh magpie/'+slurm_file)

time.sleep(10)

SPARK_MASTER_NODE = ""
try:
  SPARK_MASTER_NODE=subprocess.check_output(["grep","SPARK_MASTER_NODE",WORK_HOME+"/my-job-env-pegasus"])
except subprocess.CalledProcessError as e:
  print "Was not able to grep SPARK_MASTER_NODE from my-job-env-pegasus"
  print e
  exit(1)

#SPARK_MASTER_NODE=subprocess.check_output(["grep","SPARK_MASTER_NODE",WORK_HOME+"/my-job-env-pegasus"])
SPARK_MASTER_NODE=SPARK_MASTER_NODE[26:len(SPARK_MASTER_NODE)-2]


print "****************************************************************************"
print "Now open a new terminal and ssh to the Magpie Master Node using this command"
print "ssh "+SPARK_MASTER_NODE

#export SPARK_MASTER_NODE="catalyst177"
#os.system('bin/setup_slurm_env.sh magpie/')


