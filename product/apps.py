from django.apps import AppConfig
from decimal import Decimal

MODULE_NAME = "product"


DEFAULT_CFG = {
    "gql_query_products_perms": ["121001"],
    "gql_mutation_products_add_perms": ["121002"],
    "gql_mutation_products_edit_perms": ["121003"],
    "gql_mutation_products_delete_perms": ["121004"],
    "gql_mutation_products_duplicate_perms": ["121005"],
    "min_limit_value": Decimal(0.00),
    "max_limit_value": Decimal(100.00),
    "default_price_origin": 'P',
    "default_limit": 'C',
    "default_limit_co_insurance_value": 100,
    "default_limit_fixed_value": 0,
}


class ProductConfig(AppConfig):
    name = MODULE_NAME

    gql_query_products_perms = []

    gql_mutation_products_add_perms = []
    gql_mutation_products_edit_perms = []
    gql_mutation_products_delete_perms = []
    gql_mutation_products_duplicate_perms = []

    min_limit_value = None
    max_limit_value = None

    default_price_origin = None
    default_limit = None
    default_limit_co_insurance_value = None
    default_limit_fixed_value = None

    def _configure_permissions(self, cfg):
        ProductConfig.gql_query_products_perms = cfg["gql_query_products_perms"]
        ProductConfig.gql_mutation_products_add_perms = cfg[
            "gql_mutation_products_add_perms"
        ]
        ProductConfig.gql_mutation_products_edit_perms = cfg[
            "gql_mutation_products_edit_perms"
        ]
        ProductConfig.gql_mutation_products_delete_perms = cfg[
            "gql_mutation_products_delete_perms"
        ]
        ProductConfig.gql_mutation_products_duplicate_perms = cfg[
            "gql_mutation_products_duplicate_perms"
        ]

    def _configure_limit_values(self, cfg):
        ProductConfig.min_limit_value = cfg['min_limit_value']
        ProductConfig.max_limit_value = cfg['max_limit_value']

    def _configure_default_values(self, cfg):
        ProductConfig.default_price_origin = cfg["default_price_origin"]
        ProductConfig.default_limit = cfg["default_limit"]
        ProductConfig.default_limit_co_insurance_value = cfg["default_limit_co_insurance_value"]
        ProductConfig.default_limit_fixed_value = cfg["default_limit_fixed_value"]

    def ready(self):
        from core.models import ModuleConfiguration

        cfg = ModuleConfiguration.get_or_default(MODULE_NAME, DEFAULT_CFG)
        self._configure_permissions(cfg)
        self._configure_limit_values(cfg)
        self._configure_default_values(cfg)

    def set_dataloaders(self, dataloaders):
        from .dataloaders import ProductLoader

        dataloaders["product_loader"] = ProductLoader()
