# NCalc – syntax summary (as used by PJM)

- Values: integers (Int32), decimals `12.5` (Decimal), scientific `9E8` (Double), booleans `true/false`, strings `'text'`, dates `#2026/10/16#`.
- Parameters: `Q1`, or `[My Param]` for names with spaces.
- Operator precedence: primary `( )` > unary `! not - ~` > power > `* / %` (left to right) > `+ -` > relational `= == != <> < <= > >=` > logical (`and` before `or`).
- Built-in functions: Abs, Acos, Asin, Atan, Ceiling, Cos, Exp, Floor (PJM button: `floor`), IEEERemainder, Log, Log10, Max(a,b), Min(a,b), Pow, Round(x, n) (banker's rounding by default), Sign, Sin, Sqrt, Tan, Truncate, `in(x, a, b, …)`, `if(cond, a, b)` (only the chosen branch is evaluated).
- PJM evaluates case-insensitively in practice (`If`, `max`, `floor` work).
- Pitfalls:
  - `(a % b)` and `*` have the same precedence and are evaluated left to right: `x * y % n` is `(x * y) % n`.
  - `floor(ceiling(x))` is redundant.
  - `if((Q2-4)/2)%Nup()=0, …)` closes the `if` too early: count parentheses.
  - Integer division: force decimals with `4.0` or `1.0 *`.
