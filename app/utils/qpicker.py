from .. import model
# from .. import db


# take test_id as param and make asked_on true for selected questions
def get_questions(json_data):
    quest = {'questions': []}
    for param in json_data:
        param_id = int(param['id'])
        question = model.Questions.query.filter_by(has_asked=False).filter_by(param_id=param_id).limit(int(param['que'])).all()
        quest['questions'].append({
            'param_id': param_id,
            'data': [j.as_dict() for j in question]
        })
    return quest
