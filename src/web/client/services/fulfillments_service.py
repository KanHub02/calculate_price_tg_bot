from ..models import FulFillmentRequest, TelegramClient
from fulfillment.models import (
    MarkingType,
    MarkingTypeRange,
    FulfillmentPackage,
    FulfillmentPackageSize,
    TagingPriceRange,
    BoxPriceRange,
    MarkingBoxPriceRange,
    LayingBoxPriceRange,
    Acceptance,
    TagingPriceRangeFF
)
from stock.models import Stock, TransitPrice


class FulfillmentService:
    _model = FulFillmentRequest

    @classmethod
    def calculate_price(cls, fulfillment_request):
        ff_total_price = 0.0
        material_price = 0.0

        acceptance = Acceptance.objects.all()
        if acceptance:
            ff_total_price += acceptance[0].ff_per_price * fulfillment_request.quantity

        if fulfillment_request.package:
            package_sizes = FulfillmentPackageSize.objects.filter(
                package=fulfillment_request.package
            )
            for package_size in package_sizes:
                ff_total_price += fulfillment_request.package.ff_per_price * fulfillment_request.quantity
                material_price += package_size.price * fulfillment_request.quantity



        # Calculate price per box
        if fulfillment_request.count_of_boxes > 0:
            price_per_box = fulfillment_request.quantity // fulfillment_request.count_of_boxes
        else:
            price_per_box = 0  # Handling division by zero if count_of_boxes is not set

        if price_per_box > 0:
            transit_price = TransitPrice.objects.filter(
                stock=fulfillment_request.transit,
                quantity__lte=price_per_box,
                quantity__gte=price_per_box
            ).first()

            if transit_price:
                per_price_transit = price_per_box * transit_price.price / fulfillment_request.quantity
                fulfillment_request.per_price_transit = per_price_transit


        marking_type = fulfillment_request.marking_type
        marking_ranges = MarkingTypeRange.objects.filter(
            fulfillment_type=marking_type,
            min_quantity__lte=fulfillment_request.quantity,
            max_quantity__gte=fulfillment_request.quantity,
        )
        for marking_range in marking_ranges:
            ff_total_price += fulfillment_request.marking_type.ff_per_price * fulfillment_request.quantity
            material_price += marking_range.price

        if fulfillment_request.need_taging:
            taging_price_ranges = TagingPriceRange.objects.filter(
                min_quantity__lte=fulfillment_request.quantity,
                max_quantity__gte=fulfillment_request.quantity,
            )
            tagging_ff = TagingPriceRangeFF.objects.all()
            if tagging_ff:
                ff_total_price += tagging_ff.ff_per_price * fulfillment_request.quantity
            for range in taging_price_ranges:
                material_price += range.price * fulfillment_request.quantity

        if fulfillment_request.count_of_boxes > 0:
            box_price_ranges = BoxPriceRange.objects.filter(
                min_quantity__lte=fulfillment_request.count_of_boxes,
                max_quantity__gte=fulfillment_request.count_of_boxes,
            )
            marking_price_boxes = MarkingBoxPriceRange.objects.filter(
                min_quantity__lte=fulfillment_request.count_of_boxes,
                max_quantity__gte=fulfillment_request.count_of_boxes,
            )
            laying_price_range = LayingBoxPriceRange.objects.filter(
                min_quantity__lte=fulfillment_request.count_of_boxes,
                max_quantity__gte=fulfillment_request.count_of_boxes,
            )
            for b_range in box_price_ranges:
                material_price += b_range.price * fulfillment_request.count_of_boxes
            for m_range in marking_price_boxes:
                material_price += m_range.price * fulfillment_request.count_of_boxes

            for l_range in laying_price_range:
                material_price += l_range.price * fulfillment_request.count_of_boxes

        return ff_total_price, material_price

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

        ff_total_price, material_price = cls.calculate_price(fulfillment_request)
        fulfillment_request.material_total_price = material_price
        fulfillment_request.ff_total_price = ff_total_price
        fulfillment_request.per_price = (ff_total_price + material_price) / fulfillment_request.quantity
        fulfillment_request.save()
        return fulfillment_request.id
