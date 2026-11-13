from django.core.cache import cache

from catalog.models import Product

CACHE_TTL = 60 * 15


def get_products_by_category(category_id):
    cache_key = f"category_{category_id}"
    products = cache.get(cache_key)

    if products is None:
        products = list(Product.objects.filter(category_id=category_id))
        cache.set(cache_key, products, CACHE_TTL)

    return products