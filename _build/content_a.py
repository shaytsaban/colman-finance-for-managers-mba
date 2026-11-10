# Lesson content, shared by the deck and the summary. Executed with MODE = 'deck' or 'pdf'.
from lib import *
import json, html as _html

COURSE = 'מימון למנהלות ומנהלים'
INST = 'המסלול האקדמי המכללה למנהל · MBA'
SEM = 'סמסטר א׳ תשפ״ז'
LESSON = globals().get('LESSON', 1)
TOTAL_PARTS = {1: 6, 2: 8}[LESSON]
# per lesson: deck title, subtitle, chips, cover line and the next meeting. The first meeting date is not in the source files.
LMETA = {
 1: dict(date='', h1=('מבוא למימון:', 'מטרת הפירמה וערך עתידי'), title='מבוא למימון וערך עתידי',
         sub='למה כסף של היום שווה יותר מכסף של מחר, איך בודקים כדאיות מול האלטרנטיבה, וכמה יצטבר בעתיד, בגיליון.', chip='כל שאלה נפתרת ב-Excel',
         cover='מטרת הפירמה, ערך כפונקציה של תזרים, עיתוי וסיכון, ריבית בפועל וריבית אלטרנטיבית, ריבית דריבית, הפונקציה FV, ריבית משתנה בשלבים, ותרגול עצמי עם גיליון חי.',
         next_h='ערך עתידי של סדרה ומקרים מורכבים', next_t='הפקדה קבועה בכל תקופה והארגומנט pmt, ריבית שמשתנה באמצע סדרה, הפקדות בסכומים משתנים, הפסקה בתשלומים, וחילוץ: כמה להפקיד בכל חודש כדי להגיע ליעד.'),
 2: dict(date='', h1=('ערך עתידי של סדרה', 'ומקרים מורכבים'), title='ערך עתידי של סדרה ומקרים מורכבים',
         sub='הפקדה קבועה בכל תקופה, יעד מאוחר מההפקדה האחרונה, ריבית שמשתנה, הפקדות שמתחלפות, וכמה להפקיד כדי להגיע ליעד.', chip='כל שאלה נפתרת ב-Excel',
         cover='תזכורת למפגש 1, ערך עתידי של סדרה והארגומנט pmt, הארגומנט type, יעד מאוחר מההפקדה האחרונה, מקטעים של ריבית והפקדה, חילוץ ההפקדה בפונקציה PMT, ותרגול עצמי עם גיליון חי.',
         next_h='התאמת ריבית וחילוצים', next_t='ריבית שנתונה ביחידה אחרת מהתשלומים, ריבית נקובה וריבית אפקטיבית, ועוד חילוצים: כמה להפקיד, וכמה זמן לחסוך.')}[LESSON]
XSPECS = []        # every live sheet, in deck order: the practice workbooks are built from these
SL = []            # every slide, in order
CUR = [None]       # current part number
NACT = [0]


def S(sid, title, h, body, kick=None, cls='', kind='slide'):
    SL.append(dict(id=sid, title=title, h=h, body=link_terms(body), kick=kick, cls=cls, kind=kind, part=CUR[0]))


def ST(n, html, tag='div', cls=''):
    return f'<{tag} class="st {cls}" data-n="{n * 10}">{html}</{tag}>'


def DEF(name, text, demo, n=0, trm=None, cls=''):
    """One definition with its small numeric demonstration."""
    hd = f'[[{trm}|{name}]]' if trm else name
    inner = f'<b class="dn">{TX(hd)}</b><p>{TX(text)}</p><div class="demo"><b>דוגמה:</b> {TX(demo)}</div>'
    return ST(n, inner, cls='card def ' + cls) if n else f'<div class="card def {cls}">{inner}</div>'


def BAND(kind, text, n=0):
    lab = {'dg': 'דגש', 'trap': 'המלכודת', 'note': 'הערה'}.get(kind, '')
    inner = (f'<b>{lab}:</b> ' if lab else '') + TX(text)
    return ST(n, inner, cls='band ' + kind) if n else f'<div class="band {kind}">{inner}</div>'


def TABLE(head, rows, cls=''):
    h = ''.join(f'<th>{TX(x)}</th>' for x in head)
    b = ''.join('<tr>' + ''.join(f'<td>{TX(c)}</td>' for c in r) + '</tr>' for r in rows)
    return f'<table class="tbl2 {cls}"><tr>{h}</tr>{b}</table>'


def mc(qid, q, opts, a, why, rot=True):
    # options are written with the right answer first; a fixed rotation per question places it
    r = sum(map(ord, qid)) % len(opts) if rot else 0
    opts = opts[r:] + opts[:r]
    a = (a - r) % len(opts)
    o = ''
    for i, t in enumerate(opts):
        mark = ' correct' if MODE == 'pdf' and i == a else ''
        o += f'<button class="o{mark}" data-i="{i}">{"אבגדה"[i]}. {TX(t)}</button>'
    return f'<div class="mc" data-a="{a}" id="{qid}"><div class="q">{TX(q)}</div>{o}<div class="w"><b>הסבר:</b> {TX(why)}</div></div>'


def MCS(sid, title, h, items):
    S(sid, title, h, f'<div class="mcrow n{len(items)}">' + ''.join(items) + '</div>', kick=f'חלק {CUR[0]} · בדיקת הבנה')


def opener(n, title, q, learn, mins, note='', self=False):
    CUR[0] = n
    SL.append(dict(id=f'p-{n}', title=f'פתיחת חלק {n}: {title}', h=title, kind='opener', part=n, q=q, learn=learn, mins=mins, note=note, self=self, cls='', kick=None, body=''))


def calc(cid, title, h, intro, fields, pdfx):
    if MODE == 'pdf':
        S('c-' + cid, title, h, f'<div class="calcp"><b>מחשבון במצגת.</b> {TX(intro)} <b>דוגמה:</b> {TX(pdfx)}</div>', kind='calcp')
        return
    NACT[0] += 1
    fs = ''.join(f'<label class="cf"><span>{TX(f[1])}</span><input data-k="{f[0]}" value="{f[2]}" dir="ltr" inputmode="decimal" autocomplete="off" spellcheck="false"></label>' for f in fields)
    S('c-' + cid, title, h, f'<div class="calc" data-calc="{cid}"><div class="cin"><p class="cint">{TX(intro)}</p><div class="cfs">{fs}</div></div><div class="cout" id="out-{cid}"></div></div>', kick=f'חלק {CUR[0]} · מחשבון')


def _solitems(items, start=1):
    out, n = [], start
    for it in items:
        if it.startswith('=!'):
            out.append(ST(n, M(it[2:]), cls='eq fit').replace('class="st eq fit"', 'class="st eq fit" dir="ltr"'))
        elif it.startswith('='):
            out.append(ST(n, M(it[1:]), cls='eq').replace('class="st eq"', 'class="st eq" dir="ltr"'))
        else:
            out.append(ST(n, TX(it), 'p', 'sp'))
        n += 1
    return ''.join(out), n


def Q(sid, tag, title, stem, sol, ans, note=None, extra=None):
    """A worked question: the question beside its solution, the solution revealed click by click."""
    note = note or []
    head = f'{tag}: {title}'
    stem_html = ''.join(f'<p>{TX(x)}</p>' for x in stem)
    s1, n = _solitems(sol)
    if MODE == 'pdf':
        b = f'<div class="qstem">{stem_html}</div>{extra or ""}<div class="sol">{s1}</div><div class="band ans"><b>תשובה:</b> {TX(ans)}</div>' + ''.join(BAND(a, t) for a, t in note)
        S(sid, head, head, b, kind='q')
        return
    end = ST(n, f'<b>תשובה:</b> {TX(ans)}', cls='band ans') + ''.join(BAND(a, t, n + 1 + i) for i, (a, t) in enumerate(note))
    body = f'<div class="qg"><div class="qr"><div class="card qstem">{stem_html}</div>{extra or ""}</div><div class="solw">{s1}{end}</div></div>'
    S(sid, head, head, body, kick=f'חלק {CUR[0]} · {tag}', cls='qslide')


