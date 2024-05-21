from django.test import TestCase
from core.services import  create_or_update_interactive_user,create_or_update_core_user
from product.test_helpers import create_test_product, create_test_product_service, create_test_product_item
from medical.test_helpers import create_test_service, create_test_item
from product.gql_mutations import create_or_update_product
from product.models import Product
import re
_TEST_USER_NAME = "test_insuree_import"
_TEST_USER_PWD = "Test_insuree_import_1"
_TEST_DATA_USER = {
    "username": _TEST_USER_NAME,
    "last_name": _TEST_USER_NAME,
    "password": _TEST_USER_PWD,
    "other_names": _TEST_USER_NAME,
    "user_types": "INTERACTIVE",
    "language": "en",
    "roles": [1, 5, 9],
}

null = None

DATA_MUTATION={
    "query":"mutation ($input: UpdateProductMutationInput!) {updateProduct(input: $input) { internalId clientMutationId }}",
    "variables":{"input":{
            "name":"Fixed Cycle Cover Tahida",
            "maxMembers":9999,
            "threshold":6,
            "dateFrom":"2017-01-01",
            "dateTo":"2030-12-31",
            "recurrence":None,
            "insurancePeriod":12,
            "lumpSum":"0.00",
            "premiumAdult":"4000.00",
            "premiumChild":"4000.00",
            "maxInstallments":3,
            "registrationLumpSum":"1000.00",
            "registrationFee":None,
            "generalAssemblyLumpSum":"1000.00",
            "generalAssemblyFee":None,
            "startCycle1":"01-06",
            "startCycle2":"01-11",
            "startCycle3":None,
            "startCycle4":None,
            "renewalDiscountPerc":None,
            "renewalDiscountPeriod":None,
            "enrolmentDiscountPerc":None,
            "enrolmentDiscountPeriod":None,
            "ceilingInterpretation":"I",
            "gracePeriodEnrolment":0,
            "gracePeriodRenewal":0,
            "gracePeriodPayment":3,
            "accCodePremiums":"",
            "services":[],
            "accCodeRemuneration":"",
            "maxPolicyExtraMember":None,
            "maxPolicyExtraMemberIp":None,
            "maxPolicyExtraMemberOp":None,
            "maxCeilingPolicy":None,
            "maxCeilingPolicyIp":None,
            "maxCeilingPolicyOp":None,
            "maxNoConsultation":None,
            "maxNoSurgery":None,
            "maxNoDelivery":None,
            "maxNoHospitalization":None,
            "maxNoVisits":None,
            "maxNoAntenatal":None,
            "maxAmountConsultation":None,
            "maxAmountSurgery":None,
            "maxAmountDelivery":None,
            "maxAmountHospitalization":None,
            "maxAmountAntenatal":None,
            "deductible":None,
            "deductibleIp":None,
            "deductibleOp":None,
            "ceiling":None,
            "ceilingIp":None,
            "ceilingOp":None,
            "relativePrices":[],
            "administrationPeriod":0,
            "uuid":"eaa082a0-d71e-4526-a918-3239b098afa7",
            "code":"FCTA0041",
            "locationUuid":None,
            "clientMutationLabel":"Update product Fixed Cycle Cover Tahida",
            "clientMutationId":"a0b8d581-fa59-461a-9e29-a3d42200e13b"
            }
        }
    }

