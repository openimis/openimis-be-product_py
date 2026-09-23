from core.rights_role_test_case import RightsRoleGraphQLTestCase
from core.test_helpers import (
    create_medical_advisor_role,
    create_raf_role,
    create_right_only_user,
    create_role_user,
)
from location.test_helpers import create_basic_test_locations
from product.test_helpers import create_test_product


PRODUCTS_QUERY = """
query {
  products(first: 5) {
    edges { node { id code name } }
  }
}
"""


class ProductRightsTests(RightsRoleGraphQLTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        create_basic_test_locations()
        create_test_product("PRD1")

    def test_query_products_right(self):
        allowed = create_right_only_user(
            "r_prd_q", ["gql_query_products_perms"], district_codes=self.DISTRICT_CODES
        )
        denied = create_right_only_user("r_prd_q_no", [], district_codes=self.DISTRICT_CODES)
        self.assert_gql_ok(allowed, PRODUCTS_QUERY)
        self.assert_gql_unauthorized(denied, PRODUCTS_QUERY)


class ProductRoleTests(RightsRoleGraphQLTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        create_basic_test_locations()
        create_test_product("PRD2")
        cls.users = {
            "medical_advisor": create_role_user(
                "prd_ma", create_medical_advisor_role(), district_codes=cls.DISTRICT_CODES
            ),
            "raf": create_role_user(
                "prd_raf", create_raf_role(), district_codes=cls.DISTRICT_CODES
            ),
        }

    def test_roles_can_query_products(self):
        for name, user in self.users.items():
            with self.subTest(role=name):
                self.assert_user_has_named_perms(user, ["gql_query_products_perms"])
                self.assert_gql_ok(user, PRODUCTS_QUERY)
