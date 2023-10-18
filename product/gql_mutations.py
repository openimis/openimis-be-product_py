import datetime
from gettext import gettext as _
from operator import or_
from dataclasses import dataclass

import graphene
from core.schema import OpenIMISMutation
from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import ValidationError, PermissionDenied
from graphene.types.decimal import Decimal
from location.models import Location
from .services import (
    set_product_details,
    set_product_relative_distribution,
    set_product_deductible_and_ceiling,
    save_product_history,
    check_unique_code_product
)
from .apps import ProductConfig
from .models import Product, ProductItem, ProductService, ProductMutation, LIMIT_CHOICES
from .enums import (
    CareTypeEnum,
    CeilingExclusionEnum,
    CeilingInterpretationEnum,
    CeilingTypeEnum,
    LimitTypeEnum,
    PriceOriginEnum,
)


@dataclass
class DeductibleOrCeilingValue:
    all: Decimal
    ip: Decimal
    op: Decimal


def extract_deductibles(data):
    return DeductibleOrCeilingValue(
        data.pop("deductible", 0),
        data.pop("deductible_ip", 0),
        data.pop("deductible_op", 0),
    )


def extract_ceilings(data):
    return DeductibleOrCeilingValue(
        data.pop("ceiling", 0), data.pop(
            "ceiling_ip", 0), data.pop("ceiling_op", 0)
    )


def create_or_update_product(user, data, is_duplicate=False):
    client_mutation_id = data.pop("client_mutation_id", None)
    data.pop("client_mutation_label", None)
    product_uuid = data.pop("uuid", None)
    location_uuid = data.pop("location_uuid", None)
    conversion_product_uuid = data.pop("conversion_product_uuid", None)
    relative_prices = data.pop("relative_prices", None)
    items = data.pop("items", None)
    services = data.pop("services", None)
    ceiling_type = data.get("ceiling_type", None)
    deductibles = extract_deductibles(data)
    ceilings = extract_ceilings(data)
    hist_id=None
    incoming_code = data.get('code')
    current_product = Product.objects.filter(uuid=product_uuid).first()
    current_code = current_product.code if current_product else None

    if current_code != incoming_code:
        if check_unique_code_product(incoming_code):
            raise ValidationError(_("mutation.product_code_duplicated"))

    # Validate start cycles
    for start_cycle_key in [
        "start_cycle_1",
        "start_cycle_2",
        "start_cycle_3",
        "start_cycle_4",
    ]:
        if start_cycle_key not in data or data[start_cycle_key] is None:
            continue
        try:
            [d, m] = data[start_cycle_key].split("-")
        except ValueError:
            raise ValueError(
                f"'{data[start_cycle_key]}' is not a correct value for product.start_cycle"
            )

    if items:
        for item in items:
            values = [(item['limitation_type'], item['limit_adult']),
                      (item['limitation_type_e'], item['limit_adult_e']),
                      (item['limitation_type_r'], item['limit_adult_r']),
                      (item['limitation_type'], item['limit_child']),
                      (item['limitation_type_e'], item['limit_child_e']),
                      (item['limitation_type_r'], item['limit_child_r'])]
            # checking if value can be interpreted as percentage
            if not all([True if float(i[1]) >= 0 else False for i in values]):
                raise ValueError("Item O,R,E limits must be positive.")
            if not all([True if float(i[1]) <= 100 else False for i in values if i[0] != LIMIT_CHOICES[0][0]]):
                raise ValueError(
                    "Item O,R,E co-insurance limits must be smaller or equal to 100.")

    if services:
        for service in services:
            values = [(service['limitation_type'], service['limit_adult']),
                      (service['limitation_type_e'], service['limit_adult_e']),
                      (service['limitation_type_r'], service['limit_adult_r']),
                      (service['limitation_type'], service['limit_child']),
                      (service['limitation_type_e'], service['limit_child_e']),
                      (service['limitation_type_r'], service['limit_child_r'])]
            # checking if value can be interpreted as percentage
            if not all([True if float(i[1]) >= 0 else False for i in values]):
                raise ValueError("Service O,R,E limits must be positive.")
            if not all([True if float(i[1]) <= 100 else False for i in values if i[0] != LIMIT_CHOICES[0][0]]):
                raise ValueError(
                    "Service O,R,E co-insurance limits must be smaller or equal to 100.")

    if data["date_from"] > data["date_to"]:
        raise ValueError("date_from must be before date_to")
    if product_uuid:
        product = Product.objects.get(uuid=product_uuid)
        if product.validity_to:
            raise ValidationError("Cannot update historical data.")
        hist_id = save_product_history(product,items,services)
        for (key, value) in data.items():
            setattr(product, key, value)
    else:
        product = Product.objects.create(**data)

    if location_uuid is not None:
        product.location = Location.objects.get(uuid=location_uuid)

    if conversion_product_uuid is not None:
        product.conversion_product = Product.objects.get(
            uuid=conversion_product_uuid)
    set_product_details(product.items, 'Item', hist_id, items, user) 
    set_product_details(product.services,'Service', hist_id, services, user) 
    set_product_relative_distribution(product, hist_id, relative_prices,user)

    set_product_deductible_and_ceiling(
        product, ceiling_type, deductibles, ceilings, user
    )

    product.validity_from = datetime.datetime.now()
    product.save()

    if client_mutation_id:
        ProductMutation.object_mutated(
            user, client_mutation_id=client_mutation_id, product=product
        )

    if is_duplicate:
        return product


