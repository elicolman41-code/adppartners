"""
Client Onboarding Guide — Paycor → ADP Switch

Generates a clean, client-facing PDF that walks a business through everything
they need to gather to move payroll from Paycor to ADP for the start of a new
quarter. Mid-year/mid-quarter switches hinge on accurate year-to-date data, so
the guide leans on pulling the right reports out of Paycor before access ends.

Usage:
    python src/build_onboarding_guide.py
    python src/build_onboarding_guide.py --client "Acme LLC" --go-live 2026-07-01

Output:
    output/paycor_to_adp_onboarding_guide.pdf
"""

import argparse
import os
from datetime import date

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    HRFlowable,
    ListFlowable,
    ListItem,
    NextPageTemplate,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

# ---------------------------------------------------------------------------
# Brand palette
# ---------------------------------------------------------------------------
ADP_RED = colors.HexColor("#D0271D")
INK = colors.HexColor("#1A1A1A")
SLATE = colors.HexColor("#555555")
LIGHT = colors.HexColor("#F4F4F4")
RULE = colors.HexColor("#DDDDDD")


# ---------------------------------------------------------------------------
# Styles
# ---------------------------------------------------------------------------
def build_styles():
    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(
        "CoverTitle", parent=styles["Title"], fontName="Helvetica-Bold",
        fontSize=30, leading=36, textColor=INK, alignment=TA_LEFT,
        spaceAfter=8,
    ))
    styles.add(ParagraphStyle(
        "CoverSub", fontName="Helvetica", fontSize=14, leading=20,
        textColor=SLATE, alignment=TA_LEFT, spaceAfter=4,
    ))
    styles.add(ParagraphStyle(
        "CoverMeta", fontName="Helvetica", fontSize=10.5, leading=16,
        textColor=SLATE, alignment=TA_LEFT,
    ))
    styles.add(ParagraphStyle(
        "H1", parent=styles["Heading1"], fontName="Helvetica-Bold",
        fontSize=15, leading=19, textColor=ADP_RED, spaceBefore=6,
        spaceAfter=8,
    ))
    styles.add(ParagraphStyle(
        "H2", parent=styles["Heading2"], fontName="Helvetica-Bold",
        fontSize=11.5, leading=15, textColor=INK, spaceBefore=10,
        spaceAfter=4,
    ))
    styles.add(ParagraphStyle(
        "Body", parent=styles["BodyText"], fontName="Helvetica",
        fontSize=10, leading=15, textColor=INK, spaceAfter=6,
    ))
    styles.add(ParagraphStyle(
        "Lead", fontName="Helvetica", fontSize=10.5, leading=16,
        textColor=SLATE, spaceAfter=10,
    ))
    styles.add(ParagraphStyle(
        "Check", fontName="Helvetica", fontSize=10, leading=16,
        textColor=INK, leftIndent=2,
    ))
    styles.add(ParagraphStyle(
        "Cell", fontName="Helvetica", fontSize=9.5, leading=13,
        textColor=INK,
    ))
    styles.add(ParagraphStyle(
        "CellHead", fontName="Helvetica-Bold", fontSize=9.5, leading=13,
        textColor=colors.white,
    ))
    styles.add(ParagraphStyle(
        "Callout", fontName="Helvetica", fontSize=9.5, leading=14,
        textColor=INK,
    ))
    styles.add(ParagraphStyle(
        "TOC", fontName="Helvetica", fontSize=11, leading=22, textColor=INK,
    ))
    return styles


# ---------------------------------------------------------------------------
# Page furniture (header / footer)
# ---------------------------------------------------------------------------
def make_page_decorator(client_name):
    def decorate(canvas, doc):
        canvas.saveState()
        width, height = letter
        # Footer rule
        canvas.setStrokeColor(RULE)
        canvas.setLineWidth(0.5)
        canvas.line(0.85 * inch, 0.65 * inch, width - 0.85 * inch, 0.65 * inch)
        # Footer text
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(SLATE)
        canvas.drawString(0.85 * inch, 0.48 * inch,
                          "Payroll Onboarding Guide  •  Paycor → ADP")
        canvas.drawRightString(width - 0.85 * inch, 0.48 * inch,
                               "Page %d" % doc.page)
        if client_name:
            canvas.drawCentredString(width / 2.0, 0.48 * inch, client_name)
        canvas.restoreState()
    return decorate


def cover_background(canvas, doc):
    """Red band across the top of the cover page."""
    canvas.saveState()
    width, height = letter
    canvas.setFillColor(ADP_RED)
    canvas.rect(0, height - 2.0 * inch, width, 2.0 * inch, fill=1, stroke=0)
    canvas.setFillColor(colors.white)
    canvas.setFont("Helvetica-Bold", 13)
    canvas.drawString(0.85 * inch, height - 1.0 * inch, "ADP  PAYROLL  ONBOARDING")
    canvas.setFont("Helvetica", 10)
    canvas.drawString(0.85 * inch, height - 1.3 * inch,
                      "New Client Setup — Switching from Paycor")
    # Bottom accent bar
    canvas.setFillColor(ADP_RED)
    canvas.rect(0, 0, width, 0.22 * inch, fill=1, stroke=0)
    canvas.restoreState()


