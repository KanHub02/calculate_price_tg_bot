from django.db import models

from common.models import BaseModel
from phonenumber_field.modelfields import PhoneNumberField


class TelegramClient(BaseModel):
    tg_username = models.CharField(null=True, blank=True, max_length=255)
    tg_id = models.CharField(max_length=255)
    phone_number = PhoneNumberField(blank=True, null=True)
    tg_bio = models.TextField(null=True, blank=True)


class LogisticRequest(BaseModel):
    cargo_type = models.ForeignKey("fulfillment.CargoType", on_delete=models.DO_NOTHING, blank=True, null=True, related_name="request")
    telegram_client = models.ForeignKey("client.TelegramClient", on_delete=models.CASCADE, related_name="logistic_request", null=False, blank=False)
    express_price = models.FloatField(null=True, blank=True)
    standart_price = models.FloatField(null=True, blank=True)
    pass


class FulFillmentRequest(BaseModel):
    fulfillments = models.ManyToManyField("fulfillment.FulfillmentType", blank=True, null=True, related_name="fulfillment_requests")
    telegram_client = models.ForeignKey("client.TelegramClient", on_delete=models.CASCADE, related_name="fulfillment_request", null=False, blank=False)
    express_price = models.FloatField(null=True, blank=True)
    standart_price = models.FloatField(null=True, blank=True)
    package = models.ForeignKey("fulfillment.FulfillmentPackage", on_delete=models.DO_NOTHING, related_name="fulfillment_request", null=True, blank=True)
    pass

