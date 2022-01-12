import uuid
from django.db.models.deletion import CASCADE
from django.utils.translation import gettext_lazy
from django.db import models
from core.models import VersionedModel, ObjectMutation, UUIDModel, MutationLog


class Product(VersionedModel):
    id = models.AutoField(db_column="ProdID", primary_key=True)
    uuid = models.CharField(
        db_column="ProdUUID", max_length=36, default=uuid.uuid4, unique=True
    )
    code = models.CharField(db_column="ProductCode", max_length=8)
    name = models.CharField(db_column="ProductName", max_length=100)
    location = models.ForeignKey(
        "location.Location",
        models.DO_NOTHING,
        db_column="LocationId",
        blank=True,
        null=True,
    )
    date_from = models.DateTimeField(db_column="DateFrom")
    date_to = models.DateTimeField(db_column="DateTo")
    conversion_product = models.ForeignKey(
        "self", models.DO_NOTHING, db_column="ConversionProdID", blank=True, null=True
    )

    insurance_period = models.SmallIntegerField(db_column="InsurancePeriod")
    administration_period = models.IntegerField(
        db_column="AdministrationPeriod", blank=True, null=True
    )

    lump_sum = models.DecimalField(db_column="LumpSum", max_digits=18, decimal_places=2)
    max_members = models.SmallIntegerField(db_column="MemberCount")
    max_installments = models.IntegerField(
        db_column="MaxInstallments", blank=True, null=True
    )
    threshold = models.IntegerField(db_column="Threshold", blank=True, null=True)
    recurrence = models.IntegerField(db_column="Recurrence", blank=True, null=True)
    premium_adult = models.DecimalField(
        db_column="PremiumAdult", max_digits=18, decimal_places=2, blank=True, null=True
    )
    premium_child = models.DecimalField(
        db_column="PremiumChild", max_digits=18, decimal_places=2, blank=True, null=True
    )
    ded_insuree = models.DecimalField(
        db_column="DedInsuree", max_digits=18, decimal_places=2, blank=True, null=True
    )
    ded_op_insuree = models.DecimalField(
        db_column="DedOPInsuree", max_digits=18, decimal_places=2, blank=True, null=True
    )
    ded_ip_insuree = models.DecimalField(
        db_column="DedIPInsuree", max_digits=18, decimal_places=2, blank=True, null=True
    )
    max_insuree = models.DecimalField(
        db_column="MaxInsuree", max_digits=18, decimal_places=2, blank=True, null=True
    )
    max_op_insuree = models.DecimalField(
        db_column="MaxOPInsuree", max_digits=18, decimal_places=2, blank=True, null=True
    )
    max_ip_insuree = models.DecimalField(
        db_column="MaxIPInsuree", max_digits=18, decimal_places=2, blank=True, null=True
    )
    period_rel_prices = models.CharField(
        db_column="PeriodRelPrices", max_length=1, blank=True, null=True
    )
    period_rel_prices_op = models.CharField(
        db_column="PeriodRelPricesOP", max_length=1, blank=True, null=True
    )
    period_rel_prices_ip = models.CharField(
        db_column="PeriodRelPricesIP", max_length=1, blank=True, null=True
    )
    acc_code_premiums = models.CharField(
        db_column="AccCodePremiums", max_length=25, blank=True, null=True
    )
    acc_code_remuneration = models.CharField(
        db_column="AccCodeRemuneration", max_length=25, blank=True, null=True
    )
    ded_treatment = models.DecimalField(
        db_column="DedTreatment", max_digits=18, decimal_places=2, blank=True, null=True
    )
    ded_op_treatment = models.DecimalField(
        db_column="DedOPTreatment",
        max_digits=18,
        decimal_places=2,
        blank=True,
        null=True,
    )
    ded_ip_treatment = models.DecimalField(
        db_column="DedIPTreatment",
        max_digits=18,
        decimal_places=2,
        blank=True,
        null=True,
    )
    max_treatment = models.DecimalField(
        db_column="MaxTreatment", max_digits=18, decimal_places=2, blank=True, null=True
    )
    max_op_treatment = models.DecimalField(
        db_column="MaxOPTreatment",
        max_digits=18,
        decimal_places=2,
        blank=True,
        null=True,
    )
    max_ip_treatment = models.DecimalField(
        db_column="MaxIPTreatment",
        max_digits=18,
        decimal_places=2,
        blank=True,
        null=True,
    )
    ded_policy = models.DecimalField(
        db_column="DedPolicy", max_digits=18, decimal_places=2, blank=True, null=True
    )
    ded_op_policy = models.DecimalField(
        db_column="DedOPPolicy", max_digits=18, decimal_places=2, blank=True, null=True
    )
    ded_ip_policy = models.DecimalField(
        db_column="DedIPPolicy", max_digits=18, decimal_places=2, blank=True, null=True
    )
    max_policy = models.DecimalField(
        db_column="MaxPolicy", max_digits=18, decimal_places=2, blank=True, null=True
    )
    max_op_policy = models.DecimalField(
        db_column="MaxOPPolicy", max_digits=18, decimal_places=2, blank=True, null=True
    )
    max_ip_policy = models.DecimalField(
        db_column="MaxIPPolicy", max_digits=18, decimal_places=2, blank=True, null=True
    )
    audit_user_id = models.IntegerField(db_column="AuditUserID")

    grace_period_enrolment = models.IntegerField(db_column="GracePeriod")
    grace_period_payment = models.IntegerField(
        db_column="WaitingPeriod", blank=True, null=True
    )
    grace_period_renewal = models.IntegerField(
        db_column="GracePeriodRenewal", blank=True, null=True
    )

    registration_lump_sum = models.DecimalField(
        db_column="RegistrationLumpSum",
        max_digits=18,
        decimal_places=2,
        blank=True,
        null=True,
    )
    registration_fee = models.DecimalField(
        db_column="RegistrationFee",
        max_digits=18,
        decimal_places=2,
        blank=True,
        null=True,
    )
    general_assembly_lump_sum = models.DecimalField(
        db_column="GeneralAssemblyLumpSum",
        max_digits=18,
        decimal_places=2,
        blank=True,
        null=True,
    )
    general_assembly_fee = models.DecimalField(
        db_column="GeneralAssemblyFee",
        max_digits=18,
        decimal_places=2,
        blank=True,
        null=True,
    )

    start_cycle_1 = models.CharField(
        db_column="StartCycle1", max_length=5, blank=True, null=True
    )
    start_cycle_2 = models.CharField(
        db_column="StartCycle2", max_length=5, blank=True, null=True
    )
    start_cycle_3 = models.CharField(
        db_column="StartCycle3", max_length=5, blank=True, null=True
    )
    start_cycle_4 = models.CharField(
        db_column="StartCycle4", max_length=5, blank=True, null=True
    )
    max_no_consultation = models.IntegerField(
        db_column="MaxNoConsultation", blank=True, null=True
    )
    max_no_surgery = models.IntegerField(
        db_column="MaxNoSurgery", blank=True, null=True
    )
    max_no_delivery = models.IntegerField(
        db_column="MaxNoDelivery", blank=True, null=True
    )
    max_no_hospitalization = models.IntegerField(
        db_column="MaxNoHospitalizaion", blank=True, null=True
    )
    max_no_visits = models.IntegerField(db_column="MaxNoVisits", blank=True, null=True)
    max_amount_consultation = models.DecimalField(
        db_column="MaxAmountConsultation",
        max_digits=18,
        decimal_places=2,
        blank=True,
        null=True,
    )
    max_amount_surgery = models.DecimalField(
        db_column="MaxAmountSurgery",
        max_digits=18,
        decimal_places=2,
        blank=True,
        null=True,
    )
    max_amount_delivery = models.DecimalField(
        db_column="MaxAmountDelivery",
        max_digits=18,
        decimal_places=2,
        blank=True,
        null=True,
    )
    max_amount_hospitalization = models.DecimalField(
        db_column="MaxAmountHospitalization",
        max_digits=18,
        decimal_places=2,
        blank=True,
        null=True,
    )

    renewal_discount_perc = models.IntegerField(
        db_column="RenewalDiscountPerc", blank=True, null=True
    )
    renewal_discount_period = models.IntegerField(
        db_column="RenewalDiscountPeriod", blank=True, null=True
    )
    enrolment_discount_perc = models.IntegerField(
        db_column="EnrolmentDiscountPerc", blank=True, null=True
    )
    enrolment_discount_period = models.IntegerField(
        db_column="EnrolmentDiscountPeriod", blank=True, null=True
    )

    share_contribution = models.DecimalField(
        db_column="ShareContribution",
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
    )
    max_policy_extra_member = models.DecimalField(
        db_column="MaxPolicyExtraMember",
        max_digits=18,
        decimal_places=2,
        blank=True,
        null=True,
    )
    max_policy_extra_member_ip = models.DecimalField(
        db_column="MaxPolicyExtraMemberIP",
        max_digits=18,
        decimal_places=2,
        blank=True,
        null=True,
    )
    max_policy_extra_member_op = models.DecimalField(
        db_column="MaxPolicyExtraMemberOP",
        max_digits=18,
        decimal_places=2,
        blank=True,
        null=True,
    )
    max_ceiling_policy = models.DecimalField(
        db_column="MaxCeilingPolicy",
        max_digits=18,
        decimal_places=2,
        blank=True,
        null=True,
    )
    max_ceiling_policy_ip = models.DecimalField(
        db_column="MaxCeilingPolicyIP",
        max_digits=18,
        decimal_places=2,
        blank=True,
        null=True,
    )
    max_ceiling_policy_op = models.DecimalField(
        db_column="MaxCeilingPolicyOP",
        max_digits=18,
        decimal_places=2,
        blank=True,
        null=True,
    )
    max_amount_antenatal = models.DecimalField(
        db_column="MaxAmountAntenatal",
        max_digits=18,
        decimal_places=2,
        blank=True,
        null=True,
    )
    max_no_antenatal = models.IntegerField(
        db_column="MaxNoAntenatal", blank=True, null=True
    )
    ceiling_interpretation = models.CharField(
        max_length=1,
        db_column="CeilingInterpretation",
        blank=True,
        null=True,
        choices=(
            ("I", gettext_lazy("Claim Type")),
            ("H", gettext_lazy("Health Facility Type")),
        ),
    )
    capitation_level_1 = models.CharField(
        db_column="Level1", max_length=1, blank=True, null=True
    )
    capitation_sublevel_1 = models.ForeignKey(
        "location.HealthFacilitySubLevel",
        models.DO_NOTHING,
        db_column="Sublevel1",
        blank=True,
        null=True,
        related_name="+",
    )
    capitation_level_2 = models.CharField(
        db_column="Level2", max_length=1, blank=True, null=True
    )
    capitation_sublevel_2 = models.ForeignKey(
        "location.HealthFacilitySubLevel",
        models.DO_NOTHING,
        db_column="Sublevel2",
        blank=True,
        null=True,
        related_name="+",
    )
    capitation_level_3 = models.CharField(
        db_column="Level3", max_length=1, blank=True, null=True
    )
    capitation_sublevel_3 = models.ForeignKey(
        "location.HealthFacilitySubLevel",
        models.DO_NOTHING,
        db_column="Sublevel3",
        blank=True,
        null=True,
        related_name="+",
    )
    capitation_level_4 = models.CharField(
        db_column="Level4", max_length=1, blank=True, null=True
    )
    capitation_sublevel_4 = models.ForeignKey(
        "location.HealthFacilitySubLevel",
        models.DO_NOTHING,
        db_column="Sublevel4",
        blank=True,
        null=True,
        related_name="+",
    )
    weight_population = models.DecimalField(
        db_column="WeightPopulation",
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
    )
    weight_nb_families = models.DecimalField(
        db_column="WeightNumberFamilies",
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
    )
    weight_insured_population = models.DecimalField(
        db_column="WeightInsuredPopulation",
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
    )
    weight_nb_insured_families = models.DecimalField(
        db_column="WeightNumberInsuredFamilies",
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
    )
    weight_nb_visits = models.DecimalField(
        db_column="WeightNumberVisits",
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
    )
    weight_adjusted_amount = models.DecimalField(
        db_column="WeightAdjustedAmount",
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
    )

    @property
    def ceiling_type(self):
        if (
            self.ded_treatment
            or self.ded_op_treatment
            or self.ded_ip_treatment
            or self.max_treatment
            or self.max_ip_treatment
            or self.max_op_treatment
        ):
            return "T"
        elif (
            self.ded_policy
            or self.ded_op_policy
            or self.ded_ip_policy
            or self.max_policy
            or self.max_ip_policy
            or self.max_op_policy
        ):
            return "P"
        else:
            return "I"

    def has_cycle(self):
        return (
            bool(self.start_cycle_1)
            or bool(self.start_cycle_2)
            or bool(self.start_cycle_3)
            or bool(self.start_cycle_4)
        )

    def has_enrolment_discount(self):
        return self.enrolment_discount_perc and self.enrolment_discount_period

    def has_renewal_discount(self):
        return self.renewal_discount_perc and self.renewal_discount_period

    @property
    def member_count(self):
        from warnings import warn
        warn(
            "'member_count' has been deprecated in favor of 'max_members'",
            DeprecationWarning,
            stacklevel=2
        )
        return self.max_members

    class Meta:
        managed = False
        db_table = "tblProduct"

    CEILING_INTERPRETATION_HOSPITAL = "H"
    CEILING_INTERPRETATION_IN_PATIENT = "I"

    RELATIVE_PRICE_PERIOD_MONTH = "M"
    RELATIVE_PRICE_PERIOD_QUARTER = "Q"
    RELATIVE_PRICE_PERIOD_YEAR = "Y"