class RelativePricesInput(graphene.InputObjectType):
    care_type = graphene.Field(CareTypeEnum)
    periods = graphene.NonNull(graphene.List(
        graphene.NonNull(graphene.Decimal)))


class CreateOrUpdateProductMutation(OpenIMISMutation):
    @classmethod
    def do_mutate(cls, perms, user, **data):
        if type(user) is AnonymousUser or not user.id:
            raise ValidationError(_("mutation.authentication_required"))
        if not user.has_perms(perms):
            raise PermissionDenied(_("unauthorized"))

        data["audit_user_id"] = user.id_for_audit

        return create_or_update_product(user, data)


class ProductServiceOrItemInput(graphene.InputObjectType):
    price_origin = graphene.Field(PriceOriginEnum)
    limitation_type = graphene.Field(LimitTypeEnum)
    limitation_type_r = graphene.Field(LimitTypeEnum)
    limitation_type_e = graphene.Field(LimitTypeEnum)
    waiting_period_adult = graphene.Int()
    waiting_period_child = graphene.Int()
    limit_no_adult = graphene.Int()
    limit_no_child = graphene.Int()
    limit_adult = graphene.Decimal(
        max_digits=18, decimal_places=2, required=False, default_value=0
    )
    limit_child = graphene.Decimal(
        max_digits=18, decimal_places=2, required=False, default_value=0
    )
    limit_adult_r = graphene.Decimal(
        max_digits=18, decimal_places=2, required=False, default_value=0
    )
    limit_child_r = graphene.Decimal(
        max_digits=18, decimal_places=2, required=False, default_value=0
    )
    limit_adult_e = graphene.Decimal(
        max_digits=18, decimal_places=2, required=False, default_value=0
    )
    limit_child_e = graphene.Decimal(
        max_digits=18, decimal_places=2, required=False, default_value=0
    )
    ceiling_exclusion_adult = graphene.Field(CeilingExclusionEnum)
    ceiling_exclusion_child = graphene.Field(CeilingExclusionEnum)


class ProductServiceInput(ProductServiceOrItemInput):
    service_uuid = graphene.UUID(required=True)


class ProductItemInput(ProductServiceOrItemInput):
    item_uuid = graphene.UUID(required=True)


