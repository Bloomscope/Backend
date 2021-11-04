import os

SECRET_KEY = 'bloomscope@iitb'

# sqlite db on dev env
db_path = os.path.join(os.path.dirname(__file__), 'database.db')
db_uri = 'sqlite:///{}'.format(db_path)

# mysql db for prod or test
# db_uri = 'mysql+pymysql://root:anirudhmp@localhost:3306/0x41'

# postgress db for prod
# db_uri = 'postgresql://kxhdamszearupc:fc2a0b818f146c2e12d0428327f5d54f254a6f6591e39d14a750d51f589c814b@ec2-52-0-93-3.compute-1.amazonaws.com:5432/d5lksdo86sshue'

WTF_CSRF_ENABLED = False
SQLALCHEMY_DATABASE_URI = db_uri 
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_ECHO = False