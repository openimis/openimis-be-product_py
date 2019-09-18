from django.db import models
from core import fields


class Product(models.Model):
    id = models.AutoField(db_column='ProdID', primary_key=True)
    code = models.CharField(db_column='ProductCode', max_length=8)
    name = models.CharField(db_column='ProductName', max_length=100)
    # locationid = models.ForeignKey(Tbllocations, models.DO_NOTHING, db_column='LocationId', blank=True, null=True)
    # insuranceperiod = models.SmallIntegerField(db_column='InsurancePeriod')
    date_from = models.DateTimeField(db_column='DateFrom')
    date_to = models.DateTimeField(db_column='DateTo')
    # conversionprodid = models.ForeignKey('self', models.DO_NOTHING, db_column='ConversionProdID', blank=True, null=True)
    lump_sum = models.DecimalField(db_column='LumpSum', max_digits=18, decimal_places=2)
    member_count = models.SmallIntegerField(db_column='MemberCount')
    # premiumadult = models.DecimalField(db_column='PremiumAdult', max_digits=18, decimal_places=2, blank=True, null=True)
    # premiumchild = models.DecimalField(db_column='PremiumChild', max_digits=18, decimal_places=2, blank=True, null=True)
    # dedinsuree = models.DecimalField(db_column='DedInsuree', max_digits=18, decimal_places=2, blank=True, null=True)
    # dedopinsuree = models.DecimalField(db_column='DedOPInsuree', max_digits=18, decimal_places=2, blank=True, null=True)
    # dedipinsuree = models.DecimalField(db_column='DedIPInsuree', max_digits=18, decimal_places=2, blank=True, null=True)
    # maxinsuree = models.DecimalField(db_column='MaxInsuree', max_digits=18, decimal_places=2, blank=True, null=True)
    # maxopinsuree = models.DecimalField(db_column='MaxOPInsuree', max_digits=18, decimal_places=2, blank=True, null=True)
    # maxipinsuree = models.DecimalField(db_column='MaxIPInsuree', max_digits=18, decimal_places=2, blank=True, null=True)
    # periodrelprices = models.CharField(db_column='PeriodRelPrices', max_length=1, blank=True, null=True)
    # periodrelpricesop = models.CharField(db_column='PeriodRelPricesOP', max_length=1, blank=True, null=True)
    # periodrelpricesip = models.CharField(db_column='PeriodRelPricesIP', max_length=1, blank=True, null=True)
    # acccodepremiums = models.CharField(db_column='AccCodePremiums', max_length=25, blank=True, null=True)
    # acccoderemuneration = models.CharField(db_column='AccCodeRemuneration', max_length=25, blank=True, null=True)
    # dedtreatment = models.DecimalField(db_column='DedTreatment', max_digits=18, decimal_places=2, blank=True, null=True)
    # dedoptreatment = models.DecimalField(db_column='DedOPTreatment', max_digits=18, decimal_places=2, blank=True, null=True)
    # dediptreatment = models.DecimalField(db_column='DedIPTreatment', max_digits=18, decimal_places=2, blank=True, null=True)
    # maxtreatment = models.DecimalField(db_column='MaxTreatment', max_digits=18, decimal_places=2, blank=True, null=True)
    # maxoptreatment = models.DecimalField(db_column='MaxOPTreatment', max_digits=18, decimal_places=2, blank=True, null=True)
    # maxiptreatment = models.DecimalField(db_column='MaxIPTreatment', max_digits=18, decimal_places=2, blank=True, null=True)
    # dedpolicy = models.DecimalField(db_column='DedPolicy', max_digits=18, decimal_places=2, blank=True, null=True)
    # dedoppolicy = models.DecimalField(db_column='DedOPPolicy', max_digits=18, decimal_places=2, blank=True, null=True)
    # dedippolicy = models.DecimalField(db_column='DedIPPolicy', max_digits=18, decimal_places=2, blank=True, null=True)
    # maxpolicy = models.DecimalField(db_column='MaxPolicy', max_digits=18, decimal_places=2, blank=True, null=True)
    # maxoppolicy = models.DecimalField(db_column='MaxOPPolicy', max_digits=18, decimal_places=2, blank=True, null=True)
    # maxippolicy = models.DecimalField(db_column='MaxIPPolicy', max_digits=18, decimal_places=2, blank=True, null=True)
    grace_period = models.IntegerField(db_column='GracePeriod')
    validity_from = fields.DateTimeField(db_column='ValidityFrom')
    validity_to = fields.DateTimeField(db_column='ValidityTo', blank=True, null=True)
    legacy_id = models.IntegerField(db_column='LegacyID', blank=True, null=True)
    audit_user_id = models.IntegerField(db_column='AuditUserID')
    # rowid = models.TextField(db_column='RowID', blank=True, null=True) This field type is a guess.
    # registrationlumpsum = models.DecimalField(db_column='RegistrationLumpSum', max_digits=18, decimal_places=2, blank=True, null=True)
    # registrationfee = models.DecimalField(db_column='RegistrationFee', max_digits=18, decimal_places=2, blank=True, null=True)
    # generalassemblylumpsum = models.DecimalField(db_column='GeneralAssemblyLumpSum', max_digits=18, decimal_places=2, blank=True, null=True)
    # generalassemblyfee = models.DecimalField(db_column='GeneralAssemblyFee', max_digits=18, decimal_places=2, blank=True, null=True)
    # startcycle1 = models.CharField(db_column='StartCycle1', max_length=5, blank=True, null=True)
    # startcycle2 = models.CharField(db_column='StartCycle2', max_length=5, blank=True, null=True)
    max_no_consultation = models.IntegerField(db_column='MaxNoConsultation', blank=True, null=True)
    max_no_surgery = models.IntegerField(db_column='MaxNoSurgery', blank=True, null=True)
    max_no_delivery = models.IntegerField(db_column='MaxNoDelivery', blank=True, null=True)
    max_no_hospitalization = models.IntegerField(db_column='MaxNoHospitalizaion', blank=True, null=True)
    max_no_visits = models.IntegerField(db_column='MaxNoVisits', blank=True, null=True)
    # maxamountconsultation = models.DecimalField(db_column='MaxAmountConsultation', max_digits=18, decimal_places=2, blank=True, null=True)
    # maxamountsurgery = models.DecimalField(db_column='MaxAmountSurgery', max_digits=18, decimal_places=2, blank=True, null=True)
    # maxamountdelivery = models.DecimalField(db_column='MaxAmountDelivery', max_digits=18, decimal_places=2, blank=True, null=True)
    # maxamounthospitalization = models.DecimalField(db_column='MaxAmountHospitalization', max_digits=18, decimal_places=2, blank=True, null=True)
    # graceperiodrenewal = models.IntegerField(db_column='GracePeriodRenewal', blank=True, null=True)
    # maxinstallments = models.IntegerField(db_column='MaxInstallments', blank=True, null=True)
    # waitingperiod = models.IntegerField(db_column='WaitingPeriod', blank=True, null=True)
    # threshold = models.IntegerField(db_column='Threshold', blank=True, null=True)
    # renewaldiscountperc = models.IntegerField(db_column='RenewalDiscountPerc', blank=True, null=True)
    # renewaldiscountperiod = models.IntegerField(db_column='RenewalDiscountPeriod', blank=True, null=True)
    # startcycle3 = models.CharField(db_column='StartCycle3', max_length=5, blank=True, null=True)
    # startcycle4 = models.CharField(db_column='StartCycle4', max_length=5, blank=True, null=True)
    # administrationperiod = models.IntegerField(db_column='AdministrationPeriod', blank=True, null=True)
    # maxpolicyextramember = models.DecimalField(db_column='MaxPolicyExtraMember', max_digits=18, decimal_places=2, blank=True, null=True)
    # maxpolicyextramemberip = models.DecimalField(db_column='MaxPolicyExtraMemberIP', max_digits=18, decimal_places=2, blank=True, null=True)
    # maxpolicyextramemberop = models.DecimalField(db_column='MaxPolicyExtraMemberOP', max_digits=18, decimal_places=2, blank=True, null=True)
    # maxceilingpolicy = models.DecimalField(db_column='MaxCeilingPolicy', max_digits=18, decimal_places=2, blank=True, null=True)
    # maxceilingpolicyip = models.DecimalField(db_column='MaxCeilingPolicyIP', max_digits=18, decimal_places=2, blank=True, null=True)
    # maxceilingpolicyop = models.DecimalField(db_column='MaxCeilingPolicyOP', max_digits=18, decimal_places=2, blank=True, null=True)
    # enrolmentdiscountperc = models.IntegerField(db_column='EnrolmentDiscountPerc', blank=True, null=True)
    # enrolmentdiscountperiod = models.IntegerField(db_column='EnrolmentDiscountPeriod', blank=True, null=True)
    # maxamountantenatal = models.DecimalField(db_column='MaxAmountAntenatal', max_digits=18, decimal_places=2, blank=True, null=True)
    max_no_antenatal = models.IntegerField(db_column='MaxNoAntenatal', blank=True, null=True)
    # ceilinginterpretation = models.ForeignKey(Tblceilinginterpretation, models.DO_NOTHING, db_column='CeilingInterpretation', blank=True, null=True)
    # level1 = models.CharField(db_column='Level1', max_length=1, blank=True, null=True)
    # sublevel1 = models.ForeignKey(Tblhfsublevel, models.DO_NOTHING, db_column='Sublevel1', blank=True, null=True)
    # level2 = models.CharField(db_column='Level2', max_length=1, blank=True, null=True)
    # sublevel2 = models.ForeignKey(Tblhfsublevel, models.DO_NOTHING, db_column='Sublevel2', blank=True, null=True)
    # level3 = models.CharField(db_column='Level3', max_length=1, blank=True, null=True)
    # sublevel3 = models.ForeignKey(Tblhfsublevel, models.DO_NOTHING, db_column='Sublevel3', blank=True, null=True)
    # level4 = models.CharField(db_column='Level4', max_length=1, blank=True, null=True)
    # sublevel4 = models.ForeignKey(Tblhfsublevel, models.DO_NOTHING, db_column='Sublevel4', blank=True, null=True)
    # sharecontribution = models.DecimalField(db_column='ShareContributions', max_digits=5, decimal_places=2, blank=True, null=True)
    # weightpopulation = models.DecimalField(db_column='WeightPopulation', max_digits=5, decimal_places=2, blank=True, null=True)
    # weightnumberfamilies = models.DecimalField(db_column='WeightNumberFamilies', max_digits=5, decimal_places=2, blank=True, null=True)
    # weightinsuredpopulation = models.DecimalField(db_column='WeightInsuredPopulation', max_digits=5, decimal_places=2, blank=True, null=True)
    # weightnumberinsuredfamilies = models.DecimalField(db_column='WeightNumberInsuredFamilies', max_digits=5, decimal_places=2, blank=True, null=True)
    # weightnumbervisits = models.DecimalField(db_column='WeightNumberVisits', max_digits=5, decimal_places=2, blank=True, null=True)
    # weightadjustedamount = models.DecimalField(db_column='WeightAdjustedAmount', max_digits=5, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tblProduct'


