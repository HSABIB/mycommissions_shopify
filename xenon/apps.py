from django.apps import AppConfig


class XenonConfig(AppConfig):
    name = 'xenon'

    SHOPIFY_API_KEY = "29281c56ae2c527fbebb0e1efd74b5f3"
    SHOPIFY_API_SECRET = "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"

    SHOPIFY_API_VERSION = 'unstable'

    SHOPIFY_API_SCOPE = [
        'read_products',
        'read_all_orders'
        'read_customers',
        'read_price_rules'
        'read_discounts',
    ]
    SHOPIFY_API_SCOPE += [
        'write_price_rules',
        'write_discounts',
    ]