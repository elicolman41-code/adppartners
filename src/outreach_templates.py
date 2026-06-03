"""
Module 3 — Outreach sequence templates.

Three tracks:
  Track 1 — Grid/Buyout pitch (Priority A, strong payroll signal)
  Track 2 — Revenue Share pitch (Priority B, referral angle)
  Track 3 — Cold/Unknown (Priority C, single curiosity email)

All templates use [First Name], [Firm Name], [Neighborhood], [Competitor] as merge fields.
Subject line variants are provided for A/B testing.

CORE PITCH (all tracks):
  "You're probably recommending Gusto to your clients. ADP can match that price —
  and we pay you a lot more than Gusto does for every client you send our way.
  Most people in your position have never heard that."

[Competitor] merge field should be set to:
  - "Gusto" for Xero/cloud-native firms (Brooklyn Fi, BusinessHQ, SDO CPA)
  - "QuickBooks Payroll" for QB-heavy firms (BIT Accounting, Brooklyn CPA, ClearPath CFO)
  - "Gusto or QuickBooks" for mixed/unknown signals
  - Skip the competitor angle for staffing agencies — use cost/efficiency framing instead.
"""

from typing import NamedTuple


class EmailTemplate(NamedTuple):
    track: str
    step: int
    day: int
    channel: str  # "email" | "linkedin_dm" | "text"
    subject_variants: list[str]
    body: str
    notes: str


# ─────────────────────────────────────────────────────────────────────────────
# TRACK 1 — GRID / BUYOUT PITCH (Priority A)
# Target: firm with clear payroll signals, ready for the buyout conversation
# ─────────────────────────────────────────────────────────────────────────────

TRACK_1_EMAIL_1 = EmailTemplate(
    track="1_grid",
    step=1,
    day=1,
    channel="email",
    subject_variants=[
        "quick question about your payroll clients",
        "[Firm Name] — something worth 5 minutes of your time",
        "one-time opportunity for [First Name]",
    ],
    body="""\
Hi [First Name],

I work with accounting firms in Brooklyn and I've been seeing a handful of them \
quietly turn their payroll book into a meaningful one-time cash payment — without \
losing any of the relationships.

Not sure if it's a fit for you, but given what I know about [Firm Name], it \
seemed worth a quick note.

Would a 10-minute call this week make sense?

[Your Name]
[Your Phone] | [Your Email]""",
    notes=(
        "Keep it short. No ADP mention yet. Pure curiosity hook. "
        "Goal is one reply, not a sale. If they ask 'what is this?' — that's a win."
    ),
)

TRACK_1_FOLLOWUP_DM = EmailTemplate(
    track="1_grid",
    step=2,
    day=3,
    channel="linkedin_dm",
    subject_variants=[],
    body="""\
Hi [First Name] — sent you an email a couple days ago. I partner with accounting \
firms that process payroll in-house. There's a one-time payout structure some \
firms are using right now that I think would be worth 10 minutes to explain. \
Happy to keep it brief. Open to a quick call this week?""",
    notes=(
        "LinkedIn DM or SMS. Reference the email casually — don't resend it. "
        "Mention payroll explicitly here. Short."
    ),
)

TRACK_1_EMAIL_2 = EmailTemplate(
    track="1_grid",
    step=3,
    day=7,
    channel="email",
    subject_variants=[
        "following up — payroll buyout program",
        "the firms I've worked with in Brooklyn",
    ],
    body="""\
Hi [First Name],

Wanted to follow up once more. I've been working with a few [Neighborhood] firms \
that used this program to generate between $40,000 and $80,000 as a one-time \
payment on their existing payroll clients — paid out around 135 days after \
signing. The firms I've spoken with appreciated that it didn't affect any of \
their other client relationships.

If payroll is a meaningful part of your revenue and you've ever thought about \
what it would look like to monetize that book, I'd love 10 minutes.

[Your Name]
[Your Phone]""",
    notes=(
        "Add social proof. Give the $40–80k range to make it concrete. "
        "Don't mention ADP by name yet — some reps prefer to wait for the call."
    ),
)

TRACK_1_EMAIL_3 = EmailTemplate(
    track="1_grid",
    step=4,
    day=14,
    channel="email",
    subject_variants=[
        "last note from me",
        "closing the loop",
    ],
    body="""\
Hi [First Name],

I'll leave you alone after this — just wanted to make one last attempt since \
the timing on this type of program does matter.

If you're ever curious about what a one-time buyout of your payroll book \
could look like for [Firm Name], my door is open. No pressure, no pitch.

[Your Name]
[Your Phone]""",
    notes=(
        "Breakup email. Short. No ask beyond 'reach out whenever.' "
        "Some of the best responses come from this one."
    ),
)


