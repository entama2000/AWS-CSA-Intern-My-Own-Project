import smtplib
from email.mime.text import MIMEText
from email.header import Header

def send_email(from_email, to_email, subject, message, smtp_password):
    msg = MIMEText(message, 'plain', 'utf-8')
    msg['From'] = Header(from_email, 'utf-8')
    msg['To'] = Header(to_email, 'utf-8')
    msg['Subject'] = Header(subject, 'utf-8')

    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(from_email, smtp_password)
    server.sendmail(from_email, [to_email], msg.as_string())
    server.quit()