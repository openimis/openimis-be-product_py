from django.db.models import Q

from location.models import Location, HealthFacility
from product.models import Product

template = """"""

ALL_PRODUCTS = -1
ALL_REGIONS = -2
ALL_DISTRICTS = -3
ALL_HFS = -4
ALL_MONTHS = -5
DEFAULT_YEAR = 0



def product_derived_operational_indicators_query(user,
                                                 requested_month=ALL_MONTHS,
                                                 requested_year=DEFAULT_YEAR,
                                                 requested_region_id=ALL_REGIONS,
                                                 requested_district_id=ALL_DISTRICTS,
                                                 requested_product_id=ALL_PRODUCTS,
                                                 requested_hf_id=ALL_HFS,
                                                 **kwargs):
    # Checking the parameters received and returning an error if anything is wrong
    validated_parameters = {}
    month = int(requested_month)
    if month not in range(1, 13) and month != ALL_MONTHS:
        return {"error": "Error - the selected month is invalid"}
    year = int(requested_year)
    if year not in range(2010, 2100):
        return {"error": "Error - the selected year is invalid"}
    product_id = int(requested_product_id)
    if product_id != ALL_PRODUCTS:
        product = Product.objects.filter(validity_to=None, id=product_id).first()
        if not product:
            return {"error": "Error - the requested product does not exist"}
        validated_parameters["product"] = product
    region_id = int(requested_region_id)
    if region_id != ALL_REGIONS:
        region = Location.objects.filter(validity_to=None, type='R', id=region_id).first()
        if not region:
            return {"error": "Error - the requested region does not exist"}
        validated_parameters["region"] = region
    district_id = int(requested_district_id)
    if district_id != ALL_DISTRICTS:
        district_filters = Q(validity_to__isnull=True) & Q(type="D") & Q(id=district_id)
        if region_id != ALL_REGIONS:  # The FE pickers allow you to select a district without a region, so additional steps are required
            district_filters &= Q(parent_id=region_id)
        district = Location.objects.filter(district_filters).first()
        if not district:
            return {"error": "Error - the requested district does not exist"}
        validated_parameters["district"] = district
        if region_id == ALL_REGIONS:  # The FE pickers allow you to select a district without a region, so additional steps are required
            validated_parameters["region"] = district.parent
    hf_id = int(requested_hf_id)
    if hf_id != ALL_HFS:
        hf = HealthFacility.objects.filter(validity_to=None, id=hf_id).first()
        if not hf:
            return {"error": "Error - the requested health facility does not exist"}
        validated_parameters["hf"] = hf


    return {}
