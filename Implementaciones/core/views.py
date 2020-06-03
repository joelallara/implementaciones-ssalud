from django.views.generic.base import TemplateView
from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta

from deploy.models import DeployInfo
import smtplib


@method_decorator(login_required, name='dispatch')
class HomePageView(TemplateView):
    template_name = "core/home.html"

    def get(self, request, *args, **kwargs):
        deploys = DeployInfo.objects.filter(deploy_date__gte=datetime.now()-timedelta(days=7))[:5]
        return render(request, self.template_name, {'deploys': deploys})


def email(request, subject, message, email_receive):
    email_from = settings.EMAIL_ADDRESS
    content = 'Subject: {}\n\n{}'.format(subject, message)
    print(content)
    password = settings.EMAIL_PASSWORD
    fromemail = email_from
    email_to = email_receive
    mail = smtplib.SMTP('smtp.gmail.com', 587)
    mail.ehlo()
    try:
        mail.starttls()
        mail.login(email_from, password)
        mail.sendmail(fromemail, email_to, content.encode("utf8"))
    finally:
        mail.quit()
        mail.close()