class ProductItem(models.Model):
    id = models.AutoField(db_column='ProdItemID', primary_key=True)
    product = models.ForeignKey(Product, db_column='ProdID', on_delete=models.DO_NOTHING, related_name="items")
    item = models.ForeignKey("medical.Item", db_column='ItemID', on_delete=models.DO_NOTHING, related_name="items")
    limitation_type = models.CharField(db_column='LimitationType', max_length=1, null=True, blank=True)
    price_origin = models.CharField(db_column='PriceOrigin', max_length=1, null=True, blank=True)
    limit_adult = models.DecimalField(db_column='LimitAdult', max_digits=18, decimal_places=2, blank=True, null=True)
    limit_child = models.DecimalField(db_column='LimitChild', max_digits=18, decimal_places=2, blank=True, null=True)
    waiting_period_adult = models.IntegerField(db_column='WaitingPeriodAdult', blank=True, null=True)
    waiting_period_child = models.IntegerField(db_column='WaitingPeriodChild', blank=True, null=True)
    limit_no_adult = models.IntegerField(db_column='LimitNoAdult', blank=True, null=True)
    limit_no_child = models.IntegerField(db_column='LimitNoChild', blank=True, null=True)
    limitation_type_r = models.CharField(db_column='LimitationTypeR', max_length=1, null=True, blank=True)
    limitation_type_e = models.CharField(db_column='LimitationTypeE', max_length=1, null=True, blank=True)
    limit_adult_r = models.DecimalField(db_column='LimitAdultR', max_digits=18, decimal_places=2, blank=True, null=True)
    limit_adult_e = models.DecimalField(db_column='LimitAdultE', max_digits=18, decimal_places=2, blank=True, null=True)
    limit_child_r = models.DecimalField(db_column='LimitChildR', max_digits=18, decimal_places=2, blank=True, null=True)
    limit_child_e = models.DecimalField(db_column='LimitChildE', max_digits=18, decimal_places=2, blank=True, null=True)
    ceiling_exclusion_adult = models.CharField(db_column='CeilingExclusionAdult', max_length=1, null=True, blank=True)
    ceiling_exclusion_child = models.CharField(db_column='CeilingExclusionChild', max_length=1, null=True, blank=True)
    validity_from = fields.DateTimeField(db_column='ValidityFrom')
    validity_to = fields.DateTimeField(db_column='ValidityTo', blank=True, null=True)
    # legacy_id = models.IntegerField(db_column='LegacyID', blank=True, null=True)
    # audit_user_id = models.IntegerField(db_column='AuditUserID')
    # rowid = models.TextField(db_column='RowID', blank=True, null=True) This field type is a guess.

    class Meta:
        managed = False
        db_table = 'tblProductItems'


