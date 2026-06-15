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

    # ---- WELCOME + HOW TO USE ----
    story.append(Paragraph("Welcome — here's what to expect", styles["H1"]))
    story.append(Paragraph(
        "Switching payroll providers mid-year sounds daunting, but it comes "
        "down to one thing: handing us a complete and accurate picture of your "
        "company, your people, and what's already been paid this year. This "
        "guide breaks that into plain-English checklists. Work through each "
        "section, gather the documents, and we'll handle the rest of the build.",
        styles["Lead"]))

    story.append(callout(
        "The single most important step",
        "Because we're switching at the start of %s — not on January 1 — "
        "your <b>year-to-date payroll totals</b> have to carry over so W-2s and "
        "quarterly tax filings come out correct at year-end. The reports you "
        "pull out of Paycor (Section 2) are the backbone of the whole setup. "
        "Pull them <b>before</b> your Paycor access is turned off." % quarter,
        styles))
    story.append(Spacer(1, 10))

    story.append(Paragraph("How to use this guide", styles["H2"]))
    story.append(ListFlowable(
        [
            ListItem(Paragraph(
                "Each section is a checklist. Tick items off as you collect them.",
                styles["Body"]), value="1"),
            ListItem(Paragraph(
                "Anything you can't find, just flag it — we'll help you track it down.",
                styles["Body"]), value="2"),
            ListItem(Paragraph(
                "Send everything through the secure link we provide. Don't email "
                "Social Security numbers or bank details in plain text.",
                styles["Body"]), value="3"),
        ],
        bulletType="1", leftIndent=18))

    story.append(section_rule())

    # ---- TIMELINE ----
    story.append(Paragraph("Your switch-over timeline", styles["H1"]))
    story.append(Paragraph(
        "A clean cutover means the last Paycor run and the first ADP run line "
        "up with no gap and no overlap. Here's the rough sequence:",
        styles["Body"]))
    story.append(data_table(
        ["When", "What happens", "Who"],
        [
            ["3–4 weeks out", "Gather company, tax, and employee info (this guide)", "You"],
            ["2–3 weeks out", "Pull year-to-date reports from Paycor", "You"],
            ["2 weeks out", "We build your ADP company, employees, and YTD balances", "ADP"],
            ["1–2 weeks out", "Parallel review — we verify totals match Paycor", "Together"],
            ["Final Paycor run", "Run your last payroll on Paycor as normal", "You"],
            ["%s" % go_live, "First payroll on ADP — go live", "Together"],
            ["After go-live", "Confirm tax agencies are pointed to ADP", "ADP"],
        ],
        styles, col_widths=[1.25 * inch, 3.9 * inch, 0.95 * inch]))
    story.append(Spacer(1, 8))
    story.append(callout(
        "Why quarter-start timing helps you",
        "Going live at the start of %s means ADP files clean, full-quarter tax "
        "returns from day one. It avoids splitting a single quarter between two "
        "providers, which is the most common source of year-end tax headaches." % quarter,
        styles, accent=colors.HexColor("#2E7D32")))

    story.append(PageBreak())

    # ---- SECTION 1: COMPANY INFO ----
    story.append(Paragraph("1.  Company information", styles["H1"]))
    story.append(Paragraph(
        "The legal foundation of your payroll account. Most of this lives on "
        "your formation documents, prior tax filings, or in Paycor's company "
        "setup screens.", styles["Body"]))
    story.append(checklist([
        "Legal business name (exactly as registered with the IRS)",
        "DBA / trade name, if you use one",
        "Federal Employer Identification Number (FEIN / EIN)",
        "Business structure (LLC, S-corp, C-corp, sole prop, partnership)",
        "Legal / mailing address and all physical work locations",
        "Primary contact for payroll (name, title, email, phone)",
        "Owner / signer name and title (authorizes bank debits & tax filings)",
        "NAICS or industry code",
        "Number of employees (and 1099 contractors, if any)",
    ], styles))

    story.append(Spacer(1, 10))
    # ---- SECTION 1b: TAX ACCOUNTS ----
    story.append(Paragraph("Federal & state tax accounts", styles["H2"]))
    story.append(Paragraph(
        "ADP files and deposits your payroll taxes, so we need every active "
        "tax account ID and rate. Missing a state ID is the #1 cause of "
        "setup delays.", styles["Body"]))
    story.append(data_table(
        ["Tax account", "What we need"],
        [
            ["Federal EIN", "9-digit IRS number + deposit frequency (monthly / semiweekly)"],
            ["State withholding", "State income-tax account ID for each state you have employees in"],
            ["State unemployment (SUI/SUTA)", "Account ID + your current-year experience rate (%)"],
            ["Local / city taxes", "Any local income or occupational tax IDs (varies by location)"],
            ["Power of Attorney", "Some states need a signed POA so ADP can file — we'll send forms"],
        ],
        styles, col_widths=[2.0 * inch, 4.1 * inch]))
    story.append(Spacer(1, 8))
    story.append(callout(
        "Don't have your state rates handy?",
        "Your SUI rate changes yearly and is on the rate notice the state mails "
        "you each winter. It's also visible in Paycor under your tax setup. "
        "Send us a screenshot if you're unsure — wrong rates mean wrong deposits.",
        styles))

    story.append(PageBreak())

    # ---- SECTION 2: PAYCOR REPORTS (the critical one) ----
    story.append(Paragraph("2.  Pull these reports from Paycor", styles["H1"]))
    story.append(callout(
        "Do this while you still have Paycor access",
        "Once you give notice, your login can be shut off quickly. Export and "
        "save these reports now — as PDF and Excel/CSV where possible. They "
        "are how we rebuild your year-to-date numbers in ADP.",
        styles))
    story.append(Spacer(1, 10))
    story.append(Paragraph(
        "In Paycor, most of these live under <b>Reports</b> → <b>Payroll</b> "
        "and <b>Reports</b> → <b>Tax</b>. Pull them for the current calendar "
        "year through your last Paycor pay date.", styles["Body"]))
    story.append(checklist([
        "<b>Payroll register</b> for every pay date this calendar year",
        "<b>Year-to-date (YTD) earnings &amp; deductions</b> summary by employee",
        "<b>Quarterly tax returns</b> already filed this year (Form 941 + state)",
        "<b>Tax deposit / liability history</b> for the year",
        "<b>W-2 preview</b> or last year's W-2s and W-3",
        "<b>Employee roster</b> export with all demographic fields",
        "<b>Deduction &amp; benefit setup</b> report (what's withheld and how)",
        "<b>PTO / accrual balances</b> as of your last run",
        "<b>Contractor / 1099 payment</b> totals, if you pay any",
        "<b>Garnishment / wage-order</b> documents and balances, if any",
    ], styles))
    story.append(Spacer(1, 8))
    story.append(callout(
        "What “year-to-date” has to include",
        "For each employee: gross wages, each earning type (regular, OT, bonus), "
        "pre-tax and post-tax deductions, employer contributions, and every tax "
        "withheld (federal, Social Security, Medicare, state, local). These totals "
        "must match Paycor to the penny before we go live.",
        styles, accent=colors.HexColor("#2E7D32")))

    story.append(PageBreak())

    # ---- SECTION 3: EMPLOYEE INFO ----
    story.append(Paragraph("3.  Employee information", styles["H1"]))
    story.append(Paragraph(
        "We need a complete record for every active employee (and anyone paid "
        "this year who has since left — they still get a W-2). Most of this "
        "exports straight from the Paycor employee roster.", styles["Body"]))
    story.append(data_table(
        ["Category", "Details needed"],
        [
            ["Identity", "Full legal name, SSN, date of birth, home address"],
            ["Contact", "Personal email and phone (for self-service onboarding)"],
            ["Job", "Title, hire date, department / location, full- or part-time"],
            ["Pay", "Pay rate, salary or hourly, standard hours, pay frequency"],
            ["Tax setup", "Federal &amp; state W-4 elections (filing status, allowances)"],
            ["Direct deposit", "Bank routing &amp; account number, account type, splits"],
            ["Status", "Active, on leave, or terminated this year (with term date)"],
        ],
        styles, col_widths=[1.4 * inch, 4.7 * inch]))
    story.append(Spacer(1, 10))
    story.append(Paragraph("Supporting documents to collect", styles["H2"]))
    story.append(checklist([
        "Signed Form W-4 (federal) and state equivalent for each employee",
        "Form I-9 and work authorization on file",
        "Voided check or bank letter for each direct-deposit account",
        "Any existing offer letters or comp-change records, if handy",
    ], styles))
    story.append(Spacer(1, 8))
    story.append(callout(
        "Make onboarding easier on yourself",
        "ADP can invite employees to enter their own address, W-4, and direct "
        "deposit through secure self-service. If you'd rather not collect bank "
        "details yourself, tell us — we'll turn that on.",
        styles))

    story.append(PageBreak())

    # ---- SECTION 4: PAY POLICIES, DEDUCTIONS, BANKING ----
    story.append(Paragraph("4.  Pay setup, deductions & banking", styles["H1"]))

    story.append(Paragraph("Pay schedule & policies", styles["H2"]))
    story.append(checklist([
        "Pay frequency (weekly, bi-weekly, semi-monthly, monthly)",
        "Pay period start/end dates and check dates for the rest of the year",
        "Overtime rules and any shift differentials",
        "PTO / sick / vacation accrual policies and current balances",
        "Holiday pay and bonus practices",
    ], styles))

    story.append(Paragraph("Deductions & benefits", styles["H2"]))
    story.append(checklist([
        "Health / dental / vision premiums (employee &amp; employer share)",
        "Retirement plan (401k/IRA): provider, match formula, deferral amounts",
        "HSA / FSA contributions",
        "Garnishments or child-support orders (with case numbers and balances)",
        "Any other recurring pre-tax or post-tax deductions",
    ], styles))

    story.append(Paragraph("Banking & funding", styles["H2"]))
    story.append(checklist([
        "Business bank account that funds payroll (routing + account number)",
        "Voided business check or bank verification letter",
        "Name &amp; title of person authorized to approve ACH debits",
        "Workers' comp policy details (if using pay-as-you-go integration)",
    ], styles))
    story.append(Spacer(1, 8))
    story.append(callout(
        "General-ledger mapping (optional but worth it)",
        "If you want payroll to flow neatly into QuickBooks, Xero, or another "
        "accounting system, send your chart of accounts or current GL mapping. "
        "We'll line up the export so your bookkeeper's life gets easier.",
        styles))

    story.append(PageBreak())

    # ---- MASTER CHECKLIST ----
    story.append(Paragraph("Quick master checklist", styles["H1"]))
    story.append(Paragraph(
        "A one-page summary you can print and work through. Detail for each "
        "item is in the sections above.", styles["Lead"]))

    story.append(Paragraph("Company & tax", styles["H2"]))
    story.append(checklist([
        "Legal name, EIN, entity type, addresses, payroll contact",
        "State withholding + SUI account IDs and current SUI rate",
        "Local tax IDs and any Power-of-Attorney forms signed",
    ], styles))
    story.append(Paragraph("From Paycor (before access ends)", styles["H2"]))
    story.append(checklist([
        "YTD payroll register + earnings/deductions by employee",
        "Filed quarterly returns (941 + state) and deposit history",
        "Employee roster export, deduction setup, PTO balances",
    ], styles))
    story.append(Paragraph("Employees", styles["H2"]))
    story.append(checklist([
        "Identity, pay, and W-4 details for every employee paid this year",
        "Direct-deposit info (or opt into employee self-service)",
        "W-4, I-9, and voided checks on file",
    ], styles))
    story.append(Paragraph("Pay setup & banking", styles["H2"]))
    story.append(checklist([
        "Pay frequency, schedule, OT and PTO policies",
        "Benefits, retirement, and garnishment details",
        "Funding bank account + voided check + authorized signer",
    ], styles))

    story.append(section_rule())
    story.append(Paragraph("Questions along the way?", styles["H2"]))
    story.append(Paragraph(
        "You don't have to figure this out alone. If anything on these lists is "
        "unclear or hard to find, reach out and we'll walk through it with you. "
        "The more complete the information up front, the smoother your first "
        "ADP payroll will run.", styles["Body"]))
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
