"""
QuickBooks Online -> ADP — Report & Info Collection Guide

A friendly, step-by-step guide that walks a not-very-technical client through
finding and saving every report ADP needs to take over their payroll mid-year
(Q2 switch). Each report is broken into simple, numbered clicks for QuickBooks
Online (QBO) Payroll, plus an employee-information section.

Reuses the styling helpers from build_onboarding_guide.py.

Usage:
    python src/build_qbo_guide.py
    python src/build_qbo_guide.py --client "Acme LLC"

Output:
    output/quickbooks_to_adp_guide.pdf
"""

import argparse
import os

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    ListFlowable,
    ListItem,
    PageBreak,
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
    data_table,
    section_rule,
)


def header_band(client_name):
    def draw(canvas, doc):
        canvas.saveState()
        width, height = letter
        canvas.setFillColor(ADP_RED)
        canvas.rect(0, height - 1.15 * inch, width, 1.15 * inch, fill=1, stroke=0)
        canvas.setFillColor(colors.white)
        canvas.setFont("Helvetica-Bold", 16)
        canvas.drawString(0.85 * inch, height - 0.7 * inch,
                          "Getting Your Reports Out of QuickBooks Online")
        canvas.setFont("Helvetica", 9.5)
        canvas.drawString(0.85 * inch, height - 0.95 * inch,
                          "A simple, step-by-step guide for your switch to ADP")
        canvas.setStrokeColor(RULE)
        canvas.setLineWidth(0.5)
        canvas.line(0.85 * inch, 0.65 * inch, width - 0.85 * inch, 0.65 * inch)
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(SLATE)
        canvas.drawString(0.85 * inch, 0.48 * inch,
                          "QuickBooks Online → ADP  •  Report Collection Guide")
        canvas.drawRightString(width - 0.85 * inch, 0.48 * inch,
                               "Page %d" % doc.page)
        if client_name:
            canvas.drawCentredString(width / 2.0, 0.48 * inch, client_name)
        canvas.restoreState()
    return draw


def steps(items, styles):
    return ListFlowable(
        [ListItem(Paragraph(s, styles["Body"]), value=i + 1)
         for i, s in enumerate(items)],
        bulletType="1", leftIndent=16, bulletFontName="Helvetica-Bold",
        bulletColor=ADP_RED, spaceBefore=2)


def report_block(num, title, whatis, step_list, styles, extra=None):
    """A checkbox card: number + title, a 'what it is' line, numbered steps."""
    right = [Paragraph(
        "<font color='#D0271D'><b>%d.</b></font>  <b>%s</b>" % (num, title),
        ParagraphStyle("rt", fontName="Helvetica-Bold", fontSize=11,
                       textColor=INK, leading=15, spaceAfter=2))]
    if whatis:
        right.append(Paragraph(
            "<i>%s</i>" % whatis,
            ParagraphStyle("rw", fontName="Helvetica-Oblique", fontSize=9.5,
                           textColor=SLATE, leading=13, spaceAfter=4)))
    right.append(steps(step_list, styles))
    if extra is not None:
        right.append(Spacer(1, 4))
        right.append(extra)

    t = Table([[_checkbox(), right]], colWidths=[0.32 * inch, None])
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (0, -1), 0),
        ("TOPPADDING", (0, 0), (0, -1), 3),
        ("TOPPADDING", (1, 0), (1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
    ]))
    return t


def date_range_table(rows, styles):
    return data_table(["Run it for these dates", "Which period"], rows, styles,
                      col_widths=[2.7 * inch, 3.4 * inch])