def CAP(t):
    return f'<p class="cap">{TX(t)}</p>'


def rcard(n, t, d, m, go):
    return f'<button class="rcard" data-go="{go}"><div class="n">{n}</div><b>{t}</b><span>{TX(d)}</span><em>{m}</em></button>'


def XL(f):
    """An Excel formula. ¤ stands for the dollar sign, which the text markup reserves for math."""
    return f'<code class="xl" dir="ltr">{f}</code>'


# ---------------------------------------------------------------- activities
def _cfg(d):
    return _html.escape(json.dumps(d, ensure_ascii=False), quote=True)


def _bar(*btns):
    return '<div class="actbar">' + ''.join(btns) + '</div>'


CHK = '<button class="abtn chk">בדיקה</button>'
NXT = '<button class="abtn ghost nxt" disabled>המשך</button>'
RST = '<button class="abtn ghost rst">איפוס</button>'


def SORTER(aid, title, h, task, options, rows):
    """Each row gets one right answer out of options. rows: (text, answer index, why)."""
    if MODE == 'pdf':
        t = ''.join(f'<tr><td>{TX(a)}</td><td><b>{options[b]}</b></td><td>{TX(c)}</td></tr>' for a, b, c in rows)
        S(aid, title, h, f'<p>{TX(task)}</p><table class="tbl2"><tr><th>מצב</th><th>תשובה</th><th>נימוק</th></tr>{t}</table>')
        return
    NACT[0] += 1
    r = ''
    for a, b, c in rows:
        bs = ''.join(f'<button class="so" data-i="{i}">{o}</button>' for i, o in enumerate(options))
        r += f'<tr class="srow" data-a="{b}" data-w="{_html.escape(TX(c), quote=True)}"><td>{TX(a)}</td><td>{bs}</td></tr>'
    body = (f'<div class="act sorter" id="{aid}-w"><div class="tasktxt"><b>המשימה:</b> {TX(task)}</div><table class="stbl">{r}</table>'
            f'<div class="fbbar">בחרו תשובה בכל שורה.</div><div class="actbar">{RST}<span class="score">0 / {len(rows)}</span></div></div>')
    S(aid, title, h, body, kick=f'חלק {CUR[0]} · פעילות')


def NUMQ(qid, q, ans, tol, unit, why, hint):
    """A checked numeric question, to place inside a slide body."""
    if MODE == 'pdf':
        return f'<div class="calcp"><b>בדיקה עצמית.</b> {TX(q)} <b>תשובה:</b> <span class="n">{f'{ans:,}'.replace('-', '−')}</span> {TX(unit)}. {TX(why)}</div>'
    NACT[0] += 1
    return (f'<div class="act numq" id="{qid}" data-a="{ans}" data-tol="{tol}" data-w="{_html.escape(TX(why), quote=True)}" data-h="{_html.escape(TX(hint), quote=True)}"><div class="q">{TX(q)}</div>'
            f'<div class="numrow"><input dir="ltr" inputmode="decimal" autocomplete="off" spellcheck="false" aria-label="תשובה"><span>{TX(unit)}</span>{CHK}</div><div class="fbbar">הקלידו מספר ולחצו ״בדיקה״.</div></div>')


def _txc(s):
    return TX(s)


