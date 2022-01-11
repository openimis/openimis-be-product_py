from django.core.exceptions import PermissionDenied
from core import ExtendedConnection, prefix_filterset
from django.db.models import Q
import graphene
from graphene.relay import Node
from django.utils.translation import gettext_lazy
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
import graphene_django_optimizer as gql_optimizer

from .models import Product, ProductItem, ProductService
from .gql_mutations import (
    CreateProductMutation,
    UpdateProductMutation,
    DeleteProductMutation,
)
from .apps import ProductConfig
from django.utils.translation import gettext as _
from core import filter_validity
from .enums import (
    CareTypeEnum,
    CeilingExclusionEnum,
    CeilingInterpretationEnum,
    CeilingTypeEnum,
    LimitTypeEnum,
    PriceOriginEnum,
)


class ProductRelativePricesGQLType(graphene.ObjectType):
    care_type = graphene.Field(CareTypeEnum)
    periods = graphene.NonNull(graphene.List(graphene.NonNull(graphene.Decimal)))


def period_type_to_number(period_type):
    if period_type == "M":
        return 12
    elif period_type == "Y":
        return 1
    elif period_type == "Q":
        return 4
    else:
        return None


class ProductGQLType(DjangoObjectType):
    ceiling_interpretation = graphene.Field(CeilingInterpretationEnum)
    relative_prices = graphene.NonNull(graphene.List(ProductRelativePricesGQLType))

    ceiling_type = graphene.Field(CeilingTypeEnum)

    deductible = graphene.Decimal()
    deductible_ip = graphene.Decimal()
    deductible_op = graphene.Decimal()

    ceiling = graphene.Decimal()
    ceiling_ip = graphene.Decimal()
    ceiling_op = graphene.Decimal()

    # TODO: These resolvers should not exist and be integrated in the Product model directly
    def resolve_deductible(self, info, **kwargs):
        ceiling_type = self.ceiling_type
        if ceiling_type == "I":
            return self.ded_insuree
        elif ceiling_type == "T":
            return self.ded_treatment
        elif ceiling_type == "P":
            return self.ded_policy

    def resolve_deductible_ip(self, info, **kwargs):
        ceiling_type = self.ceiling_type
        if ceiling_type == "I":
            return self.ded_ip_insuree
        elif ceiling_type == "T":
            return self.ded_ip_treatment
        elif ceiling_type == "P":
            return self.ded_ip_policy

    def resolve_deductible_op(self, info, **kwargs):
        ceiling_type = self.ceiling_type
        if ceiling_type == "I":
            return self.ded_op_insuree
        elif ceiling_type == "T":
            return self.ded_op_treatment
        elif ceiling_type == "P":
            return self.ded_op_policy

    def resolve_ceiling_op(self, info, **kwargs):
        ceiling_type = self.ceiling_type
        if ceiling_type == "I":
            return self.max_op_insuree
        elif ceiling_type == "T":
            return self.max_op_treatment
        elif ceiling_type == "P":
            return self.max_op_policy

    def resolve_ceiling_ip(self, info, **kwargs):
        ceiling_type = self.ceiling_type
        if ceiling_type == "I":
            return self.max_ip_insuree
        elif ceiling_type == "T":
            return self.max_ip_treatment
        elif ceiling_type == "P":
            return self.max_ip_policy

    def resolve_ceiling(self, info, **kwargs):
        ceiling_type = self.ceiling_type
        if ceiling_type == "I":
            return self.max_insuree
        elif ceiling_type == "T":
            return self.max_treatment
        elif ceiling_type == "P":
            return self.max_policy

    def resolve_ceiling_type(self, info, **kwargs):
        return self.ceiling_type

    def resolve_relative_prices(self, info, **kwargs):
        relative_prices = []
        for care_type, period_type in [
            ("B", self.period_rel_prices),
            ("I", self.period_rel_prices_ip),
            ("O", self.period_rel_prices_op),
        ]:
            nb_periods = period_type_to_number(period_type)
            if nb_periods is None:
                continue
            periods = self.relative_distributions.filter(
                Q(validity_to=None) & Q(care_type=care_type) & Q(type=nb_periods)
            ).order_by("period")

            relative_prices.append(
                ProductRelativePricesGQLType(
                    care_type=care_type, periods=[x.percent for x in periods]
                )
            )

        return relative_prices

    def resolve_location(self, info):
      if "location_loader" in info.context.dataloaders and self.location_id:
          return info.context.dataloaders["location_loader"].load(self.location_id)
      return self.location

    class Meta:
        model = Product
        interfaces = (Node,)
        filter_fields = {
            "id": ["exact"],
            "uuid": ["exact"],
            "code": ["exact", "icontains", "istartswith"],
            "name": ["exact", "icontains", "istartswith"],
            "date_from": ["exact", "gt", "gte", "lt", "lte"],
            "date_to": ["exact", "gt", "gte", "lt", "lte"],
            "location": ["isnull"],
        }

        exclude_fields = (
            "capitation_level_1",
            "capitation_level_2",
            "capitation_level_3",
            "capitation_level_4",
            "capitation_sublevel_1",
            "capitation_sublevel_2",
            "capitation_sublevel_3",
            "capitation_sublevel_4",
            "weight_population",
            "weight_nb_families",
            "weight_nb_visits",
            "weight_insured_population",
            "weight_nb_insured_families",
            "weight_adjusted_amount",
            "product_set",
            "relativeindex_set",
            "contributionplan_set",
            "period_rel_prices",
            "period_rel_prices_ip",
            "period_rel_prices_op",
            "ded_insuree",
            "ded_ip_insuree",
            "ded_op_insuree",
            "max_insuree",
            "max_ip_insuree",
            "max_op_insuree",
            "ded_treatment",
            "ded_ip_treatment",
            "ded_op_treatment",
            "max_treatment",
            "max_ip_treatment",
            "max_op_treatment",
            "ded_policy",
            "ded_ip_policy",
            "ded_op_policy",
            "max_policy",
            "max_ip_policy",
            "max_op_policy",
        )
        connection_class = ExtendedConnection