def build_story(styles, client_name):
    story = []

    # ---- INTRO ----
    story.append(Paragraph("Hi — here's all you need to do", styles["H1"]))
    story.append(Paragraph(
        "To move your payroll over to ADP, I need a handful of reports out of "
        "QuickBooks. This guide shows you exactly where to click to find each "
        "one and save it. Take your time — you can't break anything, and "
        "nothing here changes your payroll.", styles["Lead"]))
    story.append(callout(
        "If you get stuck, stop and call me",
        "QuickBooks occasionally moves buttons around, so if a screen doesn't "
        "match these steps exactly, don't worry — just call and we'll do it "
        "together on the phone. When you save each report, save it as a PDF and "
        "send them all to me through the secure link I gave you (not regular "
        "email — these have Social Security and bank numbers in them).",
        styles))

    story.append(Spacer(1, 12))

    # ---- THREE THINGS TO KNOW FIRST ----
    story.append(Paragraph("Three things to know first", styles["H2"]))
    story.append(Paragraph("<b>A.  Signing in</b>", styles["Body"]))
    story.append(steps([
        "Open your web browser and go to <b>qbo.intuit.com</b>, then sign in.",
        "Look at the <b>menu down the left-hand side</b> — that's how you get "
        "everywhere. The two you'll use are <b>Reports</b> and <b>Taxes</b>.",
    ], styles))
    story.append(Spacer(1, 6))
    story.append(Paragraph("<b>B.  Saving a report as a PDF</b>", styles["Body"]))
    story.append(steps([
        "Once a report is on the screen, look at the <b>top-right corner</b>.",
        "Click the <b>printer icon</b>, or the <b>Export</b> button (a little "
        "box with a down-arrow) and choose <b>Export to PDF</b>.",
        "Save it somewhere easy to find, like your <b>Desktop</b>. Give it a "
        "clear name like “Payroll Details Q2”.",
    ], styles))
    story.append(Spacer(1, 6))
    story.append(Paragraph("<b>C.  Changing the dates on a report</b>", styles["Body"]))
    story.append(steps([
        "At the top of most reports there are two date boxes — a <b>From</b> "
        "date and a <b>To</b> date.",
        "Click each one, pick the date, then click the blue <b>Run report</b> "
        "button to refresh it.",
    ], styles))

    story.append(PageBreak())

    # ---- PART 1: TAX FORMS ----
    story.append(Paragraph("Part 1 — Tax forms you already filed", styles["H1"]))
    story.append(Paragraph(
        "These live in the <b>Taxes</b> area, not Reports. Here's how to get "
        "there for all three:", styles["Body"]))
    story.append(steps([
        "On the left menu, click <b>Taxes</b>.",
        "At the top, click <b>Payroll Tax</b>.",
        "Click the <b>Filings</b> tab.",
        "Scroll down to <b>Filed</b> (or “Quarterly forms”). Your filed forms "
        "are listed here by quarter.",
    ], styles))
    story.append(callout(
        "If you don't see them here",
        "Some accountants file these outside of QuickBooks. If a form isn't "
        "listed, just let me know — don't go hunting. The “(if applicable)” "
        "ones below may simply not exist for your business, and that's fine.",
        styles))
    story.append(Spacer(1, 10))

    story.append(report_block(
        1, "Q1 941 (federal)",
        "Your federal payroll tax return for January–March.",
        ["In the Filed list, find the <b>Q1 (Jan–Mar)</b> row.",
         "Click <b>941</b> — it opens as a PDF.",
         "Save it (see “Saving a report as a PDF” on page 1)."],
        styles))
    story.append(report_block(
        2, "Q1 State return — SIT / SUI <i>(if applicable)</i>",
        "Your state income-tax (SIT) and state unemployment (SUI) returns for Q1.",
        ["In that same Filed list, look for your <b>state forms</b> under Q1.",
         "Click each one to open it, and save each as a PDF."],
        styles))
    story.append(report_block(
        3, "Q1 Local return <i>(if applicable)</i>",
        "Only some cities/towns have a local payroll tax. You may not have one.",
        ["In the same list, look for any <b>local / city</b> form under Q1.",
         "If one is there, open and save it. If not, skip this — no problem."],
        styles))

    story.append(PageBreak())

    # ---- PART 2: PAYROLL DETAILS ----
    story.append(Paragraph("Part 2 — “Payroll Details” reports", styles["H1"]))
    story.append(Paragraph(
        "This is the big one. It's the <b>same report run three times</b>, just "
        "with different dates each time. Save a separate PDF for each.",
        styles["Body"]))
    story.append(Paragraph("How to open it (do this once):", styles["Body"]))
    story.append(steps([
        "On the left menu, click <b>Reports</b>.",
        "In the <b>search box</b> at the top, type <b>Payroll Details</b>.",
        "Click <b>Payroll Details</b> when it appears. It already lists each "
        "employee separately, which is exactly what I need.",
    ], styles))
    story.append(Spacer(1, 8))
    story.append(report_block(
        4, "Current Quarter — Payroll Details (summed by employee)",
        "April 1 through your last payroll before moving to ADP.",
        ["With the Payroll Details report open, set the dates below.",
         "Click <b>Run report</b>, then save as a PDF."],
        styles,
        extra=date_range_table(
            [["April 1  →  last payroll before ADP", "Current quarter (Q2)"]],
            styles)))
    story.append(report_block(
        5, "Prior Quarter — Payroll Details (summed by employee)",
        "All of last quarter, January 1 through March 31.",
        ["Change the dates to the ones below.",
         "Click <b>Run report</b>, then save as a separate PDF."],
        styles,
        extra=date_range_table(
            [["January 1  →  March 31", "Prior quarter (Q1)"]], styles)))
    story.append(report_block(
        6, "Year to Date — Payroll Details (summed by employee)",
        "Everything so far this year, January 1 through your last check date.",
        ["Change the dates to the ones below.",
         "Click <b>Run report</b>, then save as a third separate PDF."],
        styles,
        extra=date_range_table(
            [["January 1  →  last check date before ADP", "Year to date"]],
            styles)))

    story.append(PageBreak())

    # ---- PART 3: TAX LIABILITY ----
    story.append(Paragraph("Part 3 — Taxes you've already paid (Q2)", styles["H1"]))
    story.append(report_block(
        7, "Payroll Tax Liability report — Q2",
        "Shows the payroll taxes that have been paid/deposited this quarter.",
        ["On the left menu, click <b>Reports</b>.",
         "In the search box, type <b>Payroll Tax Liability</b> and click it.",
         "Set the dates to <b>April 1 → June 30</b> (Q2).",
         "Click <b>Run report</b>, then save as a PDF.",
         "<i>Tip:</i> if you'd rather see a simple list of payments made, the "
         "<b>Payroll Tax Payments</b> report shows each deposit — either one "
         "works."],
        styles))

    story.append(section_rule())

    # ---- PART 4: EMPLOYEE INFO ----
    story.append(Paragraph("Part 4 — Employee information", styles["H1"]))
    story.append(Paragraph(
        "I need a full record for <b>everyone paid this year</b> — even people "
        "who've left, since they still get a W-2. Here's where it all lives:",
        styles["Body"]))
    story.append(steps([
        "On the left menu, click <b>Payroll</b>, then <b>Employees</b>.",
        "Click an employee's <b>name</b> to open their profile.",
        "Their <b>Social Security number, date of birth, and address</b> are "
        "under <b>Personal info</b> (or “Profile”).",
        "Their <b>bank / direct deposit</b> details are under <b>Payment "
        "method</b>.",
        "<i>Shortcut:</i> in <b>Reports</b>, search <b>Employee Details</b> to "
        "pull a lot of this into one report you can save as a PDF.",
    ], styles))
    story.append(Spacer(1, 8))
    story.append(Paragraph("What I need for each person:", styles["H2"]))
    story.append(data_table(
        ["Category", "Details"],
        [
            ["Identity", "Full legal name, Social Security number, date of birth, home address"],
            ["Contact", "Personal email and phone number"],
            ["Job", "Title, hire date, full- or part-time"],
            ["Pay", "Pay rate (salary or hourly), standard hours, pay frequency"],
            ["Tax setup", "W-4 elections (filing status); state W-4 if your state has one"],
            ["Direct deposit", "Bank routing number, account number, and account type (checking/savings)"],
            ["Status", "Active, on leave, or left this year (with the date they left)"],
        ],
        styles, col_widths=[1.3 * inch, 4.8 * inch]))
    story.append(Spacer(1, 8))
    story.append(callout(
        "Keep this private",
        "These reports contain Social Security and bank numbers. Please send "
        "everything through the secure link I provided — never in a regular "
        "email or text. When in doubt, call me and we'll do it together.",
        styles))

    return story


def build_pdf(path, client_name):
    styles = build_styles()
    doc = BaseDocTemplate(
        path, pagesize=letter,
        leftMargin=0.85 * inch, rightMargin=0.85 * inch,
        topMargin=1.45 * inch, bottomMargin=0.9 * inch,
        title="QuickBooks Online to ADP — Report Collection Guide",
    )
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height,
                  id="main")
    doc.addPageTemplates([
        PageTemplate(id="body", frames=[frame],
                     onPage=header_band(client_name)),
    ])
    doc.build(build_story(styles, client_name))


def main():
    ap = argparse.ArgumentParser(description="Build the QuickBooks-Online-to-ADP report collection guide")
    ap.add_argument("--client", default="", help="Client business name")
    ap.add_argument("--out", default="output/quickbooks_to_adp_guide.pdf",
                    help="Output PDF path")
    args = ap.parse_args()
    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    build_pdf(args.out, args.client)
    print("Wrote %s" % args.out)


if __name__ == "__main__":
    main()
