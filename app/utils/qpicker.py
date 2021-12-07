from .. import model
# from .. import db
from uuid import uuid4


# take test_id as param and make asked_on true for selected questions
def get_questions(json_data):
    test_id = uuid4().__str__()
    quest = {'test_id': test_id,'questions': []}
    for param in json_data:
        param_id = int(param['id'])
        question = model.Questions.query.filter_by(has_asked=False).filter_by(param_id=param_id).limit(int(param['que'])).all()
        quest['questions'].append({
            'param_id': param_id,
            'data': [j.as_dict() for j in question]
        })
    return quest
