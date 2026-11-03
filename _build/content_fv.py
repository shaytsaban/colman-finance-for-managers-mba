# The future value table, shared by every lesson that solves with FV.
FVROWS = [('ריבית לתקופה', 'rate'), ('מספר תקופות', 'nper'), ('תשלום קבוע בכל תקופה', 'pmt'), ('סכום בהווה', 'pv'), ('ערך עתידי', 'fv')]


def _pctf(v):
    s = f'{v * 100:.6f}'.rstrip('0').rstrip('.')
    return 'pct' + str(len(s.split('.')[1]) if '.' in s else 0)


def fvt(cols, r1=1, corner='', lab=True):
    """A future value table in the course layout: A the Hebrew label, B the Excel name, one column per part or stage from C.
    cols: dicts h (header), rate, nper, pmt, pv. A number is typed by the student; '=..' in nper is a period conversion the student writes;
    '=..' in pv is a formula of the solution (the stage before, with the sign flipped). Returns data, sol, fmt and the fv cells."""
    d, s, f, out = {}, {}, {}, []
    if lab:
        d[f'A{r1}'] = corner or 'הנתון'
        d[f'B{r1}'] = 'שם'
        for k, (he, en) in enumerate(FVROWS):
            d[f'A{r1 + 1 + k}'] = he; d[f'B{r1 + 1 + k}'] = en
    for j, c in enumerate(cols):
        L = chr(67 + j)
        d[f'{L}{r1}'] = c['h']
        rr = {k: f'{L}{r1 + 1 + i}' for i, k in enumerate(['rate', 'nper', 'pmt', 'pv', 'fv'])}
        for k in ('rate', 'nper', 'pmt', 'pv'):
            v = c[k]
            if isinstance(v, str) and v.startswith('=') and k == 'pv':
                s[rr[k]] = v
            else:
                d[rr[k]] = v
        s[rr['fv']] = f"=FV({rr['rate']},{rr['nper']},{rr['pmt']},{rr['pv']})"
        f[rr['rate']] = _pctf(c['rate']); f[rr['pv']] = 'num2'; f[rr['fv']] = 'num2'; f[rr['pmt']] = 'num0'
        out.append(rr['fv'])
    return d, s, f, out
