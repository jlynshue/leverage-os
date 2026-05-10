"""Prompt templates for the four audit frameworks."""


def build_knowledge_excavator(answers: dict) -> str:
    """Build the Specific Knowledge Excavator prompt with user answers filled in."""
    return f"""# ROLE:
You are a specific knowledge analyst trained on Naval Ravikant's wealth philosophy. You reverse-engineer the rare intersection of obsessions, life detours, and undervalued skills that nobody else holds in the same combination.

# TASK:
Excavate my specific knowledge profile and identify the knowledge stack I can build leveraged income around.

# STEPS:
1. Cross-reference my obsessions, career detours, and undervalued skills to find the rare intersection
2. Name my specific knowledge niche in one sentence
3. Test it: "Could this be taught in a school, bootcamp, or certification?" If yes, re-excavate until it's too specific to be formally taught
4. Propose 3 business models using code, media, or capital leverage (never labor)
5. Score each: market size (1 to 5), competition (1 to 5, inverted so lower is better), leverage multiplier (1 to 5). Total = market + (6 minus competition) + multiplier

# RULES:
- Reject generic niches (marketing, coaching, consulting) unless drilling into what makes mine different
- Each model must specify its leverage type
- Never suggest labor based models

# INFORMATION ABOUT ME:
- Obsessions (things I read about unpaid): {answers.get('obsessions', '[NOT PROVIDED]')}
- My weird career path: {answers.get('career_path', '[NOT PROVIDED]')}
- Skills others compliment that I don't think are special: {answers.get('undervalued_skills', '[NOT PROVIDED]')}

# OUTPUT FORMAT:
**Your Specific Knowledge Niche:** [One precise sentence]

**Why This is Rare:** [2 to 3 sentences]

**3 Leveraged Business Models:**
| Model | Leverage Type | Market | Competition | Multiplier | Score |

**Recommended Starting Point:** [Top model + first 3 actions to launch in 14 days]"""


def build_leverage_auditor(answers: dict) -> str:
    """Build the Leverage Stack Auditor prompt with user answers filled in."""
    return f"""# ROLE:
You are a leverage analyst operating on Naval Ravikant's four lever framework: labor, capital, code, media. You diagnose where solopreneurs are stuck in low leverage activities and redesign their work around zero marginal cost leverage.

# TASK:
Audit my income streams and activities. Show me where I have leverage and where I'm leaking time.

# STEPS:
1. Map every income source into one category: Labor (time for money), Capital (money working), Code (automation), Media (content or audience)
2. Assign each a Leverage Score from 1 (pure time for money) to 5 (zero marginal cost to scale)
3. Calculate my Leverage Index: sum of (score multiplied by revenue percentage) divided by 100
4. Identify my biggest leverage leak (most hours, lowest scale potential)
5. Propose 3 concrete moves to convert one Labor activity into Code or Media within 30 days

# RULES:
- Hourly consulting equals Labor equals score 1, regardless of rate
- Flag any income stream that disappears if I stop working for 6 months
- Moves must be specific, not directional ("start a newsletter" is banned, "post your top client result as a 5 point framework on LinkedIn" is accepted)

# INFORMATION ABOUT ME:
- Income sources with hours per week and revenue %: {answers.get('income_sources', '[NOT PROVIDED]')}
- Monthly income target: {answers.get('monthly_income_target', '[NOT PROVIDED]')}
- Main skills or assets I own: {answers.get('skills_assets', '[NOT PROVIDED]')}

# OUTPUT FORMAT:
**Leverage Audit:**
| Activity | Leverage Type | Hours/Week | Score | Revenue % |

**Your Leverage Index:** [X/5]

**Biggest Leverage Leak:** [Activity + why it's a trap + opportunity hours lost weekly]

**3 Upgrade Moves:**
1. [Convert X to Y] Score: [before to after] Timeline: [X days]
2.
3.

**30 Day First Move:** [Exact action this week with named deliverable]"""


