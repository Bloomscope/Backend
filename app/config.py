import os
from datetime import timedelta

SECRET_KEY = 'bloomscope@iitb'

# sqlite db on dev env
db_path = os.path.join(os.path.dirname(__file__), 'database.db')
db_uri = 'sqlite:///{}'.format(db_path)

# mysql db for prod or test
# db_uri = 'mysql://root:anirudhmp@127.0.0.1:3306/proto'

# postgress db for prod
# db_uri = 'postgresql://kxhdamszearupc:fc2a0b818f146c2e12d0428327f5d54f254a6f6591e39d14a750d51f589c814b@ec2-52-0-93-3.compute-1.amazonaws.com:5432/d5lksdo86sshue'

WTF_CSRF_ENABLED = False
SQLALCHEMY_DATABASE_URI = db_uri 
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_ECHO = False

JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
JWT_SECRET_KEY = SECRET_KEY

JSON_SORT_KEYS = False

RAZOR_PAY_ID = 'rzp_test_Vk9SxQEHXGwJQp'
RAZOR_PAY_SECRET = 'sNGOwgoYnUAO8n3SOlMsgLGR'

# redis and celery config
CELERY_BROKER_URL = 'redis://default:anirudhmp@redis-19076.c277.us-east-1-3.ec2.cloud.redislabs.com:19076'
