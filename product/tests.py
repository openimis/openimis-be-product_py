from django.test import TestCase

from product.test_helpers import create_test_product, create_test_product_service, create_test_product_item
from medical.test_helpers import create_test_service, create_test_item

DATA_MUTATION="""{
    "query":"mutation ($input: UpdateProductMutationInput!) {
                updateProduct(input: $input) {
                        internalId
                        clientMutationId      
                }
            }",
    "variables":{"input":{
            "name":"Fixed Cycle Cover Tahida",
            "maxMembers":9999,
            "threshold":6,
            "dateFrom":"2017-01-01",
            "dateTo":"2030-12-31",
            "recurrence":null,
            "insurancePeriod":12,
            "lumpSum":"0.00",
            "premiumAdult":"4000.00",
            "premiumChild":"4000.00",
            "maxInstallments":3,
            "registrationLumpSum":"1000.00",
            "registrationFee":null,
            "generalAssemblyLumpSum":"1000.00",
            "generalAssemblyFee":null,
            "startCycle1":"01-06",
            "startCycle2":"01-11",
            "startCycle3":null,
            "startCycle4":null,
            "renewalDiscountPerc":null,
            "renewalDiscountPeriod":null,
            "enrolmentDiscountPerc":null,
            "enrolmentDiscountPeriod":null,
            "ceilingInterpretation":"CLAIM_TYPE",
            "gracePeriodEnrolment":0,
            "gracePeriodRenewal":0,
            "gracePeriodPayment":3,
            "accCodePremiums":"",
            "accCodeRemuneration":"",
            "maxPolicyExtraMember":null,
            "maxPolicyExtraMemberIp":null,
            "maxPolicyExtraMemberOp":null,
            "maxCeilingPolicy":null,
            "maxCeilingPolicyIp":null,
            "maxCeilingPolicyOp":null,
            "maxNoConsultation":null,
            "maxNoSurgery":null,
            "maxNoDelivery":null,
            "maxNoHospitalization":null,
            "maxNoVisits":null,
            "maxNoAntenatal":null,
            "maxAmountConsultation":null,
            "maxAmountSurgery":null,
            "maxAmountDelivery":null,
            "maxAmountHospitalization":null,
            "maxAmountAntenatal":null,
            "deductible":null,
            "deductibleIp":null,"deductibleOp":null,
            "ceiling":null,"ceilingIp":null,
            "ceilingOp":null,
            "relativePrices":[],"administrationPeriod":0,
            "uuid":"eaa082a0-d71e-4526-a918-3239b098afa7",
            "code":"FCTA0001",
            "locationUuid":"68753566-9d2e-4cec-936e-4c6bf1968c0d",
            "clientMutationLabel":"Update product Fixed Cycle Cover Tahida",
            "clientMutationId":"a0b8d581-fa59-461a-9e29-a3d42200e13b"}
        }
    }
"""
class HelpersTest(TestCase):
    product=None
    user=None
    def setUp(self) -> None:
        super(HelpersTest, self).setUp()
        i_user, i_user_created = create_or_update_interactive_user(
            user_id=None, data=_TEST_DATA_USER, audit_user_id=999, connected=False)
        self.user, user_created = create_or_update_core_user(
            user_uuid=None, username=_TEST_DATA_USER["username"], i_user=i_user)
        insuree, family = create_test_insuree_for_policy(with_family=True, is_head=False, custom_props={"chf_id": "paysimp"}, family_custom_props=None)
        self.product = create_test_product("ELI1",custom_props={"uuid": "eaa082a0-d71e-4526-a918-3239b098afa7"})
        service = create_test_service("V", custom_props={"code": "VVVV"})
        create_test_product_service(self.product, service, custom_props={"limit_no_adult": 20})
        item = create_test_item("A", custom_props={"name": "test_simple_batch"})
        create_test_product_item(self.product, service, custom_props={"limit_no_adult": 20})

    def test_helper(self):

        self.assertEquals(self.product.code, "ELI1")
        self.assertEquals(len(self.product.items), 1)
        self.assertEquals(len(self.product.services), 1)

    def test_save_history(self):
        create_or_update_product(self.user,DATA_MUTATION['variables']['input'])
        self.assertEquals(self.product.code, "FCTA0001")
