# Class custom e-mail sender from django
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string


class SendEmail:
    # class for sending email to user
    # carries detail of the email
    # 'content' is a dictionary carries token, domain and user info

    def __init__(self, mail_subject, from_email, to, template, content):
        self.subject = mail_subject
        self.sender = from_email
        self.recipient = to
        self.template = template
        self.content = content

    def send(self):
        # method used to send email

        message = render_to_string(self.template, self.content)
        mail = EmailMessage(
            self.subject, message, from_email=self.sender, to=[self.recipient])
        mail.content_subtype = 'html'
        mail.send()