# ─────────────────────────────────────────────────────────────────────────────
# TRACK 2 — REVENUE SHARE / BROKER PROGRAM (Priority B)
# Target: firm that does some payroll, good referral candidate
# ─────────────────────────────────────────────────────────────────────────────

TRACK_2_EMAIL_1 = EmailTemplate(
    track="2_revenue_share",
    step=1,
    day=1,
    channel="email",
    subject_variants=[
        "you're probably recommending [Competitor]. ADP pays more.",
        "[First Name] — same price for your clients, more money for you",
        "quick question about your [Competitor] referrals",
    ],
    body="""\
Hi [First Name],

You're probably recommending [Competitor] to your small business clients. \
ADP can match that price — and we pay you a lot more than [Competitor] does \
for every client you send our way. Most people in your position have never \
heard that.

Worth a quick conversation this week?

[Your Name]
[Your Phone] | [Your Email]""",
    notes=(
        "SHORT AND DIRECT. Lead with the Gusto/QB competitor comparison — that's the hook. "
        "Set [Competitor] based on the firm's known tech stack: 'Gusto' for Xero/cloud firms, "
        "'QuickBooks Payroll' for QB-heavy firms, 'Gusto or QuickBooks' for unknown. "
        "Do NOT lead with compliance or enterprise value — lead with money."
    ),
)

TRACK_2_FOLLOWUP_DM = EmailTemplate(
    track="2_revenue_share",
    step=2,
    day=3,
    channel="linkedin_dm",
    subject_variants=[],
    body="""\
Hi [First Name] — sent you an email a couple days ago. Short version: if you're \
recommending [Competitor] for payroll, ADP matches the price for your clients \
and pays you significantly more per referral. Some [Neighborhood] firms are \
adding $10–30k a year just by switching where they refer. Happy to explain in \
10 minutes.""",
    notes=(
        "Keep the competitor name front and center — that's the hook that got them "
        "to read the first email. Reinforce: same price for clients, more money for you. "
        "Give the $10–30k/year range to make it concrete."
    ),
)

TRACK_2_EMAIL_2 = EmailTemplate(
    track="2_revenue_share",
    step=3,
    day=7,
    channel="email",
    subject_variants=[
        "how the referral program works — quick overview",
        "the math on the revenue share",
    ],
    body="""\
Hi [First Name],

One more note. Here's the short version of what I'm talking about:

My firm has a partnership program where accounting firms refer their small \
business clients to us for payroll. In return, the firm earns a revenue share — \
somewhere between 25% and 75% of the payroll revenue those clients generate, \
paid monthly. There's also a volume bonus for firms that refer above a certain \
threshold.

No changing how you work with clients. No cold calling. You just stay in your \
lane and earn income from the payroll side.

If that's worth a 10-minute call, let me know. Happy to send a one-pager first \
if you'd prefer.

[Your Name]
[Your Phone]""",
    notes=(
        "This email is more detailed by design — they haven't responded, "
        "so give them enough to make a decision. Offer a one-pager as a lower-friction option."
    ),
)

TRACK_2_EMAIL_3 = EmailTemplate(
    track="2_revenue_share",
    step=4,
    day=14,
    channel="email",
    subject_variants=[
        "last email — leaving the door open",
        "signing off for now",
    ],
    body="""\
Hi [First Name],

Last note, I promise. If the idea of earning ongoing revenue from payroll \
referrals is ever interesting to you — even six months from now — feel free \
to reach out.

Best of luck with [Firm Name].

[Your Name]
[Your Phone]""",
    notes="Keep it genuinely warm. No ask. Leaves a good impression.",
)


# ─────────────────────────────────────────────────────────────────────────────
# TRACK 3 — COLD / UNKNOWN (Priority C)
# Single email only. Goal is a response, nothing else.
# ─────────────────────────────────────────────────────────────────────────────

