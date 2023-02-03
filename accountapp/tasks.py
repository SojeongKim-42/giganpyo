# tasks.py

from __future__ import absolute_import, unicode_literals
from datetime import datetime
from celery import shared_task
from django.core.mail import EmailMessage
from giganpyo.celery import app
from django.template.loader import render_to_string

# test 용 함수
@shared_task
def printTime():
    print("Testtime: ", datetime.now())
    

@app.task(bind=True)
def send_verification_email(self, title="이메일 인증을 완료해주세요", data=None, to=None):
    mail_title      = "[Giganpyo] 이메일 인증을 완료해주세요"
    mail_to         = to
    email_content = render_to_string('email.html',{
        "title": "Giganpyo 회원가입 인증",
        "link" : data
    })
    email           = EmailMessage(
        mail_title, 
        email_content, 
        to = [mail_to])
    
    email.content_subtype='html'
    email.send()
    
    return