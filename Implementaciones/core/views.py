from django.views.generic.base import TemplateView
from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings

from deploy.models import DeployInfo
import smtplib


class HomePageView(TemplateView):
    template_name = "core/home.html"

    def get(self, request, *args, **kwargs):
        deploys = DeployInfo.objects.all()[:5]
        return render(request, self.template_name, {'deploys': deploys})


def email(request, subject, message, email_receive):
    email_from = settings.EMAIL_ADDRESS
    content = 'Subject: {}\n\n{}'.format(subject, message)
    password = settings.EMAIL_PASSWORD
    fromemail = email_from
    email_to = email_receive
    mail = smtplib.SMTP('smtp.gmail.com', 587)
    mail.ehlo()
    try:
        mail.starttls()
        mail.login(email_from, password)
        mail.sendmail(fromemail, email_to, content)
    finally:
        mail.quit()
        mail.close()

