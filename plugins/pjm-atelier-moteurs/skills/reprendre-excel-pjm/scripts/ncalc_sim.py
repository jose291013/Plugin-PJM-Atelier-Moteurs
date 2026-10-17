"""Evaluate PJM NCalc formulas in Python to check them against a model.

Usage: from ncalc_sim import ev
       ev(formula, {'Q1': 2, 'Q2': 1000, 'Nup': lambda: 100})
Supports if(), Min, Max, Ceiling, floor, comparisons (=, <=, <, >=, >, !=) and
scientific literals. if() only evaluates the chosen branch, as in NCalc.
Integer division: NCalc divides two integers as integers; this simulator uses
Python division, so keep a double in every division (e.g. 2E1, 5E0).
"""
import math, re

def _split(s):
    out, d, cur = [], 0, ''
    for ch in s:
        if ch == '(': d += 1
        if ch == ')': d -= 1
        if ch == ',' and d == 0:
            out.append(cur); cur = ''; continue
        cur += ch
    out.append(cur)
    return out

def to_python(s):
    i = -1
    while True:
        i = s.find('if(', i + 1)
        if i == -1:
            return re.sub(r'(?<![<>!=])=(?!=)', '==', s).replace('<>', '!=')
        if i == 0 or not (s[i - 1].isalnum() or s[i - 1] == '_'):
            break
    d = 0
    for j in range(i + 2, len(s)):
        if s[j] == '(': d += 1
        elif s[j] == ')':
            d -= 1
            if d == 0: break
    a, b, c = _split(s[i + 3:j])
    return to_python(s[:i]) + f'(({to_python(b)}) if ({to_python(a)}) else ({to_python(c)}))' + to_python(s[j + 1:])

FUNCS = {'Min': min, 'Max': max, 'Ceiling': math.ceil, 'floor': math.floor, 'Floor': math.floor,
         'Round': round, 'Abs': abs, 'Sqrt': math.sqrt, 'Pow': pow, 'Truncate': math.trunc}

def ev(formula, env):
    return eval(to_python(formula), dict(FUNCS), dict(env))

def check(formula):
    """Static checks before saving a formula in PJM."""
    errs = []
    if len(formula) > 1400: errs.append('longer than 1400 characters')
    if formula.count('(') != formula.count(')'): errs.append('unbalanced parentheses')
    if re.search(r'<(?!=? )', formula) or re.search(r'\S<', formula): errs.append('missing space around <')
    if re.search(r'\d\.\d', formula): errs.append('decimal literal (use 45E-1, not 4.5) when Ceiling/floor/Sqrt are used')
    return errs