# ---------------------------------------------------------------------------
# Reusable builders
# ---------------------------------------------------------------------------
def _checkbox():
    """A small empty square that reads as a tick-box."""
    box = Table([[""]], colWidths=[0.13 * inch], rowHeights=[0.13 * inch])
    box.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.9, ADP_RED),
        ("BACKGROUND", (0, 0), (-1, -1), colors.white),
    ]))
    return box


def checklist(items, styles):
    rows = []
    for it in items:
        rows.append([_checkbox(), Paragraph(it, styles["Check"])])
    t = Table(rows, colWidths=[0.3 * inch, None])
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (0, -1), 0),
        ("TOPPADDING", (0, 0), (0, -1), 5),
    ]))
    return t


def data_table(header, rows, styles, col_widths=None):
    data = [[Paragraph(h, styles["CellHead"]) for h in header]]
    for r in rows:
        data.append([Paragraph(c, styles["Cell"]) for c in r])
    t = Table(data, colWidths=col_widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), ADP_RED),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT]),
        ("GRID", (0, 0), (-1, -1), 0.5, RULE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
    ]))
    return t


def callout(title, body, styles, accent=ADP_RED):
    inner = [
        Paragraph("<b>%s</b>" % title, ParagraphStyle(
            "ct", parent=styles["Callout"], textColor=accent,
            fontName="Helvetica-Bold", spaceAfter=3)),
        Paragraph(body, styles["Callout"]),
    ]
    t = Table([[inner]], colWidths=[None])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), LIGHT),
        ("LINEBEFORE", (0, 0), (0, -1), 3, accent),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
    ]))
    return t


def section_rule():
    return HRFlowable(width="100%", thickness=0.75, color=RULE,
                      spaceBefore=10, spaceAfter=10)


# ---------------------------------------------------------------------------
# Document content
# ---------------------------------------------------------------------------
def build_story(styles, client_name, go_live, quarter, prepared_by):
    story = []

    # ---- COVER ----
    story.append(Spacer(1, 2.4 * inch))
    story.append(Paragraph("Getting Set Up on ADP", styles["CoverTitle"]))
    story.append(Paragraph(
        "Your guide to gathering everything we need to move your payroll "
        "off Paycor — cleanly, accurately, and on time.", styles["CoverSub"]))
    story.append(Spacer(1, 0.5 * inch))
    story.append(HRFlowable(width="38%", thickness=2, color=ADP_RED,
                            hAlign="LEFT", spaceAfter=14))

    meta_rows = [
        ["Prepared for:", client_name or "____________________________"],
        ["Target go-live:", "%s  (start of %s)" % (go_live, quarter)],
        ["Prepared by:", prepared_by],
        ["Date prepared:", date.today().strftime("%B %d, %Y")],
    ]
    mt = Table(meta_rows, colWidths=[1.3 * inch, 4.0 * inch])
    mt.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 10.5),
        ("TEXTCOLOR", (0, 0), (0, -1), SLATE),
        ("TEXTCOLOR", (1, 0), (1, -1), INK),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
    ]))
    story.append(mt)

    story.append(NextPageTemplate("body"))
    story.append(PageBreak())

    # ---- WHAT WE NEED ----
    story.append(Paragraph("What we need from you", styles["H1"]))
    story.append(Paragraph(
        "To finish your ADP setup we only need two things: your "
        "<b>year-to-date payroll balances</b> and your <b>employee "
        "information</b>. Both export straight out of Paycor. Because we're "
        "switching mid-year, the balances are what keep your W-2s and "
        "Connecticut tax filings correct at year-end.", styles["Lead"]))
    story.append(callout(
        "Pull these from Paycor before your access ends",
        "Once you give notice, your Paycor login can be turned off quickly. "
        "Export the reports below now — as Excel/CSV and PDF — and send them "
        "through the secure link we provide. Don't email Social Security or "
        "bank numbers in plain text.",
        styles))

    story.append(Spacer(1, 14))

    # ---- 1. BALANCES ----
    story.append(Paragraph("1.  Year-to-date balances", styles["H1"]))
    story.append(Paragraph(
        "One report covers most of this: in Paycor, run a <b>Year-to-Date "
        "(YTD) earnings &amp; deductions summary by employee</b> for the "
        "current calendar year through your last Paycor pay date. For each "
        "employee we need:", styles["Body"]))
    story.append(checklist([
        "Gross wages YTD, broken out by earning type (regular, OT, bonus)",
        "Pre-tax deductions YTD (401k, health, HSA/FSA, etc.)",
        "Post-tax deductions YTD",
        "Employer contributions YTD (401k match, etc.)",
        "Federal income tax withheld YTD",
        "Social Security and Medicare withheld YTD (employee + employer)",
        "Connecticut income tax withheld YTD",
        "CT Paid Family &amp; Medical Leave withheld YTD (0.5% employee)",
        "Net pay YTD",
    ], styles))
    story.append(Spacer(1, 10))
    story.append(Paragraph("Also send (to confirm the totals tie out)", styles["H2"]))
    story.append(checklist([
        "Most recent payroll register from Paycor",
        "Quarterly returns already filed this year (Form 941 + CT returns)",
        "Tax deposit / liability history for the year",
    ], styles))
    story.append(Spacer(1, 8))
    story.append(callout(
        "These have to match to the penny",
        "We load each employee's balances into ADP exactly as Paycor reported "
        "them, then verify the company totals match before your first run. "
        "Accurate balances now = clean W-2s in January.",
        styles, accent=colors.HexColor("#2E7D32")))

    story.append(PageBreak())

    # ---- 2. EMPLOYEE INFORMATION ----
    story.append(Paragraph("2.  Employee information", styles["H1"]))
    story.append(Paragraph(
        "A complete record for everyone paid this year — including anyone who "
        "has since left, since they still receive a W-2. The Paycor "
        "<b>employee roster export</b> has most of these fields already.",
        styles["Body"]))
    story.append(data_table(
        ["Category", "Details needed"],
        [
            ["Identity", "Full legal name, SSN, date of birth, home address"],
            ["Contact", "Personal email and phone"],
            ["Job", "Title, hire date, location, full- or part-time"],
            ["Pay", "Pay rate, salary or hourly, standard hours, pay frequency"],
            ["Tax setup", "Federal W-4 and Connecticut CT-W4 elections"],
            ["Direct deposit", "Bank routing &amp; account number, account type, any splits"],
            ["Status", "Active, on leave, or terminated this year (with term date)"],
        ],
        styles, col_widths=[1.4 * inch, 4.7 * inch]))
    story.append(Spacer(1, 8))
    story.append(callout(
        "Let employees enter their own details",
        "ADP can invite each employee to enter their address, W-4/CT-W4, and "
        "direct deposit through secure self-service — so you don't have to "
        "collect bank info yourself. Just say the word and we'll turn it on.",
        styles))

    story.append(Spacer(1, 14))

    # ---- CONNECTICUT ACCOUNTS ----
    story.append(Paragraph("Connecticut tax accounts", styles["H1"]))
    story.append(Paragraph(
        "So ADP can file and deposit your Connecticut taxes, send these "
        "account numbers (they're in your Paycor tax setup):", styles["Body"]))
    story.append(data_table(
        ["Account", "What we need"],
        [
            ["Federal EIN", "9-digit IRS number"],
            ["CT withholding (DRS)", "Connecticut Tax Registration Number + deposit frequency"],
            ["CT unemployment (CTDOL)", "Registration number + current-year contribution rate (%)"],
            ["CT Paid Leave", "CT Paid Leave Authority registration (0.5% employee deduction)"],
        ],
        styles, col_widths=[1.9 * inch, 4.2 * inch]))

    story.append(section_rule())
    story.append(Paragraph("Questions?", styles["H2"]))
    story.append(Paragraph(
        "If anything here is unclear or hard to find in Paycor, reach out and "
        "we'll walk through it with you.", styles["Body"]))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "<b>%s</b>" % prepared_by, ParagraphStyle(
            "sig", fontName="Helvetica", fontSize=10.5, textColor=ADP_RED)))

    return story


