from ..model import User
from .. import db, bcrypt
import json
from datetime import datetime


'''
        format

users: [
    {
        fname: required
        mname: optional
        lname = required
        dob = required [any format]
        email = required
        password = required [ex: 123qweas  in plain text]
        phone = 7406177090
    },
    {
        fname: required
        mname: optional
        lname = required
        dob = required [any format]
        email = required
        password = required [ex: 123qweas  in plain text]
        phone = 7406177090
    }

]
'''

def mass_register(stream):
    data = json.loads(stream.decode('utf-8'))['users']
    for user in data:
        password = user.pop('password')
        dob = datetime.strptime(user.pop('dob'), '%Y-%m-%d')
        new_user = User(**user, password=bcrypt.generate_password_hash(password).decode('utf-8'), dob=dob)
        db.session.add(new_user)
    db.session.commit()