# ---------------------------------------------------------------- cartoons with a punchline
TOONS = {
 'barrel': '<rect x="28" y="20" width="64" height="88" rx="14" fill="#8a5a2b"/><rect x="24" y="38" width="72" height="7" rx="3" fill="#5b3a1a"/><rect x="24" y="84" width="72" height="7" rx="3" fill="#5b3a1a"/><circle cx="48" cy="58" r="6" fill="#fff"/><circle cx="72" cy="58" r="6" fill="#fff"/><circle cx="49" cy="59" r="3" fill="#111"/><circle cx="73" cy="59" r="3" fill="#111"/><path d="M46 72q14 11 28 0" fill="none" stroke="#fff" stroke-width="3.5" stroke-linecap="round"/><path d="M40 20l40 0-6-12-28 0z" fill="#1b2d55"/>',
 'plane': '<path d="M12 62q2-14 22-16l58-4q14 0 18 10-4 10-18 12l-58 4q-20 0-22-6z" fill="#e8eefb" stroke="#1b2d55" stroke-width="3"/><path d="M56 62l-20 34h14l28-36z" fill="#27447f"/><path d="M24 46l-10-22h10l16 20z" fill="#ff6a4d"/><circle cx="88" cy="50" r="5" fill="#111"/><path d="M80 60q8 6 16 1" fill="none" stroke="#111" stroke-width="3" stroke-linecap="round"/><path d="M104 28q6 9 0 13q-6-4 0-13z" fill="#58b8e0"/>',
 'seesaw': '<path d="M60 74l-14 26h28z" fill="#1b2d55"/><line x1="10" y1="88" x2="110" y2="52" stroke="#8a5a2b" stroke-width="7" stroke-linecap="round"/><circle cx="22" cy="68" r="13" fill="#ffd37a"/><circle cx="98" cy="34" r="13" fill="#7fe3d6"/><path d="M16 73q6-6 12 0" fill="none" stroke="#111" stroke-width="2.5"/><path d="M92 36q6 6 12 0" fill="none" stroke="#111" stroke-width="2.5"/><circle cx="18" cy="65" r="2" fill="#111"/><circle cx="26" cy="65" r="2" fill="#111"/><circle cx="94" cy="31" r="2" fill="#111"/><circle cx="102" cy="31" r="2" fill="#111"/>',
 'umbrella': '<path d="M14 58q46-56 92 0z" fill="#ff6a4d"/><line x1="60" y1="58" x2="60" y2="100" stroke="#1b2d55" stroke-width="5"/><path d="M60 100q0 10-10 8" fill="none" stroke="#1b2d55" stroke-width="5" stroke-linecap="round"/><path d="M26 12q4 6 0 9q-4-3 0-9zM60 4q4 6 0 9q-4-3 0-9zM94 12q4 6 0 9q-4-3 0-9z" fill="#58b8e0"/>',
 'lever': '<path d="M46 86l-13 22h26z" fill="#1b2d55"/><line x1="4" y1="50" x2="116" y2="92" stroke="#8a5a2b" stroke-width="6" stroke-linecap="round"/><ellipse cx="18" cy="38" rx="17" ry="15" fill="#8a93aa"/><circle cx="104" cy="74" r="9" fill="#ffd37a" stroke="#a86703" stroke-width="2"/><text x="104" y="79" text-anchor="middle" font-size="20" font-weight="800" fill="#a86703">₪</text>',
 'dice': '<rect x="14" y="30" width="60" height="60" rx="12" fill="#fff" stroke="#1b2d55" stroke-width="4" transform="rotate(-12 44 60)"/><circle cx="32" cy="48" r="5" fill="#ff6a4d"/><circle cx="56" cy="44" r="5" fill="#ff6a4d"/><circle cx="44" cy="62" r="5" fill="#ff6a4d"/><circle cx="34" cy="78" r="5" fill="#ff6a4d"/><circle cx="58" cy="74" r="5" fill="#ff6a4d"/><rect x="66" y="58" width="42" height="42" rx="9" fill="#ffd37a" stroke="#1b2d55" stroke-width="4" transform="rotate(14 87 79)"/><circle cx="87" cy="79" r="5" fill="#1b2d55"/>',
 'sweat': '<circle cx="58" cy="62" r="40" fill="#ffd37a"/><circle cx="44" cy="54" r="5" fill="#111"/><circle cx="72" cy="54" r="5" fill="#111"/><path d="M42 80q16-12 32 0" fill="none" stroke="#111" stroke-width="4" stroke-linecap="round"/><path d="M102 30q8 12 0 17q-8-5 0-17z" fill="#58b8e0"/><text x="16" y="28" font-size="28" font-weight="800" fill="#107c41">$</text>',
 'hands': '<rect x="36" y="14" width="48" height="58" rx="5" fill="#fff" stroke="#1b2d55" stroke-width="3"/><line x1="44" y1="28" x2="76" y2="28" stroke="#8a93aa" stroke-width="3"/><line x1="44" y1="38" x2="76" y2="38" stroke="#8a93aa" stroke-width="3"/><line x1="44" y1="48" x2="66" y2="48" stroke="#8a93aa" stroke-width="3"/><path d="M6 84l30-4 24 12 24-12 30 4v16H6z" fill="#27447f"/><path d="M42 82q18-12 36 0q-6 14-18 14t-18-14z" fill="#ffd37a" stroke="#a86703" stroke-width="2"/>',
 'ref': '<circle cx="60" cy="38" r="26" fill="#ffd37a"/><circle cx="50" cy="34" r="4" fill="#111"/><circle cx="70" cy="34" r="4" fill="#111"/><path d="M48 48q12 8 24 0" fill="none" stroke="#111" stroke-width="3" stroke-linecap="round"/><path d="M26 112q0-46 34-46t34 46z" fill="#fff" stroke="#111" stroke-width="3"/><path d="M42 72v40M60 66v46M78 72v40" stroke="#111" stroke-width="6"/><circle cx="98" cy="52" r="8" fill="#ff6a4d"/>',
 'hourglass': '<path d="M30 14h60v8q0 22-22 38q22 16 22 38v8H30v-8q0-22 22-38Q30 44 30 22z" fill="#eef2ff" stroke="#1b2d55" stroke-width="4"/><path d="M42 26h36q-4 16-18 26q-14-10-18-26z" fill="#ffd37a"/><path d="M38 100q6-22 22-30q16 8 22 30z" fill="#ffd37a"/>',
 'wheat': '<rect x="20" y="56" width="80" height="50" fill="#e8eefb" stroke="#1b2d55" stroke-width="3"/><path d="M14 56l46-30 46 30z" fill="#27447f"/><path d="M36 64v36M60 64v36M84 64v36" stroke="#1b2d55" stroke-width="5"/><path d="M104 12v50M104 22l-9-7M104 22l9-7M104 34l-9-7M104 34l9-7M104 46l-9-7M104 46l9-7" stroke="#e8960c" stroke-width="4" stroke-linecap="round"/>',
 'robot': '<rect x="22" y="26" width="76" height="72" rx="14" fill="#217346"/><text x="60" y="58" text-anchor="middle" font-size="24" font-weight="800" fill="#fff">fx</text><circle cx="44" cy="70" r="6" fill="#fff"/><circle cx="76" cy="70" r="6" fill="#fff"/><circle cx="45" cy="71" r="3" fill="#111"/><circle cx="77" cy="71" r="3" fill="#111"/><path d="M46 84q14 9 28 0" fill="none" stroke="#fff" stroke-width="3.5" stroke-linecap="round"/><line x1="60" y1="26" x2="60" y2="10" stroke="#217346" stroke-width="4"/><circle cx="60" cy="8" r="5" fill="#ff6a4d"/>',
 'voucher': '<rect x="10" y="36" width="100" height="52" rx="8" fill="#fff0d2" stroke="#a86703" stroke-width="3"/><line x1="78" y1="36" x2="78" y2="88" stroke="#a86703" stroke-width="3" stroke-dasharray="4 4"/><path d="M22 62l34-8-6 8 6 8z" fill="#27447f"/><text x="94" y="68" text-anchor="middle" font-size="18" font-weight="800" fill="#a86703">₪</text>',
 'bond': '<rect x="14" y="16" width="92" height="76" rx="8" fill="#fff8e6" stroke="#a86703" stroke-width="3"/><rect x="22" y="24" width="76" height="60" rx="5" fill="none" stroke="#e8c27a" stroke-width="2" stroke-dasharray="4 3"/><text x="60" y="46" text-anchor="middle" font-size="16" font-weight="800" fill="#1b2d55">100 ₪</text><circle cx="46" cy="62" r="4" fill="#111"/><circle cx="74" cy="62" r="4" fill="#111"/><path d="M48 72q12 9 24 0" fill="none" stroke="#111" stroke-width="3" stroke-linecap="round"/><path d="M60 92v18M50 110h20" stroke="#a86703" stroke-width="4" stroke-linecap="round"/>',
 'piggy': '<ellipse cx="58" cy="66" rx="40" ry="30" fill="#ffb3c1"/><circle cx="96" cy="62" r="11" fill="#ff8fa6"/><circle cx="93" cy="60" r="2" fill="#111"/><circle cx="99" cy="60" r="2" fill="#111"/><circle cx="74" cy="52" r="4" fill="#111"/><path d="M40 92v14M72 92v14" stroke="#ff8fa6" stroke-width="8" stroke-linecap="round"/><rect x="46" y="34" width="22" height="5" rx="2" fill="#7a2a3a"/><circle cx="57" cy="16" r="11" fill="#ffd37a" stroke="#a86703" stroke-width="2"/><text x="57" y="22" text-anchor="middle" font-size="17" font-weight="800" fill="#a86703">₪</text>',
 'clock': '<circle cx="60" cy="62" r="42" fill="#fff" stroke="#1b2d55" stroke-width="5"/><path d="M60 62V34M60 62l18 12" stroke="#ff6a4d" stroke-width="5" stroke-linecap="round"/><circle cx="60" cy="62" r="5" fill="#1b2d55"/><path d="M28 18l-12 12M92 18l12 12" stroke="#1b2d55" stroke-width="6" stroke-linecap="round"/><circle cx="44" cy="84" r="3" fill="#111"/><circle cx="76" cy="84" r="3" fill="#111"/>',
 'stairs': '<path d="M10 104h100v-16H86V70H62V52H38V34H14z" fill="#7fe3d6" stroke="#0f9d90" stroke-width="3"/><circle cx="26" cy="22" r="9" fill="#ffd37a"/><path d="M26 31v14M26 36l-8 6M26 36l8 6" stroke="#1b2d55" stroke-width="3" stroke-linecap="round"/><text x="98" y="62" text-anchor="middle" font-size="18" font-weight="800" fill="#c4421f">₪</text>',
 'scale': '<path d="M60 18v74M30 104h60" stroke="#1b2d55" stroke-width="5" stroke-linecap="round"/><path d="M16 40l88-10" stroke="#8a5a2b" stroke-width="5" stroke-linecap="round"/><path d="M16 40l-10 24h20zM104 30l-10 24h20z" fill="#ffd37a" stroke="#a86703" stroke-width="2"/><text x="16" y="80" text-anchor="middle" font-size="15" font-weight="800" fill="#1b2d55">r</text><text x="104" y="70" text-anchor="middle" font-size="15" font-weight="800" fill="#1b2d55">c</text><circle cx="60" cy="16" r="6" fill="#ff6a4d"/>',
 'calc': '<rect x="26" y="10" width="68" height="100" rx="10" fill="#1b2d55"/><rect x="34" y="18" width="52" height="22" rx="4" fill="#dff5f2"/><text x="82" y="35" text-anchor="end" font-size="15" font-weight="800" fill="#1b2d55">90.47</text><g fill="#fff"><rect x="34" y="48" width="14" height="12" rx="3"/><rect x="53" y="48" width="14" height="12" rx="3"/><rect x="72" y="48" width="14" height="12" rx="3"/><rect x="34" y="66" width="14" height="12" rx="3"/><rect x="53" y="66" width="14" height="12" rx="3"/><rect x="34" y="84" width="14" height="12" rx="3"/><rect x="53" y="84" width="14" height="12" rx="3"/></g><rect x="72" y="66" width="14" height="30" rx="3" fill="#ff6a4d"/>',

 'wait': '<path d="M30 14h44v6q0 18-16 28q16 10 16 28v6H30v-6q0-18 16-28Q30 38 30 20z" fill="#eef2ff" stroke="#1b2d55" stroke-width="4"/><path d="M40 24h24q-3 11-12 18q-9-7-12-18z" fill="#ffd37a"/><path d="M38 76q4-14 14-19q10 5 14 19z" fill="#ffd37a"/><path d="M80 10l30 0M84 10l10 16M92 10l12 22M100 10l8 12" stroke="#8a93aa" stroke-width="1.5"/><circle cx="96" cy="64" r="14" fill="#fff" stroke="#1b2d55" stroke-width="3"/><circle cx="91" cy="62" r="2.4" fill="#111"/><circle cx="101" cy="62" r="2.4" fill="#111"/><path d="M90 71h12" stroke="#111" stroke-width="2.5" stroke-linecap="round"/><path d="M96 78v22M96 86l-10 6M96 86l10 6M96 100l-8 14M96 100l8 14" stroke="#1b2d55" stroke-width="3" stroke-linecap="round"/>',
 'happy': '<circle cx="60" cy="54" r="34" fill="#ffd37a"/><circle cx="48" cy="46" r="4.5" fill="#111"/><circle cx="72" cy="46" r="4.5" fill="#111"/><path d="M42 62q18 18 36 0" fill="#fff" stroke="#111" stroke-width="3.5" stroke-linecap="round"/><path d="M60 88v18M44 110h32" stroke="#a86703" stroke-width="4" stroke-linecap="round"/><text x="100" y="30" text-anchor="middle" font-size="22" font-weight="800" fill="#107c41">₪</text>',
 'house': '<path d="M14 62l46-36 46 36v46H14z" fill="#e8eefb" stroke="#1b2d55" stroke-width="3"/><path d="M8 64l52-42 52 42" fill="none" stroke="#c4421f" stroke-width="6" stroke-linecap="round"/><rect x="48" y="78" width="24" height="30" fill="#8a5a2b"/><rect x="24" y="72" width="16" height="14" fill="#7fe3d6"/><rect x="80" y="72" width="16" height="14" fill="#7fe3d6"/><text x="60" y="60" text-anchor="middle" font-size="24" font-weight="800" fill="#c4421f">1%</text>',
 'market': '<rect x="14" y="70" width="18" height="34" fill="#8a93aa"/><rect x="40" y="56" width="18" height="48" fill="#5d6a86"/><rect x="66" y="40" width="18" height="64" fill="#0f9d90"/><rect x="92" y="22" width="18" height="82" fill="#25a65f"/><line x1="8" y1="106" x2="116" y2="106" stroke="#1b2d55" stroke-width="4"/><text x="44" y="30" text-anchor="middle" font-size="26" font-weight="800" fill="#1b2d55">3.5%</text>',
 'mirror': '<circle cx="28" cy="44" r="16" fill="#ffd37a"/><circle cx="23" cy="41" r="2.4" fill="#111"/><circle cx="33" cy="41" r="2.4" fill="#111"/><path d="M22 50q6 5 12 0" fill="none" stroke="#111" stroke-width="2.5"/><path d="M28 60v28M28 68l-10 8M28 68l10 8" stroke="#1b2d55" stroke-width="3.5" stroke-linecap="round"/><rect x="74" y="34" width="40" height="56" fill="#e8eefb" stroke="#1b2d55" stroke-width="3"/><path d="M70 34l24-16 24 16z" fill="#27447f"/><path d="M82 46v36M94 46v36M106 46v36" stroke="#1b2d55" stroke-width="3"/><path d="M46 46h22" stroke="#25a65f" stroke-width="4"/><path d="M62 40l8 6-8 6" fill="none" stroke="#25a65f" stroke-width="4"/><path d="M70 74H48" stroke="#c4421f" stroke-width="4"/><path d="M54 68l-8 6 8 6" fill="none" stroke="#c4421f" stroke-width="4"/><text x="57" y="36" text-anchor="middle" font-size="22" font-weight="800" fill="#25a65f">+</text><text x="58" y="100" text-anchor="middle" font-size="24" font-weight="800" fill="#c4421f">−</text>',

 'coin1': '<circle cx="60" cy="62" r="34" fill="#ffd37a" stroke="#a86703" stroke-width="3"/><circle cx="48.1" cy="56.9" r="4.4" fill="#111"/><circle cx="71.9" cy="56.9" r="4.4" fill="#111"/><path d="M46.4 70.5q13.6 11.9 27.2 0" fill="none" stroke="#111" stroke-width="2.5" stroke-linecap="round"/>',
 'coins': '<circle cx="30" cy="78" r="20" fill="#ffd37a" stroke="#a86703" stroke-width="3"/><circle cx="23.0" cy="75.0" r="2.6" fill="#111"/><circle cx="37.0" cy="75.0" r="2.6" fill="#111"/><path d="M22.0 83.0q8.0 7.0 16.0 0" fill="none" stroke="#111" stroke-width="2.5" stroke-linecap="round"/><circle cx="90" cy="78" r="20" fill="#ffd37a" stroke="#a86703" stroke-width="3"/><circle cx="83.0" cy="75.0" r="2.6" fill="#111"/><circle cx="97.0" cy="75.0" r="2.6" fill="#111"/><path d="M82.0 83.0q8.0 7.0 16.0 0" fill="none" stroke="#111" stroke-width="2.5" stroke-linecap="round"/><circle cx="60" cy="46" r="28" fill="#ffd37a" stroke="#a86703" stroke-width="3"/><circle cx="50.2" cy="41.8" r="3.6" fill="#111"/><circle cx="69.8" cy="41.8" r="3.6" fill="#111"/><path d="M48.8 53.0q11.2 9.8 22.4 0" fill="none" stroke="#111" stroke-width="2.5" stroke-linecap="round"/><path d="M8 30l8 6M112 30l-8 6M60 6v8" stroke="#ff6a4d" stroke-width="4" stroke-linecap="round"/>',
 'nocalc': '<rect x="30" y="12" width="60" height="92" rx="9" fill="#1b2d55"/><rect x="38" y="20" width="44" height="20" rx="3" fill="#dff5f2"/><g fill="#fff"><rect x="38" y="48" width="12" height="11" rx="2"/><rect x="54" y="48" width="12" height="11" rx="2"/><rect x="70" y="48" width="12" height="11" rx="2"/><rect x="38" y="64" width="12" height="11" rx="2"/><rect x="54" y="64" width="12" height="11" rx="2"/><rect x="70" y="64" width="12" height="11" rx="2"/></g><path d="M14 18L106 106M106 18L14 106" stroke="#e5484d" stroke-width="10" stroke-linecap="round"/>',
 'shrug': '<circle cx="60" cy="36" r="20" fill="#ffd37a"/><circle cx="53.0" cy="33.0" r="2.6" fill="#111"/><circle cx="67.0" cy="33.0" r="2.6" fill="#111"/><path d="M53.0 45.0q7.0 -6.0 14.0 0" fill="none" stroke="#111" stroke-width="2.5" stroke-linecap="round"/><path d="M60 56v32M60 88l-14 22M60 88l14 22M60 64q-20 -2 -32 -16M60 64q20 -2 32 -16" stroke="#1b2d55" stroke-width="5" stroke-linecap="round" fill="none"/><text x="96" y="26" font-size="30" font-weight="800" fill="#ff6a4d">?</text><text x="14" y="26" font-size="30" font-weight="800" fill="#ff6a4d">?</text>',
 'giantcoin': '<circle cx="60" cy="60" r="52" fill="#ffd37a" stroke="#a86703" stroke-width="3"/><circle cx="41.8" cy="52.2" r="6.8" fill="#111"/><circle cx="78.2" cy="52.2" r="6.8" fill="#111"/><path d="M39.2 73.0q20.8 18.2 41.6 0" fill="none" stroke="#111" stroke-width="2.5" stroke-linecap="round"/>',
 'tinycoin': '<circle cx="60" cy="84" r="13" fill="#ffd37a" stroke="#a86703" stroke-width="3"/><circle cx="55.5" cy="82.0" r="1.7" fill="#111"/><circle cx="64.5" cy="82.0" r="1.7" fill="#111"/><path d="M54.8 87.2q5.2 4.5 10.4 0" fill="none" stroke="#111" stroke-width="2.5" stroke-linecap="round"/><path d="M24 30h72" stroke="#d9d2c3" stroke-width="3" stroke-dasharray="6 6"/>',
 'sleep': '<circle cx="60" cy="66" r="32" fill="#ffd37a" stroke="#a86703" stroke-width="3"/><path d="M48.8 80.4q11.2 -9.6 22.4 0" fill="none" stroke="#111" stroke-width="2.5" stroke-linecap="round"/><path d="M40 60h12M68 60h12" stroke="#111" stroke-width="3" stroke-linecap="round"/><text x="84" y="34" font-size="26" font-weight="800" fill="#5d6a86">z</text><text x="100" y="18" font-size="24" font-weight="800" fill="#5d6a86">z</text>',
 'mailbox': '<rect x="20" y="34" width="62" height="40" rx="18" fill="#e5484d"/><rect x="48" y="74" width="8" height="38" fill="#8a5a2b"/><rect x="82" y="30" width="5" height="26" fill="#1b2d55"/><rect x="82" y="30" width="18" height="12" fill="#ffd37a"/><text x="51" y="63" text-anchor="middle" font-size="28" font-weight="800" fill="#fff">%</text>',
}


