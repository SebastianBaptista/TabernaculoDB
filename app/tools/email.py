from email.message import EmailMessage
import smtplib
import ssl



def send_email(email_reciver,cod):
    password="ynpt ptrx fuyl gema"
    email_sender="tabernaculodb@gmail.com"
    subject="Codigo de Recuperación de Contraseña de Tabernáculo DB"
    body=f"Hola, el código de recuperación de contraseña es: {cod}"
    em=EmailMessage()
    em['From']=email_sender
    em['To']=email_reciver
    em["Subject"]=subject
    em.set_content(body)
    context= ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
            smtp.login(email_sender, password)
            smtp.sendmail(email_sender,email_reciver,em.as_string())
    except Exception as ex:
        raise Exception(ex)
    