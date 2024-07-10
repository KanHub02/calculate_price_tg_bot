from django.db import models

from phonenumber_field.modelfields import PhoneNumberField


from common.models import BaseModel, SingletonModel


class Manager(BaseModel):
    full_name = models.CharField(verbose_name="ФИО", max_length=255)
    tg_username = models.CharField(
        max_length=255, null=True, blank=True, verbose_name="Имя пользователя Telegram"
    )
    tg_id = models.CharField(max_length=255, verbose_name="ID Telegram")
    phone_number = PhoneNumberField(
        blank=True, null=True, verbose_name="Номер телефона"
    )

    class Meta:
        verbose_name = "Менеджер"
        verbose_name_plural = "Менеджера"


class FeedbackLink(BaseModel):
    title = models.CharField(max_length=255, verbose_name="Название")
    link = models.URLField(verbose_name="Ссылка для отзыва", null=True, blank=True)

    class Meta:
        verbose_name = "Ссылка для отзыва"
        verbose_name = "Ссылки для отзывов"


class PartnerLead(SingletonModel):

    link = models.URLField(verbose_name="Ссылка на опросник")

    class Meta:

        verbose_name = "Стать Партнером"
        verbose_name_plural = "Стать Партнером"


class HowToUse(SingletonModel):
    text = models.TextField(verbose_name="Текст", null=True, blank=False)

    class Meta:
        verbose_name = "Как пользоваться ботом"
        verbose_name_plural = "Как пользоваться ботом"


class WorkingConditions(SingletonModel):
    text = models.TextField(verbose_name="Текст", null=True, blank=False)

    class Meta:
        verbose_name = "Условия работы"
        verbose_name_plural = "Условия работы"