def TOON(key, punch, n=0):
    """A small cartoon with a punchline, in the empty corner of a slide."""
    svg = f'<svg viewBox="0 0 120 120" dir="ltr" role="img" aria-hidden="true">{TOONS[key]}</svg>'
    return ST(n, f'{svg}<div class="bub">{TX(punch)}</div>', cls='toon') if n else f'<div class="toon">{svg}<div class="bub">{TX(punch)}</div></div>'


# ---------------------------------------------------------------- memes and animations, drawn here (no outside images)
def _svg(inner, vb='0 0 120 120', cls=''):
    return f'<svg viewBox="{vb}" dir="ltr" class="{cls}" role="img" aria-hidden="true">{inner}</svg>'


def MEME(title, panels, n=0, cls=''):
    """An original two panel meme: each panel is (svg inner or TOONS key, caption). The punchline is the contrast."""
    if MODE == 'pdf':
        return ''
    ps = ''
    for k, (art, cap) in enumerate(panels):
        art = TOONS.get(art, art)
        ps += f'<div class="mp"><div class="mart">{_svg(art)}</div><div class="mcap">{TX(cap)}</div></div>'
    inner = f'<div class="mt">{TX(title)}</div><div class="mps">{ps}</div>'
    return ST(n, inner, cls='meme ' + cls) if n else f'<div class="meme {cls}">{inner}</div>'


