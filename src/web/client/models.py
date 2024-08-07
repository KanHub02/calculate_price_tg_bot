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
        "logistic.CargoServiceType",
        on_delete=models.CASCADE,
        related_name="service_price",
        null=True,
        blank=True,
        verbose_name="Сервис",
    )
    price = models.CharField(max_length=255, verbose_name="Цена", null=True, blank=True)

    class Meta:
        verbose_name = "Тип сервиса"
        verbose_name_plural = "Тип сервиса"


class LogisticRequest(BaseModel):
    telegram_client = models.ForeignKey(
        TelegramClient,
        on_delete=models.CASCADE,
        related_name="logistic_requests",
        verbose_name="Клиент Telegram",
    )
    cargo_type = models.ForeignKey(
        "logistic.CargoType",
        on_delete=models.DO_NOTHING,
        related_name="logistic_requests",
        null=True,
        blank=True,
        verbose_name="Тип груза",
    )
    cargo_package_type = models.ForeignKey(
        "logistic.CargoPackage",
        on_delete=models.CASCADE,
        related_name="logistic_requests",
        verbose_name="Тип упаковки груза",
    )
    weight = models.FloatField(null=True, blank=True, verbose_name="Вес")
    volume = models.FloatField(null=True, blank=True, verbose_name="Объем")
    density = models.FloatField(null=True, blank=True, verbose_name="Плотность")
    price_before_insurance = models.FloatField(
        null=True, blank=True, verbose_name="Цена товара"
    )
    insurance_cost = models.FloatField(
        null=True, blank=True, verbose_name="Цена страховки"
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
    need_check_defects = models.ForeignKey(
        "fulfillment.CheckForDefectsType",
        on_delete=models.SET_NULL,
        related_name="fulfillment_requests",
        blank=True,
        null=True,
        verbose_name="Проверка на брак",
    )
    marking_type = models.ForeignKey(
        "fulfillment.MarkingType",
        on_delete=models.SET_NULL,
        related_name="fulfillment_requests",
        blank=True,
        null=True,
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
    packaging_size = models.CharField(
        verbose_name="Вид упаковки", max_length=255, null=True, blank=True
    )
    transit = models.ForeignKey(
        "stock.Stock",
        verbose_name="Транзит",
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
        related_name="fulfillment_request",
    )
    need_attachment = models.BooleanField(
        verbose_name="Вложения", default=False, null=True
    )
    need_taging = models.BooleanField(
        verbose_name="Биркование", default=False, null=True
    )
    count_of_boxes = models.FloatField(
        verbose_name="Кол-во коробов", default=0.0, null=True
    )
    honest_sign = models.BooleanField(
        verbose_name="Честный знак", default=False, null=True
    )
    material_total_price = models.FloatField(
        verbose_name="Цена за материал", null=True, blank=True, default=0.0
    )
    ff_total_price = models.FloatField(
        verbose_name="Цена за фф", null=True, blank=True, default=0.0
    )
    per_price_ff = models.FloatField(
        verbose_name="Цена за единицу фф", null=True, blank=True, default=0.0
    )
    per_price_material = models.FloatField(
        verbose_name="Цена единицы за материал", null=True, blank=True, default=0.0
    )
    per_price_transit = models.FloatField(
        verbose_name="Цена единицы за транзит", null=True, blank=True, default=0.0
    )

    class Meta:
        verbose_name = "Запрос на фулфилмент"
        verbose_name_plural = "Запросы на фулфилмент"

    def __str__(self):
        return f"Запрос на выполнение от {self.telegram_client} - {self.product_title}"


class FeedbackForUseful(BaseModel):
    telegram_client = models.ForeignKey(
        TelegramClient,
        on_delete=models.CASCADE,
        related_name="feedback_requests",
        verbose_name="Клиент Telegram",
    )
    feedback = models.TextField(verbose_name="Пожелание")

    def __str__(self):
        return f"Отзыв от {self.telegram_client.tg_id}: {self.feedback}"

    class Meta:
        verbose_name = "Отзыв по полезным статьям"
        verbose_name_plural = "Отзывы по полезным статьям"
