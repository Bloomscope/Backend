from .model import Parameters, UsersType, db


PARAMETERS = [
    (1, "Cognitive Skills"),
    (2, "Remembering"),
    (3, "Testing"),
    (4, "Coding"),
    (5, "Solving"),
    (6, "Seeing"),
    (7, "Nothing"),
    (8, "Breathing"),
    (9, "Swimming"),
]

USER_TYPES = [
    ("student", 1),
    ("parent", 2),
    ("admin", 3)
]

def create_defaults():
    for param in PARAMETERS:
        new_param = Parameters(id=param[0], param_name=param[1])
        db.session.add(new_param)
    for ut in USER_TYPES:
        new_ut = UsersType(type=ut[0], access_level=ut[1])
        db.session.add(new_ut)
    db.session.commit()