class ProductItemOrServiceManager(models.Manager):
    def filter(self, *args, **kwargs):
        keys = [x for x in kwargs if "itemsvc" in x]
        for key in keys:
            new_key = key.replace("itemsvc", self.model.model_prefix)
            kwargs[new_key] = kwargs.pop(key)
        return super(ProductItemOrServiceManager, self).filter(*args, **kwargs)


class ProductItemOrService:
    ORIGIN_PRICELIST = "P"
    ORIGIN_CLAIM = "O"
    ORIGIN_RELATIVE = "R"

    LIMIT_CO_INSURANCE = "C"
    LIMIT_FIXED_AMOUNT = "F"

    objects = ProductItemOrServiceManager()

    class Meta:
        abstract = True


LIMIT_CHOICES = (("F", gettext_lazy("Fixed")), ("C", gettext_lazy("Co-insurance")))


class ProductItem(VersionedModel, ProductItemOrService):
    id = models.AutoField(db_column="ProdItemID", primary_key=True)
    product = models.ForeignKey(
        Product, db_column="ProdID", on_delete=models.DO_NOTHING, related_name="items"
    )
    item = models.ForeignKey(
        "medical.Item",
        db_column="ItemID",
        on_delete=models.DO_NOTHING,
        related_name="items",
    )
    price_origin = models.CharField(
        db_column="PriceOrigin",
        max_length=1,
        null=True,
        blank=True,
        choices=(
            ("P", gettext_lazy("Schema Price")),
            ("O", gettext_lazy("Providers Own Price")),
            ("R", gettext_lazy("Relative Price")),
        ),
    )

    limitation_type = models.CharField(
        db_column="LimitationType",
        max_length=1,
        null=True,
        blank=True,
        choices=LIMIT_CHOICES,
    )
    limitation_type_r = models.CharField(
        db_column="LimitationTypeR",
        max_length=1,
        null=True,
        blank=True,
        choices=LIMIT_CHOICES,
    )
    limitation_type_e = models.CharField(
        db_column="LimitationTypeE",
        max_length=1,
        null=True,
        blank=True,
        choices=LIMIT_CHOICES,
    )

    waiting_period_adult = models.IntegerField(
        db_column="WaitingPeriodAdult", blank=True, null=True
    )
    waiting_period_child = models.IntegerField(
        db_column="WaitingPeriodChild", blank=True, null=True
    )
    limit_no_adult = models.IntegerField(
        db_column="LimitNoAdult", blank=True, null=True
    )
    limit_no_child = models.IntegerField(
        db_column="LimitNoChild", blank=True, null=True
    )
    limit_adult = models.DecimalField(
        db_column="LimitAdult",
        max_digits=18,
        decimal_places=2,
        blank=True,
        null=True,
    )
    limit_child = models.DecimalField(
        db_column="LimitChild", max_digits=18, decimal_places=2, blank=True, null=True
    )
    limit_adult_r = models.DecimalField(
        db_column="LimitAdultR", max_digits=18, decimal_places=2, blank=True, null=True
    )
    limit_adult_e = models.DecimalField(
        db_column="LimitAdultE", max_digits=18, decimal_places=2, blank=True, null=True
    )
    limit_child_r = models.DecimalField(
        db_column="LimitChildR", max_digits=18, decimal_places=2, blank=True, null=True
    )
    limit_child_e = models.DecimalField(
        db_column="LimitChildE", max_digits=18, decimal_places=2, blank=True, null=True
    )
    ceiling_exclusion_adult = models.CharField(
        db_column="CeilingExclusionAdult", max_length=1, null=True, blank=True
    )
    ceiling_exclusion_child = models.CharField(
        db_column="CeilingExclusionChild", max_length=1, null=True, blank=True
    )
    audit_user_id = models.IntegerField(db_column="AuditUserID")
    # rowid = models.TextField(db_column='RowID', blank=True, null=True) This field type is a guess.
    model_prefix = "item"
    objects = ProductItemOrServiceManager()

    class Meta:
        managed = False
        db_table = "tblProductItems"


