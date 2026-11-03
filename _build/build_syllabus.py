# Syllabus PDF. Run: python3 build_syllabus.py  ->  ../materials/syllabus.pdf
import html, os, shutil, subprocess, tempfile
H = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(H, '..', '..', 'iit-build', 'fonts')
CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
SITE = 'https://shaytsaban.github.io/colman-finance-for-managers-mba/'
NOTE = 'ייתכנו שינויים קלים בתוכן הקורס ובסדר הנושאים במהלך הסמסטר, בהתאם להתקדמות בשיעורים. עדכונים יפורסמו באתר הקורס.'
TBD = '<span class="tbd">יעודכן</span>'
n = lambda s: f'<span class="n">{s}</span>'
NA = 'נחמיאס א. (2014). ״תורת המימון: ניהול פיננסי של גופים עסקיים״. האוניברסיטה הפתוחה'
BMA = 'Brealey, Myers and Allen (2020)'
NS = 'נחמיאס (2014)'
rd = lambda vol, ch: f'<div>{NS}, כרך {vol}.</div>' + (f'<div class="en">{BMA}, {ch}.</div>' if ch else '')
# topics and readings as in the course syllabus (2026A); the semester and the meeting dates are new
L = [('1-2', 'מבוא למימון ומטרת הפירמה, ערך הזמן של הכסף וחישובי ערך עתידי', 'מימון: השקעות וגיוס משאבים. מטרת הפירמה וערך כפונקציה של תזרים, עיתוי וסיכון. ריבית בפועל וריבית אלטרנטיבית. ערך עתידי של סכום יחיד ושל סדרה, ריבית משתנה בשלבים, וחילוצים.', rd('א', 'Chapter 1')),
     ('3-5', 'חישובי ערך נוכחי, ריבית ושווי', 'ערך נוכחי של סכום יחיד ושל סדרות, ריבית אפקטיבית, ושווי של נכסים ועסקאות.', rd('ד', 'Chapters 3-4')),
     ('6-7', 'הלוואות ולוחות סילוקין', 'הלוואות בתשלומים קבועים (שפיצר), לוח סילוקין, ריבית וקרן בכל תשלום, ויתרת חוב.', rd('ד', 'Chapters 3-4')),
     ('8-9', 'קריטריונים לבחינת כדאיות השקעות', 'ערך נוכחי נקי (NPV, Net Present Value), שיעור תשואה פנימי (IRR, Internal Rate of Return), ובחירה בין פרויקטים.', rd('ד', 'Chapter 5')),
     ('10-11', 'קיצוב הון ובניית תחזית תזרימי מזומנים לתכניות השקעה', 'בחירת פרויקטים תחת מגבלת תקציב, ובניית תחזית תזרים מזומנים לפרויקט.', rd('ד', '')),
     ('12', 'דיון אקטואלי: מקרה בוחן (Case Study) ומשמעות מעשית של פרספקטיבה פיננסית', 'ניתוח מקרה בוחן מהשוק.', 'ללא.'),
     ('13', 'חזרה ודיון אינטגרטיבי', 'חזרה על נושאי הקורס ותרגול לקראת הבחינה.', 'ללא.')]
