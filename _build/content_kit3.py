# Helpers of lesson 3 (and later lessons): the drawings and the timeline card of lesson 2, a table for FV or PMT whose rate may be
# converted inside its cell, a click-to-open explanation, and the flow-chart node.
_FV, _PMT = _fin.FV, _fin.PMT
nf = lambda x: f'{abs(x):,.2f}'

# ---------------------------------------------------------------- drawings (copied from lesson 2, so that every lesson can use them) (original, drawn here)
TOONS.update({
 'hotdog': '<ellipse cx="60" cy="74" rx="50" ry="22" fill="#e8b45a" stroke="#a86703" stroke-width="3"/><rect x="8" y="50" width="104" height="26" rx="13" fill="#c4421f"/><path d="M20 58q8-8 16 0t16 0t16 0t16 0t16 0" fill="none" stroke="#ffd37a" stroke-width="4" stroke-linecap="round"/><circle cx="46" cy="86" r="3.5" fill="#111"/><circle cx="74" cy="86" r="3.5" fill="#111"/><path d="M50 94q10 7 20 0" fill="none" stroke="#111" stroke-width="3" stroke-linecap="round"/><path d="M40 30q4-8 0-14M60 28q4-8 0-14M80 30q4-8 0-14" fill="none" stroke="#8a93aa" stroke-width="3" stroke-linecap="round"/>',
 'car': '<path d="M14 78q0-16 14-18l10-22q3-6 10-6h30q7 0 10 6l10 22q12 2 12 18v12H14z" fill="#27447f"/><path d="M42 40h36l8 18H34z" fill="#dff5f2"/><circle cx="38" cy="92" r="12" fill="#111"/><circle cx="38" cy="92" r="5" fill="#8a93aa"/><circle cx="86" cy="92" r="12" fill="#111"/><circle cx="86" cy="92" r="5" fill="#8a93aa"/><circle cx="24" cy="72" r="5" fill="#ffd37a"/><circle cx="100" cy="72" r="5" fill="#ffd37a"/><path d="M52 76q8 6 18 0" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round"/>',
 'pause': '<circle cx="60" cy="62" r="42" fill="#fff" stroke="#1b2d55" stroke-width="5"/><rect x="42" y="42" width="12" height="40" rx="4" fill="#ff6a4d"/><rect x="66" y="42" width="12" height="40" rx="4" fill="#ff6a4d"/><text x="92" y="26" font-size="26" font-weight="800" fill="#5d6a86">z</text><text x="106" y="14" font-size="24" font-weight="800" fill="#5d6a86">z</text>',
 'calendar': '<rect x="18" y="22" width="84" height="84" rx="10" fill="#fff" stroke="#1b2d55" stroke-width="4"/><rect x="18" y="22" width="84" height="24" rx="10" fill="#ff6a4d"/><path d="M38 14v16M82 14v16" stroke="#1b2d55" stroke-width="6" stroke-linecap="round"/><circle cx="46" cy="66" r="4" fill="#111"/><circle cx="74" cy="66" r="4" fill="#111"/><path d="M46 74q14 10 28 0" fill="none" stroke="#111" stroke-width="3.5" stroke-linecap="round"/><text x="60" y="103" font-size="24" font-weight="800" fill="#0f9d90" text-anchor="middle">₪</text>',
})

def TLC(ticks, flows=None, marks=None, brace=None, W=410, fs=17):
    """A timeline in its own card, under a question. A named value (FV₃) sits above its time point;
    where a deposit already holds that place, the name moves under the axis, as a dot."""
    flows = flows or {}
    up = {k: v for k, v in (marks or {}).items() if k not in flows}
    mv = [dict(a=k, b=k, t=v) for k, v in (marks or {}).items() if k in flows]
    return f'<div class="card tlw">{TL(ticks, flows=flows, marks=up, moves=mv, brace=brace, W=W, fs=fs, fh=26, seq=1)}</div>'