TRACK_3_EMAIL_1 = EmailTemplate(
    track="3_cold",
    step=1,
    day=1,
    channel="email",
    subject_variants=[
        "quick question for [Firm Name]",
        "[First Name] — do you recommend Gusto or QuickBooks to clients?",
        "worth 2 minutes?",
    ],
    body="""\
Hi [First Name],

Quick question: when your small business clients need payroll, are you pointing \
them toward Gusto or QuickBooks?

If so, I'd love two minutes to explain why ADP pays significantly more for those \
referrals — while matching the same price your clients would pay elsewhere.

Fit or not a fit?

[Your Name]
[Your Phone] | [Your Email]""",
    notes=(
        "The question at the end is still the strategy — but now it's Gusto/QB-anchored. "
        "If they say 'yes we recommend Gusto' you have a qualified lead immediately. "
        "If they say 'no' you can still ask what they recommend. Keep it to 3 sentences."
    ),
)


# ─────────────────────────────────────────────────────────────────────────────
# Full sequence maps
# ─────────────────────────────────────────────────────────────────────────────

TRACK_1_SEQUENCE = [
    TRACK_1_EMAIL_1,
    TRACK_1_FOLLOWUP_DM,
    TRACK_1_EMAIL_2,
    TRACK_1_EMAIL_3,
]

TRACK_2_SEQUENCE = [
    TRACK_2_EMAIL_1,
    TRACK_2_FOLLOWUP_DM,
    TRACK_2_EMAIL_2,
    TRACK_2_EMAIL_3,
]

TRACK_3_SEQUENCE = [
    TRACK_3_EMAIL_1,
]

TRACK_MAP = {
    "A": TRACK_1_SEQUENCE,
    "B": TRACK_2_SEQUENCE,
    "C": TRACK_3_SEQUENCE,
}


def get_sequence_for_lead(lead: dict) -> list[EmailTemplate]:
    """Return the correct outreach sequence based on priority tier."""
    priority = lead.get("priority", "C")
    return TRACK_MAP.get(priority, TRACK_3_SEQUENCE)


def render_template(template: EmailTemplate, merge_fields: dict) -> dict:
    """
    Replace merge fields in subject and body.
    merge_fields: {first_name, firm_name, neighborhood}
    Returns {subject, body, channel, day, track, notes}.
    """
    def replace(text: str) -> str:
        text = text.replace("[First Name]", merge_fields.get("first_name", "there"))
        text = text.replace("[Firm Name]", merge_fields.get("firm_name", "your firm"))
        text = text.replace("[Neighborhood]", merge_fields.get("neighborhood", "Brooklyn"))
        text = text.replace("[Competitor]", merge_fields.get("competitor", "Gusto"))
        text = text.replace("[Your Name]", merge_fields.get("your_name", "[Your Name]"))
        text = text.replace("[Your Phone]", merge_fields.get("your_phone", "[Your Phone]"))
        text = text.replace("[Your Email]", merge_fields.get("your_email", "[Your Email]"))
        return text

    rendered_subjects = [replace(s) for s in template.subject_variants]
    rendered_body = replace(template.body)

    return {
        "track": template.track,
        "step": template.step,
        "day": template.day,
        "channel": template.channel,
        "subject_a": rendered_subjects[0] if len(rendered_subjects) > 0 else "",
        "subject_b": rendered_subjects[1] if len(rendered_subjects) > 1 else "",
        "subject_c": rendered_subjects[2] if len(rendered_subjects) > 2 else "",
        "body": rendered_body,
        "notes": template.notes,
    }


def print_all_templates():
    """Print all templates to stdout for review."""
    all_sequences = [
        ("TRACK 1 — GRID/BUYOUT (Priority A)", TRACK_1_SEQUENCE),
        ("TRACK 2 — REVENUE SHARE (Priority B)", TRACK_2_SEQUENCE),
        ("TRACK 3 — COLD OUTREACH (Priority C)", TRACK_3_SEQUENCE),
    ]

    sample_fields = {
        "first_name": "Sarah",
        "firm_name": "Smith Accounting LLC",
        "neighborhood": "Park Slope",
        "your_name": "[Your Name]",
        "your_phone": "[Your Phone]",
        "your_email": "[Your Email]",
    }

    for track_name, sequence in all_sequences:
        print("\n" + "=" * 70)
        print(track_name)
        print("=" * 70)
        for template in sequence:
            rendered = render_template(template, sample_fields)
            print(f"\n--- Step {rendered['step']} | Day {rendered['day']} | {rendered['channel'].upper()} ---")
            if rendered.get("subject_a"):
                print(f"Subject A: {rendered['subject_a']}")
            if rendered.get("subject_b"):
                print(f"Subject B: {rendered['subject_b']}")
            if rendered.get("subject_c"):
                print(f"Subject C: {rendered['subject_c']}")
            print()
            print(rendered["body"])
            print(f"\n[Internal note: {rendered['notes']}]")
