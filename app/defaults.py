from .model import Parameters, UsersType, db


PARAMETERS = [
    (1, "Remember"),
    (2, "Understand"),
    (3, "Apply"),
    (4, "Analyze"),
    (5, "Evaluate"),
    (6, "Create"),
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