class ProductService(VersionedModel, ProductItemOrService):
    id = models.AutoField(db_column="ProdServiceID", primary_key=True)
    product = models.ForeignKey(
        Product,
        db_column="ProdID",
        on_delete=models.DO_NOTHING,
        related_name="services",
    )
    service = models.ForeignKey(
        "medical.Service",
        db_column="ServiceID",
        on_delete=models.DO_NOTHING,
        related_name="services",
    )
    price_origin = models.CharField(
        db_column="PriceOrigin",
        max_length=1,
        choices=(
            ("P", gettext_lazy("Schema Price")),
            ("O", gettext_lazy("Providers Own Price")),
            ("R", gettext_lazy("Relative Price")),
        ),
    )
    limit_adult = models.DecimalField(
        db_column="LimitAdult", max_digits=18, decimal_places=2, blank=True, null=True
    )
    limit_child = models.DecimalField(
        db_column="LimitChild", max_digits=18, decimal_places=2, blank=True, null=True
    )
    waiting_period_adult = models.IntegerField(
        db_column="WaitingPeriodAdult", blank=True, null=True
    )
    waiting_period_child = models.IntegerField(
        db_column="WaitingPeriodChild", blank=True, null=True
    )
    limit_no_adult = models.IntegerField(
        db_column="LimitNoAdult", blank=True, null=True
    )
    limit_no_child = models.IntegerField(
        db_column="LimitNoChild", blank=True, null=True
    )
    limitation_type = models.CharField(
        db_column="LimitationType", max_length=1, choices=LIMIT_CHOICES
    )
    limitation_type_r = models.CharField(
        db_column="LimitationTypeR",
        max_length=1,
        null=True,
        blank=True,
        choices=LIMIT_CHOICES,
    )
    limitation_type_e = models.CharField(
        db_column="LimitationTypeE",
        max_length=1,
        null=True,
        blank=True,
        choices=LIMIT_CHOICES,
    )
    limit_adult_r = models.DecimalField(
        db_column="LimitAdultR", max_digits=18, decimal_places=2, blank=True, null=True
    )
    limit_adult_e = models.DecimalField(
        db_column="LimitAdultE", max_digits=18, decimal_places=2, blank=True, null=True
    )
    limit_child_r = models.DecimalField(
        db_column="LimitChildR", max_digits=18, decimal_places=2, blank=True, null=True
    )
    limit_child_e = models.DecimalField(
        db_column="LimitChildE", max_digits=18, decimal_places=2, blank=True, null=True
    )
    ceiling_exclusion_adult = models.CharField(
        db_column="CeilingExclusionAdult", max_length=1, null=True, blank=True
    )
    ceiling_exclusion_child = models.CharField(
        db_column="CeilingExclusionChild", max_length=1, null=True, blank=True
    )
    audit_user_id = models.IntegerField(db_column="AuditUserID")
    # rowid = models.TextField(db_column='RowID', blank=True, null=True) This field type is a guess.

    model_prefix = "service"
    objects = ProductItemOrServiceManager()

    class Meta:
        managed = False
        db_table = "tblProductServices"


class ProductMutation(UUIDModel, ObjectMutation):
    product = models.ForeignKey(Product, models.DO_NOTHING, related_name="+")
    mutation = models.ForeignKey(
        MutationLog, models.DO_NOTHING, related_name="products"
    )

    class Meta:
        managed = True
        db_table = "product_ProductMutation"
