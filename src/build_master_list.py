"""
Build master ranked prospect list from all research output files.
Scoring system (100 points max):
  - Payroll confirmed explicit: +25
  - Payroll implied/listed: +10
  - Solo/1-5 employees: +15  |  6-25: +8  |  26+: +2
  - Founded 2015+: +15  |  2010-2014: +8  |  pre-2010: +3
  - Gusto/QBO partner confirmed: +15
  - Phone confirmed: +8
  - Email confirmed: +7
  - Track 1 (direct processor): +10 bonus
  - Gusto partner: additional +5
  - Source confidence HIGH: +5  |  MEDIUM: +2
"""

import csv
import re
import os

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'output')

def score_firm(row):
    score = 0
    notes = []

    # Payroll confirmation
    payroll = str(row.get('Payroll Confirmed', row.get('payroll_confirmed', ''))).upper()
    if 'YES' in payroll or 'EXPLICIT' in payroll:
        score += 25
        notes.append('payroll_confirmed')
    elif 'IMPLIED' in payroll or 'LISTED' in payroll or 'POSSIBLE' in payroll:
        score += 10
        notes.append('payroll_implied')

    # Employee size
    emp = str(row.get('Employee Signal', row.get('Headcount', row.get('Employees', row.get('Firm Size Signal', ''))))).lower()
    if any(x in emp for x in ['solo', '1-3', '1-5', '2-5', '2-3', '3-5', '1 employee', 'sole']):
        score += 15
        notes.append('solo_ideal')
    elif any(x in emp for x in ['5-15', '5-25', '6-15', '10-19', '10-25', '12', '15', '17', '18', '20']):
        score += 8
        notes.append('small_team')
    elif any(x in emp for x in ['25+', '26+', '50', '21-50']):
        score += 2

    # Founded year
    founded = str(row.get('Founded', row.get('Year Founded', row.get('year_founded', '')))).lower()
    year_match = re.search(r'(20\d\d)', founded)
    if year_match:
        yr = int(year_match.group(1))
        if yr >= 2015:
            score += 15
            notes.append('new_firm')
        elif yr >= 2010:
            score += 8
            notes.append('mid_age_firm')
        else:
            score += 3
    else:
        score += 3  # unknown = give benefit of doubt

    # Gusto/tech partner
    gusto = str(row.get('Gusto Partner', row.get('QB ProAdvisor', row.get('Software Detected', '')))).upper()
    if 'GUSTO' in gusto and ('CONFIRMED' in gusto or 'YES' in gusto or 'PARTNER' in gusto):
        score += 20
        notes.append('gusto_partner')
    elif 'GUSTO' in gusto:
        score += 12
        notes.append('gusto_user')
    elif 'QUICKBOOKS' in gusto or 'QBO' in gusto or 'PROADVISOR' in gusto:
        score += 8
        notes.append('qbo_user')

    # Contact quality
    phone = str(row.get('Phone', '')).strip()
    if phone and phone not in ['Not confirmed', 'Not found', 'Via website', 'N/A', '', 'nan']:
        score += 8
        notes.append('phone_confirmed')

    email = str(row.get('Email', '')).strip()
    if '@' in email:
        score += 7
        notes.append('email_confirmed')

    # Track bonus
    track = str(row.get('Track', row.get('Recommended Track', ''))).upper()
    if 'TRACK 1' in track or 'GRID' in track or 'BUYOUT' in track:
        score += 10
        notes.append('track1')

    # Confidence bonus
    conf = str(row.get('Source Confidence', row.get('Confidence', ''))).upper()
    if 'HIGH' in conf:
        score += 5
    elif 'MEDIUM' in conf:
        score += 2

    return score, notes


def get_field(row, *keys):
    for k in keys:
        v = str(row.get(k, '')).strip()
        if v and v.lower() not in ['nan', 'n/a', 'not found', 'not confirmed', '']:
            return v
    return ''


