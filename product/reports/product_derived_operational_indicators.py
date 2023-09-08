from _decimal import Decimal
from datetime import timedelta

from django.db.models import Q, F, ExpressionWrapper, DateField, Sum
from django.db.models.functions import Greatest
from prompt_toolkit import search

from contribution.models import Premium
from core.calendars import ad_calendar
from core.datetimes.ad_datetime import date, AdDate
from location.models import Location, HealthFacility
from product.models import Product

template = """"""

DEFAULT_YEAR = 0
DEFAULT_PRODUCT = -1
ALL_HFS = -2
ALL_MONTHS = -3

CATEGORY_INCURRED_CLAIM_RATIO = "ICR"
CATEGORY_RENEWAL_RATIO = "RR"
CATEGORY_GROWTH_RATIO = "GR"
CATEGORY_PROMPTNESS = "P"
CATEGORY_INSUREE_PER_CLAIM = "IPC"


def generate_subtotal():
    return {
        CATEGORY_INCURRED_CLAIM_RATIO: Decimal(0.00),
        CATEGORY_RENEWAL_RATIO: Decimal(0.00),
        CATEGORY_GROWTH_RATIO: Decimal(0.00),
        CATEGORY_PROMPTNESS: Decimal(0.00),
        CATEGORY_INSUREE_PER_CLAIM: Decimal(0.00),
    }


def calculate_start_end_month_dates(year: int, month: int):
    num_days = ad_calendar.monthrange(year, month)[1]
    start_date = date(year, month, 1)
    end_date = date(year, month, num_days)
    return start_date, end_date


def date_difference_or_1(date1: AdDate, date2: AdDate):
    # Returns the difference of days between 2 dates, or 1 if the difference is < 1
    delta = date2 - date1
    if delta.days > 0:
        return delta.days
    return 1


def fetch_premium_data(search_filters: Q, start_month: AdDate, end_month: AdDate):
    premium_data = {}
    total = Decimal(0.00)

    premiums = (Premium.objects.filter(search_filters)
                               .values("pay_date",
                                       product_id=F("policy__product_id"),
                                       expiry_date=F("policy__expiry_date"),
                                       effective_date=F("policy__effective_date"))
                               .annotate(greatest_date_pay_effective=ExpressionWrapper(
                                   Greatest(F("pay_date"),
                                            F("policy__effective_date")),
                                   output_field=DateField()))
                               .annotate(greatest_date_pay_start=ExpressionWrapper(
                                   Greatest(F("pay_date"),
                                            start_month),
                                   output_field=DateField()))
                               .annotate(total_amount=Sum("amount"))
                               .order_by())

    for premium in premiums:
        expiry_date = premium["expiry_date"]
        greatest_date_pay_effective = premium["greatest_date_pay_effective"]
        amount = premium["total_amount"]
        if start_month < expiry_date <= end_month:
            multiplicator = date_difference_or_1(premium["greatest_date_pay_start"], expiry_date)
            denominator = date_difference_or_1(greatest_date_pay_effective, expiry_date)
            total += multiplicator * (amount/denominator)
        elif start_month <= greatest_date_pay_effective <= end_month:
            multiplicator = end_month.day + 1 - greatest_date_pay_effective.day
            denominator = date_difference_or_1(greatest_date_pay_effective, expiry_date)
            total += multiplicator * (amount/denominator)
        elif expiry_date > end_month and premium["effective_date"] < start_month and premium["pay_date"] < start_month:
            multiplicator = end_month.day
            expiry_date_minus_1_day = expiry_date - timedelta(days=1)
            denominator = date_difference_or_1(greatest_date_pay_effective, expiry_date_minus_1_day)
            total += multiplicator * (amount/denominator)

    premium_data["allocated"] = total
    return premium_data


def fetch_claim_data(search_filters: Q, start_month: AdDate, end_month: AdDate):
    claim_data = {}
    total = Decimal(0.00)


    return claim_data


