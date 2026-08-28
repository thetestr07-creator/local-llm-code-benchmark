# shop

A small layered shopping-cart application (in-memory, pure stdlib).

## Layout

```
shop/
  errors.py                 shared exception hierarchy
  factory.py                build_app() -> fully wired App
  cli.py                    JSON-in/JSON-out CLI wrapper
  model/
    money.py                integer-cent helpers
    product.py              Product entity
    cart.py                 Cart / CartLine entities
  store/
    base.py                 InMemoryCollection
    product_store.py        ProductStore (keyed by sku)
    cart_store.py           CartStore (keyed by cart_id)
  service/
    catalog_service.py      CatalogService
    cart_service.py         CartService
  api/
    dto.py                  ApiRequest / ApiResponse
    app.py                  App: action -> handler dispatch + error mapping
tests/
  test_smoke.py             end-to-end smoke test
```

## Layers

Requests flow **api -> service -> store -> model**. The `App` maps action strings to
handlers and translates `ValidationError/NotFound/ConflictError` into 400/404/409.

## Run

```bash
python3 tests/test_smoke.py
echo '{"action":"list_products","params":{}}' | python3 -m shop.cli
```
