from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from .model import *
from flask import abort
from .utils.decorators import current_user_proxy_obj as current_user


class AdminController(ModelView):

    # column_searchable_list = (User.email)

    def is_accessible(self):
        # if current_user().email == 'test@test.com' or current_user.user_type_id == 3:
        #     return True
        # else:
        #     return abort(403)
        return True

    def not_auth(self):
        return abort(403)


def init_app(app, db, name="Admin", url_prefix="/admin", **kwargs):
    vkwargs = {"name": name, "endpoint": "admin", "url": url_prefix}

    akwargs = {
        "template_mode": "bootstrap3",
        "static_url_path": f"/templates/{url_prefix}",
        "index_view": AdminIndexView(**vkwargs),
    }

    admin = Admin(app, **akwargs)
    admin.add_view(AdminController(User, db.session, endpoint='users_'))
    admin.add_view(AdminController(UsersType, db.session, endpoint='userstype_'))
    admin.add_view(AdminController(Plans, db.session, endpoint='plans_'))
    admin.add_view(AdminController(Subscription, db.session, endpoint='subscription_'))
    admin.add_view(AdminController(Organization, db.session, endpoint='organization_'))
    admin.add_view(AdminController(Parent, db.session, endpoint='parent_'))
    admin.add_view(AdminController(Parameters, db.session, endpoint='parameters_'))
    admin.add_view(AdminController(Parent_Child, db.session, endpoint='parent_child_'))
    admin.add_view(AdminController(TestSchedule, db.session, endpoint='testschedule_'))
    admin.add_view(AdminController(Test, db.session, endpoint='test_'))
    admin.add_view(AdminController(Questions, db.session, endpoint='questions_'))
    admin.add_view(AdminController(Results, db.session, endpoint='results_'))
    admin.add_view(AdminController(Announcements, db.session, endpoint='announcements_'))
    admin.add_view(AdminController(Complain, db.session, endpoint='complain_'))
    admin.add_view(AdminController(Token, db.session, endpoint='token_'))