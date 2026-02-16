"""
COMPLETE SECURITY ARCHITECT IMMERSION WORKSHOP
Live the Day, Learn the Practice

Based on:
- Security Patterns (securitypatterns.io)
- C4 Model (c4model.com)
- Real enterprise architecture practice
- TOGAF, SABSA, NIST frameworks

You'll learn:
✓ How to conduct stakeholder discovery
✓ How to apply security patterns to real problems
✓ How to create C4 diagrams that communicate
✓ How to make and defend architecture decisions
✓ How to build trust with technical and business leaders
✓ How to structure your work as a practicing architect
"""

import streamlit as st
import pandas as pd
import json
from datetime import datetime, time
import plotly.graph_objects as go

st.set_page_config(page_title="Security Architect Immersion", layout="wide", page_icon="🏛️")

# ============================================================================
# STYLING
# ============================================================================

st.markdown("""
<style>
    .day-header { 
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: white; padding: 2rem; border-radius: 12px; margin-bottom: 2rem;
    }
    .stakeholder-card {
        background: white; border-left: 5px solid #3b82f6;
        padding: 1.5rem; margin: 1rem 0; border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    .pattern-card {
        background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%);
        border: 2px solid #10b981; padding: 1.5rem; margin: 1rem 0;
        border-radius: 10px; cursor: pointer;
    }
    .pattern-card:hover { box-shadow: 0 4px 16px rgba(16, 185, 129, 0.3); }
    .c4-box {
        background: #f8fafc; border: 2px solid #94a3b8;
        padding: 1rem; margin: 0.5rem; border-radius: 8px;
        font-family: 'Courier New', monospace; white-space: pre;
    }
    .decision-card {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        border-left: 5px solid #f59e0b; padding: 1.5rem; margin: 1rem 0;
        border-radius: 8px;
    }
    .dialogue-user {
        background: #e0f2fe; border-left: 4px solid #0ea5e9;
        padding: 1rem; margin: 0.5rem 0; border-radius: 4px;
    }
    .dialogue-architect {
        background: #dcfce7; border-left: 4px solid #22c55e;
        padding: 1rem; margin: 0.5rem 0; border-radius: 4px;
    }
    .threat-card {
        background: #fee2e2; border-left: 4px solid #ef4444;
        padding: 1rem; margin: 0.5rem 0; border-radius: 4px;
    }
    .mitigation-card {
        background: #dbeafe; border-left: 4px solid #3b82f6;
        padding: 1rem; margin: 0.5rem 0; border-radius: 4px;
    }
    .adr-template {
        background: white; border: 2px solid #e5e7eb;
        padding: 2rem; margin: 1rem 0; border-radius: 10px;
        font-family: 'Courier New', monospace; font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# SESSION STATE
# ============================================================================

def init_state():
    defaults = {
        'day': 1, 'time': '09:00', 'scenario': 'healthcare_platform',
        'completed': [], 'relationships': {'cto': 50, 'ciso': 70, 'cfo': 40, 'vp_eng': 60},
        'architecture': {'patterns': [], 'diagrams': {}, 'decisions': [], 'questions_asked': []},
        'stakeholder_notes': {}, 'threat_model': {}, 'design_artifacts': {}
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# ============================================================================
# SECURITY PATTERNS - Based on securitypatterns.io
# ============================================================================

SECURITY_PATTERNS = {
    "authentication_gateway": {
        "name": "Authentication Gateway",
        "category": "Identity & Access",
        "problem": "Multiple applications need consistent authentication without duplicating auth logic",
        "solution": "Centralized authentication service issues tokens validated by downstream services",
        "context": "Microservices, distributed systems, multiple applications sharing identity",
        "forces": [
            "Need consistent auth across services",
            "Don't want auth logic in every service",
            "Need centralized audit trail",
            "Token format must be standardized"
        ],
        "structure": """
┌─────────────┐
│   Client    │
└──────┬──────┘
       │ 1. Auth Request (username/password)
       ▼
┌───────────────────┐
│  Auth Gateway     │
│  - Validates creds│
│  - Issues JWT     │──▶ Token Store
│  - Enforces MFA   │
└─────────┬─────────┘
          │ 2. JWT Token
          ▼
┌──────────────────┐
│  Application     │
│  - Validates JWT │
│  - Checks claims │
└──────────────────┘
""",
        "consequences": {
            "benefits": [
                "Consistent authentication across all services",
                "Centralized MFA enforcement",
                "Single audit trail for all authentication",
                "Token revocation at gateway level",
                "Simplified application code"
            ],
            "liabilities": [
                "Single point of failure (needs HA)",
                "Token theft gives broad access",
                "Token validation adds latency",
                "Complex key management"
            ]
        },
        "threats_addressed": [
            "Inconsistent authentication",
            "Credential stuffing (MFA at gateway)",
            "Weak password policies",
            "No audit trail"
        ],
        "related_patterns": ["Token-Based Authorization", "API Gateway", "Service Mesh"],
        "real_world_examples": [
            "OAuth 2.0 Authorization Server",
            "SAML Identity Provider",
            "OpenID Connect Provider"
        ]
    },
    
    "defense_in_depth": {
        "name": "Defense in Depth",
        "category": "Defense Strategy",
        "problem": "Single security control can fail, leaving system vulnerable",
        "solution": "Layer multiple independent security controls so failure of one doesn't compromise system",
        "context": "High-value assets, regulatory requirements, sophisticated attackers",
        "forces": [
            "No single control is perfect",
            "Budget constraints limit depth",
            "More layers = more complexity",
            "Controls must be independent"
        ],
        "structure": """
Attacker
   │
   ▼
┌────────────────────┐ Layer 1: Perimeter
│  Firewall/WAF      │ (Blocks 95% of attacks)
└────────┬───────────┘
         │ 5% bypass
         ▼
┌────────────────────┐ Layer 2: Network
│  IDS/IPS           │ (Detects 80% of remaining)
└────────┬───────────┘
         │ 1% bypass
         ▼
┌────────────────────┐ Layer 3: Application
│  Input Validation  │ (Blocks 90% of remaining)
└────────┬───────────┘
         │ 0.1% bypass
         ▼
┌────────────────────┐ Layer 4: Data
│  Encryption        │ (Protects data if accessed)
└────────────────────┘
""",
        "consequences": {
            "benefits": [
                "No single point of failure",
                "Time for detection and response",
                "Protects against unknown attacks",
                "Reduces blast radius"
            ],
            "liabilities": [
                "Higher cost (multiple controls)",
                "Increased complexity",
                "Alert fatigue from multiple systems",
                "May create false sense of security"
            ]
        },
        "threats_addressed": [
            "Zero-day exploits",
            "Advanced persistent threats",
            "Insider threats",
            "Control bypass"
        ],
        "related_patterns": ["Layered Security", "Fail Secure", "Separation of Concerns"],
        "real_world_examples": [
            "Bank physical security (guards + cameras + vaults + alarms)",
            "Web application (WAF + input validation + parameterized queries + encryption)",
            "Network (firewall + IDS + segmentation + encryption)"
        ]
    },
    
    "least_privilege": {
        "name": "Least Privilege",
        "category": "Access Control",
        "problem": "Users with excessive privileges increase attack surface and insider threat risk",
        "solution": "Grant minimum permissions required for job function, nothing more",
        "context": "Any system with multiple users and privilege levels",
        "forces": [
            "Users request more access than needed",
            "Access creep over time",
            "Business wants convenience",
            "Security wants minimal access"
        ],
        "structure": """
Access Request
   │
   ▼
┌──────────────────────┐
│  Job Function        │
│  - What tasks needed?│
│  - For how long?     │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│  Minimum Permissions │
│  - Read only         │
│  - Specific resources│
│  - Time-bound        │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│  Regular Review      │
│  - Still needed?     │
│  - Remove if not     │
└──────────────────────┘
""",
        "consequences": {
            "benefits": [
                "Reduces blast radius of compromised account",
                "Limits insider threat damage",
                "Audit trail more meaningful",
                "Compliance requirement satisfaction"
            ],
            "liabilities": [
                "Users request more access",
                "Breaks workflows if too restrictive",
                "Administrative overhead",
                "Requires good RBAC design"
            ]
        },
        "threats_addressed": [
            "Privilege escalation",
            "Insider threats",
            "Compromised credentials",
            "Lateral movement"
        ],
        "related_patterns": ["Role-Based Access Control", "Just-in-Time Access", "Separation of Duties"],
        "real_world_examples": [
            "Database admin can't read production data",
            "Developer can't deploy to production",
            "Support engineer has read-only access"
        ]
    },
    
    "zero_trust_network": {
        "name": "Zero Trust Network",
        "category": "Network Security",
        "problem": "Traditional 'castle and moat' assumes inside = trusted, but breaches happen",
        "solution": "Never trust, always verify - authenticate and authorize every request regardless of location",
        "context": "Cloud environments, remote work, insider threats, regulatory requirements",
        "forces": [
            "Perimeter is dissolving (cloud, mobile, remote)",
            "Insider threats exist",
            "Need flexibility without sacrificing security",
            "Legacy systems may not support"
        ],
        "structure": """
User/Service Request
   │
   ▼
┌──────────────────────┐
│  Policy Engine       │
│  1. Who (identity)   │
│  2. What (resource)  │
│  3. Where (location) │
│  4. When (time)      │
│  5. How (device)     │
└──────────┬───────────┘
           │ Evaluate
           ▼
     ┌─────────┐
     │ Allow?  │
     └────┬────┘
          │
    Yes   │   No
    ┌─────┴─────┐
    ▼           ▼
┌────────┐  ┌───────┐
│ Grant  │  │ Deny  │
│ Access │  │ + Log │
└────────┘  └───────┘
""",
        "consequences": {
            "benefits": [
                "No implicit trust based on location",
                "Limits lateral movement",
                "Detailed audit trail",
                "Works for cloud/remote"
            ],
            "liabilities": [
                "Complex to implement",
                "Every request checked (latency)",
                "Requires identity everywhere",
                "Legacy systems hard to retrofit"
            ]
        },
        "threats_addressed": [
            "Lateral movement",
            "Compromised internal network",
            "Insider threats",
            "Stolen credentials"
        ],
        "related_patterns": ["Micro-segmentation", "Identity-Based Access", "Continuous Verification"],
        "real_world_examples": [
            "Google BeyondCorp",
            "NIST SP 800-207",
            "Service mesh (Istio, Linkerd)"
        ]
    },
    
    "secure_by_default": {
        "name": "Secure by Default",
        "category": "Design Principle",
        "problem": "Developers make insecure choices when secure option is harder",
        "solution": "Make the secure path the easy path - secure defaults, guardrails, paved roads",
        "context": "Platform engineering, developer tools, infrastructure as code",
        "forces": [
            "Developers prioritize speed over security",
            "Secure configuration is complex",
            "Insecure is often the default",
            "Training doesn't scale"
        ],
        "structure": """
Developer Request
   │
   ▼
┌──────────────────────┐
│  Platform/Catalog    │
│  - Golden images     │
│  - Secure templates  │
│  - Pre-approved      │
└──────────┬───────────┘
           │ Self-service
           ▼
┌──────────────────────┐
│  Guardrails          │
│  - Policy as code    │
│  - Auto-remediation  │
│  - Compliance checks │
└──────────┬───────────┘
           │ Validation
           ▼
┌──────────────────────┐
│  Deployment          │
│  - Already secure    │
│  - No manual config  │
└──────────────────────┘
""",
        "consequences": {
            "benefits": [
                "Scales security (no bottleneck)",
                "Consistent security posture",
                "Faster development",
                "Reduces human error"
            ],
            "liabilities": [
                "Platform team becomes critical",
                "May not fit all use cases",
                "Initial platform build expensive",
                "Requires culture shift"
            ]
        },
        "threats_addressed": [
            "Misconfiguration",
            "Configuration drift",
            "Shadow IT",
            "Inconsistent security"
        ],
        "related_patterns": ["Paved Road", "Golden Path", "Platform Engineering"],
        "real_world_examples": [
            "GitHub Actions with built-in security scanning",
            "Kubernetes with PodSecurityStandards",
            "Internal developer platform"
        ]
    }
}

# ============================================================================
# SCENARIO: HEALTHCARE PLATFORM
# ============================================================================

SCENARIO = {
    "name": "HealthTech Platform - Electronic Health Records",
    "company": "MedSecure Health Systems",
    "your_role": "Senior Security Architect",
    "context": """
**Company:** Regional healthcare network serving 500,000 patients across 15 hospitals

**Current Situation:**
- Modernizing legacy EHR (Electronic Health Records) system
- Must comply with HIPAA, HITECH, state medical privacy laws
- Integration with labs, pharmacies, insurance companies
- Mobile app for patient access
- Clinician portal for doctors/nurses
- Recent ransomware attack on competitor raised board concerns

**Architecture Challenge:**
You're designing security architecture for new cloud-based EHR platform.

**Stakeholders:**
- **Dr. Robert Chen (CMIO - Chief Medical Information Officer):** Clinician, wants usability
- **Linda Martinez (CFO):** Budget-conscious, risk-averse
- **James Wilson (CTO):** Wants modern architecture, microservices
- **Sarah Johnson (CISO):** Your boss, compliance-focused
- **Dr. Emily Parker (Privacy Officer):** HIPAA expert, protective of patient data
""",
    "requirements": {
        "functional": [
            "Store patient medical records (history, medications, allergies, labs)",
            "Real-time access for clinicians (ER needs instant access)",
            "Patient portal (view records, schedule appointments, messaging)",
            "Integration with external systems (labs, pharmacies, insurance)",
            "Mobile app for clinicians (tablet access at bedside)",
            "Audit trail (who accessed which patient record, when)"
        ],
        "security": [
            "HIPAA compliance (PHI protection)",
            "Access control (role-based, clinician can only see assigned patients)",
            "Audit logging (immutable, 7-year retention)",
            "Encryption (at rest and in transit)",
            "Breach notification (report to HHS if >500 records)",
            "Data minimization (principle of least privilege)",
            "Emergency access (break-glass for life-threatening situations)"
        ],
        "constraints": [
            "Budget: $3M for security architecture",
            "Timeline: 18 months to production",
            "Cannot disrupt current EHR during migration",
            "Must support 10,000 concurrent users",
            "99.9% uptime (clinicians can't wait for systems)",
            "Rural hospitals have poor internet connectivity"
        ]
    }
}

# ============================================================================
# ACTIVITIES
# ============================================================================

def activity_stakeholder_discovery():
    """Learn to conduct stakeholder discovery"""
    st.markdown('<div class="day-header"><h2>Activity 1: Stakeholder Discovery</h2><p>Learn what they really need (not what they say they want)</p></div>', unsafe_allow_html=True)
    
    st.write("""
    **The Architect's First Job: Understand the Problem**
    
    Before you design anything, you must understand:
    - What problem are we solving?
    - Why does it matter?
    - Who are the stakeholders?
    - What are their concerns?
    - What are the constraints?
    
    Bad architects jump to solutions. Good architects ask questions.
    """)
    
    st.markdown("---")
    st.subheader("🎭 Scenario: Meeting with CMIO")
    
    st.markdown("""
    <div class="stakeholder-card">
    <h4>Dr. Robert Chen - Chief Medical Information Officer</h4>
    <p><strong>Background:</strong> Practicing emergency room physician, 20 years experience</p>
    <p><strong>Role:</strong> Represents clinician needs, focuses on patient care</p>
    <p><strong>Initial Statement:</strong></p>
    <div class="dialogue-user">
    "We need this new EHR system to be secure, obviously. But my main concern is usability.
    Our current system requires 7 clicks to order a medication. In the ER, seconds matter.
    
    Also, we had an incident last month where a nurse couldn't access a patient's allergy
    information because the 'security system' locked her out after 3 failed password attempts.
    The patient had a severe reaction to a medication we gave them because we didn't know
    about the allergy.
    
    Security is important, but if it gets in the way of patient care, people die.
    Make sure your security architecture doesn't kill anyone."
    </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("### Your Discovery Questions")
    st.write("What questions would you ask to truly understand his concerns?")
    
    questions = st.multiselect(
        "Select questions to ask (choose 3-5):",
        [
            "❌ What encryption algorithm do you want? (Too technical)",
            "✅ Can you walk me through a typical workflow? (Understand process)",
            "✅ What's the biggest security friction point today? (Find pain)",
            "✅ Tell me about the allergy incident - what happened? (Learn from failure)",
            "❌ Do you want MFA enabled? (Closed question, limits discovery)",
            "✅ How do clinicians handle emergency situations today? (Understand exceptions)",
            "✅ What would 'good security' look like to you? (Understand expectations)",
            "❌ Have you read NIST SP 800-66? (Condescending)",
            "✅ What security controls have clinicians worked around? (Find workarounds)",
            "✅ How long can a clinician wait for system access? (Quantify constraints)",
        ]
    )
    
    if len(questions) >= 3:
        st.success("✅ Good questioning! You're conducting discovery, not jumping to solutions.")
        
        st.write("### Dr. Chen's Responses")
        
        st.markdown("""
        <div class="dialogue-user">
        <strong>Typical Workflow:</strong> "In ER, patient arrives → triage nurse takes vitals →
        assigns to bed → physician sees patient → orders labs/imaging → reviews results → 
        prescribes treatment. Each step needs system access. If system is slow or blocks access,
        patient waits. Wait time = bad outcomes."
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="dialogue-user">
        <strong>Allergy Incident:</strong> "Nurse had been on vacation for 2 weeks. When she came back,
        her password had expired. She couldn't remember new password, locked account after 3 tries.
        IT said they'd reset it in 30 minutes. We couldn't wait. Used a colleague's login (yes, we
        know it's wrong). Colleague didn't have access to allergy info because not assigned to that
        patient. We prescribed penicillin. Patient was allergic. Went into anaphylactic shock."
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="dialogue-user">
        <strong>Emergency Access:</strong> "We need 'break-glass' access. If it's life-threatening,
        any clinician should be able to access any patient record. Log it, audit it later, but don't
        block it. Patient safety comes first."
        </div>
        """, unsafe_allow_html=True)
        
        st.write("### What Did You Learn?")
        
        insights = st.text_area(
            "Document key insights and constraints:",
            height=200,
            placeholder="""Example insights:
1. Constraint: Access delay = patient harm (hard requirement)
2. Problem: Password complexity vs cognitive load (nurses work 12-hour shifts)
3. Requirement: Break-glass access for emergencies (log but don't block)
4. Risk: Shared credentials due to access friction (workaround behavior)
5. Stakeholder concern: "Security that kills patients" = instant career-ender for you

Architectural implications:
- Need biometric auth (fingerprint, badge tap) - no passwords to forget
- Need emergency access with post-hoc audit
- Need fast authentication (sub-second response time)
- Access control must account for patient assignment + emergency override""",
            key="discovery_insights"
        )
        
        if insights:
            st.session_state.stakeholder_notes['cmio'] = insights
            st.markdown("""
            <div class="dialogue-architect">
            <strong>Your Response:</strong> "Thank you Dr. Chen. I understand now that:
            
            1. Access speed is a patient safety requirement, not a convenience
            2. We need break-glass access for emergencies
            3. Password-based auth has failed in practice
            
            Let me propose: Biometric authentication (badge + fingerprint) for normal access,
            emergency override with SMS notification to security team for life-threatening situations,
            and post-hoc audit review. Would that address your concerns while maintaining security?"
            </div>
            """, unsafe_allow_html=True)
            
            st.success("🎯 **Architect Win:** You understood the real requirements, not just the stated ones")

def activity_pattern_selection():
    """Interactive pattern selection workshop"""
    st.markdown('<div class="day-header"><h2>Activity 2: Security Pattern Selection</h2><p>Choose the right patterns for the problem</p></div>', unsafe_allow_html=True)
    
    st.write("""
    **Given what you learned from stakeholders, which security patterns apply?**
    
    Remember the requirements:
    - Fast access (clinicians can't wait)
    - Emergency break-glass access
    - HIPAA compliance
    - Audit trail
    - Integration with external systems
    """)
    
    st.write("### Available Security Patterns")
    
    for pattern_id, pattern in SECURITY_PATTERNS.items():
        with st.expander(f"📘 {pattern['name']}", expanded=False):
            st.write(f"**Problem:** {pattern['problem']}")
            st.write(f"**Solution:** {pattern['solution']}")
            st.write(f"**Context:** {pattern['context']}")
            
            st.write("**Forces:**")
            for force in pattern['forces']:
                st.write(f"- {force}")
            
            st.markdown(f'<div class="c4-box">{pattern["structure"]}</div>', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                st.write("**Benefits:**")
                for benefit in pattern['consequences']['benefits']:
                    st.write(f"✅ {benefit}")
            with col2:
                st.write("**Liabilities:**")
                for liability in pattern['consequences']['liabilities']:
                    st.write(f"⚠️ {liability}")
            
            st.write("**Threats Addressed:**")
            for threat in pattern['threats_addressed']:
                st.write(f"🛡️ {threat}")
            
            if st.checkbox(f"Select {pattern['name']}", key=f"pattern_{pattern_id}"):
                if pattern_id not in st.session_state.architecture['patterns']:
                    st.session_state.architecture['patterns'].append(pattern_id)
    
    if st.session_state.architecture['patterns']:
        st.write("### Your Selected Patterns")
        for pid in st.session_state.architecture['patterns']:
            st.write(f"✅ {SECURITY_PATTERNS[pid]['name']}")
        
        st.write("### Justify Your Selection")
        
        justification = st.text_area(
            "Why did you select these patterns? How do they work together?",
            height=200,
            placeholder="""For each pattern, explain:
1. Which requirement or threat does it address?
2. Why is it appropriate for this context?
3. What trade-offs are you accepting?
4. How does it interact with other patterns?

Example:
"I selected Authentication Gateway because:
- Addresses: Fast access requirement (centralized auth = single sign-on)
- Context fit: Multiple systems (EHR, labs, pharmacy) need consistent identity
- Trade-off: Single point of failure, but we'll make it highly available
- Interaction: Works with Least Privilege pattern to control access per role"
""",
            key="pattern_justification"
        )
        
        if justification:
            st.markdown("""
            <div class="dialogue-architect">
            <h4>Expert Analysis:</h4>
            
            <p><strong>Recommended Pattern Combination for Healthcare EHR:</strong></p>
            
            <ol>
                <li><strong>Authentication Gateway ✅ Must Have</strong>
                    <ul>
                        <li>Why: Single sign-on across EHR, labs, pharmacy</li>
                        <li>HIPAA: Centralized audit trail of access</li>
                        <li>Speed: Authenticate once, access all systems</li>
                    </ul>
                </li>
                
                <li><strong>Least Privilege ✅ Must Have</strong>
                    <ul>
                        <li>Why: HIPAA minimum necessary standard</li>
                        <li>Implementation: Role-based access + patient assignment</li>
                        <li>Emergency: Break-glass with post-hoc audit</li>
                    </ul>
                </li>
                
                <li><strong>Defense in Depth ✅ Must Have</strong>
                    <ul>
                        <li>Why: PHI is high-value target (ransomware risk)</li>
                        <li>Layers: Network segmentation + encryption + DLP + monitoring</li>
                        <li>Rationale: No single control protects 500,000 patient records</li>
                    </ul>
                </li>
                
                <li><strong>Zero Trust Network ⚠️ Consider</strong>
                    <ul>
                        <li>Why: Remote clinicians, mobile devices, third-party integrations</li>
                        <li>Trade-off: Complexity vs security for external access</li>
                        <li>Phased: Start with VPN, evolve to Zero Trust over 2 years</li>
                    </ul>
                </li>
                
                <li><strong>Secure by Default ✅ Should Have</strong>
                    <ul>
                        <li>Why: Scale security across development teams</li>
                        <li>Implementation: Internal platform with pre-approved patterns</li>
                        <li>Benefit: Developers can't deploy insecure configurations</li>
                    </ul>
                </li>
            </ol>
            
            <p><strong>How They Work Together:</strong></p>
            <ul>
                <li>Authentication Gateway provides identity foundation</li>
                <li>Least Privilege controls what authenticated users can access</li>
                <li>Defense in Depth protects data at multiple layers</li>
                <li>Secure by Default prevents misconfigurations</li>
            </ul>
            
            <p><strong>Pattern Conflicts to Resolve:</strong></p>
            <ul>
                <li>⚠️ Least Privilege vs Emergency Access: Resolved with break-glass pattern</li>
                <li>⚠️ Defense in Depth vs Performance: Each layer adds latency (must measure)</li>
                <li>⚠️ Zero Trust vs Rural Connectivity: May not work on slow connections</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)

def activity_c4_modeling():
    """Teach C4 model for architecture documentation"""
    st.markdown('<div class="day-header"><h2>Activity 3: C4 Architecture Diagrams</h2><p>Document your architecture so others understand it</p></div>', unsafe_allow_html=True)
    
    st.write("""
    **C4 Model = Context, Containers, Components, Code**
    
    A hierarchical way to communicate architecture at different levels of abstraction.
    
    Based on Simon Brown's C4 model (c4model.com)
    """)
    
    level = st.selectbox(
        "Select C4 Level:",
        ["Level 1: Context Diagram", "Level 2: Container Diagram", "Level 3: Component Diagram"]
    )
    
    if "Context" in level:
        st.write("### Level 1: Context Diagram")
        st.write("**Shows:** System in the context of users and other systems")
        st.write("**Audience:** Everyone (executives, business, technical)")
        st.write("**Purpose:** Big picture - what is this system and who uses it?")
        
        st.markdown("""
        <div class="c4-box">
        Example: Healthcare EHR Context Diagram

┌──────────────┐
│  Clinician   │ (Person)
│  Doctor/     │
│  Nurse       │
└──────┬───────┘
       │ Accesses patient records
       │ via web/mobile
       ▼
┌─────────────────────────────────┐
│   MedSecure EHR System          │ (System)
│                                 │
│   Electronic Health Records     │
│   - Patient records             │
│   - Medications                 │
│   - Lab results                 │
│   - Appointments                │
└────┬──────────────────┬─────────┘
     │                  │
     │ Sends orders     │ Receives results
     │                  │
     ▼                  ▼
┌──────────┐      ┌──────────────┐
│   Lab    │      │   Pharmacy   │ (External Systems)
│  System  │      │    System    │
└──────────┘      └──────────────┘

┌──────────────┐
│   Patient    │ (Person)
│              │
└──────┬───────┘
       │ Views own records
       │ via patient portal
       │
       └──▶ (MedSecure EHR System)
        </div>
        """, unsafe_allow_html=True)
        
        st.write("### Exercise: Create Context Diagram for Your System")
        
        st.write("**Step 1: Identify People (Actors)**")
        actors = st.text_area(
            "Who are the users of this system?",
            placeholder="""Example:
- Clinicians (doctors, nurses, specialists)
- Patients (viewing their own records)
- Administrators (managing the system)
- Billing staff (processing claims)""",
            key="c4_actors"
        )
        
        st.write("**Step 2: Identify External Systems**")
        external = st.text_area(
            "What other systems does this integrate with?",
            placeholder="""Example:
- Lab system (Quest Diagnostics, LabCorp)
- Pharmacy system (SureScripts for e-prescriptions)
- Insurance systems (claims processing)
- Health Information Exchange (HIE - sharing with other hospitals)""",
            key="c4_external"
        )
        
        st.write("**Step 3: Describe Relationships**")
        relationships = st.text_area(
            "How do they interact?",
            placeholder="""Example:
- Clinician → EHR: "Accesses patient records via web browser (HTTPS)"
- EHR → Lab: "Sends lab orders via HL7 interface"
- Lab → EHR: "Returns results via HL7 interface"
- Patient → EHR: "Views records via mobile app (REST API)"
- EHR → Pharmacy: "Sends prescriptions via NCPDP SCRIPT"
""",
            key="c4_relationships"
        )
        
        if actors and external and relationships:
            st.success("✅ You've identified the key elements of a Context Diagram!")
            
            st.write("### Now Add Security Annotations")
            
            security_annotations = st.text_area(
                "For each relationship, what security controls exist?",
                placeholder="""Example:
- Clinician → EHR: 
  * Authentication: SAML SSO with MFA
  * Authorization: RBAC based on role + patient assignment
  * Encryption: TLS 1.3
  * Audit: All access logged to immutable log store

- EHR → Lab:
  * Authentication: mTLS (mutual certificate authentication)
  * Authorization: Lab can only receive orders, not query patient data
  * Encryption: TLS 1.3 + HL7 message encryption
  * Audit: All orders and results logged with correlation ID
""",
                key="c4_security"
            )
            
            if security_annotations:
                st.markdown("""
                <div class="dialogue-architect">
                <h4>✅ Excellent! You've created a security-annotated Context Diagram</h4>
                
                <p><strong>What makes this diagram useful:</strong></p>
                <ul>
                    <li>Shows WHAT, not HOW (appropriate abstraction level)</li>
                    <li>Everyone can understand it (executives to engineers)</li>
                    <li>Security controls are visible (audit/compliance friendly)</li>
                    <li>Shows trust boundaries (where data crosses boundaries)</li>
                </ul>
                
                <p><strong>Next Steps:</strong></p>
                <ul>
                    <li>Level 2: Container Diagram (show internal services)</li>
                    <li>Level 3: Component Diagram (show internal modules)</li>
                    <li>Keep diagrams updated (living documentation)</li>
                </ul>
                </div>
                """, unsafe_allow_html=True)
                
                st.session_state.architecture['diagrams']['context'] = {
                    'actors': actors,
                    'external': external,
                    'relationships': relationships,
                    'security': security_annotations
                }
    
    elif "Container" in level:
        st.write("### Level 2: Container Diagram")
        st.write("**Shows:** Major technical building blocks (services, databases, etc.)")
        st.write("**Audience:** Technical stakeholders, architects, lead engineers")
        
        st.markdown("""
        <div class="c4-box">
        Example: Healthcare EHR Container Diagram

┌─────────────────────────────────────────────┐
│          MedSecure EHR System               │
│                                             │
│  ┌──────────────┐      ┌──────────────┐   │
│  │   Web App    │      │  Mobile App  │   │
│  │   (React)    │      │   (Native)   │   │
│  └──────┬───────┘      └──────┬───────┘   │
│         │ HTTPS                │ HTTPS     │
│         └──────────┬───────────┘           │
│                    ▼                        │
│         ┌────────────────────┐             │
│         │   API Gateway      │             │
│         │   - Auth (JWT)     │             │
│         │   - Rate limiting  │             │
│         │   - Logging        │             │
│         └─────────┬──────────┘             │
│                   │ Internal                │
│         ┌─────────┴─────────┐              │
│         ▼                   ▼              │
│  ┌─────────────┐    ┌──────────────┐      │
│  │  Patient    │    │  Clinical    │      │
│  │  Service    │    │   Service    │      │
│  │  (Node.js)  │    │  (Java)      │      │
│  └──────┬──────┘    └──────┬───────┘      │
│         │ Reads/Writes      │ Reads/Writes │
│         └─────────┬─────────┘              │
│                   ▼                        │
│         ┌────────────────────┐             │
│         │  Patient Database  │             │
│         │  (PostgreSQL)      │             │
│         │  - Encrypted        │             │
│         │  - Row-level        │             │
│         │    security         │             │
│         └────────────────────┘             │
└─────────────────────────────────────────────┘
        </div>
        """, unsafe_allow_html=True)

def activity_threat_modeling():
    """Interactive threat modeling session"""
    st.markdown('<div class="day-header"><h2>Activity 4: Threat Modeling</h2><p>What could go wrong and how do we prevent it?</p></div>', unsafe_allow_html=True)
    
    st.write("""
    **Threat Modeling Process:**
    1. What are we building?
    2. What can go wrong?
    3. What are we going to do about it?
    4. Did we do a good job?
    """)
    
    st.write("### System Under Analysis: Patient Portal")
    
    st.markdown("""
    <div class="stakeholder-card">
    <h4>Patient Portal Components:</h4>
    <ul>
        <li>Web application (React SPA)</li>
        <li>Mobile app (iOS/Android native)</li>
        <li>API gateway (authentication, rate limiting)</li>
        <li>Patient service (business logic)</li>
        <li>Database (patient records, medications, appointments)</li>
    </ul>
    
    <h4>Data Flows:</h4>
    <ol>
        <li>Patient logs in with username/password</li>
        <li>API gateway authenticates, returns JWT</li>
        <li>Patient requests medical records</li>
        <li>Patient service queries database</li>
        <li>Records returned to patient</li>
    </ol>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("### Identify Threats (STRIDE Methodology)")
    
    st.write("""
    **STRIDE Categories:**
    - **S**poofing: Impersonating someone else
    - **T**ampering: Modifying data
    - **R**epudiation: Denying actions
    - **I**nformation Disclosure: Exposing information
    - **D**enial of Service: Disrupting availability
    - **E**levation of Privilege: Gaining unauthorized access
    """)
    
    threats = []
    
    with st.expander("🔴 Spoofing Threats", expanded=True):
        st.write("**What spoofing threats exist?**")
        
        spoofing = st.multiselect(
            "Identify spoofing threats:",
            [
                "✅ Attacker steals patient credentials (phishing)",
                "✅ Attacker uses stolen JWT token",
                "✅ Attacker creates fake patient account",
                "❌ Attacker DDoS the API (wrong category - that's Denial of Service)",
                "✅ Attacker hijacks session (session fixation)",
                "✅ Man-in-the-middle intercepts authentication"
            ]
        )
        
        if spoofing:
            st.write("### Proposed Mitigations:")
            
            mitigations = st.text_area(
                "How would you mitigate these threats?",
                placeholder="""For each threat, propose specific controls:

Example:
Threat: Attacker steals credentials via phishing
Mitigation:
1. Multi-factor authentication (MFA) required for all logins
   - SMS OTP or authenticator app
   - Cost: $2/user/month
2. Security awareness training for patients
   - Email campaign about phishing
   - Cost: $5K/year
3. Monitor for suspicious login patterns
   - Login from new device/location = email notification
   - Cost: Included in SIEM
4. Rate limiting on login attempts
   - 5 failed attempts = temporary account lock
   - Cost: Free (API gateway feature)

Residual Risk: Sophisticated phishing may still succeed, but MFA prevents account takeover""",
                key="spoofing_mitigations"
            )
            
            if mitigations:
                st.markdown("""
                <div class="mitigation-card">
                <strong>✅ Good threat modeling! You're thinking like an architect:</strong>
                <ul>
                    <li>Identified realistic threats (not theoretical)</li>
                    <li>Proposed specific mitigations (not generic "add security")</li>
                    <li>Considered cost and implementation</li>
                    <li>Acknowledged residual risk (no perfect security)</li>
                </ul>
                </div>
                """, unsafe_allow_html=True)

def activity_adr_writing():
    """Teach Architecture Decision Records"""
    st.markdown('<div class="day-header"><h2>Activity 5: Architecture Decision Records (ADRs)</h2><p>Document the "why" behind your decisions</p></div>', unsafe_allow_html=True)
    
    st.write("""
    **Why ADRs Matter:**
    - 6 months from now, someone will ask "why did we do this?"
    - Audit will ask "what was your rationale?"
    - New team member needs to understand context
    
    **ADR = Insurance Policy Against "Why Didn't You Consider X?" Questions**
    """)
    
    st.write("### ADR Template")
    
    st.markdown("""
    <div class="adr-template">
# ADR-001: [Short Title of Decision]

**Date:** YYYY-MM-DD
**Status:** Proposed | Accepted | Deprecated | Superseded
**Deciders:** [List of people who made the decision]
**Tags:** #security #authentication #hipaa

## Context

What is the problem we're trying to solve?
What is the current situation?
What constraints exist?

## Decision

What did we decide to do?
Be specific and unambiguous.

## Alternatives Considered

### Alternative 1: [Name]
- Description
- Pros
- Cons
- Why we rejected it

### Alternative 2: [Name]
- Description
- Pros
- Cons
- Why we rejected it

## Consequences

### Positive
- What benefits do we get?

### Negative
- What trade-offs are we accepting?

### Risks
- What could go wrong?
- How do we mitigate?

## Compliance & Security

- How does this meet HIPAA/GDPR/etc?
- What security controls are required?
- What audit trail exists?

## Implementation

- What needs to be built?
- What's the timeline?
- What's the cost?

## Review Date

When should we re-evaluate this decision?
    </div>
    """, unsafe_allow_html=True)
    
    st.write("### Exercise: Write an ADR")
    
    st.write("""
    **Scenario:** You need to decide on authentication mechanism for clinician access.
    
    **Options:**
    1. Username/password (current system)
    2. RFID badge tap
    3. Biometric (fingerprint)
    4. Smart card + PIN
    """)
    
    adr_title = st.text_input("ADR Title:", "Authentication Mechanism for Clinician Access")
    
    adr_context = st.text_area(
        "Context (why is this decision needed?):",
        placeholder="""Example:
Current username/password system has usability issues:
- Clinicians forget passwords (especially after vacation)
- Password complexity requirements (12 chars, special chars) are hard to remember
- Account lockout after 3 failed attempts causes emergency access delays
- Shared credentials observed in practice (workaround behavior)

Regulatory requirements:
- HIPAA requires user authentication
- State medical board requires audit trail of access
- Joint Commission requires unique user identification

Constraints:
- Budget: $500K for authentication infrastructure
- Timeline: Must deploy in 6 months
- Users: 3,000 clinicians across 15 hospitals
- Environment: Clinical areas (sterile gloves, infection control)""",
        height=200,
        key="adr_context"
    )
    
    adr_decision = st.text_area(
        "Decision (what did you decide?):",
        placeholder="""Example:
We will implement RFID badge tap + biometric (fingerprint) authentication:

Primary authentication: RFID badge tap
- Clinician taps badge on reader (hands-free)
- Badge validates against Active Directory
- Fast (<1 second authentication)

Secondary authentication (sensitive operations): Fingerprint
- Required for accessing records of unassigned patients
- Required for modifying medication orders
- Required for exporting patient data

Emergency override: SMS to security team
- For life-threatening situations only
- Clinician enters emergency access code
- Security team receives immediate SMS notification
- Post-hoc audit review required within 24 hours""",
        height=200,
        key="adr_decision"
    )
    
    adr_alternatives = st.text_area(
        "Alternatives Considered:",
        placeholder="""Example:

Alternative 1: Username/Password Only
Pros: No hardware required, familiar to users
Cons: 
- Current system, already failed in practice
- Cognitive load (12-hour shifts, complex passwords)
- Doesn't solve emergency access problem
Rejected: Doesn't address root cause of problem

Alternative 2: Smart Card + PIN
Pros: Two-factor, government standard (FIPS 201)
Cons:
- Requires card readers at every workstation ($200K)
- PIN still has memorability issues
- Doesn't solve hands-free requirement
Rejected: Cost and usability concerns

Alternative 3: Biometric (Fingerprint) Only
Pros: Fast, hands-free, unique per user
Cons:
- Sterile gloves interfere with fingerprint reader
- Infection control concerns (touching shared surfaces)
- False reject rate may block emergency access
Rejected: Clinical environment incompatibility""",
        height=250,
        key="adr_alternatives"
    )
    
    if adr_context and adr_decision and adr_alternatives:
        st.success("✅ Excellent! You're documenting the 'why', not just the 'what'")
        
        st.write("### Complete ADR")
        
        full_adr = f"""
# ADR-001: {adr_title}

**Date:** {datetime.now().strftime('%Y-%m-%d')}
**Status:** Proposed
**Deciders:** Security Architecture Team, CMIO, CISO
**Tags:** #authentication #hipaa #usability

## Context

{adr_context}

## Decision

{adr_decision}

## Alternatives Considered

{adr_alternatives}

## Consequences

### Positive
- Fast authentication (<1 second) improves clinician workflow
- Hands-free badge tap works with sterile gloves
- Biometric for sensitive operations satisfies audit requirements
- Emergency override with SMS prevents life-threatening delays
- Unique user identification (no shared credentials)

### Negative
- Badge loss = access lost (mitigation: 24/7 badge office)
- Biometric false reject rate ~0.1% (mitigation: fallback to supervisor override)
- Cost: $300K for badge readers + $100K for biometric readers

### Risks
- Badge cloning: Mitigated by crypto-enabled badges (FIDO2)
- Emergency access abuse: Mitigated by SMS alerts + post-hoc audit
- Biometric database breach: Mitigated by storing hash only, not fingerprint image

## Compliance & Security

**HIPAA §164.312(a)(2)(i) - Unique User Identification:**
✅ Satisfied: Badge + biometric = unique identification

**HIPAA §164.312(b) - Audit Controls:**
✅ Satisfied: All access logged (badge ID, timestamp, patient accessed)

**HIPAA §164.312(a)(2)(iii) - Emergency Access:**
✅ Satisfied: Emergency override with notification + post-hoc review

**State Medical Board - Audit Trail:**
✅ Satisfied: Immutable log of all record access

## Implementation

### Phase 1 (Months 1-2): Pilot
- Deploy at 1 hospital (200 users)
- Badge readers at all workstations
- Biometric readers at nursing stations
- Monitor usability and performance

### Phase 2 (Months 3-4): Rollout
- Deploy to remaining 14 hospitals (2,800 users)
- Training program for all clinicians
- Help desk readiness

### Phase 3 (Months 5-6): Optimization
- Fine-tune authentication thresholds
- Address usability feedback
- Post-implementation review

**Total Cost:** $400K (under $500K budget)

## Review Date

6 months post-deployment: Evaluate false reject rate, emergency access frequency, user satisfaction
        """
        
        st.markdown(f'<div class="adr-template">{full_adr}</div>', unsafe_allow_html=True)
        
        if st.button("💾 Save ADR to Portfolio"):
            st.session_state.architecture['decisions'].append({
                'title': adr_title,
                'date': datetime.now().isoformat(),
                'content': full_adr
            })
            st.success("✅ ADR saved to your architecture portfolio!")
            st.balloons()

# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    # Header
    st.markdown(f"""
    <div class="day-header">
        <h1>Security Architect Immersion Workshop</h1>
        <p>Day {st.session_state.day} • {st.session_state.time} • {SCENARIO['company']}</p>
        <p><strong>Your Role:</strong> {SCENARIO['your_role']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Activity selector
    activity = st.selectbox(
        "Choose Your Activity:",
        [
            "📋 Scenario Briefing",
            "🎭 Activity 1: Stakeholder Discovery",
            "🏗️ Activity 2: Security Pattern Selection",
            "📐 Activity 3: C4 Architecture Diagrams",
            "🛡️ Activity 4: Threat Modeling",
            "📝 Activity 5: Write Architecture Decision Records",
            "📊 View Your Architecture Portfolio"
        ]
    )
    
    if "Briefing" in activity:
        st.markdown(SCENARIO['context'], unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.write("### Functional Requirements")
            for req in SCENARIO['requirements']['functional']:
                st.write(f"- {req}")
        with col2:
            st.write("### Security Requirements")
            for req in SCENARIO['requirements']['security']:
                st.write(f"- {req}")
        
        st.write("### Constraints")
        for constraint in SCENARIO['requirements']['constraints']:
            st.write(f"⚠️ {constraint}")
    
    elif "Activity 1" in activity:
        activity_stakeholder_discovery()
    
    elif "Activity 2" in activity:
        activity_pattern_selection()
    
    elif "Activity 3" in activity:
        activity_c4_modeling()
    
    elif "Activity 4" in activity:
        activity_threat_modeling()
    
    elif "Activity 5" in activity:
        activity_adr_writing()
    
    elif "Portfolio" in activity:
        st.write("### Your Architecture Portfolio")
        
        st.write("#### Selected Patterns")
        if st.session_state.architecture['patterns']:
            for pid in st.session_state.architecture['patterns']:
                st.write(f"✅ {SECURITY_PATTERNS[pid]['name']}")
        
        st.write("#### Architecture Decisions")
        if st.session_state.architecture['decisions']:
            for decision in st.session_state.architecture['decisions']:
                with st.expander(decision['title']):
                    st.text(decision['content'])
        
        st.write("#### Diagrams")
        if st.session_state.architecture['diagrams']:
            for diagram_type, diagram_data in st.session_state.architecture['diagrams'].items():
                with st.expander(f"C4 {diagram_type.title()} Diagram"):
                    for key, value in diagram_data.items():
                        st.write(f"**{key.title()}:**")
                        st.text(value)
        
        if st.button("📥 Export Portfolio"):
            portfolio = {
                'scenario': st.session_state.scenario,
                'completed': st.session_state.completed,
                'architecture': st.session_state.architecture,
                'stakeholder_notes': st.session_state.stakeholder_notes,
                'export_date': datetime.now().isoformat()
            }
            st.download_button(
                "Download JSON",
                json.dumps(portfolio, indent=2),
                f"architect_portfolio_{datetime.now().strftime('%Y%m%d')}.json",
                "application/json"
            )
    
    # Sidebar
    with st.sidebar:
        st.metric("Day", st.session_state.day)
        st.metric("Activities Completed", len(st.session_state.completed))
        
        st.write("### Stakeholder Relationships")
        for stakeholder, score in st.session_state.relationships.items():
            st.progress(score / 100)
            st.caption(f"{stakeholder.upper()}: {score}/100")
        
        st.write("### Your Progress")
        st.write(f"Patterns: {len(st.session_state.architecture['patterns'])}")
        st.write(f"Decisions: {len(st.session_state.architecture['decisions'])}")
        st.write(f"Diagrams: {len(st.session_state.architecture['diagrams'])}")

if __name__ == "__main__":
    main()
