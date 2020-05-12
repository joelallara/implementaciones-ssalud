from django.views.generic.base import TemplateView
from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings

from project.models import Project
import smtplib


class HomePageView(TemplateView):
    template_name = "core/home.html"

    def get(self, request, *args, **kwargs):
        projects = Project.projects.all()
        return render(request, self.template_name, {'projects': projects})


def email(request, subject, message, email_receive):
    email_from = 'joel.allara@gmail.com'
    content = 'Subject: {}\n\n{}'.format(subject, message)
    password = "subccomp85"
    fromemail = email_from
    email_to = email_receive
    mail = smtplib.SMTP('smtp.gmail.com', 587)
    mail.ehlo()
    mail.starttls()
    mail.login(email_from, password)
    mail.sendmail(fromemail, email_to,content)
    mail.close()
