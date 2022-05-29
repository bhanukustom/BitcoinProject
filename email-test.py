import dotenv
import os
import smtplib

dotenv.load_dotenv()

sender = "Private Person <from@example.com>"
receiver = f"A Test User <{os.getenv('email')}>"

message = f"""\
Subject: Hi Mailtrap
To: {receiver}
From: {sender}

This is a test e-mail message."""
smtp_host = os.getenv('host')
smtp_port = int(os.getenv('port'))
smtp_user = os.getenv('smtp_user')
smtp_password = os.getenv('password')

with smtplib.SMTP(smtp_host, smtp_port) as server:
    server.login(smtp_user, smtp_password)
    print("Sending email...")
    print(message)
    res = server.sendmail(sender, receiver, message)
    print(res)