def SNOWBALL(n=0):
    """Compound interest as a snowball: it rolls down the years and grows, because last year's interest starts to earn too."""
    if MODE == 'pdf':
        return ''
    g = ('<path d="M10 40 L470 150" stroke="#c9d6ee" stroke-width="10" stroke-linecap="round"/>'
         + ''.join(f'<g><line x1="{30 + 105 * i}" y1="{45 + 24 * i}" x2="{30 + 105 * i}" y2="{62 + 24 * i}" stroke="#8a93aa" stroke-width="2"/><text x="{30 + 105 * i}" y="{78 + 24 * i}" font-size="15" text-anchor="middle" fill="#5d6a86" font-weight="700" direction="rtl">שנה {i}</text></g>' for i in range(5))
         + ''.join(f'<circle cx="{30 + 105 * i}" cy="{40 + (20 + 105 * i) * 110 / 460 - r - 6:.1f}" r="{r}" fill="#eaf6fd" stroke="#b9def2" stroke-width="2"/>' for i, r in enumerate([9, 11, 14, 18, 23]))
         + '<g class="sb-roll"><circle class="sb-ball" cx="0" cy="0" r="16" fill="#fff" stroke="#58b8e0" stroke-width="3"/><path class="sb-ball" d="M-8 -4q8 -8 16 0" fill="none" stroke="#58b8e0" stroke-width="2"/><text class="sb-lab" x="0" y="5" font-size="12" text-anchor="middle" font-weight="800" fill="#1b2d55">₪</text></g>')
    inner = _svg(g, '0 0 480 190', 'snow') + '<div class="anim-cap">' + TX('בכל שנה כל הכדור, קרן וריבית, צובר ריבית חדשה. לכן הוא גדל מהר יותר ויותר.') + '</div>'
    return ST(n, inner, cls='card animw') if n else f'<div class="card animw">{inner}</div>'


def RELAY(n=0):
    """The multi-stage rule as a relay race: the FV of one stage is handed to the next one as its pv, with the sign flipped."""
    if MODE == 'pdf':
        return ''
    run = lambda x, c: (f'<g transform="translate({x} 0)"><circle cx="0" cy="40" r="13" fill="{c}"/><path d="M0 53v34M0 64l-16 12M0 64l18 -6M0 87l-14 24M0 87l16 22" stroke="#1b2d55" stroke-width="5" stroke-linecap="round"/></g>')
    g = (run(110, '#ffd37a') + run(330, '#7fe3d6')
         + '<line x1="20" y1="122" x2="460" y2="122" stroke="#d9d2c3" stroke-width="4" stroke-dasharray="10 8"/>'
         + '<text x="110" y="18" font-size="16" text-anchor="middle" font-weight="800" fill="#1b2d55" direction="rtl">שלב 1: 5%</text><text x="330" y="18" font-size="16" text-anchor="middle" font-weight="800" fill="#1b2d55" direction="rtl">שלב 2: 7%</text>'
         + '<g class="baton"><rect x="-26" y="-11" width="52" height="22" rx="8" fill="#ff6a4d"/><text class="bt1" x="0" y="5" font-size="13" text-anchor="middle" font-weight="800" fill="#fff">FV</text><text class="bt2" x="0" y="5" font-size="13" text-anchor="middle" font-weight="800" fill="#fff">pv = −FV</text></g>')
    inner = _svg(g, '0 0 480 135', 'relay') + '<div class="anim-cap">' + TX('המקל עובר: הסכום שנצבר בסוף שלב 1 נכנס ל-pv של שלב 2, בסימן הפוך.') + '</div>'
    return ST(n, inner, cls='card animw') if n else f'<div class="card animw">{inner}</div>'


def JAR(n=0):
    """A series as coins that drop into a jar every period, while the jar itself keeps growing."""
    if MODE == 'pdf':
        return ''
    coins = ''.join(f'<g class="coin c{i}"><circle cx="0" cy="0" r="11" fill="#ffd37a" stroke="#a86703" stroke-width="2.5"/><text x="0" y="5" font-size="12" text-anchor="middle" font-weight="800" fill="#a86703">₪</text></g>' for i in range(4))
    g = ('<path d="M150 50h100v14q14 6 14 22v74q0 16-16 16h-96q-16 0-16-16V86q0-16 14-22z" fill="#eef7f6" stroke="#0f9d90" stroke-width="4"/>'
         + '<rect class="jfill" x="140" y="110" width="120" height="62" fill="#7fe3d6" opacity=".75"/>'
         + coins + '<text x="440" y="80" font-size="17" font-weight="800" fill="#1b2d55" direction="rtl">pmt בכל חודש</text><text x="440" y="140" font-size="17" font-weight="800" fill="#0f9d90" direction="rtl">והכול צובר ריבית</text>')
    inner = _svg(g, '0 0 480 185', 'jar') + '<div class="anim-cap">' + TX('סדרה: אותו סכום נכנס בכל תקופה, וכל מה שכבר בפנים ממשיך לצבור ריבית.') + '</div>'
    return ST(n, inner, cls='card animw') if n else f'<div class="card animw">{inner}</div>'


# ---------------------------------------------------------------- embedded Excel
import fin as _fin


def xl_eval(data, sol):
    """Evaluate the solution in Python (fin.py): used in the PDF, and as an independent check of each exercise."""
    v, _ = _fin.evaluate({**data, **sol})
    return v


