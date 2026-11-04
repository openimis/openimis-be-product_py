from django.apps import AppConfig

from core.rights_declaration import RightsDeclaration
from decimal import Decimal

MODULE_NAME = "product"



# Rights, by entity then by action. `duplicate` has its own identifier: duplicating a
# product is an action distinct from creating one in the openIMIS catalogue.
DJANGO_PERMS = {
    "product": {
        "query": ("product.view_product", 121001),
        "create": ("product.add_product", 121002),
        "update": ("product.change_product", 121003),
        "delete": ("product.delete_product", 121004),
        "duplicate": ("product.duplicate_product", 121005),
    },
}

_PERM_CFG = {
    "gql_query_products_perms": ("product", "query"),
    "gql_mutation_products_add_perms": ("product", "create"),
    "gql_mutation_products_edit_perms": ("product", "update"),
    "gql_mutation_products_delete_perms": ("product", "delete"),
    "gql_mutation_products_duplicate_perms": ("product", "duplicate"),
}

RIGHTS = RightsDeclaration(MODULE_NAME, DJANGO_PERMS, _PERM_CFG)

perms = RIGHTS.perms
django_perms = RIGHTS.django_perm_names
configured_perms = RIGHTS.configured
require = RIGHTS.require


DEFAULT_CFG = {
    "min_limit_value": Decimal(0.00),
    "max_limit_value": Decimal(100.00),
    "default_price_origin": 'P',
    "default_limit": 'C',
    "default_limit_co_insurance_value": 100,
    "default_limit_fixed_value": 0,
}


class ProductConfig(AppConfig):
    name = MODULE_NAME

    # Rights: constants, no longer overridable. They go neither through DEFAULT_CFG
    # nor through ready(): `ModuleConfiguration.get_or_default` now ignores any
    # `_perms` key stored in the database.
    gql_query_products_perms = RIGHTS.perms("product", "query")

    gql_mutation_products_add_perms = RIGHTS.perms("product", "create")
    gql_mutation_products_edit_perms = RIGHTS.perms("product", "update")
    gql_mutation_products_delete_perms = RIGHTS.perms("product", "delete")
    gql_mutation_products_duplicate_perms = RIGHTS.perms("product", "duplicate")

    min_limit_value = None
    max_limit_value = None

    default_price_origin = None
    default_limit = None
    default_limit_co_insurance_value = None
    default_limit_fixed_value = None

    def __load_config(self, cfg):
        for field in cfg:
            if hasattr(ProductConfig, field):
                setattr(ProductConfig, field, cfg[field])

    def ready(self):
        from core.models import ModuleConfiguration

        cfg = ModuleConfiguration.get_or_default(MODULE_NAME, DEFAULT_CFG)
        self.__load_config(cfg)


    def set_dataloaders(self, dataloaders):
        from .dataloaders import ProductLoader

        dataloaders["product_loader"] = ProductLoader()