def product_derived_operational_indicators_query(user,
                                                 requested_month=ALL_MONTHS,
                                                 requested_year=DEFAULT_YEAR,
                                                 requested_product_id=DEFAULT_PRODUCT,
                                                 requested_hf_id=ALL_HFS,
                                                 **kwargs):

    # decided to get rid of location since we get it from the product

    # Checking the parameters received and returning an error if anything is wrong
    validated_parameters = {}
    month = int(requested_month)
    if month not in range(1, 13) and month != ALL_MONTHS:
        return {"error": "Error - the selected month is invalid"}
    year = int(requested_year)
    if year not in range(2010, 2100):
        return {"error": "Error - the selected year is invalid"}
    product_id = int(requested_product_id)
    product = Product.objects.filter(validity_to=None, id=product_id).first()
    if not product:
        return {"error": "Error - the requested product does not exist"}
    validated_parameters["product"] = product
    hf_id = int(requested_hf_id)
    if hf_id != ALL_HFS:
        hf = HealthFacility.objects.filter(validity_to=None, id=hf_id).first()
        if not hf:
            return {"error": "Error - the requested health facility does not exist"}
        validated_parameters["hf"] = hf
    # check if the product location is set, and which type it is

    # Product already available through parameter verification

    working_months = list(range(1, 13)) if month == ALL_MONTHS else [month]

    default_premium_filters = (Q(validity_to__isnull=True)
                               & Q(pay_date__lte=F("policy__expiry_date"))
                               & Q(policy__validity_to__isnull=True)
                               & Q(policy__status__gt=1)  # All the non-idle policies
                               & Q(policy__product_id=product.id))

    default_claim_filters = Q(validity_to__isnull=True)

    default_policy_filters = Q(validity_to__isnull=True)

    for current_month in working_months:
        start_date, end_date = calculate_start_end_month_dates(year, current_month)
        premium_data = fetch_premium_data(default_premium_filters, start_date, end_date)
        claim_data = fetch_claim_data(default_claim_filters, start_date, end_date)

        print(premium_data)

    """
    71
    75
    68
    15
    16
    40
    """

    """
    - global:
        - product validity_to = null
    - policy:
        3 - renewals:
            - policy validity_to = null
            - policy status > 1
            - policy stage == R
            - policy enroll_date in given year + given month
            - family validity_to = null
            - optional product
            - optional location (region/district) - linked through Family
            - COUNT(policy_id)
        4 - expired:
            - policy validity_to = null
            - policy status > 1
            - policy expiry_date in given year + given month
            - family validity_to = null
            - optional product
            - optional location (region/district) - linked through Family
            - COUNT(policy_id)
        5 - new:
            - policy validity_to = null
            - policy status > 1
            - policy stage == N
            - policy enroll_date in given year + given month
            - family validity_to = null
            - insuree validity_to = null
            - location pyramid validity_to = null
            - optional location (region/district) - linked through Family
            - optional product
            - COUNT(insuree_id)
        6 - total:
            - policy validity_to = null
            - policy status > 1
            - policy effective_date <= given day (end of month)
            - policy expiry_date > given day (end of month)
            - product validity_to = null
            - family validity_to = null
            - insuree validity_to = null
            - optional product
            - optional location (region/district) - linked through Family
            - COUNT(insuree_id)
        8 - insurees:
            - policy validity_to = null
            - product validity_to = null
            - family validity_to = null
            - insuree validity_to = null
            - policy status > 1
            - policy effective_date <= given day (end of month)
            - policy expiry_date > given day (end of month)
            - optional product
            - optional location (region/district) - linked through Family
            - COUNT(insuree_id)
    - claim:
        0 - base product query:
            - claim validity_to = null
            - claim item validity_to = null
            - claim service validity_to = null
            - family validity_to = null
            - insuree validity_to = null
            - batch run validity_to = null
            - optional product
            - optional district - linked through Family
            - batch run for given year + given month
        1 - remunerated:
            - claim validity_to = null
            - claim status = 16
            - claim date_from in given month + given year
            - claim item validity_to = null
            - claim item status = 1
            - claim service validity_to = null
            - claim service status = 1
            - hf validity_to = null
            - optional product
            - optional hf
            - optional location (region/district) - linked through HF
            - SUM(remunerated)
        7 - total:
            - claim validity_to = null
            - claim item validity_to = null
            - claim service validity_to = null
            - claim date_from in given month + given year
            - hf validity_to = null
            - optional product
            - optional hf
            - optional location (region/district) - linked through HF
            - COUNT(claim_id)
    - premium:
        2 - available premium:
            - premium validity_to = null
            - premium pay_date <= policy expiry_date
            - policy validity_to = null
            - policy status != 1
            - given product
            - optional location (region/district) - linked through Family
            - SUM(complicated)
    """

    return {}
