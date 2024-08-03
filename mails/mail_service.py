import imaplib
import email
from email.header import decode_header
import datetime
from mails.models import EmailMessage, EmailAccount
import re
from asgiref.sync import async_to_sync


class MailService:
    def __init__(self, email_account, consumer):
        self.email_account = email_account
        self.consumer = consumer
        self.server = self._connect()

    def _connect(self):
        if self.email_account.provider == 'yandex':
            server = imaplib.IMAP4_SSL('imap.yandex.ru')
        elif self.email_account.provider == 'gmail':
            server = imaplib.IMAP4_SSL('imap.gmail.com')
        elif self.email_account.provider == 'mailru':
            server = imaplib.IMAP4_SSL('imap.mail.ru')
        else:
            raise ValueError('Unknown email provider')

        server.login(self.email_account.email, self.email_account.password)
        return server

    def fetch_messages(self, last_received_date=None):
        self.server.select('inbox')

        if last_received_date:
            date_str = last_received_date.strftime("%d-%b-%Y")
            status, messages = self.server.search(None, f'(SINCE {date_str})')
        else:
            status, messages = self.server.search(None, 'ALL')

        if status != 'OK':
            return []

        total_messages = len(messages[0].split())
        message_list = []
        for idx, num in enumerate(messages[0].split(), start=1):
            try:
                async_to_sync(self.consumer.send_progress)({
                    'status': 'parsing',
                    'progress': f'{idx}/{total_messages}'
                })
                status, data = self.server.fetch(num, '(RFC822)')
                if status != 'OK':
                    continue

                raw_email = data[0][1]
                msg = email.message_from_bytes(raw_email)
                subject, encoding = decode_header(msg['Subject'])[0]
                if isinstance(subject, bytes):
                    try:
                        subject = subject.decode(encoding if encoding else 'utf-8')
                    except (LookupError, UnicodeDecodeError):
                        continue

                try:
                    sent_date = email.utils.parsedate_to_datetime(msg['Date'])
                except (TypeError, ValueError):
                    continue

                received_date = datetime.datetime.now()

                body = ""
                if msg.is_multipart():
                    for part in msg.walk():
                        if part.get_content_type() == "text/plain" and "attachment" not in part.get(
                                "Content-Disposition", ""):
                            try:
                                body = part.get_payload(decode=True).decode(part.get_content_charset() or 'utf-8')
                            except UnicodeDecodeError:
                                body = part.get_payload(decode=True).decode('latin1')
                            except LookupError:
                                continue
                            break
                else:
                    try:
                        body = msg.get_payload(decode=True).decode(msg.get_content_charset() or 'utf-8')
                    except UnicodeDecodeError:
                        body = msg.get_payload(decode=True).decode('latin1')
                    except LookupError:
                        continue

                attachments = []
                if msg.is_multipart():
                    for part in msg.walk():
                        if part.get_content_maintype() == 'multipart':
                            continue
                        if part.get('Content-Disposition') is None:
                            continue

                        file_name = part.get_filename()
                        if bool(file_name):
                            attachments.append(file_name)

                if self.email_account.provider == 'mailru':
                    body = self._process_mailru_body(body)

                email_message = {
                    'email_account': self.email_account,
                    'subject': subject,
                    'sent_date': sent_date,
                    'received_date': received_date,
                    'body': body,
                    'attachments': attachments
                }
                message_list.append(email_message)
            except:
                continue

        return message_list

    def _process_mailru_body(self, body):
        body = re.sub(r'<[^>]+>', '', body)
        body = body.replace('\r', '').replace('\n', ' ').strip()
        return body

    def save_messages(self, messages):
        for msg in messages:
            EmailMessage.objects.create(**msg)
