from product.models import Product, ProductService, ProductItem
from product.test_factories import (
    ProductFactory,
    ProductServiceFactory,
    ProductItemFactory,
)


def create_test_product(code=None, valid=True, custom_props=None):
    custom_props = {k: v for k, v in (custom_props or {}).items() if hasattr(Product, k)}
    code = custom_props.pop('code', code or 'TST-HPD')
    product = Product.objects.filter(code=code, validity_to__isnull=valid).first()
    if not product and 'uuid' in custom_props:
        product = Product.objects.filter(uuid=custom_props['uuid'],).first()
    if not product and 'id' in custom_props:
        product = Product.objects.filter(id=custom_props['id'],).first()
    if not product:
        return ProductFactory(
            **{
                "code": code,
                "validity_to": None if valid else "2019-01-01",
                **custom_props
            }
        )
    if custom_props:
        Product.objects.filter(id=product.id).update(**custom_props)
        product.refresh_from_db()
    return product


def create_test_product_service(product, service, valid=True, custom_props=None):
    custom_props = {k: v for k, v in (custom_props or {}).items() if hasattr(ProductService, k)}
    existing = ProductService.objects.filter(
        product=product,
        service=service,
        validity_to__isnull=True
    )
    obj = existing.first()
    if obj is not None:
        if custom_props:
            existing.update(**custom_props)
            obj.refresh_from_db()
        return obj
    return ProductServiceFactory(
        **{
            "product": product,
            "service": service,
            "validity_to": None if valid else "2019-01-01",
            **custom_props
        }
    )


def create_test_product_item(product, item, valid=True, custom_props=None):
    custom_props = {k: v for k, v in (custom_props or {}).items() if hasattr(ProductItem, k)}
    existing = ProductItem.objects.filter(
        product=product,
        item=item,
        validity_to__isnull=True
    )
    obj = existing.first()
    if obj is not None:
        if custom_props:
            existing.update(**custom_props)
            obj.refresh_from_db()
        return obj
    return ProductItemFactory(
        **{
            "product": product,
            "item": item,
            "validity_to": None if valid else "2019-01-01",
            **custom_props
        }
    )
