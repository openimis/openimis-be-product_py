from django.apps import AppConfig

MODULE_NAME = "product"


DEFAULT_CFG = {
    "gql_query_products_perms": ["121001"],
    "gql_mutation_products_add_perms": ["121002"],
    "gql_mutation_products_edit_perms": ["121003"],
    "gql_mutation_products_delete_perms": ["121004"],
    "gql_mutation_products_duplicate_perms": ["121005"],
}


class ProductConfig(AppConfig):
    name = MODULE_NAME

    gql_query_products_perms = []

    gql_mutation_products_add_perms = []
    gql_mutation_products_edit_perms = []
    gql_mutation_products_delete_perms = []
    gql_mutation_products_duplicate_perms = []

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

    def ready(self):
        from core.models import ModuleConfiguration

        cfg = ModuleConfiguration.get_or_default(MODULE_NAME, DEFAULT_CFG)
        self._configure_permissions(cfg)

    def set_dataloaders(self, dataloaders):
        from .dataloaders import ProductLoader

        dataloaders["product_loader"] = ProductLoader()
