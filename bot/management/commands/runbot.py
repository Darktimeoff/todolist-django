from django.conf import settings
from django.core.management import BaseCommand

from bot.tg.client import TgClient
from bot.tg.dc import Message
from bot.models import TgUser
from goals.models import Goal

class Command(BaseCommand):
    help = "run bot"

    tg_client: TgClient

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tg_client = TgClient(settings.BOT_TOKEN)

    def handle_unverify_user(self, user: TgUser, message: Message):
        code = user.set_verification_code()
        self.tg_client.send_message(message.chat.id, f"Your verification code is {code}, please enter on the site")

    def fetch_tasks(self, msg: Message, tg_user: TgUser):
        gls = Goal.objects.filter(user=tg_user.user)
        if gls.count() > 0:
            resp_msg = [f"#{item.pk} {item.title}" for item in gls]
            self.tg_client.send_message(msg.chat.id, "\n".join(resp_msg))
        else:
            self.tg_client.send_message(msg.chat.id, "[goals list is empty]")

    def handle_verify_user(self, user: TgUser, message: Message):
        if not message.text:
            return
        
        if "/goals" in message.text:
            self.fetch_tasks(message, user)
        else:
            self.tg_client.send_message(message.chat.id, "[unknown command]")

    def handle_message(self, message: Message):
        tg_user, created = TgUser.objects.get_or_create(
            tg_id=message.from_.id,
            defaults={
                "tg_chat_id": message.chat.id,
                "username": message.from_.username
            }
        )

        if created:
            self.tg_client.send_message(message.chat.id, f"Hi, {message.from_.first_name or tg_user.username}")

        if tg_user.user:
            self.handle_verify_user(tg_user, message)
        else:
            self.handle_unverify_user(tg_user, message)


    def handle(self, *args, **kwargs):
        offset = 0

        while True:
            res = self.tg_client.get_updates(offset=offset)
            for item in res.result:
                offset = item.update_id + 1
                self.handle_message(item.message)