def load_file(filepath, source_label):
    firms = []
    try:
        with open(filepath, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                name = get_field(row, 'Firm Name', 'firm_name', 'Name')
                if not name or name.lower() in ['nan', '']:
                    continue
                # Skip placeholder/duplicate rows
                if any(x in name.lower() for x in ['see #', 'already listed', 'see firm', '(see ', 'n/a']):
                    continue

                score, score_notes = score_firm(row)

                firm = {
                    'Firm Name': name,
                    'Owner': get_field(row, 'Owner Name', 'Owner', 'owner_name', 'Principal'),
                    'Phone': get_field(row, 'Phone', 'phone'),
                    'Email': get_field(row, 'Email', 'email'),
                    'Website': get_field(row, 'Website', 'website'),
                    'Address': get_field(row, 'Address', 'address'),
                    'ZIP': get_field(row, 'ZIP', 'zip'),
                    'Founded': get_field(row, 'Founded', 'Year Founded', 'founded'),
                    'Headcount': get_field(row, 'Employee Signal', 'Headcount', 'Employees', 'Firm Size Signal'),
                    'Payroll Confirmed': get_field(row, 'Payroll Confirmed', 'payroll_confirmed'),
                    'Software': get_field(row, 'Software Detected', 'Payroll Software Detected', 'Software'),
                    'Gusto Partner': get_field(row, 'Gusto Partner'),
                    'Track': get_field(row, 'Track', 'Recommended Track'),
                    'Opening Line': get_field(row, 'Best Opening Line', 'opening_line'),
                    'Best Contact': get_field(row, 'Best Contact Method', 'best_contact'),
                    'Risk Flags': get_field(row, 'Risk Flags', 'risk_flags'),
                    'Confidence': get_field(row, 'Source Confidence', 'Confidence'),
                    'Category': get_field(row, 'Category', 'Caribbean / Community Signal', 'Gusto Partner'),
                    'Score': score,
                    'Score Notes': ' | '.join(score_notes),
                    'Source File': source_label,
                }
                firms.append(firm)
    except Exception as e:
        print(f"  Warning: could not load {filepath}: {e}")
    return firms


def assign_tier(score):
    if score >= 75:
        return 'TIER 1 — ACT NOW'
    elif score >= 55:
        return 'TIER 2 — HIGH PRIORITY'
    elif score >= 35:
        return 'TIER 3 — MEDIUM PRIORITY'
    else:
        return 'TIER 4 — QUALIFY FIRST'


def main():
    files = [
        ('research_identified_targets.csv', 'Deep Research Targets'),
        ('solo_centers_of_influence_targets.csv', 'Solo / Gusto Partners'),
        ('caribbean_haitian_brooklyn_targets.csv', 'Caribbean / Haitian Community'),
        ('naics_541219_new_targets.csv', 'NAICS 541219 New Finds'),
        ('non_accountant_targets.csv', 'Non-Accountant Partners'),
        ('never_referring_ranked.csv', 'Salesforce — Never Referring'),
        ('previously_referring_ranked.csv', 'Salesforce — Previously Referring'),
        ('agent_research_new_finds.csv', 'Multi-Agent Deep Research'),
    ]

    all_firms = []
    for filename, label in files:
        path = os.path.join(OUTPUT_DIR, filename)
        loaded = load_file(path, label)
        print(f"  {label}: {len(loaded)} firms")
        all_firms.extend(loaded)

    # Deduplicate by firm name (normalized)
    seen = {}
    deduped = []
    for firm in all_firms:
        key = re.sub(r'[^a-z0-9]', '', firm['Firm Name'].lower())[:25]
        if key not in seen:
            seen[key] = True
            deduped.append(firm)

    # Manual overrides based on research context
    overrides = {
        'innovativeaccountingsolutions': 98,   # 106 confirmed Gusto clients — highest referral volume in Brooklyn
        'profitasllc': 92,                      # 100+ clients, Gusto partner, Park Slope
        'payrollhelpllc': 89,                   # 29 Gusto clients, medical niche
        'sdocpa': 18,                           # Confirmed active Gusto ADVOCATE — lowest conversion probability
        'taxtargetgroupllc': 95,               # 1,100+ business clients — largest book value
        'citipayrollservices': 94,              # IS a payroll bureau — textbook Grid target
        'jeanclaudedenisincometax': 96,         # Haitian community institution, 44 years, explicit payroll
        'mcbtax': 92,                           # Haitian directory listed x2, explicit payroll
    }
    for firm in deduped:
        key = re.sub(r'[^a-z0-9]', '', firm['Firm Name'].lower())[:30]
        for override_key, override_score in overrides.items():
            if key.startswith(override_key[:15]):
                firm['Score'] = override_score
                if override_score < 30:
                    firm['Score Notes'] += ' | MANUAL_DEPRIORITIZED'
                else:
                    firm['Score Notes'] += ' | MANUAL_BOOSTED'
                break

    # Sort by score descending
    deduped.sort(key=lambda x: x['Score'], reverse=True)

    # Add rank and tier
    for i, firm in enumerate(deduped, 1):
        firm['Master Rank'] = i
        firm['Tier'] = assign_tier(firm['Score'])

    print(f"\n  Total unique firms: {len(deduped)}")

    # Write master CSV
    out_path = os.path.join(OUTPUT_DIR, 'master_ranked_all_firms.csv')
    fieldnames = [
        'Master Rank', 'Tier', 'Score', 'Firm Name', 'Owner', 'Phone', 'Email',
        'Website', 'Address', 'ZIP', 'Founded', 'Headcount', 'Payroll Confirmed',
        'Software', 'Gusto Partner', 'Track', 'Opening Line', 'Best Contact',
        'Risk Flags', 'Confidence', 'Source File', 'Score Notes',
    ]
    with open(out_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(deduped)

    print(f"  Written to: {out_path}")

    # Print tier summary
    from collections import Counter
    tier_counts = Counter(f['Tier'] for f in deduped)
    print("\n  TIER BREAKDOWN:")
    for tier in ['TIER 1 — ACT NOW', 'TIER 2 — HIGH PRIORITY', 'TIER 3 — MEDIUM PRIORITY', 'TIER 4 — QUALIFY FIRST']:
        print(f"    {tier}: {tier_counts.get(tier, 0)} firms")

    # Print top 20
    print("\n  TOP 20 FIRMS:")
    print(f"  {'Rank':<5} {'Score':<6} {'Firm':<45} {'Source'}")
    print("  " + "-"*95)
    for f in deduped[:20]:
        print(f"  {f['Master Rank']:<5} {f['Score']:<6} {f['Firm Name'][:44]:<45} {f['Source File']}")


if __name__ == '__main__':
    print("Building master ranked list...")
    main()
