import os

# SERVER CONFIGURATION

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5000



# FLASK CONFIGURATION

DEBUG = False

# The secret key used by Flask to encrypt session keys
SECRET_KEY = os.urandom(24)



# SQLALCHEMY CONFIGURATION

# The URI of the database
#SQLALCHEMY_DATABASE_URI = "mysql://pegasus:secret@127.0.0.1:3306/pegasus_service"
SQLALCHEMY_DATABASE_URI = 'sqlite:///%s/.pegasus/workflow.db' % os.getenv('HOME')
#SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/test.db'

# Set to True to log SQL queries
#SQLALCHEMY_ECHO = False

# Set to change the SQLAlchemy connection pool size
#SQLALCHEMY_POOL_SIZE = 5

# Set to change the connection timeout (in seconds)
#SQLALCHEMY_POOL_TIMEOUT = 10

# Set to change how long connections remain before being recycled (in seconds)
# Default is 2 hours for MySQL
#SQLALCHEMY_POOL_RECYCLE = 2 * 60 * 60


# Cache Configuration
CACHE_TYPE = 'simple'

# SERVICE CONFIGURATION

# Path to the directory where the service stores all its files
STORAGE_DIR = os.path.join(os.getenv('HOME'), ".pegasus", "service")



# CLIENT CONFIGURATION

# Service endpoint. This is only required if you install the service
# at a URL other than "http://SERVER_HOST:SERVER_PORT/".
ENDPOINT = None

# User credentials
USERNAME = "pandey1"
PASSWORD = "abc"



# ENSEMBLE MANAGER CONFIGURATION

# Workflow processing interval in seconds
EM_INTERVAL = 60
EV_INTERVAL = 1

# Path to Pegasus home directory
PEGASUS_HOME = "/usr/workspace/wsb/alemm/pegasus/pegasus-4.7.5dev"

# Path to Condor home directory
#CONDOR_HOME = "/usr"

