from .. import model, db, create_app as app
import json


'''
        format
{
    "test_id": test_id,
    "has_negative_marks": false|true
    "quiz_data": [
        {
            "question_id": question_id,
            "user_choice": 'options'
        }
    ]
}
'''


class Eval:
    def __init__(self, data):
        print(type(data))
        self.data = data#json.loads(data)
        self.total_marks = 0
        self.marks_scored = 0
        self.test_id = None
        self.has_negative_marks = False
        self.total_questions = 0
        self.correctly_answered = 0
        self.resp = {'result': []}

    def __pre_process(self):
        self.test_id = self.data['test_id']
        self.has_negative_marks = self.data['has_negative_marks']
        self.total_questions = len(self.data['quiz_data'])

    def evaluate(self):
        self.__pre_process()
        with app().app_context():
            for question in self.data['quiz_data']:
                quest = model.Questions.query.filter_by(id=question['question_id']).first()
                if quest.ans == question['user_choice']:
                    self.correctly_answered += 1
                    self.marks_scored += quest.marks
                    self.total_marks += quest.marks
                    self.resp['result'].append({
                        'question_id': quest.id,
                        'total_marks': quest.marks,
                        'marks_received': quest.marks,
                        'user_choice': question['user_choice'],
                        'correct_ans': quest.ans
                    })
                else:
                    self.total_marks += quest.marks
                    self.resp['result'].append({
                        'question_id': quest.id,
                        'total_marks': quest.marks,
                        'marks_received': 0,
                        'user_choice': question['user_choice'],
                        'correct_ans': quest.ans
                    })
        self.resp['test_id'] = self.test_id
        self.resp['total_marks'] = self.total_marks
        self.resp['result_quest'] = f'{self.correctly_answered}/{self.total_questions}'
        self.resp['result_marks'] = f'{self.marks_scored}/{self.total_marks}'
    
        return self.resp