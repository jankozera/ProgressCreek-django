from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import get_template

from profiles.errors import MailServiceError


class EmailService:
    @staticmethod
    def send_mail(message, htmlmessage, recipents, subject):
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            recipents,
            html_message=htmlmessage,
        )


class UserMailService(EmailService):
    @staticmethod
    def register_company_user(email, token, company):
        try:
            plain_text = get_template("emails/register-company-user.txt")
            html_text = get_template("emails/register-company-user.html")
            url = settings.FRONTEND_URL + "register/"
            subject = "Du har blivit inbjuden till organisation MiH"
            context = {
                "email": email,
                "token": token,
                "url": url,
                "company": company,
            }
            text_content = plain_text.render(context)
            html_content = html_text.render(context)
            super(UserMailService, UserMailService).send_mail(
                text_content,
                html_content,
                [email],
                subject,
            )
        except Exception as e:
            raise MailServiceError from e
