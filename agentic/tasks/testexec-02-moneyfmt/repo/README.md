# moneykit

Small helpers for parsing and formatting money as whole **integer cents**.

```python
from moneykit import parse_amount, format_cents

parse_amount("1,234.50")   # -> 123450
format_cents(123450)       # -> "$1,234.50"
format_cents(-500)         # -> "-$5.00"
```

## Layout

- `moneykit/core.py` — `parse_amount` and `format_cents` (the two functions to implement)
- `moneykit/grouping.py` — thousands-separator helper (implemented)
- `moneykit/rounding.py` — misc rounding helpers (implemented)
- `moneykit/constants.py` — shared constants
- `moneykit/cli.py` — `python -m moneykit.cli parse "5.00"`

## Tests

```
python3 tests/test_money.py
```
