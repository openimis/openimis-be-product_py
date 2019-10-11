from django.apps import AppConfig

MODULE_NAME = "product"

DEFAULT_CFG = {
    "gql_query_products_perms": []
}


class ProductConfig(AppConfig):
    name = MODULE_NAME

    gql_query_products_perms = []

    def _configure_permissions(self, cfg):
        ProductConfig.gql_query_products_perms = cfg[
            "gql_query_products_perms"]

    def ready(self):
        from core.models import ModuleConfiguration
        cfg = ModuleConfiguration.get_or_default(MODULE_NAME, DEFAULT_CFG)
        self._configure_permissions(cfg)
