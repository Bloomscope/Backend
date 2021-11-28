import json
import csv
# from ..model import User
# from .. import db, bcrypt


class MassRegister:
    def __init__(self, mime, stream) -> None:
        self.mime = mime
        self.stream = stream
        self.response = {
            'errors': None,
            'total_students': 0,
        }
        self.total = 0

    def __json(self):
        try:
            data = json.loads(self.stream)
        except Exception as e:
            self.response['errors'] = {e.__class__.__name__: e.__str__()}

    def __csv(self):
        try:
            data = csv.DictReader(self.stream, )
        except Exception as e:
            self.response['errors'] = {e.__class__.__name__: e.__str__()}

    def __call__(self):
        if 'json' in self.mime:
            self.__json()
        elif 'csv' in self.mime:
            self.__csv
        else:
            self.response['errors'] = {'UnKnown File Type': 'Currently accepts json or csv files only.'}
        return self.response
