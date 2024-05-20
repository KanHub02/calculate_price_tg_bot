from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from common.models import BaseModel

class TelegramClient(BaseModel):
    tg_username = models.CharField(max_length=255, null=True, blank=True, verbose_name='Имя пользователя Telegram')
    tg_id = models.CharField(max_length=255, verbose_name='ID Telegram')
    phone_number = PhoneNumberField(blank=True, null=True, verbose_name='Номер телефона')
    tg_bio = models.TextField(null=True, blank=True, verbose_name='Биография')

    class Meta:
        verbose_name = 'Клиент Telegram'
        verbose_name_plural = 'Клиенты Telegram'

    def __str__(self):
        return f'{self.tg_username} ({self.tg_id})'


class CargoServicePrice(BaseModel):
    logistic_request = models.ForeignKey("client.LogisticRequest", on_delete=models.CASCADE, related_name="service_price", null=True, blank=True)
    cargo_service = models.ForeignKey("fulfillment.CargoServiceType", on_delete=models.CASCADE, related_name="service_price", null=True, blank=True)
    price = models.FloatField()

class LogisticRequest(BaseModel):
    telegram_client = models.ForeignKey(
        TelegramClient,
        on_delete=models.CASCADE,
        related_name="logistic_requests",
        verbose_name='Клиент Telegram'
    )
    cargo_type = models.ForeignKey(
        'fulfillment.CargoType',
        on_delete=models.DO_NOTHING,
        related_name="logistic_requests",
        null=True, blank=True,
        verbose_name='Тип груза'
    )
    cargo_package_type = models.ForeignKey(
        'fulfillment.CargoPackage',
        on_delete=models.CASCADE,
        related_name="logistic_requests",
        verbose_name='Тип упаковки груза'
    )
    weight = models.FloatField(null=True, blank=True, verbose_name='Вес')
    quantity = models.FloatField(null=True, blank=True, verbose_name='Количество')
    insurance_cost = models.FloatField(null=True, blank=True, verbose_name="Cтоимость товара")
    express_price = models.CharField(max_length=255, null=True, blank=True, verbose_name='Цена за экспресс-доставку')
    standart_price = models.CharField(max_length=255, null=True, blank=True, verbose_name='Цена за стандартную доставку')


    class Meta:
        verbose_name = 'Логистический запрос'
        verbose_name_plural = 'Логистические запросы'

    def __str__(self):
        return f'Запрос от {self.telegram_client}'

class FulFillmentRequest(BaseModel):
    telegram_client = models.ForeignKey(
        TelegramClient,
        on_delete=models.CASCADE,
        related_name="fulfillment_requests",
        verbose_name='Клиент Telegram'
    )
    fulfillments = models.ManyToManyField(
        'fulfillment.FulfillmentType',
        related_name="fulfillment_requests",
        blank=True,
        verbose_name='Виды выполнения'
    )
    express_price = models.FloatField(null=True, blank=True, verbose_name='Цена за экспресс-выполнение')
    standart_price = models.FloatField(null=True, blank=True, verbose_name='Цена за стандартное выполнение')
    package = models.ForeignKey(
        'fulfillment.FulfillmentPackage',
        on_delete=models.DO_NOTHING,
        related_name="fulfillment_requests",
        null=True, blank=True,
        verbose_name='Упаковка'
    )

    class Meta:
        verbose_name = 'Запрос на выполнение'
        verbose_name_plural = 'Запросы на выполнение'

    def __str__(self):
        return f'Запрос на выполнение от {self.telegram_client}'

# Remember to ensure that related classes in the 'fulfillment' module also have appropriate verbose_name attributes set.