class ProductService(models.Model):
    id = models.AutoField(db_column='ProdServiceID', primary_key=True)
    product = models.ForeignKey(Product, db_column='ProdID', on_delete=models.DO_NOTHING, related_name="products")
    service = models.ForeignKey("medical.Service", db_column='ServiceID', on_delete=models.DO_NOTHING,
                                related_name="products")
    limitation_type = models.CharField(db_column='LimitationType', max_length=1)
    price_origin = models.CharField(db_column='PriceOrigin', max_length=1)
    limit_adult = models.DecimalField(db_column='LimitAdult', max_digits=18, decimal_places=2, blank=True, null=True)
    limit_child = models.DecimalField(db_column='LimitChild', max_digits=18, decimal_places=2, blank=True, null=True)
    waiting_period_adult = models.IntegerField(db_column='WaitingPeriodAdult', blank=True, null=True)
    waiting_period_child = models.IntegerField(db_column='WaitingPeriodChild', blank=True, null=True)
    limit_no_adult = models.IntegerField(db_column='LimitNoAdult', blank=True, null=True)
    limit_no_child = models.IntegerField(db_column='LimitNoChild', blank=True, null=True)
    limitation_type_r = models.CharField(db_column='LimitationTypeR', max_length=1, null=True, blank=True)
    limitation_type_e = models.CharField(db_column='LimitationTypeE', max_length=1, null=True, blank=True)
    limit_adult_r = models.DecimalField(db_column='LimitAdultR', max_digits=18, decimal_places=2, blank=True, null=True)
    limit_adult_e = models.DecimalField(db_column='LimitAdultE', max_digits=18, decimal_places=2, blank=True, null=True)
    limit_child_r = models.DecimalField(db_column='LimitChildR', max_digits=18, decimal_places=2, blank=True, null=True)
    limit_child_e = models.DecimalField(db_column='LimitChildE', max_digits=18, decimal_places=2, blank=True, null=True)
    ceiling_exclusion_adult = models.CharField(db_column='CeilingExclusionAdult', max_length=1, null=True, blank=True)
    ceiling_exclusion_child = models.CharField(db_column='CeilingExclusionChild', max_length=1, null=True, blank=True)
    validity_from = fields.DateTimeField(db_column='ValidityFrom')
    validity_to = fields.DateTimeField(db_column='ValidityTo', blank=True, null=True)
    # legacy_id = models.IntegerField(db_column='LegacyID', blank=True, null=True)
    audit_user_id = models.IntegerField(db_column='AuditUserID')
    # rowid = models.TextField(db_column='RowID', blank=True, null=True) This field type is a guess.

    class Meta:
        managed = False
        db_table = 'tblProductServices'

    LIMIT_CO_INSURANCE = 'C'
    LIMIT_FIXED_AMOUNT = 'F'
    LIMIT_OTHER = 'O'

    ORIGIN_PRICELIST = 'P'
    ORIGIN_CLAIM = 'O'
    ORIGIN_RELATIVE = 'R'
    ORIGIN_EMERGENCY = 'E'