class ProductInputType(OpenIMISMutation.Input):
    name = graphene.String(required=True)
    date_from = graphene.Date(required=True)
    date_to = graphene.Date(required=True)
    insurance_period = graphene.Int(required=True)
    administration_period = graphene.Int()
    max_members = graphene.Int(default_value=0)
    max_installments = graphene.Int()
    recurrence = graphene.Int()
    location_uuid = graphene.UUID()
    conversion_product_uuid = graphene.UUID()
    acc_code_remuneration = graphene.String()
    acc_code_premiums = graphene.String()

    lump_sum = graphene.Decimal(
        max_digits=18, decimal_places=2, required=False, default_value=0
    )
    premium_adult = graphene.Decimal(
        max_digits=18, decimal_places=2, required=False, default_value=0
    )
    premium_child = graphene.Decimal(
        max_digits=18, decimal_places=2, required=False, default_value=0
    )
    threshold = graphene.Int()
    share_contribution = graphene.Decimal(
        max_digits=18, decimal_places=2, required=False
    )

    grace_period_renewal = graphene.Int(default_value=0)
    grace_period_payment = graphene.Int(default_value=0)
    grace_period_enrolment = graphene.Int(default_value=0)

    registration_lump_sum = graphene.Decimal(
        max_digits=18, decimal_places=2, required=False
    )
    registration_fee = graphene.Decimal(
        max_digits=18, decimal_places=2, required=False)
    general_assembly_lump_sum = graphene.Decimal(
        max_digits=18, decimal_places=2, required=False
    )
    general_assembly_fee = graphene.Decimal(
        max_digits=18, decimal_places=2, required=False
    )

    start_cycle_1 = graphene.String()
    start_cycle_2 = graphene.String()
    start_cycle_3 = graphene.String()
    start_cycle_4 = graphene.String()

    renewal_discount_perc = graphene.Int(default_value=0)
    renewal_discount_period = graphene.Int(default_value=0)
    enrolment_discount_perc = graphene.Int(default_value=0)
    enrolment_discount_period = graphene.Int(default_value=0)

    # Deductibles & Ceilings
    ceiling_interpretation = graphene.Field(CeilingInterpretationEnum)
    ceiling_type = graphene.Field(CeilingTypeEnum)

    deductible = graphene.Decimal(max_digits=18, decimal_places=2)
    deductible_ip = graphene.Decimal(
        max_digits=18,
        decimal_places=2,
    )
    deductible_op = graphene.Decimal(
        max_digits=18,
        decimal_places=2,
    )

    ceiling = graphene.Decimal(
        max_digits=18,
        decimal_places=2,
    )
    ceiling_ip = graphene.Decimal(
        max_digits=18,
        decimal_places=2,
    )
    ceiling_op = graphene.Decimal(max_digits=18, decimal_places=2)

    max_ceiling_policy = graphene.Decimal(
        max_digits=18, decimal_places=2, required=False
    )
    max_ceiling_policy_ip = graphene.Decimal(
        max_digits=18, decimal_places=2, required=False
    )
    max_ceiling_policy_op = graphene.Decimal(
        max_digits=18, decimal_places=2, required=False
    )

    max_policy_extra_member = graphene.Decimal(
        max_digits=18, decimal_places=2, required=False
    )
    max_policy_extra_member_op = graphene.Decimal(
        max_digits=18, decimal_places=2, required=False
    )
    max_policy_extra_member_ip = graphene.Decimal(
        max_digits=18, decimal_places=2, required=False
    )

    max_no_consultation = graphene.Int()
    max_no_surgery = graphene.Int()
    max_no_delivery = graphene.Int()
    max_no_hospitalization = graphene.Int()
    max_no_visits = graphene.Int()
    max_no_antenatal = graphene.Int()

    max_amount_consultation = graphene.Decimal(max_digits=18, decimal_places=2)
    max_amount_surgery = graphene.Decimal(max_digits=18, decimal_places=2)
    max_amount_delivery = graphene.Decimal(max_digits=18, decimal_places=2)
    max_amount_hospitalization = graphene.Decimal(
        max_digits=18, decimal_places=2)
    max_amount_antenatal = graphene.Decimal(max_digits=18, decimal_places=2)

    relative_prices = graphene.List(RelativePricesInput)
    items = graphene.List(graphene.NonNull(ProductItemInput))
    services = graphene.List(graphene.NonNull(ProductServiceInput))


