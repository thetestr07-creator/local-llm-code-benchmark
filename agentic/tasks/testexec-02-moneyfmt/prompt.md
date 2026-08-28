Implement the stubbed functions `parse_amount` and `format_cents` in
`moneykit/core.py` so that the test suite passes. Run the tests with
`python3 tests/test_money.py` to check your work.

The module works with whole **integer cents** internally (no floats in results).

## `parse_amount(s)` -> int

Parse a human-typed money string into a signed integer number of cents.

- Input is a `str`. Leading/trailing whitespace is ignored.
- An optional leading `-` (with optional surrounding spaces, e.g. `"- 5.00"`)
  marks a negative amount. `+` is also accepted as an explicit positive sign.
- An optional leading currency symbol `$` may appear (after the sign or before
  it, e.g. `"-$5"`, `"$-5"`, `"$5"`). At most one `$`.
- Thousands separators (commas) may appear in the integer part and must be
  ignored: `"1,234.50"` -> `123450`.
- The fractional part is optional. If present it is introduced by `.` and may
  have **0, 1, or 2** digits: `"5"` -> `500`, `"5.7"` -> `570`, `"5.75"` -> `575`.
  A trailing dot with no digits (`"5."`) is valid and means `.00`.
- The integer part is optional when a fractional part is given: `".5"` -> `50`.
- More than 2 fractional digits is an error.
- Empty string, a bare sign, a bare `$`, letters, or any other malformed input
  raises `ValueError`.
- Negative zero normalizes to `0` (i.e. `parse_amount("-0.00") == 0`).

## `format_cents(cents, symbol="$", grouping=True)` -> str

Render a signed integer number of cents as a display string.

- `cents` is an `int`. A non-int (e.g. a float) raises `TypeError`.
- Always shows exactly two fractional digits: `500` -> `"$5.00"`.
- Negative amounts put the sign **before** the symbol: `-500` -> `"-$5.00"`.
- Zero is never shown as negative: `format_cents(0)` -> `"$0.00"`.
- When `grouping` is `True`, the integer part uses commas as thousands
  separators: `123450` -> `"$1,234.50"`; `-123456789` -> `"-$1,234,567.89"`.
- When `grouping` is `False`, no commas are inserted.
- `symbol` may be any string (including `""`); it is placed immediately before
  the digits, after any sign.

Do not change the function signatures. Keep the module importable.
