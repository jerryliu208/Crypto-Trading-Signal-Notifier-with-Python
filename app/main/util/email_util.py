import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from app.main.config.application_config import ApplicationConfig

class EmailUtil():
    
    @staticmethod
    def send_email(subject, message, receiver):
        sender = ApplicationConfig.smtp_username
        
        msg = MIMEMultipart()
        msg['From'] = sender
        msg['To'] = receiver
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'plain'))

        server = smtplib.SMTP(ApplicationConfig.smtp_host, ApplicationConfig.smtp_port)
        server.starttls()
        server.login(sender, ApplicationConfig.smtp_password)
        text = msg.as_string()
        server.sendmail(sender, receiver, text)
        server.quit()
        
    @staticmethod
    def batch_send_email(subject, message, receivers):
        sender = ApplicationConfig.smtp_username
        
        server = smtplib.SMTP(ApplicationConfig.smtp_host, ApplicationConfig.smtp_port)
        server.starttls()
        server.login(sender, ApplicationConfig.smtp_password)
        
        for receiver in receivers:
            msg = MIMEMultipart()
            msg['From'] = sender
            msg['To'] = receiver
            msg['Subject'] = subject
            msg.attach(MIMEText(message, 'plain'))
            text = msg.as_string()
            server.sendmail(sender, receiver, text)
        
        server.quit()