class CreateProductMutation(CreateOrUpdateProductMutation):
    _mutation_module = "product"
    _mutation_class = "CreateProductMutation"

    class Input(ProductInputType):
        code = graphene.String(required=True)

    @classmethod
    def async_mutate(cls, user, **data):
        try:
            cls.do_mutate(
                ProductConfig.gql_mutation_products_add_perms,
                user,
                **data,
            )
        except ValueError as exc:
            return [
                {
                    "message": str(exc)
                }
            ]
        except Exception as exc:
            return [
                {
                    "message": _("product.mutation.failed_to_create_product"),
                    "detail": str(exc),
                }
            ]


class DuplicateProductMutation(OpenIMISMutation):
    _mutation_module = "product"
    _mutation_class = "DuplicateProductMutation"

    class Input(ProductInputType):
        code = graphene.String(required=True)
        uuid = graphene.UUID(required=False)

    @classmethod
    def async_mutate(cls, user, **data):
        try:
            cls.do_mutate(
                ProductConfig.gql_mutation_products_add_perms,
                user,
                **data,
            )
        except ValueError as exc:
            return [
                {
                    "message": str(exc)
                }
            ]
        except Exception as exc:
            return [
                {
                    "message": _("product.mutation.failed_to_duplicate_product"),
                    "detail": str(exc),
                }
            ]

    @classmethod
    def do_mutate(cls, perms, user, **data):
        if type(user) is AnonymousUser or not user.id:
            raise ValidationError(_("mutation.authentication_required"))
        if not user.has_perms(perms):
            raise PermissionDenied(_("unauthorized"))
        current_uuid = data.pop("uuid") if "uuid" in data else None

        data["audit_user_id"] = user.id_for_audit

        duplicate_items = True #if 'items' not in data else False
        duplicate_services = True #if 'services' not in data else False

        new_product = create_or_update_product(user, data, is_duplicate=True)

        if duplicate_items:
            new_product_items = ProductItem.objects.filter(product=Product.objects.get(uuid=current_uuid,
                                                           validity_to__isnull=True))
            for item in new_product_items:
                # create a new instance by setting pk = None
                item.pk = None
                item.product = new_product
                item.save()

        if duplicate_services:
            new_product_services = ProductService.objects.filter(product=Product.objects.get(uuid=current_uuid,
                                                                 validity_to__isnull=True))
            for service in new_product_services:
                # create a new instance by setting pk = None
                service.pk = None
                service.product = new_product
                service.save()

        return new_product


class UpdateProductMutation(CreateOrUpdateProductMutation):
    _mutation_module = "product"
    _mutation_class = "UpdateProductMutation"

    class Input(ProductInputType):
        uuid = graphene.UUID(required=True)
        code = graphene.String(required=True)

    @classmethod
    def async_mutate(cls, user, **data):
        try:
            cls.do_mutate(
                ProductConfig.gql_mutation_products_edit_perms,
                user,
                **data,
            )
        except Exception as exc:
            return [
                {
                    "message": _("product.mutation.failed_to_update_product")
                    % {"uuid": data["uuid"]},
                    "detail": str(exc),
                }
            ]


class DeleteProductMutation(OpenIMISMutation):
    _mutation_module = "product"
    _mutation_class = "DeleteProductMutation"

    class Input(OpenIMISMutation.Input):
        uuids = graphene.List(graphene.String)

    @classmethod
    def async_mutate(cls, user, **data):
        if not user.has_perms(ProductConfig.gql_mutation_products_delete_perms):
            raise PermissionDenied(_("unauthorized"))
        errors = []

        for uuid in data["uuids"]:
            product = Product.objects.filter(uuid=uuid).first()
            if product is None:
                errors.append(
                    {
                        "title": uuid,
                        "list": [
                            {
                                "message": _("product.validation.id_does_not_exist")
                                % {"id", uuid}
                            }
                        ],
                    }
                )
                continue
            try:
                product.delete_history()
            except Exception as exc:
                errors.append(
                    {
                        "title": uuid,
                        "list": [
                            {
                                "message": _(
                                    "product.mutation.failed_to_delete_product"
                                )
                                % {"uuid": product.uuid},
                                "detail": str(exc),
                            }
                        ],
                    }
                )

        if len(errors) == 1:
            errors = errors[0]["list"]
        return errors
