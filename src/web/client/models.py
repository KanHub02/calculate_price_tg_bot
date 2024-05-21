from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from common.models import BaseModel


class TelegramClient(BaseModel):
    tg_username = models.CharField(
        max_length=255, null=True, blank=True, verbose_name="Имя пользователя Telegram"
    )
    tg_id = models.CharField(max_length=255, verbose_name="ID Telegram")
    phone_number = PhoneNumberField(
        blank=True, null=True, verbose_name="Номер телефона"
    )
    tg_bio = models.TextField(null=True, blank=True, verbose_name="Биография")

    class Meta:
        verbose_name = "Клиент Telegram"
        verbose_name_plural = "Клиенты Telegram"

    def __str__(self):
        return f"{self.tg_username} ({self.tg_id})"


class CargoServicePrice(BaseModel):
    logistic_request = models.ForeignKey(
        "client.LogisticRequest",
        on_delete=models.CASCADE,
        related_name="service_price",
        null=True,
        blank=True,
    )
    cargo_service = models.ForeignKey(
        "fulfillment.CargoServiceType",
        on_delete=models.CASCADE,
        related_name="service_price",
        null=True,
        blank=True,
    )
    price = models.FloatField()


class LogisticRequest(BaseModel):
    telegram_client = models.ForeignKey(
        TelegramClient,
        on_delete=models.CASCADE,
        related_name="logistic_requests",
        verbose_name="Клиент Telegram",
    )
    cargo_type = models.ForeignKey(
        "fulfillment.CargoType",
        on_delete=models.DO_NOTHING,
        related_name="logistic_requests",
        null=True,
        blank=True,
        verbose_name="Тип груза",
    )
    cargo_package_type = models.ForeignKey(
        "fulfillment.CargoPackage",
        on_delete=models.CASCADE,
        related_name="logistic_requests",
        verbose_name="Тип упаковки груза",
    )
    weight = models.FloatField(null=True, blank=True, verbose_name="Вес")
    quantity = models.FloatField(null=True, blank=True, verbose_name="Количество")
    insurance_cost = models.FloatField(
        null=True, blank=True, verbose_name="Cтоимость товара"
    )

    class Meta:
        verbose_name = "Запрос на груз"
        verbose_name_plural = "Запросы на груз"

    def __str__(self):
        return f"Запрос от {self.telegram_client}"


class FulFillmentRequest(BaseModel):
    product_title = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="Товар"
    )
    quantity = models.FloatField(null=True, blank=True, verbose_name="Количество")
    telegram_client = models.ForeignKey(
        TelegramClient,
        on_delete=models.CASCADE,
        related_name="fulfillment_requests",
        verbose_name="Клиент Telegram",
    )
    marking_type = models.ManyToManyField(
        "fulfillment.MarkingType",
        related_name="fulfillment_requests",
        blank=True,
        verbose_name="Вид Маркировки",
    )
    package = models.ForeignKey(
        "fulfillment.FulfillmentPackage",
        on_delete=models.DO_NOTHING,
        related_name="fulfillment_requests",
        null=True,
        blank=True,
        verbose_name="Упаковка",
    )
    transit = models.ForeignKey("stock.Stock", verbose_name="Транзит", on_delete=models.DO_NOTHING, null=True, blank=True, related_name="fulfillment_request")
    need_attachment = models.BooleanField(verbose_name="Вложения")
    need_taging = models.BooleanField(verbose_name="Биркование")
    count_of_boxes = models.FloatField(verbose_name="Кол-во коробов")
    honest_sign = models.BooleanField(verbose_name="Честный знак")

    class Meta:
        verbose_name = "Запрос на фулфилмент"
        verbose_name_plural = "Запросы на фулфилмент"

    def __str__(self):
        return f"Запрос на выполнение от {self.telegram_client}"


# Remember to ensure that related classes in the 'fulfillment' module also have appropriate verbose_name attributes set.
