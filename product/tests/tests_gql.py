import base64
from unittest import mock
from django.test import TestCase

import graphene
import datetime
from product.models import Product
from core.models import TechnicalUser
from core.models.openimis_graphql_test_case import openIMISGraphQLTestCase
from core.test_helpers import create_test_interactive_user
from policyholder.tests.helpers import *
from contribution_plan.tests.helpers import create_test_contribution_plan, \
    create_test_contribution_plan_bundle, create_test_contribution_plan_bundle_details
from product import schema as product_schema
from graphene import Schema
from graphene.test import Client
from graphene_django.utils.testing import GraphQLTestCase
from django.conf import settings
import json
import uuid
from graphql_jwt.shortcuts import get_token


class MutationTestProduct(openIMISGraphQLTestCase):
    # This is required by some version of graphene but is never used. It should be set to the schema but the import
    # is shown as an error in the IDE, so leaving it as True.
    admin_user = None


    class BaseTestContext:
        def __init__(self, user):
            self.user = user

    class AnonymousUserContext:
        user = mock.Mock(is_anonymous=True)

    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.filter(username='admin', i_user__isnull=False).first()
        super(MutationTestProduct, cls).setUpClass()
        if not cls.user:
            cls.user=create_test_interactive_user(username='admin', password='S\/pe®Pąßw0rd™', roles=[1])
        # some test data so as to created contract properly
        cls.user_token = get_token(cls.user, cls.BaseTestContext(user=cls.user))
        cls.product = Product.objects.filter(code='BCTA0001').first()
    def test_mutation_update_product(self):
        time_stamp = datetime.datetime.now()
        mutation_raw = """
    mutation ($input: UpdateProductMutationInput!) {
      updateProduct(input: $input) {
        internalId
        clientMutationId
      }
    }
  """
        null = None
        variables_param = f"""{{
  "input": {{
    "name": "Basic Cover Tahida Updated",
    "maxMembers": 6,
    "threshold": null,
    "dateFrom": "2017-01-01",
    "dateTo": "2030-12-31",
    "recurrence": null,
    "insurancePeriod": 12,
    "lumpSum": "10000.00",
    "premiumAdult": null,
    "premiumChild": null,
    "registrationLumpSum": null,
    "registrationFee": null,
    "generalAssemblyLumpSum": null,
    "generalAssemblyFee": null,
    "startCycle1": null,
    "startCycle2": null,
    "startCycle3": null,
    "startCycle4": null,
    "renewalDiscountPerc": null,
    "renewalDiscountPeriod": null,
    "enrolmentDiscountPerc": null,
    "enrolmentDiscountPeriod": null,
    "ceilingInterpretation": "CLAIM_TYPE",
    "gracePeriodEnrolment": 0,
    "gracePeriodRenewal": 0,
    "gracePeriodPayment": 0,
    "accCodePremiums": "",
    "accCodeRemuneration": "",
    "maxPolicyExtraMember": null,
    "maxPolicyExtraMemberIp": null,
    "maxPolicyExtraMemberOp": null,
    "maxCeilingPolicy": null,
    "maxCeilingPolicyIp": null,
    "maxCeilingPolicyOp": null,
    "maxNoConsultation": null,
    "maxNoSurgery": null,
    "maxNoDelivery": null,
    "maxNoHospitalization": null,
    "maxNoVisits": null,
    "maxNoAntenatal": null,
    "maxAmountConsultation": null,
    "maxAmountSurgery": null,
    "maxAmountDelivery": null,
    "maxAmountHospitalization": null,
    "maxAmountAntenatal": null,
    "deductible": null,
    "deductibleIp": null,
    "deductibleOp": null,
    "ceiling": null,
    "ceilingIp": null,
    "ceilingOp": null,
    "administrationPeriod": 0,
    "uuid": "{str(self.product.uuid)}",
    "maxInstallments": 1,
    "code": "{self.product.code}",
    "locationUuid": "{str(self.product.location.uuid)}",
    "clientMutationLabel": "Update product Basic Cover Tahida",
    "clientMutationId": "a15498d1-bc77-4516-99d6-23d5d2023d96"
  }}
}}"""
  
        content=self.send_mutation_raw(mutation_raw,  self.user_token, variables_param)     
        
        
  
  
  