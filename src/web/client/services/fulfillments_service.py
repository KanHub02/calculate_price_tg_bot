from ..models import FulFillmentRequest, TelegramClient
from fulfillment.models import (
    MarkingType,
    MarkingTypeRange,
    FulfillmentPackage,
    FulfillmentPackageSize,
    TagingPriceRange,
    BoxPriceRange,
)
from stock.models import Stock


class FulfillmentService:
    _model = FulFillmentRequest

    @classmethod
    def calculate_price(cls, fulfillment_request):
        total_price = 0.0

        if fulfillment_request.package:
            package_sizes = FulfillmentPackageSize.objects.filter(
                package=fulfillment_request.package
            )
            for package_size in package_sizes:
                total_price += package_size.price * fulfillment_request.quantity

        marking_types = fulfillment_request.marking_type.all()
        for marking_type in marking_types:
            marking_ranges = MarkingTypeRange.objects.filter(
                fulfillment_type=marking_type,
                min_quantity__lte=fulfillment_request.quantity,
                max_quantity__gte=fulfillment_request.quantity,
            )
            for marking_range in marking_ranges:
                total_price += marking_range.price

        if fulfillment_request.need_taging:
            taging_price_ranges = TagingPriceRange.objects.filter(
                min_quantity__lte=fulfillment_request.quantity,
                max_quantity__gte=fulfillment_request.quantity,
            )
            for range in taging_price_ranges:
                total_price += range.price * fulfillment_request.quantity

        if fulfillment_request.count_of_boxes > 0:
            box_price_ranges = BoxPriceRange.objects.filter(
                min_quantity__lte=fulfillment_request.count_of_boxes,
                max_quantity__gte=fulfillment_request.count_of_boxes,
            )
            for range in box_price_ranges:
                total_price += range.price * fulfillment_request.count_of_boxes

        return total_price

    @classmethod
    def create_request(cls, validated_data):
        telegram_client = TelegramClient.objects.get(
            tg_id=validated_data["tg_client_id"]
        )
        marking_type = MarkingType.objects.filter(
            id=validated_data["marking_type_id"]
        ).first()
        package = FulfillmentPackage.objects.filter(id=validated_data["package_id"])
        stock = Stock.objects.filter(id=validated_data["stock_id"]).first()
        total_price = 0.0
        fulfillment_request = FulFillmentRequest(
            product_title=validated_data["product_title"],
            quantity=validated_data["quantity"],
            telegram_client=telegram_client,
            marking_type=marking_type,
            package=package,
            transit=stock,
            need_attachment=validated_data["need_attachment"],
            need_taging=validated_data["need_taging"],
            count_of_boxes=validated_data["count_of_boxes"],
            honest_sign=validated_data["honest_sign"],
        )

        total_price = cls.calculate_price(fulfillment_request)
        fulfillment_request.per_price = total_price / fulfillment_request.quantity
        return fulfillment_request, total_price
