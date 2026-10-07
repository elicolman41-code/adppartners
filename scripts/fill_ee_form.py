"""Fill ADP Employee Information Form (EI002) with comb-aligned, flattened text.
usage: python fill_ee_form.py BLANK.pdf OUT.pdf data.json  (data = {field_name: value}; checkboxes use "X")"""
import sys, json, pymupdf as fitz
blank, out, data = sys.argv[1], sys.argv[2], json.load(open(sys.argv[3]))
doc = fitz.open(blank); page = doc[0]
geo = {w.field_name: (fitz.Rect(w.rect), w.text_maxlen or 0) for w in page.widgets()}
for w in list(page.widgets()): page.delete_widget(w)
for name, v in data.items():
    if name not in geo or v in (None, ""): continue
    r, ml = geo[name]; v = str(v); fs = 10
    if ml > 1:
        if name in ("PayRateAmt1", "undefined_20", "undefined_24", "undefined_12", "undefined_16"): v = v.rjust(ml)
        cw = r.width / ml
        for i, ch in enumerate(v[:ml]):
            if ch == " ": continue
            tw = fitz.get_text_length(ch, "cour", fs)
            page.insert_text((r.x0 + i*cw + (cw-tw)/2, r.y1-4), ch, fontname="cour", fontsize=fs)
    else:
        tw = fitz.get_text_length(v, "cour", fs)
        page.insert_text((r.x0 + (r.width-tw)/2, r.y1-4), v, fontname="cour", fontsize=fs)
doc.save(out, garbage=3, deflate=True)
