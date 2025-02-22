from email.message import EmailMessage


def get_forgot_password_message(email_to: str, link: str) -> EmailMessage:
    email = EmailMessage()
    email['Subject'] = 'Сброс пароля'
    email['From'] = 'Stuffr'
    email['To'] = email_to
    email.set_content(
        '<div>'
        '<h2>Здравствуйте!<h2>'
        f'<p>Для сброса пароля перейдите по ссылке {link}</p>'
        '</div>',
        subtype='html',
    )
    return email


def get_reset_password_message(email_to: str) -> EmailMessage:
    email = EmailMessage()
    email['Subject'] = 'Пароль изменен'
    email['From'] = 'Stuffr'
    email['To'] = email_to
    email.set_content(
        '<div>'
        '<h2>Здравствуйте!<h2>'
        f'<p>Пароль для аккаунта {email_to} успешно изменен</p>'
        '</div>',
        subtype='html',
    )
    return email