class ProductItemGQLType(DjangoObjectType):
    ceiling_exclusion_adult = graphene.Field(CeilingExclusionEnum)
    ceiling_exclusion_child = graphene.Field(CeilingExclusionEnum)
    limitation_type = graphene.Field(LimitTypeEnum)
    limitation_type_r = graphene.Field(LimitTypeEnum)
    limitation_type_e = graphene.Field(LimitTypeEnum)
    price_origin = graphene.Field(PriceOriginEnum)

    @classmethod
    def get_queryset(cls, queryset, info):
        return queryset.filter(validity_to=None)

    class Meta:
        model = ProductItem
        interfaces = (Node,)
        filter_fields = {
            "id": ["exact"],
        }
        connection_class = ExtendedConnection


class ProductServiceGQLType(DjangoObjectType):
    ceiling_exclusion_adult = graphene.Field(CeilingExclusionEnum)
    ceiling_exclusion_child = graphene.Field(CeilingExclusionEnum)
    limitation_type = graphene.Field(LimitTypeEnum)
    limitation_type_r = graphene.Field(LimitTypeEnum)
    limitation_type_e = graphene.Field(LimitTypeEnum)
    price_origin = graphene.Field(PriceOriginEnum)

    @classmethod
    def get_queryset(cls, queryset, info):
        return queryset.filter(validity_to=None)

    class Meta:
        model = ProductService
        interfaces = (Node,)
        filter_fields = {
            "id": ["exact"],
        }
        connection_class = ExtendedConnection


class Query(graphene.ObjectType):
    products = DjangoFilterConnectionField(
        ProductGQLType,
        location=graphene.Int(),
        show_history=graphene.Boolean(),
        search=graphene.String(description=gettext_lazy("Search in `name` & `code`")),
    )
    product = graphene.Field(ProductGQLType, id=graphene.ID(), uuid=graphene.String())

    def resolve_product(self, info, **kwargs):
        if not info.context.user.has_perms(ProductConfig.gql_query_products_perms):
            raise PermissionDenied(_("unauthorized"))
        if kwargs.get("id", None) is not None:
            return Node.get_node_from_global_id(info, kwargs["id"])
        elif kwargs.get("uuid", None) is not None:
            return Product.objects.get(uuid=kwargs["uuid"])

        return None

    def resolve_products(
        self, info, location=None, search=None, show_history=False, **kwargs
    ):
        if not info.context.user.has_perms(ProductConfig.gql_query_products_perms):
            raise PermissionDenied(_("unauthorized"))

        qs = Product.objects
        if not show_history:
            qs = qs.filter(*filter_validity(**kwargs))

        if search is not None:
            qs = qs.filter(Q(name__icontains=search) | Q(code__icontains=search))

        if location is not None:
            from location.models import Location

            qs = qs.filter(
                Q(location__in=Location.objects.parents(location))
                | Q(location__id=location)
            )

        return gql_optimizer.query(qs, info)


class Mutation(graphene.ObjectType):
    create_product = CreateProductMutation.Field()
    update_product = UpdateProductMutation.Field()
    delete_product = DeleteProductMutation.Field()
