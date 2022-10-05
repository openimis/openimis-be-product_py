import graphene


class CareTypeEnum(graphene.Enum):
    IN_PATIENT = "I"
    OUT_PATIENT = "O"
    BOTH = "B"


class CeilingInterpretationEnum(graphene.Enum):
    CLAIM_TYPE = "I"
    HEALTH_FACILITY_TYPE = "H"


class CeilingTypeEnum(graphene.Enum):
    TREATMENT = "T"
    POLICY = "P"
    INSUREE = "I"


class PriceOriginEnum(graphene.Enum):
    PRICELIST = "P"
    PROVIDER = "O"
    RELATIVE = "R"


class LimitTypeEnum(graphene.Enum):
    CO_INSURANCE = "C"
    FIXED_AMOUNT = "F"


class CeilingExclusionEnum(graphene.Enum):
    HOSPITAL = "H"
    NON_HOSPITAL = "N"
    BOTH = "B"
