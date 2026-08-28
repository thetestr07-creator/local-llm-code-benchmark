"""Builds a fully-wired App with in-memory stores. One call, ready to use."""
from .store.product_store import ProductStore
from .store.cart_store import CartStore
from .service.catalog_service import CatalogService
from .service.cart_service import CartService
from .api.app import App


def build_app():
    product_store = ProductStore()
    cart_store = CartStore()
    catalog = CatalogService(product_store)
    carts = CartService(cart_store, product_store)
    return App(catalog=catalog, carts=carts)
