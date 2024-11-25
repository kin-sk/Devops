from flask_mail import Mail, Message

mail = Mail()

def configure_mail(app):
    app.config["MAIL_SERVER"] = "smtp.gmail.com"
    app.config["MAIL_PORT"] = 587
    app.config["MAIL_USE_TLS"] = True
    app.config["MAIL_USERNAME"] = "your_email@gmail.com"
    app.config["MAIL_PASSWORD"] = "your_password"
    mail.init_app(app)

def send_contact_email(app, form_data):
    msg = Message(
        subject=f"お問い合わせ: {form_data['subject']}",
        sender=app.config["MAIL_USERNAME"],
        recipients=["recipient_email@gmail.com"],  # 宛先
        body=f"""
        姓: {form_data['last_name']}
        名: {form_data['first_name']}
        メールアドレス: {form_data['email']}
        件名: {form_data['subject']}
        内容:
        {form_data['message']}
        """
    )
    with app.app_context():
        mail.send(msg)
