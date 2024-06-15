from ..models import FulFillmentRequest, TelegramClient
from fulfillment.models import (
    MarkingType,
    MarkingTypeRange,
    FulfillmentPackage,
    FulfillmentPackageSize,
    Acceptance,
    Recalculation,
    Attachment,
    TagingPriceRange,
    TagingPriceRangeFF,
    BoxPriceRange,
    MarkingBoxPriceRangeFF,
    LayingBoxPriceRange,
)
from stock.models import Stock, TransitPrice


class FulfillmentService:
    _model = FulFillmentRequest

    @classmethod
    def calculate_price(cls, fulfillment_request):
        ff_total_price = 0.0
        material_price = 0.0

        # Acceptance calculation
        if fulfillment_request:
            acceptance = Acceptance.objects.filter(
                min_quantity__lte=fulfillment_request.quantity,
                max_quantity__gte=fulfillment_request.quantity,
            ).first()
            print(acceptance)
            if acceptance:
                print(acceptance.price * fulfillment_request.quantity)
                ff_total_price += acceptance.price * fulfillment_request.quantity

        # Recalculation calculation
        if fulfillment_request:
            recalculation = Recalculation.objects.filter(
                min_quantity__lte=fulfillment_request.quantity,
                max_quantity__gte=fulfillment_request.quantity,
            ).first()

            print(recalculation)
            if recalculation:
                print(recalculation.price * fulfillment_request.quantity)
                ff_total_price += recalculation.price * fulfillment_request.quantity

        # Attachment calculation
        if fulfillment_request.need_attachment:
            attachment = Attachment.objects.filter(
                min_quantity__lte=fulfillment_request.quantity,
                max_quantity__gte=fulfillment_request.quantity,
            ).first()
            print(attachment)
            if attachment:
                print(attachment.price * fulfillment_request.quantity)
                ff_total_price += attachment.price * fulfillment_request.quantity

        # Packaging calculation
        if fulfillment_request.package:
            package_size = FulfillmentPackageSize.objects.filter(
                size=fulfillment_request.packaging_size,
                package=fulfillment_request.package,
            ).first()
            if package_size:
                material_price += package_size.price * fulfillment_request.quantity

        # Marking type calculation
        if fulfillment_request.marking_type:
            marking_range = MarkingTypeRange.objects.filter(
                fulfillment_type=fulfillment_request.marking_type,
                min_quantity__lte=fulfillment_request.quantity,
                max_quantity__gte=fulfillment_request.quantity,
            ).first()
            print(marking_range)
            if marking_range:
                print(marking_range.price * fulfillment_request.quantity)
                ff_total_price += marking_range.price * fulfillment_request.quantity

        # Tagging price calculation
        if fulfillment_request.need_taging:
            tagging = TagingPriceRange.objects.filter(
                min_quantity__lte=fulfillment_request.quantity,
                max_quantity__gte=fulfillment_request.quantity,
            ).first()
            if tagging:
                material_price += tagging.price * fulfillment_request.quantity

        # Box price calculation
        if fulfillment_request.count_of_boxes > 0:
            box_range = BoxPriceRange.objects.filter(
                min_quantity__lte=fulfillment_request.count_of_boxes,
                max_quantity__gte=fulfillment_request.count_of_boxes,
            ).first()
            if box_range:
                material_price += box_range.price * fulfillment_request.count_of_boxes

        if fulfillment_request.count_of_boxes > 0:
            price_per_box = (
                fulfillment_request.quantity // fulfillment_request.count_of_boxes
            )
        else:
            price_per_box = 0  # Handling division by zero if count_of_boxes is not set

        if price_per_box > 0:
            # Ищем транзитную цену, которая соответствует количеству единиц в коробке
            transit_price = (
                TransitPrice.objects.filter(
                    stock=fulfillment_request.transit,
                    quantity__lte=price_per_box,  # Должно быть меньше или равно количеству в коробке
                )
                .order_by("-quantity")
                .first()
            )  # Выбираем наибольшее подходящее значение

            if transit_price:
                print(transit_price)
                # Рассчитываем стоимость транзита на единицу товара
                per_price_transit = (
                    price_per_box
                    * transit_price.price
                    / fulfillment_request.count_of_boxes
                )
                fulfillment_request.per_price_transit = per_price_transit

        fulfillment_request.per_price_material = (
            material_price / fulfillment_request.quantity
        )
        fulfillment_request.per_price_ff = (
            ff_total_price
        ) / fulfillment_request.quantity
        fulfillment_request.ff_total_price = ff_total_price
        fulfillment_request.material_total_price = material_price
        fulfillment_request.save()

    @classmethod
    def create_request(cls, validated_data):
        telegram_client = TelegramClient.objects.filter(
            tg_id=validated_data["tg_client_id"]
        ).first()
        marking_type = MarkingType.objects.filter(
            id=validated_data["marking_type_id"]
        ).first()
        package = FulfillmentPackage.objects.filter(
            id=validated_data["package_id"]
        ).first()
        stock = Stock.objects.filter(id=validated_data["stock_id"]).first()
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
            honest_sign=validated_data.get("honest_sign"),
            packaging_size=validated_data.get("packaging_size"),
        )
        fulfillment_request.save()
        cls.calculate_price(fulfillment_request)

        return fulfillment_request.id
