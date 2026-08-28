Exactly one function in `accesskit/roles.py` has a security bug: it grants access
that it should deny. Review the code and identify which function is wrong.

Do NOT modify `accesskit/roles.py`. Instead, write a file named `findings.json` at
the repository root with this exact shape:

```json
{"buggy_function": "<name of the buggy function>"}
```

Use the function's name as it appears in the source (e.g. `can_view`, `can_edit`,
`can_delete`, `is_admin`).
