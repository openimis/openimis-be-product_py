import re

from core import ExtendedConnection
from django.db.models import Q
import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from .models import Product


class ProductGQLType(DjangoObjectType):
    class Meta:
        model = Product
        interfaces = (graphene.relay.Node,)
        filter_fields = {
            'id': ['exact'],
            'code': ['exact', 'icontains', 'istartswith'],
            'name': ['exact', 'icontains', 'istartswith'],
        }
        connection_class = ExtendedConnection


class Query(graphene.ObjectType):
    products = DjangoFilterConnectionField(ProductGQLType)
    products_str = DjangoFilterConnectionField(
        ProductGQLType,
        str=graphene.String()
    )

    def resolve_products_str(self, info, **kwargs):
        str = kwargs.get('str')
        if str is not None:
            return Product.objects.filter(
                Q(code__icontains=str) | Q(name__icontains=str)
            )
        else:
            return Product.objects.all()
