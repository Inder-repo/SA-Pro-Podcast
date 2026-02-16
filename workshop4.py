"""
ADVANCED ENTERPRISE SECURITY ARCHITECTURE WORKSHOP
Professional Training Platform - Standalone Version
All content in single file for easy deployment
"""

import streamlit as st
import json
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
from typing import Dict, List, Optional

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Enterprise Security Architecture Masterclass",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CUSTOM CSS
# ============================================================================

st.markdown("""
<style>
    .scenario-box {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        border-left: 5px solid #f59e0b;
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    .case-study {
        background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
        border-left: 5px solid #2563eb;
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    .success-pattern {
        background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
        border-left: 5px solid #059669;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    }
    
    .stButton > button {
        border-radius: 6px;
        font-weight: 600;
        transition: all 0.3s;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

def init_session_state():
    """Initialize comprehensive session state"""
    defaults = {
        'current_day': 1,
        'current_session': 1,
        'current_subsection': 1,
        'completed_exercises': [],
        'day1': {
            'complexity_assessment': {},
            'ma_integration': {},
            'arb_decisions': {},
            'toolchain': {},
            'pasta': {},
            'supply_chain': {},
            'cloud_threats': {},
            'compliance': {}
        },
        'day2': {},
        'day3': {},
        'day4': {},
        'notes': {}
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session_state()

# ============================================================================
# CURRICULUM STRUCTURE
# ============================================================================

CURRICULUM = {
    "Day 1": {
        "title": "Enterprise Context & Architecture at Scale",
        "duration": "4 Hours",
        "sessions": {
            "1.1": {
                "title": "The Reality of Enterprise Architecture",
                "subsections": {
                    "1.1.1": {"title": "What's Different at Enterprise Scale?", "duration": "20 min"},
                    "1.1.2": {"title": "Architecture Governance at Scale", "duration": "20 min"},
                    "1.1.3": {"title": "The Architect's Toolchain", "duration": "20 min"}
                }
            },
            "1.2": {
                "title": "Advanced Threat Modeling",
                "subsections": {
                    "1.2.1": {"title": "Beyond STRIDE: PASTA", "duration": "30 min"},
                    "1.2.2": {"title": "Supply Chain Threat Modeling", "duration": "30 min"},
                    "1.2.3": {"title": "Cloud-Native Threat Modeling", "duration": "30 min"}
                }
            },
            "1.3": {
                "title": "Regulatory Complexity & Compliance",
                "subsections": {
                    "1.3.1": {"title": "Multi-Jurisdiction Compliance", "duration": "30 min"},
                    "1.3.2": {"title": "Compliance as Code", "duration": "30 min"},
                    "1.3.3": {"title": "Audit Readiness Architecture", "duration": "30 min"}
                }
            }
        }
    },
    "Day 2": {
        "title": "Real-World Architecture Challenges",
        "duration": "4 Hours",
        "sessions": {
            "2.1": {
                "title": "M&A Integration Architecture",
                "subsections": {
                    "2.1.1": {"title": "The M&A Security Challenge", "duration": "30 min"},
                    "2.1.2": {"title": "Technical Debt Remediation", "duration": "30 min"},
                    "2.1.3": {"title": "Multi-Cloud Security", "duration": "30 min"}
                }
            },
            "2.2": {
                "title": "Zero Trust Architecture",
                "subsections": {
                    "2.2.1": {"title": "Zero Trust Fundamentals", "duration": "30 min"},
                    "2.2.2": {"title": "BeyondCorp Implementation", "duration": "30 min"},
                    "2.2.3": {"title": "Zero Trust for Legacy", "duration": "30 min"}
                }
            },
            "2.3": {
                "title": "Threat Intelligence & Attack Surface",
                "subsections": {
                    "2.3.1": {"title": "Attack Surface Management", "duration": "30 min"},
                    "2.3.2": {"title": "Threat Intelligence Operations", "duration": "30 min"},
                    "2.3.3": {"title": "Red Team / Purple Team", "duration": "30 min"}
                }
            }
        }
    },
    "Day 3": {
        "title": "Documentation & Communication",
        "duration": "4 Hours",
        "sessions": {
            "3.1": {
                "title": "Architecture Documentation",
                "subsections": {
                    "3.1.1": {"title": "C4 Architecture Diagrams", "duration": "30 min"},
                    "3.1.2": {"title": "Architecture Decision Records", "duration": "30 min"}
                }
            },
            "3.2": {
                "title": "Executive Communication",
                "subsections": {
                    "3.2.1": {"title": "Board-Level Presentations", "duration": "30 min"},
                    "3.2.2": {"title": "FAIR Risk Quantification", "duration": "30 min"},
                    "3.2.3": {"title": "Crisis Communication", "duration": "30 min"}
                }
            },
            "3.3": {
                "title": "Building Architecture Practice",
                "subsections": {
                    "3.3.1": {"title": "Hiring Architects", "duration": "30 min"},
                    "3.3.2": {"title": "ARB Operating Model", "duration": "30 min"},
                    "3.3.3": {"title": "Architecture KPIs", "duration": "30 min"}
                }
            }
        }
    },
    "Day 4": {
        "title": "Capstone & Crisis Scenarios",
        "duration": "4 Hours",
        "sessions": {
            "4.1": {
                "title": "Capstone Exercise",
                "subsections": {
                    "4.1.1": {"title": "Complete Discovery", "duration": "45 min"},
                    "4.1.2": {"title": "Solution Design", "duration": "60 min"},
                    "4.1.3": {"title": "Board Defense", "duration": "45 min"}
                }
            },
            "4.2": {
                "title": "Crisis Simulation",
                "subsections": {
                    "4.2.1": {"title": "Live Breach Response", "duration": "45 min"},
                    "4.2.2": {"title": "Post-Breach Redesign", "duration": "45 min"}
                }
            },
            "4.3": {
                "title": "Graduation & Portfolio",
                "subsections": {
                    "4.3.1": {"title": "Portfolio Review", "duration": "30 min"},
                    "4.3.2": {"title": "Final Assessment", "duration": "30 min"}
                }
            }
        }
    }
}

# ============================================================================
# MODEL ANSWERS DATABASE
# ============================================================================

ANSWERS = {
    "ma_nightmare_90day": """
**PHASE 1: DISCOVERY (Day 1-14)**

Week 1: Asset & Risk Inventory
- Scan all IP ranges, cloud accounts, domains
- Export all IAM users, service accounts, certificates
- Collect compliance certifications (SOC 2, PCI, HIPAA)
- Run vulnerability scans for critical findings

Week 2: Documentation & Assessment
- Interview acquired company's security team
- Document current-state architecture diagrams
- Identify single points of failure
- Map data flows for sensitive data
- Create initial risk register (20+ risks)

**PHASE 2: STABILIZATION (Day 15-60)**

Week 3-4: Immediate Firefighting
- Patch critical vulnerabilities (CVSS 9.0+)
- Enable MFA on all admin accounts
- Close publicly exposed storage buckets
- Implement basic monitoring and alerting

Week 5-6: IAM Bridge (Don't migrate yet)
- Set up SSO federation between IdPs
- Enable conditional access policies
- Document emergency access procedures
- Test authentication flows

Week 7-8: Network & Monitoring
- Establish VPN or cloud interconnect
- Implement network segmentation
- Deploy logs to your SIEM
- Test disaster recovery procedures

**PHASE 3: INTEGRATION (Day 61-90)**

Week 9-10: User Migration
- Migrate 10% pilot group to your IAM
- Monitor issues, fix authentication problems
- Migrate remaining users in waves
- Decommission their IdP

Week 11-12: System Migration
- Migrate critical systems to standards
- Consolidate monitoring into SIEM
- Integrate vulnerability management
- Update compliance documentation

Week 13: Validation
- Post-integration security assessment
- Update architecture documentation
- Conduct DR tabletop exercise
- Present findings to executives

**DEFERRED (Post-90 Days):**
1. PCI CDE migration (6+ months needed)
2. Legacy AD retirement (12-month project)
3. Perfect security tool consolidation
4. Security team integration/optimization

**ACCEPTED RISKS:**
1. Bridged network (not Zero Trust) for 90 days
   - Mitigation: Enhanced monitoring
   - Accepted by: VP Engineering + CISO
2. Understaffed security (2 people until backfill)
   - Mitigation: Contractor support
   - Accepted by: CISO + CFO
""",
    
    "arb_scope_answers": {
        "1": "DELEGATE - Standard implementation, no review needed",
        "2": "ARB REQUIRED - Deviation from standard (Istio not approved)",
        "3": "ARB REQUIRED - Handles PII, high risk data",
        "4": "DELEGATE - Like-for-like migration",
        "5": "ARB REQUIRED - Company-wide impact, executive approval needed",
        "6": "DELEGATE - Low-risk SaaS, lightweight vendor review OK",
        "7": "ARB REQUIRED - Crypto + open source = legal + export control review"
    },
    
    "pasta_stages": """
**Stage 1: Business Objectives (Quantified)**
NOT: "Secure the application"
YES: "Prevent $5M annual fraud from account takeover"

Objectives:
- Prevent account takeover: $5M annual loss → $500K target
- Maintain 99.99% uptime: $500K/hour downtime cost
- Pass PCI-DSS: Required for $500M/year revenue
- Protect customer trust: Breach = 20% churn = $100M loss

**Stage 2: Technical Scope**
NOT: "The web application"
YES: "React SPA → API Gateway → Auth Service → Payment Service → Postgres"

Include all trust boundaries with controls at each.

**Stage 3: Application Decomposition**
- Context diagram (external view)
- Container diagram (services/databases)
- Component diagram (internal modules)
- Security controls at EACH boundary

**Stage 4: Threat Analysis**
Map to MITRE ATT&CK:
- Initial Access → T1078 (Valid Accounts)
- Execution → T1059 (Command Execution)
- Persistence → T1136 (Create Account)
[Full kill chain with tactics]

**Stage 5: Vulnerability Analysis**
- CVE/CWE mapping
- Exploitability assessment
- Likelihood based on attacker capability
- Public exploits available?

**Stage 6: Attack Modeling**
For each attack path:
- Enumerate full kill chain
- Identify detection/prevention at each stage
- Calculate residual risk (if X fails, does Y catch it?)

**Stage 7: Risk & Impact (FAIR)**
- TEF: 500 attempts/year
- Vulnerability: 2% success rate
- LEF: 10 attacks/year
- SLE: $1.55M per incident
- ALE: $15.5M annual expected loss

With controls:
- New LEF: 1.5 attacks/year
- New ALE: $2.3M
- Risk reduced: $13.2M
- ROI: 1,786% first year
"""
}

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def calculate_progress() -> Dict:
    """Calculate overall progress"""
    total = sum(
        len(session['subsections'])
        for day in CURRICULUM.values()
        for session in day['sessions'].values()
    )
    completed = len(st.session_state.completed_exercises)
    return {
        'completed': completed,
        'total': total,
        'percentage': (completed / total * 100) if total > 0 else 0
    }

def mark_complete(exercise_id: str):
    """Mark exercise complete"""
    if exercise_id not in st.session_state.completed_exercises:
        st.session_state.completed_exercises.append(exercise_id)
        st.success(f"✅ Exercise '{exercise_id}' completed!")
        st.balloons()

# ============================================================================
# NAVIGATION
# ============================================================================

def render_sidebar():
    """Sidebar with navigation"""
    st.sidebar.title("🏛️ Enterprise Security")
    st.sidebar.caption("Architecture Masterclass")
    st.sidebar.markdown("---")
    
    # Progress
    progress = calculate_progress()
    st.sidebar.metric(
        "Progress",
        f"{progress['completed']}/{progress['total']}",
        f"{progress['percentage']:.0f}%"
    )
    st.sidebar.progress(progress['percentage'] / 100)
    
    st.sidebar.markdown("---")
    
    # Current location
    day_key = list(CURRICULUM.keys())[st.session_state.current_day - 1]
    session_key = list(CURRICULUM[day_key]['sessions'].keys())[st.session_state.current_session - 1]
    subsection_key = list(CURRICULUM[day_key]['sessions'][session_key]['subsections'].keys())[st.session_state.current_subsection - 1]
    
    st.sidebar.info(f"**Current:**\n{day_key}\n{subsection_key}")
    
    st.sidebar.markdown("---")
    
    # Quick navigation
    for day_idx, (day_key, day_data) in enumerate(CURRICULUM.items(), 1):
        with st.sidebar.expander(f"📅 {day_key}", expanded=(day_idx == st.session_state.current_day)):
            for sess_idx, (sess_key, sess_data) in enumerate(day_data['sessions'].items(), 1):
                if st.button(
                    f"{sess_key}: {sess_data['title']}",
                    key=f"nav_{day_idx}_{sess_idx}",
                    use_container_width=True
                ):
                    st.session_state.current_day = day_idx
                    st.session_state.current_session = sess_idx
                    st.session_state.current_subsection = 1
                    st.rerun()
    
    st.sidebar.markdown("---")
    
    if st.sidebar.button("📥 Export Portfolio"):
        export_portfolio()

def export_portfolio():
    """Export portfolio as JSON"""
    portfolio = {
        'metadata': {
            'date': datetime.now().isoformat(),
            'progress': calculate_progress()
        },
        'completed': st.session_state.completed_exercises,
        'day1': st.session_state.day1,
        'day2': st.session_state.day2,
        'day3': st.session_state.day3,
        'day4': st.session_state.day4
    }
    
    st.sidebar.download_button(
        "💾 Download JSON",
        json.dumps(portfolio, indent=2, default=str),
        f"portfolio_{datetime.now().strftime('%Y%m%d')}.json",
        "application/json"
    )

# ============================================================================
# CONTENT RENDERERS
# ============================================================================

def render_1_1_1():
    """What's Different at Enterprise Scale?"""
    
    st.markdown("""
    <div class="scenario-box">
    <h3>🎯 The Enterprise Reality</h3>
    <p><strong>Architecture at Scale = Managing Constraints You Didn't Choose</strong></p>
    <ul>
        <li><strong>Technical Debt:</strong> 10+ year old systems</li>
        <li><strong>Political Debt:</strong> Previous architects' decisions</li>
        <li><strong>Organizational Debt:</strong> 15 different teams</li>
        <li><strong>Regulatory Arbitrage:</strong> 40+ conflicting laws</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Exercise 1: Complexity Assessment
    st.subheader("📝 Exercise 1: Complexity Variables")
    
    tabs = st.tabs(["Your Work", "Model Answer"])
    
    with tabs[0]:
        col1, col2 = st.columns(2)
        with col1:
            tech = st.text_area("Technical Debt:", height=150, key="tech1")
            pol = st.text_area("Political Debt:", height=150, key="pol1")
        with col2:
            org = st.text_area("Organizational Debt:", height=150, key="org1")
            reg = st.text_area("Regulatory Arbitrage:", height=150, key="reg1")
        
        if st.button("💾 Save Assessment"):
            st.session_state.day1['complexity_assessment'] = {
                'tech': tech, 'pol': pol, 'org': org, 'reg': reg
            }
            st.success("Saved!")
    
    with tabs[1]:
        st.info("""
**Technical Debt Examples:**
- Windows Server 2012 (EOL, no patches)
- Custom COBOL payroll system
- SAP with 500+ customizations
- Mainframe handling critical transactions

**Political Debt Examples:**
- CTO mandated Oracle (personal relationship)
- "Temporary" compliance exception from 2019
- Vendor contracts with auto-renewal
- Previous architect's decisions everyone defends
        """)
    
    st.markdown("---")
    
    # Exercise 2: M&A 90-Day Plan
    st.subheader("📝 Exercise 2: M&A 90-Day Integration")
    
    st.markdown("""
    <div class="case-study">
    <h4>Scenario: Post-Merger Architecture Nightmare</h4>
    <p>Your company ($10B) acquires competitor ($2B). 90 days to integrate.</p>
    <p><strong>Their infrastructure:</strong></p>
    <ul>
        <li>3 different cloud accounts (no centralized IAM)</li>
        <li>Kubernetes with no service mesh</li>
        <li>On-prem AD that can't be retired</li>
        <li>PCI CDE in data center (6-month lease left)</li>
        <li>Security team of 2 (both leaving)</li>
    </ul>
    <p><strong>Create your 90-day plan.</strong></p>
    </div>
    """, unsafe_allow_html=True)
    
    plan_tabs = st.tabs(["Your Plan", "Model Answer"])
    
    with plan_tabs[0]:
        discovery = st.text_area("Discovery (D1-14):", height=150, key="disc")
        stabilization = st.text_area("Stabilization (D15-60):", height=150, key="stab")
        integration = st.text_area("Integration (D61-90):", height=150, key="integ")
        
        col1, col2 = st.columns(2)
        with col1:
            deferred = st.text_area("Deferred:", height=100, key="defer")
        with col2:
            risks = st.text_area("Accepted Risks:", height=100, key="risk")
        
        if st.button("💾 Save Plan"):
            st.session_state.day1['ma_integration'] = {
                'discovery': discovery,
                'stabilization': stabilization,
                'integration': integration,
                'deferred': deferred,
                'risks': risks
            }
            st.success("Plan saved!")
    
    with plan_tabs[1]:
        st.success(ANSWERS['ma_nightmare_90day'])
    
    # Completion
    if st.session_state.day1.get('complexity_assessment') and st.session_state.day1.get('ma_integration'):
        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Mark Exercise 1 Complete"):
                mark_complete("complexity_variables")
        with col2:
            if st.button("✅ Mark Exercise 2 Complete"):
                mark_complete("ma_nightmare")

def render_1_1_2():
    """Architecture Governance at Scale"""
    
    st.markdown("""
    <div class="scenario-box">
    <h3>🏛️ ARB at Scale</h3>
    <p>You're reviewing 50–100 architectures/year, not 5.</p>
    <p><strong>How do you scale without becoming a bottleneck?</strong></p>
    </div>
    """, unsafe_allow_html=True)
    
    # ARB Scope Quiz
    st.subheader("📝 Exercise: ARB Scope Quiz")
    
    scenarios = [
        {"id": 1, "text": "New microservice using standard platform, no PII"},
        {"id": 2, "text": "New microservice wants to use Istio (not standard)"},
        {"id": 3, "text": "New data pipeline ingesting PII"},
        {"id": 4, "text": "Migrating Oracle to managed DB (like-for-like)"},
        {"id": 5, "text": "Replacing company-wide identity provider"},
        {"id": 6, "text": "New SaaS vendor (no PII access)"},
        {"id": 7, "text": "Open-source library with crypto code"}
    ]
    
    quiz_tabs = st.tabs(["Take Quiz", "View Answers"])
    
    with quiz_tabs[0]:
        answers = {}
        for s in scenarios:
            st.write(f"**{s['id']}.** {s['text']}")
            answers[s['id']] = st.radio(
                "Decision:",
                ["ARB Required", "Delegate"],
                key=f"q{s['id']}"
            )
            st.markdown("---")
        
        if st.button("Check Answers"):
            score = 0
            for key, val in ANSWERS['arb_scope_answers'].items():
                st.write(f"**{key}.** {val}")
            st.metric("Score", "See answers above")
    
    with quiz_tabs[1]:
        for key, val in ANSWERS['arb_scope_answers'].items():
            st.write(f"**{key}.** {val}")

def render_1_2_1():
    """PASTA Threat Modeling"""
    
    st.markdown("""
    <div class="scenario-box">
    <h3>🎯 PASTA: 7-Stage Threat Analysis</h3>
    <p><strong>Scenario:</strong> Payment API processing $500M/day</p>
    <p>Recent pen test found 15 authorization bugs.</p>
    <p><strong>Board asks:</strong> "How do we avoid a Capital One breach?"</p>
    </div>
    """, unsafe_allow_html=True)
    
    tabs = st.tabs([f"Stage {i+1}" for i in range(7)])
    
    with tabs[0]:
        st.write("**Stage 1: Business Objectives**")
        objectives = st.text_area(
            "Define objectives in $ terms:",
            height=150,
            placeholder="Example: Prevent $5M fraud annually"
        )
    
    with tabs[6]:
        st.write("**Stage 7: Risk & Impact (FAIR)**")
        
        col1, col2 = st.columns(2)
        with col1:
            tef = st.number_input("Threat Event Frequency (attempts/year):", 1, 10000, 500)
            vuln = st.slider("Vulnerability (% success):", 0.0, 100.0, 2.0)
        with col2:
            sle = st.number_input("Single Loss Expectancy ($M):", 0.0, 50.0, 1.55)
        
        lef = tef * (vuln / 100)
        ale = lef * sle
        
        st.metric("ALE (Annual Loss Expectancy)", f"${ale:.1f}M")
        
        st.success(f"""
**Calculation:**
- LEF: {lef:.1f} successful attacks/year
- SLE: ${sle}M per incident
- **ALE: ${ale:.1f}M annual expected loss**
        """)
    
    # Model Answer
    with st.expander("📖 View Complete PASTA Model Answer"):
        st.info(ANSWERS['pasta_stages'])

# Placeholder renderers
def render_placeholder(title: str):
    st.title(title)
    st.info("This section is under development. Structure ready for implementation.")
    st.write("Follow the pattern from Sessions 1.1.1 and 1.1.2 to complete this section.")

# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    render_sidebar()
    
    # Get current location
    day_key = list(CURRICULUM.keys())[st.session_state.current_day - 1]
    session_key = list(CURRICULUM[day_key]['sessions'].keys())[st.session_state.current_session - 1]
    subsection_key = list(CURRICULUM[day_key]['sessions'][session_key]['subsections'].keys())[st.session_state.current_subsection - 1]
    current = CURRICULUM[day_key]['sessions'][session_key]['subsections'][subsection_key]
    
    # Header
    st.title(f"{subsection_key}: {current['title']}")
    st.caption(f"{day_key} • {session_key} • {current['duration']}")
    st.markdown("---")
    
    # Route to content
    day = st.session_state.current_day
    session = st.session_state.current_session
    subsection = st.session_state.current_subsection
    
    if day == 1:
        if session == 1:
            if subsection == 1:
                render_1_1_1()
            elif subsection == 2:
                render_1_1_2()
            else:
                render_placeholder(current['title'])
        elif session == 2:
            if subsection == 1:
                render_1_2_1()
            else:
                render_placeholder(current['title'])
        else:
            render_placeholder(current['title'])
    else:
        render_placeholder(current['title'])
    
    # Navigation
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("⬅️ Previous"):
            navigate_previous()
    with col3:
        if st.button("Next ➡️"):
            navigate_next()

def navigate_previous():
    if st.session_state.current_subsection > 1:
        st.session_state.current_subsection -= 1
    elif st.session_state.current_session > 1:
        st.session_state.current_session -= 1
        day_key = list(CURRICULUM.keys())[st.session_state.current_day - 1]
        session_key = list(CURRICULUM[day_key]['sessions'].keys())[st.session_state.current_session - 1]
        st.session_state.current_subsection = len(CURRICULUM[day_key]['sessions'][session_key]['subsections'])
    elif st.session_state.current_day > 1:
        st.session_state.current_day -= 1
        day_key = list(CURRICULUM.keys())[st.session_state.current_day - 1]
        st.session_state.current_session = len(CURRICULUM[day_key]['sessions'])
        last_session_key = list(CURRICULUM[day_key]['sessions'].keys())[-1]
        st.session_state.current_subsection = len(CURRICULUM[day_key]['sessions'][last_session_key]['subsections'])
    st.rerun()

def navigate_next():
    day_key = list(CURRICULUM.keys())[st.session_state.current_day - 1]
    session_key = list(CURRICULUM[day_key]['sessions'].keys())[st.session_state.current_session - 1]
    
    if st.session_state.current_subsection < len(CURRICULUM[day_key]['sessions'][session_key]['subsections']):
        st.session_state.current_subsection += 1
    elif st.session_state.current_session < len(CURRICULUM[day_key]['sessions']):
        st.session_state.current_session += 1
        st.session_state.current_subsection = 1
    elif st.session_state.current_day < len(CURRICULUM):
        st.session_state.current_day += 1
        st.session_state.current_session = 1
        st.session_state.current_subsection = 1
    st.rerun()

if __name__ == "__main__":
    main()
