from django.db import models
from common.models import BaseModel


class FulfillmentType(BaseModel):
    title = models.CharField(max_length=255, null=False, blank=False)


class FulfillmentTypeRange(BaseModel):
    fulfillment_type = models.ForeignKey(
        "fulfillment.FulfillmentType",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name="fulfillment_type_range",
    )
    min_quantity = models.PositiveIntegerField()
    max_quantity = models.PositiveIntegerField()
    price = models.FloatField()


class CargoType(BaseModel):
    title = models.CharField(max_length=255, null=False, blank=False)


class CargoTypeRange(BaseModel):
    cargo_type = models.ForeignKey(
        "fulfillment.CargoType",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name="cargo_type_range",
    )
    min_quantity = models.PositiveIntegerField()
    max_quantity = models.PositiveIntegerField()
    price = models.FloatField()


class CargoPackage(BaseModel):
    title = models.CharField(max_length=255, null=False, blank=False)


class FulfillmentPackage(BaseModel):
    title = models.CharField(max_length=255, null=False, blank=False)
