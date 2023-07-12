from product.reports import product_sales

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
]
