from core.dataloaders import DataLoader

from .models import Product


class ProductLoader(DataLoader):
    def batch_load_fn(self, keys):
        products = {
            product.id: product for product in Product.objects.filter(id__in=keys)
        }
        return [products.get(product_id) for product_id in keys]
