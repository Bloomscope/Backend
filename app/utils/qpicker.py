from .. import model
from .. import db
from uuid import uuid4


def get_questions():
    params = model.Parameters.query.all()
    test_id = uuid4().__str__()
    quest = {'test_id': test_id,'questions': []}
    for i in params:
        question = model.Questions.query.filter_by(has_asked=False).filter_by(param_id=i.id).limit(10).all()
        quest['questions'].append({
            'param_id': i.id,
            'param_name': i.param_name,
            'data': [j.as_dict() for j in question]
        })
    return quest