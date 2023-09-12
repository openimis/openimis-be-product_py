from product.reports import product_sales, product_derived_operational_indicators
from product.reports.product_derived_operational_indicators import product_derived_operational_indicators_query

report_definitions = [
    {
        "name": "product_sales",
        "engine": 0,
        "default_report": product_sales.template,
        "description": "Product sales",
        "module": "product",
        "python_query": product_sales.product_sales_query,
        "permission": ["131205"],
    },
    {
        "name": "product_derived_operational_indicators",
        "engine": 0,
        "default_report": product_derived_operational_indicators.template,
        "description": "Product Derived operational indicators",
        "module": "product",
        "python_query": product_derived_operational_indicators_query,
        "permission": ["131203"],
    },
]