def _fmtx(v, f=''):
    """A cell value as the sheet shows it. f: pct0..pct6, num0..num6 or '' (up to 2 decimals)."""
    if isinstance(v, str): return v
    if v is None: return ''
    m = re.fullmatch(r'(pct|num)(\d)', f or '')
    if m:
        d = int(m.group(2)); x = v * 100 if m.group(1) == 'pct' else v
        t = f'{x:,.{d}f}' + ('%' if m.group(1) == 'pct' else '')
    else:
        x = round(v, 2); t = f'{x:,.2f}'.rstrip('0').rstrip('.') if x != int(x) else f'{int(x):,}'
    return t.replace('-', '−')


_ARGN = {'PV': ['rate', 'nper', 'pmt', 'fv', 'type'], 'FV': ['rate', 'nper', 'pmt', 'pv', 'type'], 'PMT': ['rate', 'nper', 'pv', 'fv', 'type'],
         'NPER': ['rate', 'pmt', 'pv', 'fv', 'type'], 'RATE': ['nper', 'pmt', 'pv', 'fv', 'type'], 'NPV': ['rate']}


def _argnames(data, sol, head):
    """Shay, 2026-11-03: beside the Hebrew label, the English name of the argument it feeds (rate, nper, pmt, pv, fv),
    so the order of the arguments is visible where the student points. Read from the solution's function calls."""
    names = {}
    for f in sol.values():
        if not str(f).startswith('='): continue
        for m in re.finditer(r'\b(PV|FV|PMT|NPER|RATE|NPV)\(', f):
            i, depth, args, cur = m.end(), 1, [], ''
            while i < len(f) and depth:
                ch = f[i]
                if ch == '(': depth += 1
                elif ch == ')':
                    depth -= 1
                    if not depth: break
                if ch == ',' and depth == 1: args.append(cur); cur = ''
                else: cur += ch
                i += 1
            args.append(cur)
            for k, a in enumerate(args):
                r = re.fullmatch(r'\$?([A-Z]+)\$?(\d+)', a.strip())
                if r and k < len(_ARGN[m.group(1)]):
                    names.setdefault(r.group(1) + r.group(2), _ARGN[m.group(1)][k])
    for cell, nm in names.items():
        col, row = re.match(r'([A-Z]+)(\d+)', cell).groups(); row = int(row)
        # the label of the row (a text cell to its right in the sheet, so a lower column letter), or else the header of its column
        lab = [a for a in data if re.fullmatch(r'[A-Z]+' + str(row), a) and isinstance(data[a], str) and not data[a].startswith('=') and a[0] < col]
        if not lab:
            lab = [a for a in data if a[0] == col and isinstance(data[a], str) and int(re.sub('[A-Z]', '', a)) < row and int(re.sub('[A-Z]', '', a)) in head]
        if not lab: continue
        rowtxt = ' '.join(str(data[a]) for a in data if re.fullmatch(r'[A-Z]+' + str(row), a) and isinstance(data[a], str))
        a = lab[0]
        # nper is the number of payments in the series, never 'years': the label says so
        if nm == 'nper' and re.fullmatch(r'(מספר )?שנים|שנה', str(data[a]).strip()):
            data[a] = 'מספר תשלומים'
        if re.search(r'\b' + nm + r'\b', rowtxt) or re.search(r'\b' + nm + r'\b', str(data[a])) or '(' in str(data[a]): continue
        data[a] = f'{data[a]} ({nm})'
    # by role, on every sheet (Shay, 2026-11-03): the Excel name of each parameter beside its Hebrew label
    labels = {a: v for a, v in data.items() if isinstance(v, str) and not v.startswith('=') and int(re.sub('[A-Z]', '', a)) not in head}
    amort = any(re.search(r'יתר[הת]', str(v)) for v in data.values())
    for a, v in labels.items():
        t = v.strip()
        if '(' in t: continue
        if re.fullmatch(r'מספר תשלומים', t): data[a] = t + ' (nper)'
        elif not amort and re.fullmatch(r'ערך נקוב', t): data[a] = t + ' (fv)'
        elif not amort and re.fullmatch(r'קופון( שנתי| לחצי שנה| לרבעון| לתשלום)?', t): data[a] = t + ' (pmt)'
    return data


ROLE = {'rate': 'הריבית לתקופה אחת. בסדרה: לתקופת התשלום', 'nper': 'מספר התקופות. בסדרה: מספר התשלומים', 'pmt': 'התשלום הקבוע בכל תקופה',
        'pv': 'הסכום החד פעמי בתחילת השלב', 'fv': 'הערך העתידי'}


def _one_cell_steps(data, inputs, given_f, steps, head, fmt):
    """Shay, 2026-11-10: ״צעד אחר צעד״ must really be one step at a time. Every click writes one cell: first each number of the question,
    in the order of the table, with what the cell means; then each formula. A written step that fills several cells is split, and its
    note stays on its last cell."""
    typed = {**inputs, **given_f}
    def rc(a):
        m = re.match(r'([A-Z]+)(\d+)', a); return m.group(1), int(m.group(2))
    def text(a):
        v = data.get(a); return v if isinstance(v, str) and not v.startswith('=') else ''
    def num(a):
        r = typed.get(a, '')
        try: return float(r[:-1]) / 100 if r.endswith('%') else float(r)
        except ValueError: return None
    multi = len({rc(a)[0] for a in typed if rc(a)[0] > 'B'}) > 1
    def label(a):
        col, row = rc(a)
        name = text(f'B{row}') if col > 'B' else ''
        lab = text(f'A{row}') if col > 'A' else ''
        hd = [text(f'{col}{h}') for h in head if h < row and text(f'{col}{h}')]
        if not lab: return (hd[-1] if hd else a), ''
        lab = re.sub(r'\s*\((rate|nper|pmt|pv|fv)\)$', '', lab)
        return (f'{hd[-1]}, {lab}' if hd and multi and name in ROLE else lab), (name if name in ROLE else '')
    def has_pmt(a):
        col, row = rc(a)
        pr = [r for r in range(1, 40) if text(f'B{r}') == 'pmt']
        v = num(f'{col}{pr[0]}') if pr else None
        return bool(v)
    def note_in(a):
        lab, name = label(a); raw = typed[a]; v = num(a)
        t = f'<b>{lab}' + (f' ({name})' if name else '') + ':</b> כותבים ' + XL(raw) + '.'
        if name == 'pmt': t += ' אין הפקדה קבועה בשלב הזה.' if v == 0 else (' ההפקדה הקבועה. הכסף יוצא, ולכן במינוס.' if v is not None and v < 0 else ' תשלום קבוע שמתקבל: בפלוס.')
        elif name == 'pv': t += ' אין סכום חד פעמי בתחילת הדרך.' if v == 0 else (' סכום חד פעמי שמופקד: הכסף יוצא, ולכן במינוס.' if v is not None and v < 0 else ' סכום שמתקבל היום: בפלוס.')
        elif name == 'rate': t += (' יש הפקדות, ולכן זו הריבית לתקופת תשלום.' if has_pmt(a) else ' הריבית הנתונה, לתקופה אחת.') + ' אחוזים כותבים עם סימן האחוז.'
        elif name == 'nper': t += (' יש הפקדות, ולכן זה מספר ההפקדות.' if has_pmt(a) else ' מספר תקופות הריבית, באותה יחידה כמו rate.') + (' ההמרה נכתבת כנוסחה.' if a in given_f else '')
        elif name == 'fv': t += ' הסכום העתידי נתון הפעם.'
        return t
    def note_f(a, f):
        lab, name = label(a)
        if re.fullmatch(r'=-[A-Z]+\d+', f): return f'<b>{lab}' + (f' ({name})' if name else '') + ':</b> ' + XL(f) + '. ה-FV של השלב הקודם נכנס לכאן בסימן הפוך: הוא שוב הפקדה.'
        return f'<b>{lab}:</b> כותבים ' + XL(f.replace('$', '¤')) + '.'
    out, done = [], set()
    order = sorted(typed, key=lambda a: (rc(a)[0], rc(a)[1]))
    def enter(pred):
        for a in order:
            if a not in done and pred(a):
                done.add(a); out.append(dict(cells={a: typed[a]}, note=note_in(a), sel=a))
    for st in steps:
        cols = {rc(a)[0] for a in st['cells']}
        refs = set(re.findall(r'\$?([A-Z]{1,2})\$?(\d+)', ' '.join(str(f) for f in st['cells'].values())))
        need = {c + r for c, r in refs}
        # ranges (D2:D4) count too
        for c1, r1, c2, r2 in re.findall(r'([A-Z])(\d+):([A-Z])(\d+)', ' '.join(str(f) for f in st['cells'].values())):
            need |= {chr(c) + str(r) for c in range(ord(c1), ord(c2) + 1) for r in range(int(r1), int(r2) + 1)}
        enter(lambda a: rc(a)[0] in cols and rc(a)[0] > 'B' and text(f'B{rc(a)[1]}') in ROLE or a in need)
        ks = list(st['cells'])
        if st.get('sel2'):           # one formula dragged over a range stays one step: that is how it is done in Excel
            out.append(st); continue
        for k in ks[:-1]:
            out.append(dict(cells={k: st['cells'][k]}, note=note_f(k, str(st['cells'][k])), sel=k))
        out.append(dict(cells={ks[-1]: st['cells'][ks[-1]]}, note=st['note'], sel=ks[-1]))
    if len(done) < len(order):   # a number no formula step asked for: entered first
        rest = [dict(cells={a: typed[a]}, note=note_in(a), sel=a) for a in order if a not in done]
        out = rest + out
    return out


