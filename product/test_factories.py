import factory

from product.models import Product, ProductService, ProductItem


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    code = "TST-HPD"
    name = factory.LazyAttribute(lambda o: "Test product " + o.code)
    lump_sum = 123.45
    max_members = 5
    grace_period_enrolment = 1
    insurance_period = 12
    date_from = "2019-01-01"
    date_to = "2049-01-01"
    validity_from = "2019-01-01"
    audit_user_id = -1


class ProductServiceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductService

    product = factory.SubFactory(ProductFactory)
    limitation_type = ProductService.LIMIT_CO_INSURANCE  # mandatory field
    # not mandatory but should be set if limitation_type is
    limit_adult = 100
    limit_child = 100
    price_origin = ProductService.ORIGIN_PRICELIST
    waiting_period_adult = 0
    waiting_period_child = 0
    validity_from = "2019-01-01"
    audit_user_id = -1


class ProductItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductItem

    product = factory.SubFactory(ProductFactory)
    limitation_type = ProductItem.LIMIT_CO_INSURANCE  # mandatory field
    # not mandatory but should be set if limitation_type is
    limit_adult = 100
    limit_child = 100
    price_origin = ProductItem.ORIGIN_PRICELIST
    waiting_period_adult = 0
    waiting_period_child = 0
    validity_from = "2019-01-01"
    audit_user_id = -1
