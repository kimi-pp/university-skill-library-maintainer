---
name: indie-business-ops
description: Business operations framework for indie iOS/macOS developers. Use when the user wants to understand business structures (LLC, sole proprietorship), tax implications, bookkeeping, legal considerations, or operational aspects of running an indie app business.
---

# Indie Business Operations Skill

Business operations framework for indie iOS/macOS developers. Use this skill when the user wants to understand business structures (LLC, sole proprietorship), tax implications, bookkeeping, legal considerations, or operational aspects of running an indie app business.

## When to Use This Skill

Trigger on phrases like "LLC", "business structure", "taxes", "self-employment tax", "S-corp", "bookkeeping", "track expenses", "business account", "tax deductions", "should I form a company", or any questions about the business side of indie app development.

**Important Note**: This skill provides educational information, not legal or tax advice. The user's situation may vary significantly based on location, revenue, and personal circumstances. Always recommend consulting a CPA or attorney for specific decisions.

## Business Structure Decision Framework

### Sole Proprietorship (Default)

When you earn money from your app without forming a legal entity, you're automatically a sole proprietor.

**Characteristics**:
- No formal registration required (except business license in some jurisdictions)
- Personal name appears as seller in App Store
- All income reported on personal tax return (Schedule C)
- No liability protection—personal assets at risk

**Best for**:
- Just starting out, validating ideas
- Revenue under $1,000/month
- Minimal legal risk
- Keeping things simple

**App Store Implications**: Apple allows individual/sole proprietor accounts. Your personal name shows as the "seller."

### Limited Liability Company (LLC)

A separate legal entity that provides liability protection while maintaining tax simplicity.

**Advantages**:
- Limited liability: Personal assets protected from business debts/lawsuits
- Credibility: Company name appears in App Store
- Tax flexibility: Can elect different tax treatments
- Relatively simple to maintain

**Disadvantages**:
- Formation costs: $50-500+ depending on state
- Annual fees: Many states charge annual registration fees
- More recordkeeping required
- May need registered agent service ($50-300/year)

**When to Consider LLC**:
- Consistent revenue over $1,000/month
- Customer-facing products with potential liability
- Want company name in App Store
- Peace of mind about personal asset protection

### S-Corporation Election

Not a business structure—it's a tax election that an LLC (or corporation) can make with the IRS.

**How It Works**:
- Business owners pay themselves a "reasonable salary"
- Remaining profits distributed as dividends
- Dividends not subject to self-employment tax (15.3%)

**Example**:
LLC generates $120,000/year profit:
- Without S-Corp: ~$18,000 in self-employment tax
- With S-Corp (paying $70,000 salary): ~$10,700 in payroll taxes
- Potential savings: ~$7,000+

**When S-Corp Makes Sense**:
- Consistent profits above $50,000-60,000/year after expenses
- Below this threshold, added complexity rarely justifies savings
- Requires paying yourself a "reasonable salary" (IRS scrutinizes)
- Additional payroll administration

**Added Complexity**:
- Must run payroll (even just for yourself)
- Quarterly payroll tax filings
- Annual S-Corp return (Form 1120-S)
- Accounting costs increase

### C-Corporation

Full corporate structure with separate taxation.

**Characteristics**:
- Corporation pays corporate income tax
- Shareholders pay tax on dividends ("double taxation")
- Most complex structure

**When Relevant**:
- Planning to raise venture capital
- Going public someday
- Rarely appropriate for indie developers

### Decision Flowchart

```
Are you making consistent revenue?
├─ No → Sole proprietorship (keep it simple)
└─ Yes → Do you want liability protection?
    ├─ No → Sole proprietorship
    └─ Yes → Form an LLC
        └─ Are profits > $50k/year?
            ├─ No → Stay as standard LLC
            └─ Yes → Consult CPA about S-Corp election
```

## Tax Fundamentals

### Income Tax

Revenue minus legitimate business expenses equals taxable income.

**Example**:
- Revenue: $50,000
- Expenses (software, hardware, services): $10,000
- Taxable income: $40,000

You pay income tax based on your tax bracket on this amount.

### Self-Employment Tax (US)

Sole proprietors and LLC members pay both employer and employee portions of Social Security and Medicare.

**Rate**: 15.3% (12.4% Social Security + 2.9% Medicare) on net profit

**Example**: $40,000 net profit = ~$6,120 in self-employment tax (in addition to income tax)

This is why S-Corp election becomes attractive at higher profit levels.

### Quarterly Estimated Taxes

Unlike employees who have taxes withheld, self-employed individuals must pay estimated taxes quarterly.

**Due Dates** (US):
- Q1: April 15
- Q2: June 15
- Q3: September 15
- Q4: January 15

**Penalty Avoidance**: Pay at least 100% of last year's tax liability (110% if high income) or 90% of current year's liability.

### Common Deductible Expenses

**Definitely Deductible**:
- Apple Developer Program fee ($99/year)
- Software subscriptions (development tools, design software, analytics)
- Hardware purchased for development
- Cloud hosting and services
- Professional services (accounting, legal)
- Business portion of home office
- Business internet and phone
- Continuing education (courses, books, conferences)

**Partially Deductible**:
- Computer used for both personal and business
- Home office (if dedicated space meets IRS requirements)
- Internet/phone (business use percentage)

**Startup Costs**:
- IRS allows up to $5,000 deduction in first year (if total startup costs under $50,000)
- Remainder amortized over 15 years

### International Considerations

If you're not in the US, tax treatment varies significantly by country. Key considerations:

**VAT/GST**: Many countries require collecting and remitting value-added tax. Apple handles this for App Store purchases but not for other revenue sources.

**Digital Services Taxes**: Some jurisdictions have specific taxes on digital services.

**Tax Treaties**: May affect how income is taxed across borders.

