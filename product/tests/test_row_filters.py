"""get_queryset honours the OP-2029 validity contract (epic OP-3317, phase 1).

Explicit validity values return the expected rows; a caller asking for
nothing gets what it got before the contract existed.
"""

from datetime import datetime, timedelta

from django.test import TestCase

from core.models.row_filters import Validity
from core.test_helpers import assert_row_filters, create_test_interactive_user, mark_deleted
from product.models import Product
from product.test_helpers import create_test_product


class ProductRowFiltersTest(TestCase):
    def test_product(self):
        user = create_test_interactive_user(username="productrowfilters")
        live = create_test_product("RWF1")
        deleted = mark_deleted(create_test_product("RWF2"))
        assert_row_filters(
            self, Product, Product.objects.filter(id__in=[live.id, deleted.id]), user,
            live.id, deleted.id, default_hides_deleted=False,
        )

    def test_a_validity_date_picks_the_version_valid_then(self):
        user = create_test_interactive_user(username="productrowfilters")
        product = create_test_product("RWF3")
        copy_id = product.save_history()
        rows = Product.objects.filter(code="RWF3")
        # Before the product's validity_from: nothing; now: the live version and,
        # until its validity_to, the superseded one.
        self.assertFalse(
            Product.get_queryset(rows, user, validity=Validity.at(product.validity_from - timedelta(days=1))).exists()
        )
        self.assertIn(
            product.id,
            Product.get_queryset(rows, user, validity=Validity.at(datetime.now() + timedelta(seconds=1)))
            .values_list("id", flat=True),
        )
        self.assertNotEqual(product.id, copy_id)