rows = ''.join(f'<tr{" class=hi" if i == 0 else ""}><td class="c">{n(k)}</td><td><b>{t}</b><div class="w">{w}</div></td><td class="rd">{r}</td></tr>' for i, (k, t, w, r) in enumerate(L))
body = f'''
<div class="hd"><div class="k">המסלול האקדמי המכללה למנהל · MBA · סמסטר א׳ תשפ״ז</div><h1 class="t">מימון למנהלות ומנהלים</h1><div class="s">סילבוס הקורס</div></div>
<table class="meta"><tr><td>קוד הקורס</td><td>{n('2121226')}</td></tr><tr><td>היקף</td><td>{n(3)} נקודות זכות, {n(3)} שעות סמסטריאליות</td></tr>
<tr><td>מרצה</td><td>ד״ר שי צבאן, {n('shay.tsaban@gmail.com')}</td></tr><tr><td>מתרגלים</td><td>{TBD}</td></tr>
<tr><td>מועד המפגש הראשון</td><td>{TBD}</td></tr><tr><td>אתר הקורס</td><td><span class="url">{SITE}</span></td></tr></table>
<h3>תקציר הקורס</h3>
<p>המימון הוא ענף שמחבר בין ניהול לכלכלה, ומהחשובים בעסקים בכלל ובניהול עסקי בפרט. ביסודו עומד הצורך לכמת את המשמעות הכספית של עסקאות, אירועים כלכליים, פרויקטים ואמצעי מימון, לתהליכי החלטה מובנים שמטרתם השאת ערך הפירמה לבעליה.</p>
<p>הקורס עוסק בסוגיות הליבה: משמעות הריבית וערך הזמן של הכסף, חישובי ריבית וכדאיות השקעות, ניהול סיכונים פיננסיים, והשפעת אי הוודאות על תמחור נכסים ועל קבלת החלטות פיננסיות.</p>
<h3>תוצרי למידה: בסוף הקורס הסטודנטים</h3>
<ul><li>ידעו לבנות ולתכנן תקציב ולערוך תחזיות פיננסיות.</li><li>יוכלו ליישם את הקשר בין ריבית, תזרימי מזומנים וערך לצורכי הערכת שווי נכסים.</li>
<li>יפתחו פרספקטיבה ניהולית בפן הפיננסי, בהקשר של ניהול סיכונים ומשמעותם.</li><li>ידעו להפעיל שיקולים בבחירה בין חלופות עסקיות ובין חלופות לגיוס הון.</li></ul>
<h3>תוכנית הקורס וקריאה</h3>
<table class="plan"><thead><tr><th>שיעורים</th><th>נושא</th><th>קריאה רלוונטית</th></tr></thead><tbody>{rows}</tbody></table>
<div class="note">{NOTE}</div>
<h3>שיטות הוראה</h3>
<p>הרצאות שבהן שזור תרגול. כל שאלה נפתרת בגיליון Excel, צעד אחר צעד. בכל שיעור מצגת אינטראקטיבית עם גיליונות Excel חיים: הסטודנטים כותבים נוסחה בתוך השקף ומקבלים משוב. לכל שיעור באתר: סיכום כתוב, קובץ תרגול ב-Excel וקובץ פתרונות עם נוסחאות חיות.</p>
<h3>דרישות הקורס והרכב הציון</h3>
<table class="meta"><tr><td>בחינה מסכמת</td><td>{n('100%')} מהציון הסופי</td></tr></table>
<ul><li>הבחינה בקמפוס, על מחשבי המכללה, ב-Excel. כל החישובים נעשים בגיליון, וכל דרך החישוב צריכה להיות מתועדת בו.</li><li>{n(10)} שאלות פתוחות, במשקל שווה. חומר עזר כתוב מותר בשימוש.</li>
<li>תרגילי הקורס מתפרסמים עם פתרון מלא, לתרגול עצמי. אין חובת הגשה.</li><li>נוכחות ואיחורים: בהתאם לתקנון.</li></ul>
<h3>רשימת קריאה</h3>
<p><b>חובה:</b></p><ul><li>{NA}.</li><li class="en">Brealey R., Myers S. and Allen F. (2020). Principles of Corporate Finance. 13th Edition. McGraw Hill.</li></ul>
<p><b>רשות:</b></p><ul><li class="en">Haas J. (2021). Corporate Finance in a Nutshell. West Academic.</li><li class="en">Piper M. (2020). Corporate Finance Made Simple. Simple Subjects.</li><li class="en">Craney W., Barlett R., Geis G. (2020). Corporate Finance: Principles and Practice. 4th Edition. Foundation Press.</li></ul>
<h3>יצירת קשר</h3>
<p>פניות לד״ר שי צבאן במייל: {n('shay.tsaban@gmail.com')}. חובה לרשום בכל פנייה את שם המוסד ואת שם הקורס.</p>'''
CSS = '''
@font-face{font-family:"David";src:url("david.ttf");font-weight:400}
@font-face{font-family:"David";src:url("davidbd.ttf");font-weight:700}
@page{size:A4;margin:16mm;@bottom-center{content:counter(page);font-family:"David";font-size:10pt;color:#5d6a86}}
:root{--ink:#16213a;--navy:#1b2d55;--coral:#ff6a4d;--mut:#5d6a86;--line:#d9d2c3}
*{box-sizing:border-box;-webkit-print-color-adjust:exact;print-color-adjust:exact}
html{direction:rtl}body{font-family:"David";font-size:11.8pt;line-height:1.34;color:var(--ink);margin:0}
.n{direction:ltr;unicode-bidi:isolate}
.hd{background:linear-gradient(160deg,#0f1b33 0%,#1b2d55 60%,#27447f 100%);color:#fff;border-radius:3mm;padding:6mm 8mm;margin-bottom:4mm}
.hd .k{color:#7fe3d6;font-weight:700;font-size:12pt}.hd h1.t{color:#fff;margin:1.5mm 0 1mm;font-size:24pt}.hd .s{color:#d6e0f7;font-size:13.5pt}
h3{font-size:13.4pt;color:var(--navy);margin:4mm 0 1.2mm;break-after:avoid;border-bottom:.5mm solid var(--coral);padding-bottom:.6mm}
p{margin:0 0 1.6mm}ul{margin:0 0 1.6mm;padding-right:6mm}li{margin-bottom:.5mm}
table{width:100%;border-collapse:collapse;font-size:10.8pt;margin:1.2mm 0 2mm}th{background:var(--navy);color:#fff;text-align:right;padding:1mm 2mm}td{padding:1mm 2mm;border-bottom:.25mm solid var(--line);vertical-align:top}tr{break-inside:avoid}
table.meta td:first-child{font-weight:700;width:30mm;color:var(--navy)}td.c{text-align:center;font-weight:700}td.r{white-space:nowrap}
tr.hi td{background:#fff0d2}.note{background:#eef2ff;border-right:1.2mm solid var(--navy);border-radius:1mm;padding:1.2mm 2.6mm;font-size:10.8pt}
.url{direction:ltr;unicode-bidi:isolate;font-family:Arial,sans-serif;font-size:10pt;color:var(--navy)}
.tbd{background:#fff0d2;border:.3mm dashed #a86703;border-radius:1mm;padding:0 2mm;font-weight:700;color:#7a4a00}
.lit{list-style:none;padding:0}.lit .n{display:block;text-align:left}
.w{font-size:10.4pt;color:#2a3858;margin-top:.4mm}td.rd{font-size:10pt;width:62mm}li.en,div.en{direction:ltr;text-align:left;unicode-bidi:isolate}
'''
page = f'<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><title>מימון למנהלות ומנהלים | סילבוס</title><style>{CSS}</style></head><body>{body}</body></html>'
assert '—' not in page and '־' not in page
d = tempfile.mkdtemp(dir=os.environ.get('TMPDIR'))
for f in ('david.ttf', 'davidbd.ttf'): shutil.copy(os.path.join(FONTS, f), d)
open(os.path.join(d, 's.html'), 'w', encoding='utf8').write(page)
out = os.path.abspath(os.path.join(H, '..', 'materials', 'syllabus.pdf'))
subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--no-sandbox', f'--user-data-dir={d}/p', '--no-pdf-header-footer', '--virtual-time-budget=6000', f'--print-to-pdf={out}', 'file://' + d + '/s.html'], capture_output=True, timeout=120)
shutil.rmtree(d, True)
import fitz
D = fitz.open(out); print('pages', len(D), 'bytes', os.path.getsize(out), sorted({f[3].split('+')[-1] for p in D for f in p.get_fonts()}))
