import json
import logging
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

logger = logging.getLogger(__name__)


class MailConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        logger.debug("WebSocket connection opened")
        await self.accept()

    async def disconnect(self, close_code):
        logger.debug("WebSocket connection closed")

    async def receive(self, text_data):
        logger.debug("Received data: %s", text_data)
        text_data_json = json.loads(text_data)
        email_account_id = text_data_json.get('email_account_id')

        from .models import EmailAccount, EmailMessage
        from .mail_service import MailService

        if email_account_id is not None:
            try:
                email_account = await sync_to_async(EmailAccount.objects.get)(id=email_account_id)

                mail_service = MailService(email_account, self)

                last_message = await sync_to_async(
                    EmailMessage.objects.filter(email_account=email_account).order_by('-received_date').first)()
                last_received_date = last_message.received_date if last_message else None

                messages = await sync_to_async(mail_service.fetch_messages)(last_received_date)

                total_messages = len(messages)
                for idx, msg in enumerate(messages):
                    await sync_to_async(mail_service.save_messages)([msg])
                    await self.send(text_data=json.dumps({
                        'status': 'saving',
                        'progress': f'{idx + 1}/{total_messages}'
                    }))
                    await self.send(text_data=json.dumps({
                        'subject': msg['subject'],
                        'sent_date': msg['sent_date'].strftime('%Y-%m-%d %H:%M:%S'),
                        'received_date': msg['received_date'].strftime('%Y-%m-%d %H:%M:%S'),
                        'body': msg['body'],
                        'attachments': msg['attachments'],
                    }))
            except EmailAccount.DoesNotExist:
                logger.error("EmailAccount with id %d not found", email_account_id)
                await self.send(text_data=json.dumps({
                    'error': 'EmailAccount not found'
                }))
            except Exception as e:
                logger.error("Error processing emails: %s", str(e))
                await self.send(text_data=json.dumps({
                    'error': 'An error occurred while processing emails'
                }))
        else:
            logger.error("No email_account_id provided")
            await self.send(text_data=json.dumps({
                'error': 'No email_account_id provided'
            }))

    async def send_progress(self, message):
        await self.send(text_data=json.dumps(message))
