"""The API application: routes ApiRequests to handler methods and maps errors to statuses."""
from .dto import ApiRequest, ApiResponse
from ..errors import NotFound, ValidationError, ConflictError
from ..service.catalog_service import CatalogService
from ..service.cart_service import CartService


class App:
    """Wires the services together and exposes a single `handle(request)` entry point.

    Action -> handler mapping lives in `self._routes`. Each handler takes the `params`
    dict and returns a JSON-able body; exceptions are translated to HTTP-like statuses:
        ValidationError -> 400, NotFound -> 404, ConflictError -> 409, other -> 500.
    """

    def __init__(self, catalog=None, carts=None):
        self.catalog = catalog
        self.carts = carts
        self._routes = {
            "add_product": self._add_product,
            "list_products": self._list_products,
            "create_cart": self._create_cart,
            "add_to_cart": self._add_to_cart,
            "remove_from_cart": self._remove_from_cart,
            "cart_summary": self._cart_summary,
        }

    # ---- dispatch ----
    def handle(self, request):
        handler = self._routes.get(request.action)
        if handler is None:
            return ApiResponse(404, {"error": "unknown action: %s" % request.action})
        try:
            body = handler(request.params)
        except ValidationError as e:
            return ApiResponse(400, {"error": str(e)})
        except NotFound as e:
            return ApiResponse(404, {"error": str(e)})
        except ConflictError as e:
            return ApiResponse(409, {"error": str(e)})
        except Exception as e:  # noqa: BLE001 - API boundary
            return ApiResponse(500, {"error": str(e)})
        return ApiResponse(200, body)

    # ---- handlers ----
    def _add_product(self, p):
        product = self.catalog.add_product(p["sku"], p["name"], p["price_dollars"])
        return {"sku": product.sku, "price_cents": product.price_cents}

    def _list_products(self, p):
        return [{"sku": x.sku, "name": x.name, "price_cents": x.price_cents}
                for x in self.catalog.list_products()]

    def _create_cart(self, p):
        cart = self.carts.create_cart(p["owner"])
        return {"cart_id": cart.cart_id, "owner": cart.owner}

    def _add_to_cart(self, p):
        self.carts.add_to_cart(p["cart_id"], p["sku"], p.get("qty", 1))
        return self.carts.summary(p["cart_id"])

    def _remove_from_cart(self, p):
        self.carts.remove_from_cart(p["cart_id"], p["sku"])
        return self.carts.summary(p["cart_id"])

    def _cart_summary(self, p):
        return self.carts.summary(p["cart_id"])
