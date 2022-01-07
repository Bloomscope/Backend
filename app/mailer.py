from flask_mail import  Message
from flask import render_template, current_app as app
from . import mail, celery


@celery.task
def send_informative_mail(**kwargs):
    '''
    function to be used when sending informative mails that doesnt need dynamic data to be rendered.

    named args to be sent are,

    title -> title of mail
    email -> receipient email
    template -> html template file name that should be rendered
    fname -> user first name.
    '''
    with app.app_context():
        msg = Message(kwargs['title'], sender='anirudhmp@colabo.in', recipients=[kwargs['email']])
        msg.html = render_template(f'{kwargs["template"]}.html', fname=kwargs['fname'])
        mail.send(msg)


@celery.task
def send_test_mails(**kwargs):
    '''
    mails that are to be sent when new tests are assigned.

    named args to be sent are,

    email -> receipient email
    template -> html template file name that should be rendered
    fname -> user first name.
    '''
    with app.app_context():
        msg = Message('New tests has been assigned', sender='anirudhmp@colabo.in', recipients=[kwargs['email']])
        msg.html = render_template(f'{kwargs["template"]}.html', fname=kwargs['fname'])
        mail.send(msg)


@celery.task
def send_result_mails(**kwargs):
    '''
    results related mails that are to be sent.

    named args to be sent are,

    email -> receipient email
    template -> html template file name that should be rendered
    fname -> user first name
    test_name -> name of the test.
    '''
    with app.app_context():
        msg = Message(f'Your test ({kwargs["test_name"]}) results are available', sender='anirudhmp@colabo.in', recipients=[kwargs['email']])
        msg.html = render_template(f'{kwargs["template"]}.html', fname=kwargs['fname'])
        mail.send(msg)