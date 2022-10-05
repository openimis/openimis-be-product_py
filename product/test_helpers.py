from product.models import Product, ProductService, ProductItem


def create_test_product(code, valid=True, custom_props=None):
    return Product.objects.create(
        **{
            "code": code,
            "name": "Test product " + code,
            "lump_sum": 123.45,
            "max_members": 1,
            "grace_period_enrolment": 1,
            "insurance_period": 12,
            "date_from": "2019-01-01",
            "date_to": "2049-01-01",
            "validity_from": "2019-01-01",
            "validity_to": None if valid else "2019-01-01",
            "audit_user_id": -1,
            **(custom_props if custom_props else {})
        }
    )


def create_test_product_service(product, service, valid=True, custom_props=None):
    return ProductService.objects.create(
        **{
            "product": product,
            "service": service,
            "limitation_type": ProductService.LIMIT_CO_INSURANCE,  # mandatory field
            "limit_adult": 100,  # not mandatory but should be set if limitation_type is
            "limit_child": 100,  # "
            "price_origin": ProductService.ORIGIN_PRICELIST,
            "validity_from": "2019-01-01",
            "validity_to": None if valid else "2019-01-01",
            "waiting_period_adult": 2,
            "waiting_period_child": 1,
            "audit_user_id": -1,
            **(custom_props if custom_props else {})
        }
    )


def create_test_product_item(product, item, valid=True, custom_props=None):
    return ProductItem.objects.create(
        **{
            "product": product,
            "item": item,
            "limitation_type": ProductItem.LIMIT_CO_INSURANCE,  # mandatory field
            "limit_adult": 100,  # not mandatory but should be set if limitation_type is
            "limit_child": 100,  # "
            "waiting_period_adult": 2,
            "waiting_period_child": 1,
            "price_origin": ProductItem.ORIGIN_PRICELIST,
            "validity_from": "2019-01-01",
            "validity_to": None if valid else "2019-01-01",
            "audit_user_id": -1,
            **(custom_props if custom_props else {})
        }
    )