**Professional Advice Essential**: International tax is complex—get local professional guidance.

## Bookkeeping Basics

### Why Bother

Good bookkeeping:
- Makes tax time dramatically easier
- Helps you understand business health
- Required if you want to raise money or sell the business
- Catches problems early

### Minimum Viable Bookkeeping

**Separate Bank Account**:
Create a dedicated business checking account. Never mix personal and business funds.

**Track All Income**:
- App Store sales (download from App Store Connect)
- Other revenue sources (consulting, sponsorships)
- RevenueCat or similar provides detailed reports

**Track All Expenses**:
- Save receipts (digitally is fine)
- Categorize consistently
- Note business purpose

**Monthly Review**:
Spend 30 minutes monthly reconciling accounts and reviewing numbers.

### Bookkeeping Tools

**Wave** (Free):
- Free accounting software
- Basic invoicing
- Connects to bank accounts
- Good for simple businesses

**Xero** (Starts ~$12/month):
- More robust features
- 1,000+ integrations
- Better reporting
- Good for growing businesses

**QuickBooks** (Starts ~$15/month):
- Industry standard
- Extensive features
- Large ecosystem
- Can handle complex needs

**Spreadsheet**:
For very simple businesses, a well-organized spreadsheet works. But dedicated software is better as you grow.

### When to Hire Help

Consider professional bookkeeping when:
- Revenue exceeds $50,000-100,000/year
- Multiple income streams
- International customers (VAT complexity)
- You're spending hours on bookkeeping instead of building

## Legal Considerations

### App Store Compliance

**Apple Developer Agreement**:
- Read it (seriously)
- Understand prohibited behaviors
- Subscription auto-renewal requirements
- Privacy policy requirements

**Privacy Policy**:
Required for any app that collects data. Must be publicly accessible.

**Terms of Service**:
Recommended for any app with accounts or user-generated content.

### Intellectual Property

**Your Code**: You own code you write. Use version control as evidence of creation.

**Open Source**: Understand licenses of libraries you use. Some require attribution, some have restrictions on commercial use.

**Trademarks**: Consider registering your app name if it becomes valuable. At minimum, search existing trademarks before naming.

**App Store Screenshots**: Using other apps' screenshots or UI may violate their IP.

### User Data

**GDPR** (EU): Applies if you have EU users. Requires consent for data collection, right to deletion, etc.

**CCPA** (California): Similar requirements for California residents.

**Apple's Privacy Nutrition Labels**: Must accurately describe data collection in App Store.

**Best Practice**: Collect minimal data, be transparent about usage, provide deletion mechanism.

## Revenue Tracking for App Developers

### App Store Revenue

**App Store Connect**:
- Download financial reports monthly
- Reports show sales, taxes withheld, net payments
- Keep historical data for tax purposes

**RevenueCat Dashboard**:
- Real-time subscription metrics
- More granular than App Store Connect
- Integrates with analytics

### Multi-Country Considerations

Apple handles:
- Currency conversion
- Many local taxes (VAT, GST)
- Payment processing

You receive consolidated USD (or your chosen currency) payments.

### Revenue Recognition

**Cash Basis** (Simpler): Record revenue when received
**Accrual Basis** (More accurate): Record revenue when earned

Most indie developers use cash basis. Switch to accrual if you get serious or need investors.

## Getting Started Checklist

### Day One

1. Open separate business bank account
2. Start tracking expenses from day one
3. Save receipts digitally (photo apps work)

### When You Start Making Money

4. Understand estimated tax requirements
5. Set aside 25-30% of revenue for taxes
6. Consider accounting software

### When Revenue Becomes Consistent ($1K+/month)

7. Research LLC formation in your state
8. Consult with CPA about structure
9. Formalize bookkeeping process

### When Profits Grow ($50K+/year)

10. Discuss S-Corp election with CPA
11. Consider professional bookkeeping
12. Review business insurance options

## Tools Summary

**Formation**:
- Your state's Secretary of State website (DIY)
- Stripe Atlas ($500, Delaware LLC/C-Corp)
- LegalZoom, Bizee, Northwest Registered Agent (full service)

**Bookkeeping**:
- Wave (free)
- Xero (~$12/month)
- QuickBooks (~$15/month)

**Revenue Tracking**:
- RevenueCat (free tier available)
- App Store Connect (free, required)

**Tax Preparation**:
- TurboTax, H&R Block (consumer)
- CPA for complex situations

## Common Mistakes

**Mistake**: Not separating business and personal finances
**Fix**: Open business bank account immediately

**Mistake**: Not saving for taxes
**Fix**: Set aside 25-30% of all revenue

**Mistake**: Forming LLC too early
**Fix**: Wait until you have meaningful revenue

**Mistake**: Forming LLC in Delaware when you don't need to
**Fix**: Home state is usually simplest unless specific reasons

**Mistake**: DIY-ing complex tax decisions
**Fix**: $500 for CPA consultation is worth it for S-Corp decisions

**Mistake**: Over-optimizing for tax savings early
**Fix**: Time is better spent building product than minimizing small tax bills

## When to Get Professional Help

**CPA/Accountant**:
- Revenue exceeds $50,000/year
- Considering S-Corp election
- Multiple income streams
- International customers
- Any confusion about taxes

**Attorney**:
- LLC formation (optional—many DIY successfully)
- Partnership agreements
- Complex contracts
- IP concerns

**Registered Agent**:
- Required in most states for LLC
- Receives legal documents on behalf of business
- Services cost $50-300/year

## References

- IRS Publication 334: Tax Guide for Small Business
- IRS Publication 535: Business Expenses
- State Secretary of State websites (LLC formation)
- Calmops Indie Hacker Tax Guide
- TRUiC LLC Formation Guide