def _xsheet(sid, task, data, sol, widths, head, rows=None, cols=None, hints=None, remind=None, partial=None, chart=None, values=False, done='', extra='',
            fmt=None, traps=None, allow=None, r0=1, maxh=None, tol=None, need=None, needMsg=None, xname=None, xtitle=None, steps=None, side=False, title='', signMsg=None, qtext=None, build=None):
    """The live sheet itself. side=True: the sheet sits beside a question, and its feedback goes under the question (an element .xfb)."""
    fmt = fmt or {}
    # Shay, 2026-11-03: the sheet holds no number of the solution. Every number of the question (and every period number) is typed by the student,
    # and every given formula is written by the student. Only text labels stay as the structure of the table.
    def _raw(a, v):
        if isinstance(v, float) and re.fullmatch(r'pct\d', fmt.get(a, '') or ''):
            return f'{round(v * 100, 10):.12g}%'
        return f'{v:.15g}' if isinstance(v, float) else str(v)
    inputs = {a: _raw(a, v) for a, v in data.items() if isinstance(v, (int, float)) and not isinstance(v, bool)}
    given_f = {a: v for a, v in data.items() if isinstance(v, str) and v.startswith('=')}
    for a, v in data.items():
        if a in inputs:
            r = inputs[a]; back = float(r[:-1]) / 100 if r.endswith('%') else float(r)
            assert abs(back - v) <= 1e-12 * max(1, abs(v)), (sid, a, v, r)
    data = {a: v for a, v in data.items() if a not in inputs and a not in given_f}
    sol = {**inputs, **given_f, **sol}
    data = _argnames(dict(data), sol, head)
    if steps and MODE == 'deck':
        steps = _one_cell_steps(data, inputs, given_f, steps, head, fmt)
    elif steps:   # the summary keeps the short form: the data, the period conversions, then each formula
        steps = ([dict(cells=dict(inputs), note='מזינים את נתוני השאלה בתאים, כפי שהם כתובים בשאלה. אחוזים כותבים עם סימן האחוז.', sel=next(iter(inputs)))] if inputs else []) + \
                ([dict(cells=dict(given_f), note='התאמות לתקופה: ' + ' '.join(f'{a}: {f}' for a, f in given_f.items()))] if given_f else []) + steps
    partial = list(inputs) + list(given_f) + list(partial or [a for a in sol if a not in inputs and a not in given_f][:1])
    vals = xl_eval(data, sol)
    targets = list(sol)
    rs = rows or max(int(re.sub('[A-Z]', '', a)) for a in list(data) + targets)
    cs = cols or max(ord(a[0]) - 64 for a in list(data) + targets)
    for st in steps or []:
        assert all(st['cells'][a] == sol[a] for a in st['cells']), (sid, 'a step must write the solution formula')
    if steps: assert set().union(*[set(st['cells']) for st in steps]) == set(sol), (sid, 'the steps must cover every target')
    XSPECS.append(dict(qtext=qtext or task, vin=list(inputs), sid=sid, name=xname or sid, title=xtitle or re.sub('<[^>]+>', '', title), task=re.sub('<[^>]+>', '', task).replace('¤', '$'), data=data, sol=sol, fmt=fmt, widths=widths, head=head, rows=rs, cols=cs, r0=r0, vals=vals, part=CUR[0]))
    if MODE == 'pdf':
        L = [chr(65 + i) for i in range(cs)]
        t = ''
        for r in range(r0, rs + 1):
            cells = []
            for c in L:
                a = f'{c}{r}'
                x = vals.get(a) if (a in sol or str(data.get(a, '')).startswith('=')) else data.get(a, '')
                cells.append(_fmtx(x, fmt.get(a, '')) if not isinstance(x, str) else x)
            if any(cells):
                tag = 'th' if r in head else 'td'
                t += f'<tr><td class="rn">{r}</td>' + ''.join(f'<{tag}>{TX(x)}</{tag}>' for x in cells) + '</tr>'
        hdr = '<tr><th class="rn"></th>' + ''.join(f'<th>{c}</th>' for c in L) + '</tr>'
        if steps:
            fm = '<ol class="xsteps">' + ''.join(f'<li>{TX(FXW(st["note"]))} ' + ' '.join(f'<span class="fx"><b>{a}</b> ' + XL(st['cells'][a].replace('$', '¤')) + '</span>' for a in _repr_targets(st['cells'])) + '</li>' for st in steps) + '</ol>'
        else:
            fm = '<p class="fml">' + ' '.join(f'<span class="fx"><b>{a}</b> ' + XL(sol[a].replace('$', '¤')) + '</span>' for a in _repr_targets(sol)) + '</p>'
        return f'<p class="qstem">{TX(task)}</p><table class="tbl2 xlp">{hdr}{t}</table>{fm}'
    NACT[0] += 1
    # Shay, 2026-11-10: use the screen. The live sheet shows spare empty rows and columns, as a full Excel window does; the slide fit
    # caps its height to the free space, and scrolling reaches the spare rows. The spec (and the workbooks) keep the real size.
    real_w = sum(widths) + max(0, cs - len(widths)) * 92
    pad_c = max(0, int(((560 if side else 760) - real_w - 50) // 80))
    widths = list(widths) + [92] * max(0, cs - len(widths)) + [80] * pad_c
    cfgd = dict(rows=rs + 14, cols=cs + pad_c, widths=widths, data={k: str(v) for k, v in data.items()}, targets=targets, solution=sol, headRows=head, inputs=[], fmt=fmt, solFmt=fmt,
                hints=[TX(FXW(x)) for x in (hints or ['קראו שוב את כותרת העמודה, וכתבו את החישוב במילים לפני הנוסחה.'])], remind=TX(FXW(remind or '')), partial=partial or targets[:1], values=values, done=TX(FXW(done)))
    if not remind: cfgd.pop('remind')
    if traps: cfgd['traps'] = {a: [[f, TX(FXW(m))] for f, m in L] for a, L in traps.items()}
    if allow is not None: cfgd['allow'] = allow
    if r0 > 1: cfgd['r0'] = r0
    cfgd['maxh'] = maxh or 2000   # the real height is fitted to the slide at runtime
    if tol is not None: cfgd['tol'] = tol
    if signMsg: cfgd['signMsg'] = TX(signMsg)
    if inputs: cfgd['vin'] = list(inputs)
    if build:
        # the label cells of each group are held back, and appear one group per click
        bc = [a for cells, _ in build for a in cells]
        assert all(a in data for a in bc), (sid, 'a build cell must be a label')
        cfgd['bdata'] = {a: data[a] for a in bc}
        cfgd['data'] = {k: v for k, v in cfgd['data'].items() if k not in bc}
        cfgd['build'] = [dict(cells=cells, note=TX(FXW(note))) for cells, note in build]
    if need: cfgd['need'] = need; cfgd['needMsg'] = needMsg or ''
    if steps: cfgd['steps'] = [dict(cells=st['cells'], note=TX(FXW(st['note'])), **({'sel': st['sel']} if st.get('sel') else {}), **({'sel2': st['sel2']} if st.get('sel2') else {})) for st in steps]
    sv = ''
    if chart:
        cfgd['chart'] = chart
        sv = f'<svg class="xlc" viewBox="0 0 {chart.get("W", 470)} {chart.get("H", 330)}" role="img" aria-label="תרשים"></svg>'
    if side:
        return cfgd, f'<div class="tasktxt sm">{TX(task)}</div><div class="sheet"></div>{extra}'
    return cfgd, f'<div class="tasktxt">{TX(task)}</div><div class="xlrow{"" if chart else " solo"}"><div class="sheet"></div><div class="xlside">{sv}</div></div>{extra}'


def XLS(sid, title, h, task, data, sol, widths, head, **kw):
    """A slide with one live sheet and its task."""
    r = _xsheet(sid, task, data, sol, widths, head, title=h, **kw)
    if MODE == 'pdf':
        S(sid, title, h, r); return
    cfgd, inner = r
    S(sid, title, h, f'<div class="act xlq" id="{sid}-x" data-cfg="{_cfg(cfgd)}">{inner}</div>', kick=f'חלק {CUR[0]} · אקסל בתוך השקף')


def QX(sid, tag, title, stem, task, data, sol, widths, head, note=None, qmc='', **kw):
    """A question beside the live sheet in which it is solved. No algebra: the steps are formulas in the sheet."""
    head_t = f'{tag}: {title}' if tag else title
    stem_html = ''.join(f'<p>{TX(x)}</p>' for x in stem)
    # a timeline under the question builds click by click; the notes come after its last click
    off = max([int(x) // 10 for x in re.findall(r'data-n="(\d+)"', qmc)] or [0])
    notes = ''.join(BAND(x[0], x[1], x[2] + off) if MODE == 'deck' and len(x) > 2 else BAND(x[0], x[1]) for x in (note or []))   # (kind, text) or (kind, text, click): revealed beside the sheet
    r = _xsheet(sid, task, data, sol, widths, head, side=True, title=head_t, qtext=' '.join(re.sub('<[^>]+>', '', x) for x in stem), **kw)
    if MODE == 'pdf':
        S(sid, head_t, head_t, f'<div class="qstem">{stem_html}</div>{qmc}{r}{notes}', kind='q'); return
    cfgd, inner = r
    ch = cfgd.get('chart')
    sv = f'<svg class="xlc" viewBox="0 0 {ch.get("W", 470)} {ch.get("H", 330)}" role="img" aria-label="תרשים"></svg>' if ch else ''
    wide = ' wide' if sum(widths) > 470 else ''   # a sheet with many columns takes more of the slide, the question less
    S(sid, head_t, head_t, f'<div class="act xlq qx{wide}" id="{sid}-x" data-cfg="{_cfg(cfgd)}"><div class="qr"><div class="card qstem">{stem_html}</div>{qmc}{sv}{notes}</div><div class="xw">{inner}<div class="xfb"></div></div></div>',
      kick=f'חלק {CUR[0]} · {tag or "שאלה ואקסל"}', cls='qslide')


def MCX(sid, title, h, item, task, data, sol, widths, head, **kw):
    """A multiple choice question with a live sheet beside it, where the answer is computed with the right formula."""
    qt = re.sub('<[^>]+>', ' ', item.split('<div class="w">')[0]); qt = re.sub(r'\s+', ' ', qt).strip()
    r = _xsheet(sid, task, data, sol, widths, head, side=True, title=h, qtext=qt + ' ' + re.sub('<[^>]+>', '', task), **kw)
    if MODE == 'pdf':
        S(sid, title, h, item + r); return
    cfgd, inner = r
    S(sid, title, h, f'<div class="act xlq qx" id="{sid}-x" data-cfg="{_cfg(cfgd)}"><div class="qr">{item}</div><div class="xw">{inner}<div class="xfb"></div></div></div>', kick=f'חלק {CUR[0]} · שאלה ואקסל', cls='qslide')


def _repr_targets(sol):
    """One formula per column of targets (the first one), so the PDF shows the pattern without repeating dragged copies."""
    seen, out = set(), []
    for a in sol:
        c = re.match(r'[A-Z]+', a).group(0)
        if c not in seen: seen.add(c); out.append(a)
    return out


def SOLVE(sid, title, h, story, parts, hints, remind, steps):
    """A math exercise: parts (label, answer, tolerance). Buttons give a hint, a reminder, a partial or a full solution."""
    if MODE == 'pdf':
        p = ''.join(f'<li>{TX(l)} <b>{_fmtv(float(a)) if not isinstance(a, str) else a}</b></li>' for l, a, t in parts)
        S(sid, title, h, f'<p class="qstem">{TX(story)}</p><ol>{p}</ol>' + ''.join(f'<p>{TX(x)}</p>' for x in steps))
        return
    NACT[0] += 1
    ps = ''.join(f'<label class="svp" data-a="{a}" data-tol="{t}"><span>{TX(l)}</span><input dir="ltr" inputmode="decimal" autocomplete="off" spellcheck="false"></label>' for l, a, t in parts)
    ss = ''.join(f'<div class="svs">{TX(x)}</div>' for x in steps)
    cfgd = dict(hints=[TX(x) for x in hints], remind=TX(remind))
    btn = lambda c, t: f'<button class="abtn ghost {c}">{t}</button>'
    S(sid, title, h, f'<div class="act sv" id="{sid}-w" data-cfg="{_cfg(cfgd)}"><div class="tasktxt">{TX(story)}</div><div class="svps">{ps}</div><div class="actbar">{CHK}{btn("hnt", "💡 רמז")}{btn("rmd", "📐 תזכורת נוסחה")}{btn("prt", "פתרון חלקי")}{btn("ful", "פתרון מלא")}{RST}</div><div class="fbbar">הקלידו את התשובות, ולחצו ״בדיקה״. הפסד כותבים כמספר שלילי.</div><div class="svsol">{ss}</div></div>', kick=f'חלק {CUR[0]} · תרגיל')


def CASE(sid, title, story, qtext, opts, a, why, steps, toon=None):
    """One situation on its own slide: a question, then a multi step explanation revealed by clicks."""
    q = mc(sid + '-q', qtext, opts, a, why, rot=False)
    st = ''.join(ST(i + 1, TX(x), 'p', 'sp') for i, x in enumerate(steps))
    S(sid, title, title, f'<div class="qg"><div class="qr"><div class="card qstem"><p>{TX(story)}</p></div>{q}</div><div class="solw card">{st}</div></div>', kick=f'חלק {CUR[0]} · מקרה', cls='qslide')


def STEPS(chart, items, cls=''):
    """A chart built click by click beside its explanation. items: prose or '=' + math, in click order."""
    return f'<div class="qg"><div class="card chartw">{chart}</div><div class="rl">{items}</div></div>'


def RL(items, start=1):
    out = ''
    for i, x in enumerate(items):
        n = start + i
        if isinstance(x, tuple):
            n, x = x
        out += ST(n, M(x[1:]), cls='eq').replace('class="st eq"', 'class="st eq" dir="ltr"') if x.startswith('=') else ST(n, TX(x), 'p', 'sp')
    return out


exec(R('content_g.py'))
for _f in ['content_fv.py'] + {1: ['content_l1a.py', 'content_l1b.py', 'content_l1c.py'], 2: ['content_l2a.py', 'content_l2b.py', 'content_l2c.py']}[LESSON]:
    exec(R(_f))
