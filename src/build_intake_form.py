"""
Paycor -> ADP — New Client Setup / Data Collection Form

A short, fillable intake form for moving a client off Paycor onto ADP at the
start of Q3. Captures the company header fields and lists every document to
collect, each mapped to where it lives in Paycor. State filings are
Connecticut-specific (CT-941 for state income tax, UC-2/UC-5A for state
unemployment) since the client is in CT.

Reuses the styling helpers from build_onboarding_guide.py.

Usage:
    python src/build_intake_form.py
    python src/build_intake_form.py --client "Acme LLC" --first-check 2026-07-03

Output:
    output/paycor_to_adp_setup_form.pdf
"""

import argparse
import os
from datetime import date

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    HRFlowable,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

from build_onboarding_guide import (
    ADP_RED,
    INK,
    LIGHT,
    RULE,
    SLATE,
    _checkbox,
    build_styles,
    callout,
    make_page_decorator,
    section_rule,
)


def header_band(client_name, first_check):
    def draw(canvas, doc):
        canvas.saveState()
        width, height = letter
        # Top red band
        canvas.setFillColor(ADP_RED)
        canvas.rect(0, height - 1.15 * inch, width, 1.15 * inch, fill=1, stroke=0)
        canvas.setFillColor(colors.white)
        canvas.setFont("Helvetica-Bold", 16)
        canvas.drawString(0.85 * inch, height - 0.7 * inch,
                          "New Client Setup — Paycor to ADP")
        canvas.setFont("Helvetica", 9.5)
        canvas.drawString(0.85 * inch, height - 0.95 * inch,
                          "Information & documents we need to build your payroll")
        # Footer
        canvas.setStrokeColor(RULE)
        canvas.setLineWidth(0.5)
        canvas.line(0.85 * inch, 0.65 * inch, width - 0.85 * inch, 0.65 * inch)
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(SLATE)
        canvas.drawString(0.85 * inch, 0.48 * inch,
                          "Paycor → ADP  •  New Client Setup")
        canvas.drawRightString(width - 0.85 * inch, 0.48 * inch,
                               "Page %d" % doc.page)
        if client_name:
            canvas.drawCentredString(width / 2.0, 0.48 * inch, client_name)
        canvas.restoreState()
    return draw


def field_rows(rows, styles):
    """Label + underlined fill-in line for each row."""
    data = []
    for label, prefill in rows:
        data.append([
            Paragraph("<b>%s</b>" % label, ParagraphStyle(
                "fl", fontName="Helvetica-Bold", fontSize=10, textColor=INK,
                leading=14)),
            Paragraph(prefill or "&nbsp;", ParagraphStyle(
                "fv", fontName="Helvetica", fontSize=10, textColor=SLATE,
                leading=14)),
        ])
    t = Table(data, colWidths=[2.0 * inch, 4.1 * inch])
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "BOTTOM"),
        ("TOPPADDING", (0, 0), (-1, -1), 9),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("LINEBELOW", (1, 0), (1, -1), 0.6, RULE),
    ]))
    return t


