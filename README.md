# מימון למנהלות ומנהלים (MBA)

אתר הקורס: https://shaytsaban.github.io/colman-finance-for-managers-mba/

המסלול האקדמי המכללה למנהל, MBA. ד״ר שי צבאן. זה קורס נפרד מהקורס בעל השם הדומה באוניברסיטה הפתוחה (13005).

- `index.html`: דף הבית.
- `lectures/lecture-1/`: מצגת השיעור (`presentation.html`) וסיכום PDF (`summary.pdf`).
- `materials/`: סילבוס, קובץ התרגול של שיעור 1 (`practice-1.xlsx`) וקובץ הפתרונות (`practice-1-solutions.xlsx`), באותן כתובות תאים כמו במצגת.
- `_build/`: מקורות הבנייה. התוכן כתוב פעם אחת (`content_*.py`) ומזין גם את המצגת וגם את הסיכום.
  - `python3 build_deck.py 1`: המצגת. גיליונות ה-Excel החיים רצים על `xl.js`.
  - `python3 test_deck.py`: בדיקה בדפדפן ללא ממשק: שקפים שחורגים, כיוון מספרים, וכל גיליון: דוחה תשובה שגויה, מקבל נוסחה נכונה בכמה כתיבים, ומחזיר משוב ייעודי לכל טעות מוגדרת.
  - `node tests/real_input.js ../lectures/lecture-1/presentation.html`: הקלדה וגרירה אמיתיות של עכבר ומקלדת.
  - `python3 build_xlsx.py 1`: קובץ התרגול וקובץ הפתרונות. כל תשובה נבדקת שלוש פעמים: `fin.py`, המנוע של המצגת, וחישוב מחדש ב-LibreOffice.
  - `python3 tests/fin_ref.py`: פונקציות המימון של המנוע מול LibreOffice.
  - `python3 build_summary.py 1`, `python3 build_syllabus.py`, `python3 build_hub.py`.
  - פונטי David נטענים מ-`../iit-build/fonts` ואינם נשמרים כאן.