# ---------------------------------------------------------------------------
# Assemble document
# ---------------------------------------------------------------------------
def build_pdf(path, client_name, go_live, quarter, prepared_by):
    styles = build_styles()
    doc = BaseDocTemplate(
        path, pagesize=letter,
        leftMargin=0.85 * inch, rightMargin=0.85 * inch,
        topMargin=0.9 * inch, bottomMargin=0.9 * inch,
        title="Paycor to ADP Onboarding Guide", author=prepared_by,
    )

    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height,
                  id="main")
    cover_frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width,
                        doc.height, id="cover")

    decorate = make_page_decorator(client_name)
    doc.addPageTemplates([
        PageTemplate(id="cover", frames=[cover_frame],
                     onPage=cover_background),
        PageTemplate(id="body", frames=[frame], onPage=decorate),
    ])

    story = build_story(styles, client_name, go_live, quarter, prepared_by)
    doc.build(story)


def quarter_from_date(d):
    q = (d.month - 1) // 3 + 1
    return "Q%d %d" % (q, d.year)


def main():
    ap = argparse.ArgumentParser(description="Build the Paycor-to-ADP client onboarding PDF")
    ap.add_argument("--client", default="", help="Client business name")
    ap.add_argument("--go-live", default="2026-07-01",
                    help="Target first-ADP-payroll date (YYYY-MM-DD)")
    ap.add_argument("--prepared-by", default="Your ADP Partner Team",
                    help="Name shown as the document preparer")
    ap.add_argument("--out", default="output/paycor_to_adp_onboarding_guide.pdf",
                    help="Output PDF path")
    args = ap.parse_args()

    try:
        gl = date.fromisoformat(args.go_live)
        go_live_str = gl.strftime("%B %d, %Y")
        quarter = quarter_from_date(gl)
    except ValueError:
        go_live_str = args.go_live
        quarter = "the new quarter"

    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    build_pdf(args.out, args.client, go_live_str, quarter, args.prepared_by)
    print("Wrote %s" % args.out)


if __name__ == "__main__":
    main()