def doc_item(title, detail, paycor, styles):
    """A checkbox row: bold title, detail, and a 'In Paycor' locator line."""
    body = [Paragraph("<b>%s</b>" % title, ParagraphStyle(
        "dt", fontName="Helvetica-Bold", fontSize=10, textColor=INK,
        leading=14, spaceAfter=1))]
    if detail:
        body.append(Paragraph(detail, ParagraphStyle(
            "dd", fontName="Helvetica", fontSize=9.5, textColor=INK,
            leading=13, spaceAfter=1)))
    if paycor:
        body.append(Paragraph("In Paycor: %s" % paycor, ParagraphStyle(
            "dp", fontName="Helvetica-Oblique", fontSize=8.5,
            textColor=ADP_RED, leading=12)))
    t = Table([[_checkbox(), body]], colWidths=[0.3 * inch, None])
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (0, -1), 0),
        ("TOPPADDING", (0, 0), (0, -1), 4),
        ("TOPPADDING", (1, 0), (1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    return t


def build_story(styles, client_name, first_check, last_run_label):
    story = []

    # ---- COMPANY HEADER FIELDS ----
    story.append(Paragraph("Company information", styles["H1"]))
    story.append(field_rows([
        ("Tax ID (FEIN):", ""),
        ("Legal Business Name:", client_name),
        ("Legal Business Address:", ""),
        ("Delivery Address:", ""),
        ("1st Check Date with ADP:", first_check),
    ], styles))

    story.append(Spacer(1, 14))

    # ---- DOCUMENTS TO COLLECT ----
    story.append(Paragraph("Documents to collect from Paycor", styles["H1"]))
    story.append(Paragraph(
        "Please pull the items below out of Paycor and send them through the "
        "secure link we provide. Export to Excel/CSV and PDF where possible. "
        "Do this while you still have Paycor access.", styles["Body"]))
    story.append(Spacer(1, 4))

    story.append(doc_item(
        "Bank proof",
        "Voided check or online-banking screenshot showing the full routing "
        "number, account number, bank name, and business name (business bank "
        "account).", None, styles))
    story.append(doc_item(
        "Quarterly tax filings — Q1 &amp; Q2",
        "Federal Form 941 and Connecticut state filings (CT-941 state income "
        "tax; UC-2 / UC-5A state unemployment).",
        "Taxes → Quarterly Tax Package / Tax Documents", styles))
    story.append(doc_item(
        "Employee Earnings Record",
        "Two pulls: dated 1/1 – 6/30, and dated 1/1 – today.",
        "Reports → Employee Earnings Record", styles))
    story.append(doc_item(
        "Worker Profile report",
        "Employee demographic / census export (name, SSN, DOB, address, hire "
        "date, status, pay rate, W-4 / CT-W4).",
        "Reports → Worker / Employee Profile (census)", styles))

    story.append(section_rule())

    # ---- Q3 / MID-YEAR BALANCES ----
    story.append(Paragraph(
        "Year-to-date balances — Q3 start (July 1 – Sept 30)", styles["H1"]))
    story.append(callout(
        "Why these matter",
        "We're switching mid-year, so your year-to-date and prior-quarter "
        "balances have to carry into ADP exactly. They're what keep your W-2s "
        "and quarterly tax returns correct at year-end. “%s” below "
        "means your final Paycor pay date before going live on ADP." % last_run_label,
        styles, accent=colors.HexColor("#2E7D32")))
    story.append(Spacer(1, 10))

    story.append(doc_item(
        "YTD report",
        "From 1/1 through %s." % last_run_label,
        "Reports → Employee Earnings Record (year-to-date)", styles))
    story.append(doc_item(
        "PQYTD — Prior Quarter Year-to-Date",
        "From 1/1 – 6/30 (closes out Q1 + Q2).",
        "Reports → Employee Earnings Record, dated 1/1 – 6/30", styles))
    story.append(doc_item(
        "Payroll-by-payroll, gross to net",
        "Each pay date from 7/1 through %s." % last_run_label,
        "Reports → Payroll Register / Payroll Journal (per check date)",
        styles))
    story.append(doc_item(
        "Proof of federal tax deposits — current quarter only (Q3)",
        "Confirmation of 941 deposits already made this quarter.",
        "Taxes → Tax Liability / Tax Payment History", styles))
    story.append(doc_item(
        "Proof of state &amp; local tax deposits — current quarter only (Q3)",
        "Connecticut withholding, unemployment, and any local deposits made "
        "this quarter.",
        "Taxes → Tax Liability / Tax Payment History", styles))
    story.append(doc_item(
        "Q1 &amp; Q2 — Form 941",
        "Filed federal quarterly returns.", None, styles))
    story.append(doc_item(
        "Q1 &amp; Q2 — SIT and SUI filings",
        "Connecticut state income tax (CT-941) and state unemployment "
        "(UC-2 / UC-5A) for both quarters.", None, styles))

    return story


def build_pdf(path, client_name, first_check, last_run_label):
    styles = build_styles()
    doc = BaseDocTemplate(
        path, pagesize=letter,
        leftMargin=0.85 * inch, rightMargin=0.85 * inch,
        topMargin=1.45 * inch, bottomMargin=0.9 * inch,
        title="Paycor to ADP New Client Setup Form",
    )
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height,
                  id="main")
    doc.addPageTemplates([
        PageTemplate(id="body", frames=[frame],
                     onPage=header_band(client_name, first_check)),
    ])
    doc.build(build_story(styles, client_name, first_check, last_run_label))


def main():
    ap = argparse.ArgumentParser(description="Build the Paycor-to-ADP new client setup form")
    ap.add_argument("--client", default="", help="Client legal business name")
    ap.add_argument("--first-check", default="",
                    help="1st check date with ADP (free text, e.g. 2026-07-03)")
    ap.add_argument("--last-run", default="last Paycor payroll processed",
                    help="Label for the final Paycor pay date before go-live")
    ap.add_argument("--out", default="output/paycor_to_adp_setup_form.pdf",
                    help="Output PDF path")
    args = ap.parse_args()

    first = args.first_check
    if first:
        try:
            first = date.fromisoformat(first).strftime("%B %d, %Y")
        except ValueError:
            pass

    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    build_pdf(args.out, args.client, first, args.last_run)
    print("Wrote %s" % args.out)


if __name__ == "__main__":
    main()
