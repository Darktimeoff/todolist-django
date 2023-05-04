from django.db import models
import random

CODE_VOCABULARY = "qwertyuasdfghkzxvbnm123456789"

class TgUser(models.Model):
    tg_id = models.BigIntegerField(unique=True)
    tg_chat_id = models.BigIntegerField(verbose_name="tg chat id")
    username = models.CharField(max_length=512, null=True, default=None)

    verification_code = models.CharField(max_length=32, blank=True, null=True, default=None)

    user = models.OneToOneField(
        "core.User",
        on_delete=models.PROTECT,
        related_name="tg_user",
        null=True,
        default=None
    )

    def set_verification_code(self):
        code = "".join([random.choice(CODE_VOCABULARY) for _ in range(12)])
        self.verification_code = code

        return code