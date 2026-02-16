"""
ADVANCED ENTERPRISE SECURITY ARCHITECTURE WORKSHOP
Professional Training Platform - Teaching Real Architecture Judgment

This platform teaches WHAT MAKES A GOOD ARCHITECT:
- Trade-off decision making under constraints
- Quantifying risk in business terms
- Communicating technical decisions to executives
- Designing systems that remain secure when controls fail
- Navigating organizational politics and legacy debt
"""

import streamlit as st
import json
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
from typing import Dict, List, Optional
import hashlib

st.set_page_config(
    page_title="Enterprise Security Architect Masterclass",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# PROFESSIONAL STYLING
# ============================================================================

st.markdown("""
<style>
    .main-header { 
        font-size: 2.5rem; 
        font-weight: 700; 
        color: #1e293b; 
        margin-bottom: 0.5rem; 
    }
    .scenario-critical {
        background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
        border-left: 6px solid #dc2626;
        padding: 2rem;
        border-radius: 10px;
        margin: 1.5rem 0;
        box-shadow: 0 4px 12px rgba(220, 38, 38, 0.2);
    }
    .scenario-critical h3 { color: #991b1b; margin-top: 0; }
    
    .architect-insight {
        background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
        border-left: 6px solid #2563eb;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1.5rem 0;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2);
    }
    .architect-insight h4 { color: #1e40af; margin-top: 0; }
    
    .trade-off-analysis {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        border-left: 6px solid #f59e0b;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .decision-matrix {
        background: white;
        border: 2px solid #e5e7eb;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    .expert-critique {
        background: #f9fafb;
        border-left: 4px solid #6366f1;
        padding: 1rem;
        margin: 1rem 0;
        font-style: italic;
    }
    
    .common-mistake {
        background: #fef2f2;
        border-left: 4px solid #ef4444;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    
    .best-practice {
        background: #f0fdf4;
        border-left: 4px solid #22c55e;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    
    .architectural-principle {
        background: #f5f3ff;
        border: 2px solid #8b5cf6;
        border-radius: 8px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    
    .risk-quantification {
        background: linear-gradient(135deg, #f0fdfa 0%, #ccfbf1 100%);
        border-left: 6px solid #14b8a6;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# SESSION STATE
# ============================================================================

def init_state():
    defaults = {
        'current_day': 1,
        'current_section': 1,
        'completed_exercises': [],
        'work': {
            'complexity_analysis': {},
            'ma_integration': {},
            'arb_decisions': {},
            'governance_design': {},
            'toolchain': {},
            'pasta_models': {},
            'supply_chain': {},
            'k8s_threats': {},
            'compliance_architecture': {},
            'policy_code': {},
            'audit_evidence': {},
            'ma_playbook': {},
            'tech_debt': {},
            'multicloud': {},
            'zero_trust': {},
            'beyondcorp': {},
            'legacy_zt': {},
            'attack_surface': {},
            'threat_intel': {},
            'red_team': {},
            'c4_diagrams': {},
            'adrs': {},
            'board_decks': {},
            'fair_analysis': {},
            'breach_comms': {},
            'hiring': {},
            'arb_model': {},
            'kpis': {},
            'capstone': {}
        },
        'scores': {},
        'insights_unlocked': []
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# ============================================================================
# ARCHITECTURAL WISDOM DATABASE
# ============================================================================

ARCHITECTURAL_PRINCIPLES = {
    "constraints_not_blank_slate": """
**Fundamental Truth: You're Not Designing on a Blank Slate**

Junior architects say: "We should use the best technology"
Senior architects say: "Given these constraints, here's the optimal solution"

Constraints you WILL face:
- Technical: 10-year-old mainframes you can't replace ($5M/month revenue depends on them)
- Political: CTO's personal relationship with Oracle (3-year contract, $2M/year)
- Organizational: 15 teams, each with different standards, none willing to change
- Financial: Security budget is 1% of revenue, not the 3% you need
- Timeline: Board wants it done in 90 days, you know it needs 12 months

**The Architect's Job:** Make the best decision WITHIN these constraints, document what you're NOT doing and why, and get executive sign-off on accepted risks.
""",
    
    "defense_in_depth": """
**Defense-in-Depth: Designing for Control Failure**

Amateur thinking: "We have a firewall, we're secure"
Architect thinking: "When the firewall is bypassed, what catches the attacker?"

Real architecture question: "What happens when THIS control fails?"

Example: Payment API Security
- Layer 1: WAF blocks 95% of attacks → 5% get through
- Layer 2: API Gateway validates JWT → Token theft bypasses this
- Layer 3: Application validates tenant_id → Code bug might bypass
- Layer 4: Database RLS enforces isolation → Privilege escalation bypasses
- Layer 5: Encryption at rest → Compromised credentials bypass
- Layer 6: Anomaly detection → Alerts on unusual patterns

**Critical Architecture Principle:** 
No single control is perfect. Design assuming EACH control will fail.
Calculate residual risk at each layer.
""",

    "quantify_everything": """
**Quantify Risk in Dollars, Not High/Medium/Low**

Board doesn't understand "Critical vulnerability"
Board DOES understand "$15.5M annual expected loss"

Use FAIR Model:
- TEF (Threat Event Frequency): How many times per year?
- Vulnerability: What % of attacks succeed?
- LEF (Loss Event Frequency): TEF × Vulnerability
- SLE (Single Loss Expectancy): Cost if it happens once
- ALE (Annual Loss Expectancy): LEF × SLE

Example: Ransomware Risk
- TEF: 50 attempts/year (industry average)
- Vulnerability: 10% success (with current controls)
- LEF: 5 successful attacks/year
- SLE: $12.3M per incident (response, downtime, fines, churn)
- ALE: $61.5M/year

Then calculate control ROI:
- Control cost: $10M + $2M/year
- Risk reduction: 10% → 2% (80% reduction)
- New ALE: $12.3M
- Savings: $49.2M/year
- ROI: 472% first year

**Present to board:** "For $10M investment, we reduce risk by $49.2M annually. 472% ROI."
""",

    "document_why": """
**Architecture Decision Records: The "Why" Matters More Than "What"**

Bad ADR: "We will use Kubernetes"
Good ADR: "We chose Kubernetes over ECS because..."

Every ADR must have:
1. **Context:** Current state, problem statement
2. **Decision:** What we're doing (clear, unambiguous)
3. **Alternatives Considered:** What we rejected and why
4. **Consequences:** Trade-offs (positive AND negative)
5. **Risks:** What could go wrong + mitigations
6. **Compliance Mapping:** How this meets regulations
7. **Rollback Plan:** How to undo if this fails
8. **Review Date:** When to re-evaluate

**Why this matters:**
- 6 months later, someone asks "why did we do this?"
- Compliance audit asks "show me your decision rationale"
- New architect wants to change it (needs to understand the constraints)
- Control fails, need to know what was considered

The ADR is your insurance policy against "why didn't you consider X?" questions.
"""
}

EXPERT_CRITIQUES = {
    "ma_integration_common_failures": """
**Expert Critique: Why M&A Integrations Fail**

❌ **Failure Mode 1: Trying to Do Everything**
Mistake: "We'll migrate their IAM, consolidate monitoring, redesign their architecture, and retire their data center in 90 days"
Reality: You'll fail at all of it.

✅ **Architect Approach:**
Phase 1: Stabilization (don't make it worse)
Phase 2: Integration (converge on common patterns)
Phase 3: Optimization (cost savings)

Defer anything non-critical. Document what you're NOT doing.

❌ **Failure Mode 2: Ignoring Political Reality**
Mistake: "Their architecture is terrible, we're replacing everything"
Reality: Their team will resist, their CTO will escalate, you'll get overruled.

✅ **Architect Approach:**
"Their architecture made sense in 2019 given their constraints. Here's how we'll modernize while respecting what works."

Find champions in their organization. Make them part of the solution.

❌ **Failure Mode 3: No Risk Register**
Mistake: Assume everything will work perfectly
Reality: Authentication will break, users will be locked out, systems will fail.

✅ **Architect Approach:**
- Document 20+ risks with likelihood and impact
- Define rollback procedures for each phase
- Get executive sign-off on accepted risks
- Plan for 30% help desk ticket increase

❌ **Failure Mode 4: Forgetting Compliance**
Mistake: Migrate first, think about SOC 2 later
Reality: You invalidate their compliance, fail your next audit.

✅ **Architect Approach:**
- Review their SOC 2 report before touching anything
- Understand which controls can't be changed during integration
- Plan compliance consolidation (don't break theirs before fixing it)
- Consider delaying audit renewal if integration is mid-cycle
""",

    "threat_model_mistakes": """
**Expert Critique: Why Threat Models Fail**

❌ **Mistake 1: Focusing on Theoretical Threats**
Amateur: "What if a nation-state attacks us?"
Architect: "What's the business impact of credential stuffing (happens daily)?"

**Reality Check:**
- Nation-state attack: 0.01% probability, you can't prevent it anyway
- Credential stuffing: 15% probability, $5M impact, controllable

**Architect Principle:** Focus on HIGH PROBABILITY threats you can actually mitigate.

❌ **Mistake 2: Not Mapping to Business Impact**
Amateur: "SQL injection vulnerability (CVSS 9.8)"
Architect: "SQL injection could expose 50K records = $500K fine + $2M churn = $2.5M loss"

Board doesn't care about CVSS scores. Board cares about dollars.

❌ **Mistake 3: Ignoring Insider Threats**
Amateur: "All threats are external attackers"
Architect: "What if an SRE with production access goes rogue?"

**Reality:** 
- External breach: Attacker needs to bypass 5 layers
- Insider threat: Already inside, has credentials, knows the systems

Design for insider threat: Least privilege, separation of duties, audit all privileged access.

❌ **Mistake 4: Single Control Failure**
Amateur: "We have RLS, tenant isolation is solved"
Architect: "If RLS has a bug, what's the second line of defense?"

**Every control has failure modes:**
- RLS policy typo → Fails open → Cross-tenant access
- RLS performance issue → Team disables it → No isolation
- RLS privilege escalation → Superuser bypasses → Admin sees all data

**Architect Solution:** App-level validation + RLS + encryption + anomaly detection
""",

    "zero_trust_reality": """
**Expert Critique: Zero Trust Implementation Reality**

❌ **Marketing Myth:** "Buy our Zero Trust product!"
✅ **Architecture Reality:** Zero Trust is a 2-3 year journey, not a product.

**NIST SP 800-207 Maturity Levels:**

**Level 0: Traditional (where you are)**
- VPN = inside the network = trusted
- Perimeter security (firewall)
- No encryption inside
- Broad access once authenticated

**Level 1: Basic (6 months, $500K)**
- MFA for all access
- Network segmentation
- Some device health checks
- Still trust-based on network location

**Level 2: Intermediate (12-18 months, $2M)**
- Identity-centric (not network-centric)
- Device posture enforcement
- Micro-segmentation
- Just-in-time access
- Encryption everywhere (mTLS)

**Level 3: Advanced (24-36 months, $5M)**
- Continuous authentication
- Behavioral analytics (UEBA)
- Data-centric security
- Policy-as-code (automated)
- Full visibility (100% traffic logged)

**Architect Reality Check:**

Board says: "Implement Zero Trust this year"
Architect says: "We can reach Level 1 this year ($500K), Level 2 in 18 months ($2M total). Level 3 is a 3-year journey."

**Don't promise Level 3 in 6 months. You'll fail, get fired, and the next architect will start over.**

**Phased Approach:**
- Q1-Q2: MFA everywhere, pilot micro-segmentation
- Q3-Q4: Device management, basic posture checks
- Year 2: Identity-centric access, mTLS service mesh
- Year 3: Continuous auth, behavioral analytics

Document this timeline. Get executive buy-in. Track progress quarterly.
"""
}

# ============================================================================
# DEEP CONTENT - DAY 1, SESSION 1.1.1
# ============================================================================

def render_day1_s1_1():
    """What's Different at Enterprise Scale - DEEP CONTENT"""
    
    st.markdown('<h1 class="main-header">1.1.1: What\'s Different at Enterprise Scale?</h1>', unsafe_allow_html=True)
    
    # Critical Framing
    st.markdown("""
    <div class="scenario-critical">
    <h3>⚠️ The Architect's Fundamental Challenge</h3>
    <p><strong>Junior thinking:</strong> "Design the perfect architecture"</p>
    <p><strong>Senior thinking:</strong> "Make the best decision given constraints I didn't choose"</p>
    <br>
    <p><strong>Your job as architect:</strong> Navigate technical debt, political debt, organizational chaos, and conflicting regulations while delivering something that actually works.</p>
    <p><strong>Success metric:</strong> Not perfection. It's a solution that survives contact with reality.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Architectural Principle
    st.markdown("""
    <div class="architectural-principle">
    <h4>🏛️ Architectural Principle: Constraints Define Architecture</h4>
    """ + ARCHITECTURAL_PRINCIPLES['constraints_not_blank_slate'] + """
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Exercise 1: Real Complexity Analysis
    st.subheader("📝 Exercise 1: Enterprise Complexity Analysis")
    
    st.markdown("""
    <div class="architect-insight">
    <h4>🎯 What Makes This Exercise Different</h4>
    <p>This isn't about listing tools. It's about understanding:</p>
    <ul>
        <li><strong>Why</strong> the debt exists (history, not just "bad decisions")</li>
        <li><strong>Who</strong> benefits from keeping it (political reality)</li>
        <li><strong>What</strong> would break if you changed it (blast radius)</li>
        <li><strong>How much</strong> it would cost to fix (TCO vs risk)</li>
    </ul>
    <p><strong>Architect skill being tested:</strong> Can you diagnose the patient before prescribing pills?</p>
    </div>
    """, unsafe_allow_html=True)
    
    tabs = st.tabs(["📋 Your Analysis", "✅ Expert Example", "💡 How to Think Like an Architect"])
    
    with tabs[0]:
        st.write("### Document Your Enterprise Complexity")
        
        # Technical Debt - With Guidance
        st.write("#### 1. Technical Debt Analysis")
        st.caption("Don't just list systems. For each, document: Why it exists, Revenue dependency, Replacement cost, Replacement risk")
        
        tech_debt_data = {
            'System': st.text_input("Legacy System Name:", key="td_sys"),
            'Age': st.number_input("Years in production:", 1, 50, 10, key="td_age"),
            'Revenue_Dependency': st.text_input("Revenue at risk if it fails ($M/month):", key="td_rev"),
            'Why_Cant_Replace': st.text_area("Why can't you replace it?", key="td_why", height=100),
            'Replacement_Cost': st.text_input("Estimated replacement cost ($M):", key="td_cost"),
            'Replacement_Timeline': st.text_input("Realistic timeline (months):", key="td_time")
        }
        
        if st.button("💾 Save Technical Debt Analysis"):
            st.session_state.work['complexity_analysis']['technical_debt'] = tech_debt_data
            st.success("✅ Technical debt analysis saved!")
        
        st.markdown("---")
        
        # Political Debt - With Guidance
        st.write("#### 2. Political Debt Analysis")
        st.caption("Document the politics around decisions. Who made them? Who defends them? What's their leverage?")
        
        political = st.text_area(
            "Political constraints (be honest, this is confidential):",
            height=150,
            placeholder="""Example:
- CTO mandated Oracle (personal relationship with account team, 10+ year history)
- VP Engineering refuses to migrate off monolith (built it in 2015, sees it as legacy)
- Board member is former AWS executive (pressure to use AWS, even where not optimal)
- Compliance exception granted by previous CISO (now with different company, current team inherited it)""",
            key="political_debt"
        )
        
        if political:
            st.session_state.work['complexity_analysis']['political_debt'] = political
        
        st.markdown("---")
        
        # Organizational Debt
        st.write("#### 3. Organizational Debt Mapping")
        
        col1, col2 = st.columns(2)
        with col1:
            num_teams = st.number_input("Number of engineering teams:", 1, 100, 15)
            num_standards = st.number_input("Different tech standards in use:", 1, 50, 8)
            shadow_it = st.number_input("Known shadow IT projects:", 0, 50, 3)
        with col2:
            ma_integrations = st.number_input("M&A integrations in past 3 years:", 0, 20, 2)
            team_turnover = st.slider("Annual team turnover rate (%):", 0, 100, 25)
            avg_tenure = st.slider("Average employee tenure (years):", 0, 20, 3)
        
        org_narrative = st.text_area(
            "Describe the organizational complexity:",
            height=150,
            placeholder="Example: 15 teams across 3 acquisitions. Each has different standards. Original company uses Java/Spring, Acquisition A uses Python/Django, Acquisition B uses .NET. No unified architecture. Each team reports to different VP. Matrix org structure means no clear decision authority.",
            key="org_narrative"
        )
        
        if st.button("💾 Save Organizational Analysis"):
            st.session_state.work['complexity_analysis']['organizational'] = {
                'num_teams': num_teams,
                'num_standards': num_standards,
                'shadow_it': shadow_it,
                'ma_integrations': ma_integrations,
                'turnover': team_turnover,
                'tenure': avg_tenure,
                'narrative': org_narrative
            }
            st.success("✅ Organizational analysis saved!")
        
        st.markdown("---")
        
        # Regulatory Arbitrage
        st.write("#### 4. Regulatory Conflict Analysis")
        st.caption("Where do regulations conflict? What's architecturally impossible to comply with?")
        
        jurisdictions = st.multiselect(
            "Operating jurisdictions:",
            ["United States", "European Union (GDPR)", "United Kingdom", "China", "India", 
             "Brazil", "Canada", "Australia", "Japan", "Other"],
            default=["United States", "European Union (GDPR)"]
        )
        
        conflicts = st.text_area(
            "Document regulatory conflicts:",
            height=150,
            placeholder="""Example:
**Conflict 1: GDPR vs US CLOUD Act**
- GDPR: Prohibits transfer of EU data to US without adequate protection
- CLOUD Act: US govt can subpoena data from US companies, even if stored abroad
- Impact: If we're US company storing EU data in Frankfurt, CLOUD Act subpoena violates GDPR
- Architectural implication: Need EU subsidiary to hold keys, or encryption with split key management

**Conflict 2: China Data Localization vs Global ML Models**
- China: All data must stay in China
- Business need: ML models require aggregated global data for fraud detection
- Impact: Can't use Chinese data to train models, or can't operate in China
- Decision needed: Separate models per region, or exit China market""",
            key="reg_conflicts"
        )
        
        if st.button("💾 Save Regulatory Analysis"):
            st.session_state.work['complexity_analysis']['regulatory'] = {
                'jurisdictions': jurisdictions,
                'conflicts': conflicts
            }
            st.success("✅ Regulatory analysis saved!")
    
    with tabs[1]:
        st.write("### Expert-Level Complexity Analysis")
        
        st.markdown("""
        <div class="best-practice">
        <h4>✅ Example: Real Enterprise Complexity Documentation</h4>
        
        <p><strong>Technical Debt: Mainframe Payment Processing</strong></p>
        <ul>
            <li><strong>System:</strong> IBM z/Series mainframe running COBOL</li>
            <li><strong>Age:</strong> 42 years (installed 1982)</li>
            <li><strong>Revenue Dependency:</strong> $50M/month (all credit card processing)</li>
            <li><strong>Why Can't Replace:</strong>
                <ul>
                    <li>5 million lines of COBOL code, no documentation</li>
                    <li>Original developers retired or deceased</li>
                    <li>Unknown business logic embedded in code</li>
                    <li>Replacement would require 5-year rewrite project</li>
                    <li>Risk of breaking existing card processor certifications</li>
                </ul>
            </li>
            <li><strong>Replacement Cost:</strong> $50M (3-year project)</li>
            <li><strong>Replacement Risk:</strong> 30% chance of catastrophic failure during cutover</li>
            <li><strong>Architectural Decision:</strong> Keep mainframe, build API wrapper
                <ul>
                    <li>Cost: $5M (API layer)</li>
                    <li>Timeline: 6 months</li>
                    <li>Risk: Low (wrapper fails, mainframe still works)</li>
                    <li>Trade-off: Still have mainframe, but can modernize around it</li>
                </ul>
            </li>
        </ul>
        
        <p><strong>Political Debt: Oracle Vendor Lock-in</strong></p>
        <ul>
            <li><strong>Situation:</strong> CTO mandated Oracle database across all applications</li>
            <li><strong>History:</strong> CTO worked at Oracle for 10 years before joining</li>
            <li><strong>Contract:</strong> $2M/year, 3-year agreement, auto-renewal</li>
            <li><strong>Impact:</strong> 
                <ul>
                    <li>Engineering wants to use Postgres (open source, better for OLTP)</li>
                    <li>New applications forced to use Oracle (adds $200K/year per app)</li>
                    <li>Oracle-specific SQL prevents database portability</li>
                </ul>
            </li>
            <li><strong>Architectural Approach:</strong>
                <ul>
                    <li>Don't fight the CTO directly (you'll lose)</li>
                    <li>Build business case: Show TCO difference ($5M over 3 years)</li>
                    <li>Propose: "Oracle for critical systems, Postgres for new development"</li>
                    <li>Let CFO make the case (CTO won't override CFO on cost)</li>
                    <li>Document in ADR: "We use Postgres where Oracle not required by policy"</li>
                </ul>
            </li>
        </ul>
        
        <p><strong>Organizational Debt: Post-M&A Architecture Fragmentation</strong></p>
        <ul>
            <li><strong>Situation:</strong> 5 acquisitions in 3 years, none integrated</li>
            <li><strong>Impact:</strong>
                <ul>
                    <li>6 different identity providers (Okta, Azure AD, Auth0, 3× on-prem AD)</li>
                    <li>4 different cloud providers (AWS, Azure, GCP, on-prem)</li>
                    <li>8 different tech stacks (Java, Python, .NET, Node.js, PHP, Go, Ruby, Rust)</li>
                    <li>No unified monitoring, logging, or security tools</li>
                </ul>
            </li>
            <li><strong>Cost:</strong> $10M/year operational overhead (duplicate tools, inefficiency)</li>
            <li><strong>Architectural Strategy:</strong>
                <ul>
                    <li>Phase 1: Bridge (federate identity, don't migrate yet)</li>
                    <li>Phase 2: Standardize (new apps must use approved platforms)</li>
                    <li>Phase 3: Consolidate (migrate old apps over 3 years)</li>
                    <li>Accept: Will be multi-cloud for 5+ years (cost of doing business)</li>
                </ul>
            </li>
        </ul>
        
        <p><strong>Regulatory Arbitrage: GDPR/CLOUD Act Conflict</strong></p>
        <ul>
            <li><strong>Problem:</strong> US company, EU customers, CLOUD Act applies</li>
            <li><strong>Architectural Solutions:</strong>
                <ol>
                    <li><strong>Data Residency:</strong> EU data in Frankfurt, encrypted with keys held by EU subsidiary
                        <ul>
                            <li>US govt subpoena gets encrypted data (useless without keys)</li>
                            <li>EU subsidiary not subject to CLOUD Act</li>
                            <li>Cost: $500K setup + $200K/year</li>
                        </ul>
                    </li>
                    <li><strong>Data Minimization:</strong> Don't store PII, only pseudonymized data
                        <ul>
                            <li>GDPR doesn't apply to truly anonymized data</li>
                            <li>Trade-off: Reduced analytics capability</li>
                        </ul>
                    </li>
                    <li><strong>Contractual:</strong> Customer signs DPA acknowledging risk
                        <ul>
                            <li>Disclose CLOUD Act in contract</li>
                            <li>Customer accepts risk (common for B2B SaaS)</li>
                        </ul>
                    </li>
                </ol>
            </li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with tabs[2]:
        st.write("### How to Think Like an Architect")
        
        st.markdown("""
        <div class="architect-insight">
        <h4>🧠 Architect Mindset vs Engineer Mindset</h4>
        
        <table>
        <tr>
            <th>Situation</th>
            <th>❌ Engineer Thinking</th>
            <th>✅ Architect Thinking</th>
        </tr>
        <tr>
            <td><strong>Legacy Mainframe</strong></td>
            <td>"This is ancient, we should replace it"</td>
            <td>"Why was this built? What does it do well? What would break if we replaced it? What's the cost/benefit/risk analysis?"</td>
        </tr>
        <tr>
            <td><strong>Vendor Lock-in</strong></td>
            <td>"Oracle is expensive, switch to Postgres"</td>
            <td>"Who made this decision? Why? What's their leverage? Can I build a business case the CFO will buy? What's the migration risk?"</td>
        </tr>
        <tr>
            <td><strong>Multiple Standards</strong></td>
            <td>"Everyone should use the same stack"</td>
            <td>"Why do these teams use different stacks? What would it cost to converge? What's the value? Is the juice worth the squeeze?"</td>
        </tr>
        <tr>
            <td><strong>Regulatory Conflict</strong></td>
            <td>"Just comply with both"</td>
            <td>"Where do these regulations conflict? What's architecturally impossible? What are my options? What does each cost?"</td>
        </tr>
        </table>
        
        <h4>🎯 The Architect's Framework</h4>
        <p>For every piece of complexity, ask:</p>
        <ol>
            <li><strong>Why does this exist?</strong> (History, not judgment)</li>
            <li><strong>What problem did it solve?</strong> (Was it right at the time?)</li>
            <li><strong>What changed?</strong> (Why is it a problem now?)</li>
            <li><strong>What would it cost to fix?</strong> (Money, time, risk)</li>
            <li><strong>What's the value of fixing it?</strong> (ROI calculation)</li>
            <li><strong>What are my options?</strong> (Always have 3+ alternatives)</li>
            <li><strong>What am I recommending and why?</strong> (Clear decision with rationale)</li>
        </ol>
        
        <h4>⚠️ Common Failure Modes</h4>
        
        <div class="common-mistake">
        <strong>Mistake 1: "The previous architect was an idiot"</strong><br>
        Reality: They made the best decision given 2015 constraints. You have 2024 constraints.<br>
        <strong>Better:</strong> "This made sense in 2015 when cloud wasn't mature. Now we have better options."
        </div>
        
        <div class="common-mistake">
        <strong>Mistake 2: "Just rewrite everything"</strong><br>
        Reality: Rewrites fail 80% of the time, take 3× longer than estimated, and break existing functionality.<br>
        <strong>Better:</strong> "Strangler fig pattern: Build new around old, migrate incrementally, retire old when safe."
        </div>
        
        <div class="common-mistake">
        <strong>Mistake 3: "Ignore the politics"</strong><br>
        Reality: The best technical solution that ignores politics gets killed in committee.<br>
        <strong>Better:</strong> "Understand who has power, what they care about, build coalitions, let them take credit."
        </div>
        
        <div class="common-mistake">
        <strong>Mistake 4: "Technology will solve it"</strong><br>
        Reality: Most problems are organizational, not technical.<br>
        <strong>Better:</strong> "This is a people problem. Technology can help, but we need org change, process change, and culture change."
        </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Exercise completion
    if st.session_state.work['complexity_analysis']:
        st.markdown("---")
        st.success("✅ Complexity analysis in progress")
        if st.button("🎯 Mark Exercise Complete & Continue"):
            st.session_state.completed_exercises.append("complexity_analysis")
            st.balloons()
            st.success("Exercise marked complete! Proceeding to M&A Integration exercise...")

# ============================================================================
# DEEP CONTENT - M&A INTEGRATION
# ============================================================================

def render_ma_integration_deep():
    """M&A 90-Day Integration - REAL ARCHITECT THINKING"""
    
    st.markdown('<h2>Exercise 2: Post-Merger Architecture Nightmare</h2>', unsafe_allow_html=True)
    
    # Critical Scenario
    st.markdown("""
    <div class="scenario-critical">
    <h3>🔥 Real-World M&A Crisis</h3>
    <p><strong>Your company ($10B market cap) acquires competitor ($2B)</strong></p>
    <p><strong>Board mandate:</strong> "Integrate in 90 days. Make it secure. Don't break anything. Enable SSO. Meet SOX compliance."</p>
    <br>
    <p><strong>Their infrastructure (discovered Day 1):</strong></p>
    <ul>
        <li>🔴 3 AWS accounts (no centralized IAM, root passwords on sticky notes)</li>
        <li>🔴 Kubernetes clusters (no service mesh, no RBAC, cluster admin for everyone)</li>
        <li>🔴 On-prem Active Directory (20-year-old, can't retire, 50+ legacy apps depend on it)</li>
        <li>🔴 PCI CDE in colo data center (lease expires in 6 months, vendor out of business)</li>
        <li>🔴 Security team of 2 people (both gave notice, leaving in 30 days)</li>
        <li>🔴 Last SOC 2 audit: 15 findings, none remediated, expires in 90 days</li>
    </ul>
    <br>
    <p><strong>Additional problems discovered Week 1:</strong></p>
    <ul>
        <li>💣 $5M/month revenue flows through systems you now own</li>
        <li>💣 Their largest customer (30% of revenue) has audit rights, coming in Month 2</li>
        <li>💣 Their CTO (who built all of this) is now your boss's boss</li>
        <li>💣 Your CFO expects $2M cost synergies (read: cut their IT budget)</li>
    </ul>
    <br>
    <p style="color: #991b1b; font-weight: 700; font-size: 1.2rem;">
    What's your 90-day plan? What do you defer? What breaks? What risks do you accept?
    </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Expert Critique First
    st.markdown("""
    <div class="expert-critique">
    <h4>🎓 Expert Critique: Read This BEFORE You Plan</h4>
    """ + EXPERT_CRITIQUES['ma_integration_common_failures'] + """
    </div>
    """, unsafe_allow_html=True)
    
    tabs = st.tabs(["📋 Your 90-Day Plan", "✅ Expert Playbook", "💡 Architect Decision Framework"])
    
    with tabs[0]:
        st.write("### Build Your Integration Plan")
        
        st.info("""
**Planning Principles:**
1. **Phase 1 (Discovery):** Understand before acting
2. **Phase 2 (Stabilization):** Don't make things worse
3. **Phase 3 (Integration):** Converge on standards
4. **Critical:** Document what you're NOT doing and why
        """)
        
        # Phase 1: Discovery
        st.write("#### Phase 1: Discovery (Day 1-14)")
        
        discovery_checklist = st.multiselect(
            "What will you discover?",
            [
                "Complete asset inventory (all IP ranges, cloud accounts, domains)",
                "Access inventory (all IAM users, service accounts, API keys)",
                "Compliance inventory (SOC 2, PCI, HIPAA, GDPR status)",
                "Risk assessment (vulnerability scan, critical findings)",
                "Architecture documentation (current state diagrams)",
                "Data flow mapping (where PII/PCI data flows)",
                "Dependency mapping (what depends on what)",
                "Interview key personnel (before they leave!)",
                "Financial analysis (what's their OpEx, where can we save)",
                "Contract review (vendor contracts, customer SLAs)"
            ],
            default=[
                "Complete asset inventory (all IP ranges, cloud accounts, domains)",
                "Access inventory (all IAM users, service accounts, API keys)",
                "Risk assessment (vulnerability scan, critical findings)"
            ]
        )
        
        discovery_narrative = st.text_area(
            "Discovery plan (be specific about deliverables):",
            height=150,
            placeholder="""Example:
Week 1:
- Run Nmap scan on all IP ranges (deliverable: IP inventory spreadsheet)
- Export IAM users from all 3 AWS accounts (deliverable: Access matrix)
- Run Qualys vulnerability scan (deliverable: Risk register with CVSS 9+ prioritized)
- Interview their security team (2 people, 30 days left) - knowledge transfer is critical
- Review SOC 2 report (15 findings) - understand which ones block integration

Week 2:
- Document current-state architecture (deliverable: C4 diagrams - context, container, component)
- Map all data flows for PCI data (deliverable: Data flow diagram with trust boundaries)
- Review all vendor contracts (deliverable: Contract inventory with renewal dates)
- Assess DR capabilities (deliverable: DR runbook, or lack thereof)
- Create initial risk register (deliverable: Jira board with 20+ identified risks)""",
            key="ma_discovery"
        )
        
        # Phase 2: Stabilization
        st.write("#### Phase 2: Stabilization (Day 15-60)")
        st.caption("Goal: Don't make things worse. Fix critical issues. Build bridges, don't migrate yet.")
        
        stabilization_priorities = st.multiselect(
            "Stabilization priorities (pick max 5):",
            [
                "Patch critical vulnerabilities (CVSS 9.0+)",
                "Enable MFA on all admin accounts",
                "Close publicly exposed resources (S3 buckets, databases)",
                "Implement basic monitoring and alerting",
                "Set up SSO federation (bridge, don't migrate)",
                "Establish network connectivity (VPN or cloud interconnect)",
                "Deploy centralized logging (forward to your SIEM)",
                "Enable CloudTrail/audit logging on all accounts",
                "Document incident response procedures",
                "Train their team on your standards"
            ],
            default=[
                "Patch critical vulnerabilities (CVSS 9.0+)",
                "Enable MFA on all admin accounts",
                "Close publicly exposed resources (S3 buckets, databases)"
            ]
        )
        
        stabilization_narrative = st.text_area(
            "Stabilization plan (week-by-week):",
            height=150,
            placeholder="""Example:
Week 3-4 (Immediate Firefighting):
- Patch all systems with CVSS 9+ vulns (expected: 50+ systems)
- Rollback plan: If patch breaks system, rollback within 2 hours
- Success metric: 100% CVSS 9+ patched by end Week 4

Week 5-6 (IAM Bridge - Don't Migrate Yet):
- Set up SAML federation between your Okta and their on-prem AD
- Test with pilot group (10 users)
- Document: This is a bridge, not the final state
- Why bridge: Migration will take 6+ months, this gives us SSO in 30 days
- Trade-off: Operational complexity (two IdPs), but low risk

Week 7-8 (Monitoring & Logging):
- Deploy Datadog agents to all systems
- Forward logs to your Splunk
- Set up basic alerts (system down, high error rate, failed auth attempts)
- Why: Can't manage what we can't see""",
            key="ma_stabilization"
        )
        
        # Phase 3: Integration
        st.write("#### Phase 3: Integration (Day 61-90)")
        st.caption("Goal: Converge on common standards. Actual migration starts here.")
        
        integration_narrative = st.text_area(
            "Integration plan:",
            height=150,
            placeholder="""Example:
Week 9-10 (User Migration):
- Migrate 10% of users to your Okta (pilot group)
- Monitor for issues: Failed auth, locked accounts, broken apps
- Success criteria: <5% help desk tickets, no critical apps broken
- If successful: Migrate remaining 90% in Week 11-12
- If issues: Rollback pilot group, extend timeline

Week 11-12 (System Migration):
- Migrate critical apps to your standards
- Priority: PCI systems first (colo lease expires soon)
- For each app: Test in dev, migrate in maintenance window, 24-hour soak test
- Rollback procedure documented for each app

Week 13 (Validation):
- Post-integration security assessment
- Update architecture documentation
- Conduct DR tabletop exercise (test the integrated system)
- Present to executive team: What worked, what didn't, what's next""",
            key="ma_integration"
        )
        
        # Critical: What Are You Deferring?
        st.write("#### What Are You Deferring? (Be Honest)")
        st.error("This is the most important section. Most M&A failures come from trying to do too much.")
        
        deferred_items = st.text_area(
            "List everything you're deferring past 90 days:",
            height=150,
            placeholder="""Example:
1. PCI CDE migration (6+ months)
   - Why defer: Colo lease expires in 6 months, but migration requires 4-6 months planning
   - Mitigation: Extend lease by 3 months ($50K cost)
   - Risk: Higher cost, but lower risk than rushing migration

2. Legacy AD retirement (12+ months)
   - Why defer: 50+ legacy apps depend on it, would require app rewrites
   - Mitigation: Keep AD, federate to cloud IAM
   - Trade-off: Operational complexity, but apps keep working

3. Perfect tool consolidation
   - Why defer: They use GitLab, we use GitHub. Migration is 6+ month project
   - Mitigation: Support both for now
   - Cost: $50K/year for duplicate tools
   - Decision: Not worth the migration risk for $50K savings

4. Security team integration
   - Why defer: Can't force culture integration in 90 days
   - Approach: Keep both teams, slowly integrate over 6-12 months
   - Risk: Duplicate processes, inconsistent standards
   - Accepted: Better than forcing it and people quit""",
            key="ma_deferred"
        )
        
        # Accepted Risks
        st.write("#### Accepted Risks (Get Executive Sign-Off)")
        st.warning("Document risks you're accepting. Get CISO + CFO sign-off. CYA.")
        
        accepted_risks = st.text_area(
            "Risks you're accepting:",
            height=150,
            placeholder="""Example:
Risk 1: Bridged Network (Not Zero Trust) for 90 days
- Description: VPN between networks, not micro-segmented
- Likelihood: Medium | Impact: High
- Why accepting: Zero Trust takes 12+ months, we need integration now
- Mitigation: Enhanced monitoring, network IDS, 24/7 SOC
- Compensating control: All traffic logged, anomaly detection
- Accepted by: VP Engineering (signature) + CISO (signature)
- Review date: 90 days from now

Risk 2: Understaffed Security (2 people leaving)
- Description: Down from 2 security engineers to 0 for 30-60 days
- Likelihood: High | Impact: Medium
- Why accepting: Can't hire fast enough
- Mitigation: Contractor support ($200K), prioritize critical issues only
- Accepted by: CISO (signature) + CFO (approved budget)
- Review date: Monthly until backfilled

Risk 3: SOC 2 Expiration During Integration
- Description: Their SOC 2 expires in 90 days, might not pass re-audit
- Likelihood: High | Impact: High
- Why accepting: Can't fix 15 findings during integration chaos
- Mitigation: Delay audit by 3 months, fix findings before re-audit
- Cost: $50K audit delay + $200K remediation
- Accepted by: CFO (approved cost) + General Counsel (legal risk)""",
            key="ma_risks"
        )
        
        if st.button("💾 Save Complete 90-Day Plan", type="primary"):
            st.session_state.work['ma_integration'] = {
                'discovery': {
                    'checklist': discovery_checklist,
                    'narrative': discovery_narrative
                },
                'stabilization': {
                    'priorities': stabilization_priorities,
                    'narrative': stabilization_narrative
                },
                'integration': {
                    'narrative': integration_narrative
                },
                'deferred': deferred_items,
                'risks': accepted_risks,
                'timestamp': datetime.now().isoformat()
            }
            st.success("✅ 90-day plan saved!")
            st.balloons()
    
    with tabs[1]:
        st.write("### Expert-Level M&A Integration Playbook")
        
        # Show the complete expert playbook here
        st.markdown("""
        <div class="best-practice">
        <h4>✅ Enterprise Architect's M&A Integration Playbook</h4>
        
        <p><strong>Phase 1: Discovery (Day 1-14) - "Diagnose Before Prescribing"</strong></p>
        
        <p><em>Week 1: Asset & Access Inventory</em></p>
        <ul>
            <li><strong>Technical Assets:</strong>
                <ul>
                    <li>Run Nmap/Masscan on all IP ranges (deliverable: Complete IP inventory)</li>
                    <li>Enumerate cloud resources (AWS Config, Azure Resource Graph, GCP Asset Inventory)</li>
                    <li>Discover all domains/subdomains (Certificate Transparency logs, DNS enumeration)</li>
                    <li>Find shadow IT (SaaS discovery via OAuth audit, expense reports, DNS logs)</li>
                </ul>
            </li>
            <li><strong>Access Inventory:</strong>
                <ul>
                    <li>Export all IAM users (cloud + on-prem AD + service accounts)</li>
                    <li>Document privileged access (who has root/admin/sudo)</li>
                    <li>Find API keys/service accounts (GitHub, AWS, GCP, etc.)</li>
                    <li>Review MFA coverage (spoiler: it's probably 20%)</li>
                </ul>
            </li>
            <li><strong>Risk Assessment:</strong>
                <ul>
                    <li>Vulnerability scan with Qualys/Rapid7 (prioritize CVSS 9.0+)</li>
                    <li>Identify internet-exposed assets (Shodan, Censys, BinaryEdge)</li>
                    <li>Check for public S3 buckets, exposed databases, open admin panels</li>
                    <li>Review past incidents (if they'll admit to them)</li>
                </ul>
            </li>
        </ul>
        
        <p><em>Week 2: Architecture & Compliance</em></p>
        <ul>
            <li><strong>Documentation:</strong>
                <ul>
                    <li>Interview their security team (CRITICAL: they're leaving in 30 days)</li>
                    <li>Extract tribal knowledge (undocumented dependencies, workarounds, passwords)</li>
                    <li>Document current-state architecture (C4 diagrams: context, container, component)</li>
                    <li>Map data flows for sensitive data (PCI, PII, PHI)</li>
                </ul>
            </li>
            <li><strong>Compliance Review:</strong>
                <ul>
                    <li>Review SOC 2 Type II report (read the findings, not just the opinion)</li>
                    <li>Check PCI DSS Attestation of Compliance (AOC) - is it current?</li>
                    <li>Review customer contracts (audit rights? SLA commitments? Data residency?)</li>
                    <li>Identify compliance gaps (15 SOC 2 findings = 15 problems to fix)</li>
                </ul>
            </li>
            <li><strong>Deliverables:</strong>
                <ul>
                    <li>Complete asset inventory (spreadsheet or CMDB)</li>
                    <li>Risk register (Jira/ServiceNow with 20+ identified risks)</li>
                    <li>Current-state architecture diagrams (C4 context + container)</li>
                    <li>Compliance gap analysis (what breaks if we integrate?)</li>
                    <li>Knowledge transfer document (from their team before they leave)</li>
                </ul>
            </li>
        </ul>
        
        <p><strong>Phase 2: Stabilization (Day 15-60) - "Don't Make Things Worse"</strong></p>
        
        <p><em>Week 3-4: Immediate Firefighting</em></p>
        <ul>
            <li><strong>Critical Vulnerabilities:</strong>
                <ul>
                    <li>Patch all CVSS 9.0+ vulns (expect 50-100 systems)</li>
                    <li>Test patches in dev first (don't break production)</li>
                    <li>Rollback plan for each patch (2-hour rollback window)</li>
                    <li>Success metric: 100% CVSS 9+ patched by end of Week 4</li>
                </ul>
            </li>
            <li><strong>MFA Everywhere:</strong>
                <ul>
                    <li>Enable MFA on all admin accounts (AWS root, AD Domain Admin)</li>
                    <li>Enforce MFA for VPN access</li>
                    <li>Low-hanging fruit, high impact, minimal disruption</li>
                </ul>
            </li>
            <li><strong>Exposed Resources:</strong>
                <ul>
                    <li>Close public S3 buckets (unless legitimately needed)</li>
                    <li>Restrict RDS/database security groups (why is Postgres public?)</li>
                    <li>Fix admin panels exposed to internet (why is Jenkins public?)</li>
                </ul>
            </li>
        </ul>
        
        <p><em>Week 5-6: IAM Bridge (Don't Migrate Yet)</em></p>
        <ul>
            <li><strong>Why Bridge First:</strong>
                <ul>
                    <li>Full IAM migration takes 6+ months</li>
                    <li>Board wants SSO in 90 days</li>
                    <li>Bridge gives us SSO without migration risk</li>
                </ul>
            </li>
            <li><strong>Implementation:</strong>
                <ul>
                    <li>Set up SAML federation: Your Okta ↔ Their AD</li>
                    <li>Test with pilot group (10 users, not VIPs)</li>
                    <li>Monitor for issues: Failed auth, broken apps, locked accounts</li>
                    <li>If successful: Expand to 100 users, then all</li>
                </ul>
            </li>
            <li><strong>Trade-offs:</strong>
                <ul>
                    <li>Pro: SSO in 30 days, low risk, reversible</li>
                    <li>Con: Operational complexity (two IdPs to manage)</li>
                    <li>Accepted: Temporary complexity better than rushed migration</li>
                </ul>
            </li>
        </ul>
        
        <p><em>Week 7-8: Network & Monitoring</em></p>
        <ul>
            <li><strong>Network Connectivity:</strong>
                <ul>
                    <li>Establish VPN or cloud interconnect</li>
                    <li>Implement network segmentation (don't flatten networks)</li>
                    <li>Document network topology (before and after)</li>
                </ul>
            </li>
            <li><strong>Centralized Logging:</strong>
                <ul>
                    <li>Deploy log forwarders (Splunk Universal Forwarder, Datadog agent)</li>
                    <li>Forward to your SIEM (Splunk, Sumo Logic, Datadog)</li>
                    <li>Set up basic alerts (system down, failed auth, high error rate)</li>
                </ul>
            </li>
            <li><strong>Why This Matters:</strong>
                <ul>
                    <li>Can't manage what you can't see</li>
                    <li>Need visibility before making changes</li>
                    <li>Logging is insurance policy for when things break</li>
                </ul>
            </li>
        </ul>
        
        <p><strong>Phase 3: Integration (Day 61-90) - "Converge on Standards"</strong></p>
        
        <p><em>Week 9-10: User Migration</em></p>
        <ul>
            <li>Migrate 10% of users to your Okta (pilot group)</li>
            <li>Monitor help desk tickets: <5% ticket rate = success</li>
            <li>If issues: Fix before expanding (don't migrate more until pilot works)</li>
            <li>Week 11-12: Migrate remaining 90% in waves (not all at once)</li>
            <li>Decommission their IdP (after 30-day soak period)</li>
        </ul>
        
        <p><em>Week 11-12: System Migration</em></p>
        <ul>
            <li>Priority 1: PCI systems (colo lease expires in 6 months)</li>
            <li>Priority 2: Critical apps (high revenue dependency)</li>
            <li>Priority 3: Everything else (can wait)</li>
            <li>For each app: Dev test → Staging test → Prod migration → 24hr soak test</li>
            <li>Rollback procedure documented and tested for each app</li>
        </ul>
        
        <p><em>Week 13: Validation & Documentation</em></p>
        <ul>
            <li>Post-integration security assessment (did we make things worse?)</li>
            <li>Update all architecture documentation (current-state = target-state)</li>
            <li>Conduct DR tabletop exercise (test the integrated system)</li>
            <li>Executive presentation: What worked, what didn't, what's next</li>
        </ul>
        
        <p><strong>What We're Deferring (Post-90 Days)</strong></p>
        <ol>
            <li><strong>PCI CDE Migration (6 months):</strong> Lease expires, but proper migration needs planning</li>
            <li><strong>Legacy AD Retirement (12 months):</strong> 50+ apps depend on it, not fixable in 90 days</li>
            <li><strong>Perfect Tool Consolidation:</strong> GitLab vs GitHub, not worth migration risk</li>
            <li><strong>Security Team Integration:</strong> Culture doesn't integrate in 90 days</li>
        </ol>
        
        <p><strong>Accepted Risks (Executive Sign-Off Required)</strong></p>
        <ol>
            <li><strong>Bridged Network (Not Zero Trust):</strong> Accepted for 90 days, enhanced monitoring</li>
            <li><strong>Understaffed Security:</strong> Contractor support until backfilled</li>
            <li><strong>SOC 2 Expiration:</strong> Delay audit by 3 months, fix findings first</li>
        </ol>
        
        <p><strong>Success Metrics</strong></p>
        <ul>
            <li>✅ No major outages during integration</li>
            <li>✅ SSO enabled for 100% of users by Day 90</li>
            <li>✅ All CVSS 9+ vulns patched</li>
            <li>✅ Centralized logging operational</li>
            <li>✅ Risk register approved by CISO + CFO</li>
            <li>✅ Post-integration security assessment shows no regression</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with tabs[2]:
        st.write("### Architect Decision Framework")
        
        st.markdown("""
        <div class="architectural-principle">
        <h4>🏛️ The M&A Integration Decision Framework</h4>
        
        <p>Use this framework for EVERY decision during M&A:</p>
        
        <h5>1. Classify the Decision</h5>
        <ul>
            <li><strong>🔴 One-Way Door:</strong> Hard to reverse (user migration, app cutover)
                <ul>
                    <li>Analysis required: Deep dive, risk analysis, rollback plan</li>
                    <li>Approval required: CISO + VP Engineering + CFO</li>
                    <li>Timeline: Allow 4-6 weeks for planning</li>
                </ul>
            </li>
            <li><strong>🟢 Two-Way Door:</strong> Reversible (SSO federation, monitoring deployment)
                <ul>
                    <li>Analysis required: Basic testing</li>
                    <li>Approval required: Architect</li>
                    <li>Timeline: Can move quickly</li>
                </ul>
            </li>
        </ul>
        
        <h5>2. Calculate Business Impact</h5>
        <ul>
            <li><strong>Revenue at Risk:</strong> How much revenue depends on this system?</li>
            <li><strong>Customer Impact:</strong> Will customers notice? Will they churn?</li>
            <li><strong>Employee Impact:</strong> Will employees be disrupted? Help desk surge?</li>
            <li><strong>Compliance Impact:</strong> Does this affect SOC 2, PCI, GDPR?</li>
        </ul>
        
        <h5>3. Estimate Cost vs Value</h5>
        <ul>
            <li><strong>Cost to Do It:</strong> Money, time, risk</li>
            <li><strong>Cost to NOT Do It:</strong> Opportunity cost, risk accumulation</li>
            <li><strong>Value of Doing It:</strong> Business benefit, risk reduction</li>
            <li><strong>Decision:</strong> Do if Value > Cost, defer if Cost > Value</li>
        </ul>
        
        <h5>4. Identify What Could Go Wrong</h5>
        <ul>
            <li><strong>Best Case:</strong> Everything works perfectly</li>
            <li><strong>Expected Case:</strong> Minor issues, 10% help desk ticket increase</li>
            <li><strong>Worst Case:</strong> Complete failure, rollback required, revenue impact</li>
            <li><strong>Plan For:</strong> Expected case, prepare for worst case</li>
        </ul>
        
        <h5>5. Document Your Decision</h5>
        <ul>
            <li><strong>ADR:</strong> Architecture Decision Record with context, decision, alternatives, consequences</li>
            <li><strong>Risk Register:</strong> Add to Jira with likelihood, impact, mitigation</li>
            <li><strong>Runbook:</strong> Step-by-step execution plan with rollback procedures</li>
            <li><strong>Communication Plan:</strong> Who needs to know? When? How?</li>
        </ul>
        
        <h5>Example: User Migration Decision</h5>
        <table style="width: 100%; border-collapse: collapse;">
        <tr style="background: #f3f4f6;">
            <th style="padding: 12px; text-align: left; border: 1px solid #e5e7eb;">Question</th>
            <th style="padding: 12px; text-align: left; border: 1px solid #e5e7eb;">Analysis</th>
        </tr>
        <tr>
            <td style="padding: 12px; border: 1px solid #e5e7eb;"><strong>Decision Type</strong></td>
            <td style="padding: 12px; border: 1px solid #e5e7eb;">🔴 One-Way Door (hard to rollback user migration)</td>
        </tr>
        <tr>
            <td style="padding: 12px; border: 1px solid #e5e7eb;"><strong>Business Impact</strong></td>
            <td style="padding: 12px; border: 1px solid #e5e7eb;">
                - Revenue Risk: $0 (SSO doesn't affect revenue)<br>
                - Customer Impact: None (internal users only)<br>
                - Employee Impact: High (2000 users need to re-authenticate)<br>
                - Compliance: Positive (centralized IAM = better audit trail)
            </td>
        </tr>
        <tr>
            <td style="padding: 12px; border: 1px solid #e5e7eb;"><strong>Cost vs Value</strong></td>
            <td style="padding: 12px; border: 1px solid #e5e7eb;">
                - Cost: $200K (implementation) + 30% help desk surge ($50K)<br>
                - Value: $500K/year (eliminate duplicate IAM) + better security<br>
                - ROI: 200% first year, 500% over 3 years<br>
                - Decision: Do it
            </td>
        </tr>
        <tr>
            <td style="padding: 12px; border: 1px solid #e5e7eb;"><strong>What Could Go Wrong</strong></td>
            <td style="padding: 12px; border: 1px solid #e5e7eb;">
                - Best Case: Seamless migration, <1% issues<br>
                - Expected: 10% help desk ticket increase, minor app breakage<br>
                - Worst Case: Authentication failures, users locked out, apps break<br>
                - Mitigation: Pilot group first, 24-hour rollback window
            </td>
        </tr>
        <tr>
            <td style="padding: 12px; border: 1px solid #e5e7eb;"><strong>Documentation</strong></td>
            <td style="padding: 12px; border: 1px solid #e5e7eb;">
                - ADR-0042: "Migrate users to Okta SSO"<br>
                - Risk-043: "User migration may cause auth failures" (Medium likelihood, Medium impact)<br>
                - Runbook: "User Migration Procedure" (step-by-step with rollback)<br>
                - Comm Plan: Email users 1 week before, again day-of, help desk on standby
            </td>
        </tr>
        </table>
        </div>
        """, unsafe_allow_html=True)

# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    # Sidebar (simplified for now)
    with st.sidebar:
        st.title("🏛️ Security Architect")
        st.caption("Enterprise Masterclass")
        
        progress = len(st.session_state.completed_exercises)
        st.metric("Completed", progress)
        
        if st.button("📥 Export Portfolio"):
            portfolio = {
                'completed': st.session_state.completed_exercises,
                'work': st.session_state.work,
                'timestamp': datetime.now().isoformat()
            }
            st.download_button(
                "Download JSON",
                json.dumps(portfolio, indent=2, default=str),
                f"portfolio_{datetime.now().strftime('%Y%m%d')}.json",
                "application/json"
            )
    
    # Route to content
    if st.session_state.current_day == 1 and st.session_state.current_section == 1:
        render_day1_s1_1()
        st.markdown("---")
        render_ma_integration_deep()
    else:
        st.title("Additional Content")
        st.info("More sections being developed...")

if __name__ == "__main__":
    main()