TOONS.update({
 'flag': '<path d="M30 110V14" stroke="#1b2d55" stroke-width="6" stroke-linecap="round"/><path d="M33 16h58l-14 20 14 20H33z" fill="#ff6a4d"/><circle cx="56" cy="34" r="3.5" fill="#fff"/><circle cx="70" cy="34" r="3.5" fill="#fff"/><path d="M54 44q9 6 18 0" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round"/><ellipse cx="30" cy="110" rx="18" ry="5" fill="#d9d2c3"/>',
 'ruler': '<rect x="8" y="44" width="104" height="30" rx="5" fill="#ffd37a" stroke="#a86703" stroke-width="3"/><path d="M20 44v12M32 44v8M44 44v12M56 44v8M68 44v12M80 44v8M92 44v12M104 44v8" stroke="#a86703" stroke-width="3"/><circle cx="46" cy="64" r="2.6" fill="#111"/><circle cx="74" cy="64" r="2.6" fill="#111"/><path d="M52 68q8 5 16 0" fill="none" stroke="#111" stroke-width="2.5" stroke-linecap="round"/><text x="60" y="30" text-anchor="middle" font-size="22" font-weight="800" fill="#c4421f">12 ≠ 1</text>',
 'bank': '<rect x="18" y="52" width="84" height="50" fill="#e8eefb" stroke="#1b2d55" stroke-width="3"/><path d="M10 52l50-32 50 32z" fill="#27447f"/><path d="M34 60v36M52 60v36M70 60v36M88 60v36" stroke="#1b2d55" stroke-width="5"/><rect x="12" y="100" width="96" height="9" rx="2" fill="#1b2d55"/><text x="60" y="46" text-anchor="middle" font-size="20" font-weight="800" fill="#ffd37a">%</text>',
 'magnify': '<circle cx="50" cy="50" r="30" fill="#dff5f2" stroke="#1b2d55" stroke-width="6"/><path d="M72 72l30 30" stroke="#1b2d55" stroke-width="10" stroke-linecap="round"/><text x="50" y="60" text-anchor="middle" font-size="30" font-weight="800" fill="#c4421f">?</text>',
})


def ft(cols, target='fv', corner='', r1=1):
    """The course table of five rows (rate, nper, pmt, pv, fv), one column per question or per stage, from column C.
    target: the row that holds the formula, 'fv' (=FV) or 'pmt' (=PMT). A rate written as '=...' is a conversion the student writes inside
    the cell; nper written as '=...' is a period count the student writes; pv written as '=...' is a formula of the solution.
    Returns data, sol, fmt and the target cells."""
    d, s, f, out = {f'A{r1}': corner or 'הנתון', f'B{r1}': 'שם'}, {}, {}, []
    for k, (he, en) in enumerate(FVROWS):
        d[f'A{r1 + 1 + k}'] = he; d[f'B{r1 + 1 + k}'] = en
    for j, c in enumerate(cols):
        L = chr(67 + j)
        d[f'{L}{r1}'] = c['h']
        rr = {k: f'{L}{r1 + 1 + i}' for i, k in enumerate(['rate', 'nper', 'pmt', 'pv', 'fv'])}
        tg = c.get('target', target)
        for k in ('rate', 'nper', 'pmt', 'pv', 'fv'):
            if k == tg: continue
            v = c[k]
            if isinstance(v, str) and v.startswith('=') and (k == 'pv' or k == 'rate' and re.fullmatch(r'=[A-Z]\d+', v)):
                s[rr[k]] = v
            else:
                d[rr[k]] = v
        s[rr[tg]] = {'fv': f"=FV({rr['rate']},{rr['nper']},{rr['pmt']},{rr['pv']})", 'pmt': f"=PMT({rr['rate']},{rr['nper']},{rr['pv']},{rr['fv']})",
                     'nper': f"=NPER({rr['rate']},{rr['pmt']},{rr['pv']},{rr['fv']})", 'rate': f"=RATE({rr['nper']},{rr['pmt']},{rr['pv']},{rr['fv']})"}[tg]
        f[rr['rate']] = 'pct4' if tg == 'rate' or isinstance(c['rate'], str) else _pctf(c['rate'])
        f[rr['pv']] = 'num2'; f[rr['fv']] = 'num2' if tg == 'fv' else 'num0'; f[rr['pmt']] = 'num2' if tg == 'pmt' else 'num0'
        if tg == 'nper': f[rr['nper']] = 'num2'
        out.append(rr[tg])
    return d, s, f, out


def MORE(label, text, cls=''):
    """A dashed link that opens a small explanation over the slide, and closes on a second click. cls: 'left' and/or 'up' place the box."""
    if MODE == 'pdf':
        return f' <span class="morep">({TX(text)})</span>'
    return f'<details class="more {cls}"><summary>{TX(label)}</summary><div class="mb">{TX(text)}</div></details>'


def FNODE(k, q, yes, no):
    return (f'<div class="fnode c{k}"><div class="fnum">{k}</div><div class="fdia">{TX(q)}</div>'
            f'<div class="fy"><b class="tag">כן</b>{TX(yes)}</div><div class="fn"><b class="tag">לא</b>{TX(no)}</div></div>')


def SUMSTOP(sid, part, items, toon=None):
    """An interim stop at the end of a part: what we learned, in plain words."""
    S(sid, f'מה למדנו בחלק {part}', f'עוצרים רגע: מה למדנו בחלק {part}',
      '<ol class="steps">' + ''.join(ST(i + 1, f'<span>{TX(x)}</span>', 'li') for i, x in enumerate(items)) + '</ol>'
      + (TOON(toon[0], toon[1], len(items) + 1) if toon else ''), kick=f'חלק {part} · סיכום ביניים')