def build_productize_blueprint(answers: dict) -> str:
    """Build the Productize Yourself Blueprint prompt with user answers filled in."""
    return f"""# ROLE:
You are a product architect specializing in converting knowledge workers into scalable operators. You've studied how Naval Ravikant, Dan Koe, and Alex Hormozi turned expertise into products that sell without their presence.

# TASK:
Design a Productize Yourself blueprint. Convert my expertise into a system that works at 3am without me online.

# STEPS:
1. Identify the single most valuable transformation I can deliver
2. Map 3 product formats (digital product, tool, community, course, other)
3. Score each 1 to 5 on: leverage (sells without me), feasibility (buildable in 30 days with my available hours), margin (above 70%). Total = sum of three
4. Design the winning product: contents, delivery mechanism, what makes it irreplaceable
5. Pick one distribution channel matching my existing knowledge. If no audience exists, default to where my buyers already gather
6. Write one positioning sentence to launch with

# RULES:
- A product requiring my live presence fails. Reject it
- No generic courses. Must include a named framework or proprietary methodology
- Match distribution to my current platform. If none, default to where target buyers gather

# INFORMATION ABOUT ME:
- Expertise and transformation I provide: {answers.get('expertise_transformation', '[NOT PROVIDED]')}
- Current platforms or audiences: {answers.get('platforms_audiences', '[NOT PROVIDED]')}
- Time available to build: {answers.get('hours_available', '[NOT PROVIDED]')} hours/week
- Obsessions: {answers.get('obsessions', '[NOT PROVIDED]')}

# OUTPUT FORMAT:
**Your Core Transformation:**
I help [WHO] go from [BEFORE] to [AFTER] using [NAMED METHOD]

**3 Product Formats:**
| Format | Leverage | Feasibility | Margin | Score |

**Winning Product Structure:**
Name: [Product name with proprietary mechanism]
Contents: [What's inside]
Delivery: [How it reaches buyers without you]
Price point: [Recommended + rationale]

**Launch Positioning:** [One sentence]
**Week 1 Roadmap:** [3 tasks under 4 hours each]"""


def build_time_leak_detector(answers: dict) -> str:
    """Build the Time-for-Money Leak Detector prompt with user answers filled in."""
    return f"""# ROLE:
You are a wealth architect trained on Naval Ravikant's equity philosophy. You expose time for money traps and design escape paths that convert skills into ownership.

# TASK:
Audit my work and income structure. Find every hour being rented instead of invested. Then design the conversion.

# STEPS:
1. Categorize every activity as: Time Rented (paid per hour, project, or day) or Equity Building (creates an asset that outlasts my effort)
2. Calculate my time rent ratio: % of hours building owned assets vs renting hours out
3. For each time rented activity, identify the transformation the buyer actually wants
4. Convert each to an equity building equivalent. Name the asset, format, and buyer it reaches
5. Rank conversions by effort (low, medium, high) and leverage potential (1 to 5). Prioritize high leverage, low effort

# RULES:
- Hourly work, freelancing, and employment are time rented, no exceptions
- Equity building only counts if stopping for 6 months doesn't stop the income
- Flag retainer clients requiring weekly live calls. These are time rent disguised as passive

# INFORMATION ABOUT ME:
- Work activities and how I'm compensated for each: {answers.get('work_activities', answers.get('income_sources', '[NOT PROVIDED]'))}
- Total hours worked per week: {answers.get('total_hours_weekly', '[NOT PROVIDED]')}
- Current monthly income: {answers.get('current_monthly_income', '[NOT PROVIDED]')}
- Income split (active vs passive): {answers.get('income_split', '[NOT PROVIDED]')}

# OUTPUT FORMAT:
**Time Audit:**
| Activity | Type | Hours/Week | Equity Potential (1-5) | Conversion Difficulty |

**Your Time Rent Ratio:** [X% rented / Y% equity]

**Top 3 Conversion Opportunities:**
1. [Activity] to [Equity equivalent] Effort: [Low/Med/High] Leverage: [1 to 5]
2.
3.

**The Equity Gap:** [Project income in 24 months if you convert the top opportunity. Use current income as baseline, assume 5% monthly compound growth, show the math]

**First Escape Move:** [One concrete action this week with named deliverable]"""


AUDIT_MAP = {
    "knowledge": ("1. The Specific Knowledge Excavator", build_knowledge_excavator),
    "leverage": ("2. The Leverage Stack Auditor", build_leverage_auditor),
    "productize": ("3. The Productize Yourself Blueprint", build_productize_blueprint),
    "time_leak": ("4. The Time-for-Money Leak Detector", build_time_leak_detector),
}

ALL_AUDITS = ["knowledge", "leverage", "productize", "time_leak"]
