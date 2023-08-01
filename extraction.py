import os
import imaplib
import email
import asyncio
import concurrent.futures
from email.utils import parseaddr
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class EmailFetcher:
    def __init__(self):
        self.user = os.getenv("EMAIL_USER")
        self.password = os.getenv("EMAIL_PASSWORD")
        self.host = os.getenv("IMAP_HOST")
        self.smtp_server = os.getenv("SMTP_SERVER")

    def login(self):
        mail = imaplib.IMAP4_SSL(self.host)
        mail.login(self.user, self.password)
        mail.select("inbox")
        return mail

    async def fetch_new_emails(self):
        loop = asyncio.get_event_loop()
        with concurrent.futures.ThreadPoolExecutor() as pool:
            new_emails = await loop.run_in_executor(pool, self._fetch_new_emails)
        return new_emails

    def _fetch_new_emails(self):
        mail = self.login()
        response, email_ids_bytes = mail.uid("search", None, "UNSEEN")
        if response != 'OK':
            print("Failed to search emails.")
            return []

        email_ids = email_ids_bytes[0].decode('utf-8').split()

        if len(email_ids) == 0:
            print("No emails in inbox.")
            return []

        new_emails = []
        for email_id in email_ids:
            response, email_data = mail.uid("fetch", email_id, "(BODY[])")
            if response != 'OK':
                print(f"Failed to fetch email with ID {email_id}.")
                continue
            raw_email = email_data[0][1]
            email_message = email.message_from_bytes(raw_email)

            # Extract the sender's name and email address
            sender_name, sender_addr = parseaddr(email_message['From'])

            new_emails.append((email_message, sender_name, sender_addr))
            mail.uid('store', email_id, '+FLAGS', '(\\Seen)')

        mail.logout()

        return new_emails


    def send_email(self, recipient, subject, body):
        msg = MIMEMultipart()
        msg['From'] = self.user
        msg['To'] = recipient
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP(self.smtp_server, 587)
        server.starttls()
        server.login(self.user, self.password)
        text = msg.as_string()
        server.sendmail(self.user, recipient, text)
        server.quit()