DATA_MUTATION_UPDATE={
    "query":"mutation ($input: UpdateProductMutationInput!) {updateProduct(input: $input) { internalId clientMutationId }}",
    "variables":{"input":{
            "name":"Fixed Cycle Cover Tahida",
            "maxMembers":9999,
            "threshold":6,
            "dateFrom":"2017-01-01",
            "dateTo":"2030-12-31",
            "recurrence":None,
            "insurancePeriod":12,
            "lumpSum":"0.00",
            "premiumAdult":"4000.00",
            "premiumChild":"4000.00",
            "maxInstallments":3,
            "registrationLumpSum":"1000.00",
            "registrationFee":None,
            "generalAssemblyLumpSum":"1000.00",
            "generalAssemblyFee":None,
            "startCycle1":"01-06",
            "startCycle2":"01-11",
            "startCycle3":None,
            "startCycle4":None,
            "renewalDiscountPerc":None,
            "renewalDiscountPeriod":None,
            "enrolmentDiscountPerc":None,
            "enrolmentDiscountPeriod":None,
            "ceilingInterpretation":"I",
            "gracePeriodEnrolment":0,
            "gracePeriodRenewal":0,
            "gracePeriodPayment":3,
            "accCodePremiums":"",
            "items": [
                {
                    "ceilingExclusionAdult": None,
                    "ceilingExclusionChild": None,
                    "itemUuid": "71efb78b-64ee-4a68-be29-87daf566eb25",
                    "limitAdult": "100.00",
                    "limitAdultE": "100.00",
                    "limitAdultR": "100.00",
                    "limitationType": "C",
                    "limitationTypeE": "C",
                    "limitationTypeR": "C",
                    "limitChild": "100.00",
                    "limitChildE": "100.00",
                    "limitChildR": "100.00",
                    "limitNoAdult": None,
                    "limitNoChild": None,
                    "priceOrigin": "P",
                    "waitingPeriodAdult": None,
                    "waitingPeriodChild": None
                }
            ],
            "services":[
                {
                    "ceilingExclusionAdult": None,
                    "ceilingExclusionChild": None,
                    "limitAdult": "100.00",
                    "limitAdultE": "100.00",
                    "limitAdultR": "100.00",
                    "limitationType": "C",
                    "limitationTypeE": "C",
                    "limitationTypeR": "C",
                    "limitChild": "100.00",
                    "limitChildE": "100.00",
                    "limitChildR": "100.00",
                    "limitNoAdult": None,
                    "limitNoChild": None,
                    "priceOrigin": "P",
                    "serviceUuid": "488d8bcb-5b88-438c-9077-f177f6f32625",
                    "waitingPeriodAdult": None,
                    "waitingPeriodChild": None
                }
            ],
            "accCodeRemuneration":"",
            "maxPolicyExtraMember":None,
            "maxPolicyExtraMemberIp":None,
            "maxPolicyExtraMemberOp":None,
            "maxCeilingPolicy":None,
            "maxCeilingPolicyIp":None,
            "maxCeilingPolicyOp":None,
            "maxNoConsultation":None,
            "maxNoSurgery":None,
            "maxNoDelivery":None,
            "maxNoHospitalization":None,
            "maxNoVisits":None,
            "maxNoAntenatal":None,
            "maxAmountConsultation":None,
            "maxAmountSurgery":None,
            "maxAmountDelivery":None,
            "maxAmountHospitalization":None,
            "maxAmountAntenatal":None,
            "deductible":None,
            "deductibleIp":None,
            "deductibleOp":None,
            "ceiling":None,
            "ceilingIp":None,
            "ceilingOp":None,
            "relativePrices":[],
            "administrationPeriod":0,
            "uuid":"eaa082a0-d71e-4526-a918-3239b098afa7",
            "code":"FCTA0041",
            "locationUuid":None,
            "clientMutationLabel":"Update product Fixed Cycle Cover Tahida",
            "clientMutationId":"a0b8d581-fa59-461a-9e29-a3d42200e13b"
            }
        }
    }


class HelpersTest(TestCase):
    product=None
    user=None
    def setUp(self) -> None:
        super(HelpersTest, self).setUp()
        i_user, i_user_created = create_or_update_interactive_user(
            user_id=None, data=_TEST_DATA_USER, audit_user_id=999, connected=False)
        self.user, user_created = create_or_update_core_user(
            user_uuid=None, username=_TEST_DATA_USER["username"], i_user=i_user)
        self.product = create_test_product("ELI1",custom_props={"uuid": "eaa082a0-d71e-4526-a918-3239b098afa7"})
        service = create_test_service("V", custom_props={"code": "VVVV", 'uuid':"488d8bcb-5b88-438c-9077-f177f6f32625"})
        create_test_product_service(self.product, service, custom_props={"limit_no_adult": 20})
        item = create_test_item("A", custom_props={"name": "test_simple_batch", 'uuid':"71efb78b-64ee-4a68-be29-87daf566eb25"})
        create_test_product_item(self.product, item, custom_props={"limit_no_adult": 20})

    def test_helper(self):

        self.assertEquals(self.product.code, "ELI1")
        self.assertEquals(len(self.product.items.all()), 1)
        self.assertEquals(len(self.product.services.all()), 1)

    def test_save_history(self):
        pattern = re.compile(r'(?<=[a-z0-9])(?=[A-Z])')
        data={pattern.sub('_', key).lower(): DATA_MUTATION['variables']['input'][key] for key in DATA_MUTATION['variables']['input']}
        create_or_update_product(self.user,data)
        self.product=Product.objects.filter(uuid = 'eaa082a0-d71e-4526-a918-3239b098afa7').first()
        self.assertEquals(self.product.code, "FCTA0041")
        self.assertEquals(len(self.product.items.all()), 1)
        self.assertEquals(len(self.product.services.all()), 0)
        
    def test_save(self):
 
        data = self.to_camel_case_key(DATA_MUTATION_UPDATE['variables']['input'])
        create_or_update_product(self.user,data)
        self.product=Product.objects.filter(uuid = 'eaa082a0-d71e-4526-a918-3239b098afa7').first()
        self.assertEquals(self.product.code, "FCTA0041")
        self.assertEquals(len(self.product.items.all()), 1)
        self.assertEquals(len(self.product.services.all()), 1)
        
    def to_camel_case_key(self, input):
        pattern = re.compile(r'(?<!^)(?=[A-Z]|[0-9]+)')
        if isinstance(input, list):
            res = []
            for elm in input:
                res.append(self.to_camel_case_key(elm))
            return res
        elif isinstance(input, dict):
            res = {}
            for key in input:
                res[pattern.sub('_', key).lower()]=self.to_camel_case_key(input[key])
            return res    
        else:
            return input