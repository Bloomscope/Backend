import json
# from ..model import Questions


'''
JSON Format

"data": [
    {
        'qid': int|number,
        'question': str|img,
        'question_type': str|url[for images or other data],
        'options': {
            [
                {
                    'opt': str|img,
                    'value': str|img,
                    'opt_type': str|url
                }
            ],
        'answer': option,
        'explanation': str|image|null,
        'parameters': [param_id|int]
        }
    }
]

        ......example.....

"data": [
    {
        'qid': 1,
        'question': hello,
        'question_type': str,
        'options': {
            [
                {
                    'opt': 'A',
                    'value': 'world!',
                    'opt_type': str
                },
                {
                    'opt': 'B',
                    'value': 'World',
                    'opt_type': str
                },
                {
                    'opt': 'C',
                    'value': 'noned',
                    'opt_type': str
                }
            ],
        'answer': 'A',
        'explanation': 'in cs its hello world!',
        'parameters': [1,4,6]
        }
    }
]
'''

def add_questions(f):
    '''
    f -> file buffer|data buffer
    returns None
    '''
    pass