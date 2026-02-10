from product.models import Product, ProductService, ProductItem


def create_test_product(code=None, valid=True, custom_props=None):
    if custom_props is None:
        custom_props = {}
    else:
        custom_props = {k: v for k, v in custom_props.items() if hasattr(Product, k)} 
    if 'code' in custom_props:
        code = custom_props.pop('code')
    elif not code:
        code = 'TST-HPD'        
    product = Product.objects.filter(code=code, validity_to__isnull=valid).first()
    if not product and 'uuid' in custom_props:
        product = Product.objects.filter(uuid=custom_props['uuid'],).first()
    if not product and 'id' in custom_props:
        product = Product.objects.filter(id=custom_props['id'],).first()
    if not product:
        product = Product.objects.create(
            **{
                "code": code,
                "name": "Test product " + code,
                "lump_sum": 123.45,
                "max_members": 5,
                "grace_period_enrolment": 1,
                "insurance_period": 12,
                "date_from": "2019-01-01",
                "date_to": "2049-01-01",
                "validity_from": "2019-01-01",
                "validity_to": None if valid else "2019-01-01",
                "audit_user_id": -1,
                **custom_props
            }
        )
    elif custom_props:
        Product.objects.filter(id=product.id).update(**custom_props)
        product.refresh_from_db()
    return product


def create_test_product_service(product, service, valid=True, custom_props=None):
    if custom_props is None:
        custom_props = {}
    else:
        custom_props = {k: v for k, v in custom_props.items() if hasattr(ProductService, k)} 
    obj = ProductService.objects.filter(
        product=product,
        service=service,
        validity_to__isnull=True
    ).first()
    if obj is not None:
        if custom_props:
            ProductService.objects.filter(
                product=product,
                service=service,
                validity_to__isnull=True
            ).update(**custom_props)
            obj.refresh_from_db()
    else:
        obj = ProductService.objects.create(
            **{
                "product": product,
                "service": service,
                "limitation_type": ProductService.LIMIT_CO_INSURANCE,  # mandatory field
                "limit_adult": 100,  # not mandatory but should be set if limitation_type is
                "limit_child": 100,  # "
                "price_origin": ProductService.ORIGIN_PRICELIST,
                "validity_from": "2019-01-01",
                "validity_to": None if valid else "2019-01-01",
                "waiting_period_adult": 0,
                "waiting_period_child": 0,
                "audit_user_id": -1,
                **custom_props
            }
        )
    return obj


def create_test_product_item(product, item, valid=True, custom_props=None):
    if custom_props is None:
        custom_props = {}
    else:
        custom_props = {k: v for k, v in custom_props.items() if hasattr(ProductItem, k)} 
    obj = ProductItem.objects.filter(
        product=product,
        item=item,
        validity_to__isnull=True
    ).first()
    if obj is not None:
        if custom_props:
            ProductItem.objects.filter(
                product=product,
                item=item,
                validity_to__isnull=True
            ).update(**custom_props)
            obj.refresh_from_db()
    else:
        obj = ProductItem.objects.create(
            **{
                "product": product,
                "item": item,
                "limitation_type": ProductItem.LIMIT_CO_INSURANCE,  # mandatory field
                "limit_adult": 100,  # not mandatory but should be set if limitation_type is
                "limit_child": 100,  # "
                "waiting_period_adult": 0,
                "waiting_period_child": 0,
                "price_origin": ProductItem.ORIGIN_PRICELIST,
                "validity_from": "2019-01-01",
                "validity_to": None if valid else "2019-01-01",
                "audit_user_id": -1,
                **custom_props
            }
        )
    return obj
