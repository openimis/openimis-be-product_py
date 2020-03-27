import re
from django.core.exceptions import PermissionDenied
from core import ExtendedConnection
from core import filter_validity
from django.db.models import Q
import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from .models import Product, ProductItem
from .apps import ProductConfig
from django.utils.translation import gettext as _


class ProductGQLType(DjangoObjectType):
    class Meta:
        model = Product
        interfaces = (graphene.relay.Node,)
        filter_fields = {
            'uuid': ['exact'],
            'code': ['exact', 'icontains', 'istartswith'],
            'name': ['exact', 'icontains', 'istartswith'],
        }
        connection_class = ExtendedConnection
    @classmethod
    def get_queryset(cls, queryset, info):
        queryset = queryset.filter(*filter_validity())
        return queryset


class ProductItemGQLType(DjangoObjectType):
    class Meta:
        model = ProductItem
        interfaces = (graphene.relay.Node,)
        filter_fields = {
            'id': ['exact'],
        }
        connection_class = ExtendedConnection


class ProductServiceGQLType(DjangoObjectType):
    class Meta:
        model = ProductItem
        interfaces = (graphene.relay.Node,)
        filter_fields = {
            'id': ['exact'],
        }
        connection_class = ExtendedConnection


class Query(graphene.ObjectType):
    products = DjangoFilterConnectionField(ProductGQLType)
    products_str = DjangoFilterConnectionField(
        ProductGQLType,
        str=graphene.String()
    )

    def resolve_products(self, info, **kwargs):
        if not info.context.user.has_perms(ProductConfig.gql_query_products_perms):
            raise PermissionDenied(_("unauthorized"))
        pass

    def resolve_products_str(self, info, **kwargs):
        if not info.context.user.has_perms(ProductConfig.gql_query_products_perms):
            raise PermissionDenied(_("unauthorized"))
        str = kwargs.get('str')
        if str is not None:
            return Product.objects.filter(
                Q(code__icontains=str) | Q(name__icontains=str)
            )
        else:
            return Product.objects.all()
