import logging

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
    CheckForDefectsType,
    CheckForDefectsRange,
    HonestSign

)
from stock.models import Stock, TransitPrice


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("FULFILLMENT_SERVICE")


class FulfillmentService:
    _model = FulFillmentRequest

    @classmethod
    def calculate_price(cls, fulfillment_request: FulFillmentRequest):
        user = fulfillment_request.telegram_client.tg_username
        logger.info(f"{user} -> Init calculation process")
        ff_total_price = 0.0
        material_price = 0.0

        # Acceptance calculation
        acceptance = Acceptance.objects.filter(
            min_quantity__lte=fulfillment_request.quantity,
            max_quantity__gte=fulfillment_request.quantity,
        ).first()
        if acceptance:
            ff_acceptance_price = acceptance.price * fulfillment_request.quantity
            ff_total_price += ff_acceptance_price
            logger.info(f"Acceptance price: {ff_acceptance_price}")

        # Recalculation calculation
        recalculation = Recalculation.objects.filter(
            min_quantity__lte=fulfillment_request.quantity,
            max_quantity__gte=fulfillment_request.quantity,
        ).first()
        if recalculation:
            ff_recalculation_price = recalculation.price * fulfillment_request.quantity
            ff_total_price += ff_recalculation_price
            logger.info(f"Recalculation price: {ff_recalculation_price}")
        #Honest sign
        if fulfillment_request.honest_sign:
            honest_sign = HonestSign.objects.filter(
                min_quantity__lte=fulfillment_request.quantity,
                max_quantity__gte=fulfillment_request.quantity,
            ).first()
            if honest_sign:
                ff_honest_sign_price = honest_sign.price * fulfillment_request.quantity
                ff_total_price += ff_honest_sign_price
                logger.info(f"Honest sign: {ff_honest_sign_price}")
            pass
        # Attachment calculation
        if fulfillment_request.need_attachment:
            attachment = Attachment.objects.filter(
                min_quantity__lte=fulfillment_request.quantity,
                max_quantity__gte=fulfillment_request.quantity,
            ).first()
            if attachment:
                ff_attachment_price = attachment.price * fulfillment_request.quantity
                ff_total_price += ff_attachment_price
                logger.info(f"Attachment price: {ff_attachment_price}")

        # Marking type calculation
        if fulfillment_request.marking_type:
            marking_range = MarkingTypeRange.objects.filter(
                fulfillment_type=fulfillment_request.marking_type,
                min_quantity__lte=fulfillment_request.quantity,
                max_quantity__gte=fulfillment_request.quantity,
            ).first()
            if marking_range:
                ff_marking_price = marking_range.price * fulfillment_request.quantity
                ff_total_price += ff_marking_price
                logger.info(f"Marking price: {ff_marking_price}")

        # Tagging price calculation
        if fulfillment_request.need_taging:
            tagging = TagingPriceRange.objects.filter(
                min_quantity__lte=fulfillment_request.quantity,
                max_quantity__gte=fulfillment_request.quantity,
            ).first()
            if tagging:
                material_price += tagging.price * fulfillment_request.quantity
                logger.info(f"Tagging price: {tagging.price * fulfillment_request.quantity}")

        # Packaging calculation
        if fulfillment_request.package:
            package_size = FulfillmentPackageSize.objects.filter(
                size=fulfillment_request.packaging_size,
                package=fulfillment_request.package,
            ).first()
            if package_size:
                material_price += package_size.price * fulfillment_request.quantity
                logger.info(f"Packaging price: {package_size.price * fulfillment_request.quantity}")

        # Box price calculation
        boxes_count = fulfillment_request.quantity / fulfillment_request.count_of_boxes

        box_range = BoxPriceRange.objects.filter(
            min_quantity__lte=boxes_count,
            max_quantity__gte=boxes_count,
        ).first()
        if box_range:
            box_price = box_range.price * boxes_count
            material_price += box_price
            logger.info(f"Box price: {boxes_count} * {box_range.price} = {box_price}")

        # Transit price calculation
        if fulfillment_request.count_of_boxes > 0 and fulfillment_request.transit:
            transit_price = (
                TransitPrice.objects.filter(
                    stock=fulfillment_request.transit,
                    quantity__lte=boxes_count,
                )
                .order_by("-quantity")
                .first()
            )
            if transit_price:
                total_transit_price = transit_price.price * boxes_count
                
                logger.info(f"Transit price: {boxes_count} * {transit_price.price} = {total_transit_price}")
            else:
                total_transit_price = 0.0
        else:
            total_transit_price = 0.0

        # Check for defects calculation
        if fulfillment_request.need_check_defects:
            defect_range = CheckForDefectsRange.objects.filter(
                defect_type=fulfillment_request.need_check_defects,
                min_quantity__lte=fulfillment_request.quantity,
                max_quantity__gte=fulfillment_request.quantity,
            ).first()
            if defect_range:
                defect_check_price = defect_range.price * fulfillment_request.quantity
                ff_total_price += defect_check_price
                logger.info(f"Defect check price: {defect_check_price}")
        material_price += fulfillment_request.quantity * 11
        fulfillment_request.per_price_material = material_price / fulfillment_request.quantity if fulfillment_request.quantity else 0
        fulfillment_request.per_price_ff = ff_total_price / fulfillment_request.quantity if fulfillment_request.quantity else 0
        fulfillment_request.ff_total_price = ff_total_price
        fulfillment_request.material_total_price = material_price
        fulfillment_request.per_price_transit = total_transit_price / fulfillment_request.quantity
        total_price = ff_total_price + material_price + total_transit_price
        fulfillment_request.save()
        logger.info(f"ff_total_price: {ff_total_price}")
        logger.info(f"material_total_price: {material_price}")
        logger.info(f"transit_total_price: {total_transit_price}")
        logger.info(f"Total price: {total_price}")

        return fulfillment_request

    @classmethod
    def create_request(cls, validated_data):
        need_check_defects_type = None
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
        need_check_defects_type_id = validated_data.get("defect_check_id")
        if need_check_defects_type_id:
            need_check_defects_type = CheckForDefectsType.objects.filter(id=need_check_defects_type_id).first()
        fulfillment_request = FulFillmentRequest(
            product_title=validated_data["product_title"],
            quantity=validated_data["quantity"],
            telegram_client=telegram_client,
            need_check_defects=need_check_defects_type,
            marking_type=marking_type,
            package=package,
            transit=stock,
            need_attachment=validated_data["need_attachment"],
            need_taging=validated_data["need_taging"],
            count_of_boxes=validated_data["count_of_boxes"],
            honest_sign=validated_data.get("honest_sign"),
            packaging_size=validated_data.get("packaging_size"),
        )
        modified_ff = cls.calculate_price(fulfillment_request)

        return modified_ff.id
