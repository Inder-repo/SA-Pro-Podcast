"""
ENTERPRISE SECURITY ARCHITECTURE WORKSHOP
Live Workshop + Independent Challenges

Based on:
- Security Patterns (securitypatterns.io)
- Real enterprise architecture practice
- Produces actual architectural artifacts
- Peer review and defense sessions
- Instructor-led + self-paced modes

Outputs Real Artifacts:
✓ Security Pattern Documents
✓ Threat-to-Control Traceability Matrices
✓ C4 Container Diagrams with Security Overlays
✓ Architecture Decision Records
✓ Risk & Control Backlogs
✓ Architecture Review Board Summaries
"""

import streamlit as st
import pandas as pd
import json
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(
    page_title="Enterprise Security Architecture Workshop",
    page_icon="🏛️",
    layout="wide"
)

# ============================================================================
# STYLING
# ============================================================================

st.markdown("""
<style>
    .workshop-header {
        background: linear-gradient(135deg, #0f172a 0%, #1e3a5f 100%);
        color: white; padding: 2rem; border-radius: 12px;
        margin-bottom: 2rem; box-shadow: 0 8px 16px rgba(0,0,0,0.3);
    }
    .artifact-card {
        background: white; border-left: 6px solid #3b82f6;
        padding: 1.5rem; margin: 1rem 0; border-radius: 10px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    .pattern-template {
        background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%);
        border: 3px solid #10b981; padding: 2rem; margin: 1rem 0;
        border-radius: 12px; font-family: 'Courier New', monospace;
    }
    .threat-control-matrix {
        background: white; border: 2px solid #e5e7eb;
        border-radius: 8px; padding: 1rem; margin: 1rem 0;
    }
    .instructor-note {
        background: #fef3c7; border-left: 5px solid #f59e0b;
        padding: 1rem; margin: 1rem 0; border-radius: 6px;
    }
    .peer-review {
        background: #dbeafe; border-left: 5px solid #3b82f6;
        padding: 1rem; margin: 1rem 0; border-radius: 6px;
    }
    .defense-question {
        background: #fee2e2; border-left: 5px solid #ef4444;
        padding: 1rem; margin: 0.5rem 0; border-radius: 6px;
        font-weight: 600;
    }
    .arb-summary {
        background: linear-gradient(135deg, #f5f3ff 0%, #ede9fe 100%);
        border: 3px solid #8b5cf6; padding: 1.5rem;
        margin: 1rem 0; border-radius: 10px;
    }
    .stride-tag {
        display: inline-block; padding: 0.3rem 0.8rem;
        margin: 0.2rem; border-radius: 20px; font-size: 0.85rem;
        font-weight: 600;
    }
    .spoofing { background: #fee2e2; color: #991b1b; }
    .tampering { background: #fef3c7; color: #92400e; }
    .repudiation { background: #dbeafe; color: #1e40af; }
    .info-disclosure { background: #fce7f3; color: #9f1239; }
    .dos { background: #f3e8ff; color: #6b21a8; }
    .elevation { background: #ffedd5; color: #9a3412; }
    .c4-diagram {
        background: #f8fafc; border: 3px dashed #94a3b8;
        padding: 2rem; margin: 1rem 0; border-radius: 10px;
        font-family: 'Courier New', monospace; white-space: pre;
        font-size: 0.9rem;
    }
    .control-backlog {
        background: white; border: 2px solid #e5e7eb;
        padding: 1.5rem; margin: 1rem 0; border-radius: 10px;
    }
    .complexity-low { background: #d1fae5; color: #065f46; }
    .complexity-medium { background: #fef3c7; color: #92400e; }
    .complexity-high { background: #fee2e2; color: #991b1b; }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# SESSION STATE
# ============================================================================

def init_state():
    defaults = {
        'mode': 'live_workshop',  # live_workshop or independent
        'current_part': 'A',
        'role': 'architect',  # architect, instructor, peer_reviewer
        'team_name': 'Team Alpha',
        'artifacts': {
            'problem_statement': {},
            'patterns': [],
            'threat_control_matrix': [],
            'c4_diagrams': {},
            'arb_summary': {},
            'control_backlog': [],
            'defense_notes': {}
        },
        'peer_reviews': [],
        'presentation_ready': False,
        'completed_tasks': []
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# ============================================================================
# SECURITY PATTERN TEMPLATE
# ============================================================================

PATTERN_TEMPLATE = """
# SECURITY PATTERN TEMPLATE
# Based on SecurityPatterns.io

## Pattern Metadata
Pattern Name: [Short, descriptive name]
Category: [Identity, Data Protection, Network, Application, etc.]
Maturity: [Draft | Review | Approved]
Author: [Your name/team]
Date: [YYYY-MM-DD]

## 1. SCOPE
What boundaries does this pattern address?
- Systems: [Which systems/components]
- Data: [Which data classifications]
- Users: [Which user types]
- Environment: [Cloud, on-prem, hybrid]

## 2. PROBLEM STATEMENT
What security problem does this solve?

Clear description of:
- The security challenge
- Why existing approaches fail
- Business/compliance drivers

## 3. ASSETS AFFECTED
What needs protection?

| Asset | Classification | Criticality | Location |
|-------|---------------|-------------|----------|
| Customer PII | Confidential | High | Database |
| Payment Tokens | Restricted | Critical | Token Vault |
| API Keys | Secret | High | Key Management |

## 4. THREAT MODELING (STRIDE)

### Spoofing
- [Threat description]
- Attack vectors: [How attacker could spoof]
- Impact: [What happens if successful]

### Tampering
- [Threat description]
- Attack vectors: [How attacker could tamper]
- Impact: [What happens if successful]

### Repudiation
- [Threat description]
- Attack vectors: [How attacker could deny actions]
- Impact: [What happens if successful]

### Information Disclosure
- [Threat description]
- Attack vectors: [How attacker could steal data]
- Impact: [What happens if successful]

### Denial of Service
- [Threat description]
- Attack vectors: [How attacker could disrupt]
- Impact: [What happens if successful]

### Elevation of Privilege
- [Threat description]
- Attack vectors: [How attacker could escalate]
- Impact: [What happens if successful]

## 5. TARGET STATE SOLUTION DESIGN

### Architecture Diagram
[ASCII or reference to C4 diagram]

### Components
1. [Component 1]
   - Purpose:
   - Technology:
   - Security properties:

2. [Component 2]
   - Purpose:
   - Technology:
   - Security properties:

### Data Flows
1. [Flow 1]: [Source] → [Destination]
   - Protocol:
   - Encryption:
   - Authentication:
   - Authorization:

## 6. CONTROL MAPPING (Threat → Control Traceability)

| Threat ID | Threat (STRIDE) | Control | Implementation | Effectiveness | Residual Risk |
|-----------|-----------------|---------|----------------|---------------|---------------|
| T-01 | Spoofing: Fake API tokens | Mutual TLS + JWT validation | API Gateway | 95% | 5% (insider threat) |
| T-02 | Tampering: Modified inputs | Schema validation + WAF | Input pipeline | 90% | 10% (zero-day) |
| T-03 | Info Disclosure: PII leak | Field-level encryption | Database layer | 99% | 1% (key compromise) |

## 7. PATTERN DESCRIPTION

### When to Use
- [Scenario 1]
- [Scenario 2]
- [Scenario 3]

### When NOT to Use
- [Anti-pattern scenario 1]
- [Anti-pattern scenario 2]

### Prerequisites
- [Requirement 1]
- [Requirement 2]

### Alternatives Considered
1. [Alternative 1]
   - Pros:
   - Cons:
   - Why rejected:

2. [Alternative 2]
   - Pros:
   - Cons:
   - Why rejected:

## 8. IMPLEMENTATION GUIDANCE

### Phase 1: [Timeline]
- [Activity 1]
- [Activity 2]
- Success criteria:

### Phase 2: [Timeline]
- [Activity 1]
- [Activity 2]
- Success criteria:

### Estimated Cost
- Development: [Amount]
- Infrastructure: [Amount]
- Operational (annual): [Amount]
- Total: [Amount]

### Team Requirements
- [Role 1]: [# people, duration]
- [Role 2]: [# people, duration]

## 9. COMPLIANCE MAPPING

| Requirement | Standard | Section | How Pattern Satisfies |
|-------------|----------|---------|----------------------|
| Encryption at rest | PCI-DSS | 3.4 | Field-level encryption with AES-256 |
| Access control | HIPAA | §164.312(a)(1) | RBAC with least privilege |
| Audit logging | SOX | Section 404 | Immutable audit trail |

## 10. SUCCESS METRICS

### Security Metrics
- [Metric 1]: [Target]
- [Metric 2]: [Target]

### Operational Metrics
- [Metric 1]: [Target]
- [Metric 2]: [Target]

### Business Metrics
- [Metric 1]: [Target]
- [Metric 2]: [Target]

## 11. RELATED PATTERNS
- [Pattern 1]: [Relationship]
- [Pattern 2]: [Relationship]

## 12. REFERENCES
- [Reference 1]
- [Reference 2]
"""

# ============================================================================
# LIVE WORKSHOP - SCENARIO
# ============================================================================

GLOBAL_PAYMENT_SCENARIO = {
    "title": "Global Payment Platform Modernization",
    "organization": "FinServe Global Inc.",
    "context": """
A financial services organization is modernizing its payment platform.

**The platform will:**
- Accept payments from mobile and web applications
- Store customer PII and payment tokens
- Integrate with third-party fraud and identity services  
- Run in hybrid (cloud + on-prem) environment

**Security Architecture Goal:**
Produce a defensible architecture that meets enterprise risk requirements 
and integrates reusable security patterns.

**Compliance Requirements:**
- PCI-DSS (Payment Card Industry Data Security Standard)
- GDPR (General Data Protection Regulation)
- SOX (Sarbanes-Oxley) - financial controls

**Constraints:**
- Must integrate with legacy on-premises identity system
- Budget constraints limit custom infrastructure
- Must maintain 99.99% uptime
- Cannot disrupt existing payment processing during migration
""",
    "stakeholders": [
        "CISO - Compliance and risk focus",
        "CTO - Modern architecture, scalability",
        "CFO - Cost control, ROI justification",
        "Chief Risk Officer - Risk quantification",
        "VP Engineering - Team velocity, developer experience"
    ]
}

# ============================================================================
# PART A - PROBLEM FORMULATION
# ============================================================================

def render_part_a_problem_formulation():
    """Part A: Architecture Problem Formulation (35 mins)"""
    
    st.markdown("""
    <div class="workshop-header">
        <h1>PART A: Architecture Problem Formulation</h1>
        <p>Duration: 35 minutes</p>
        <p><strong>Deliverable:</strong> Security Problem Definition Document</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Instructor Example
    with st.expander("📘 Instructor Walkthrough Example", expanded=True):
        st.markdown("""
        <div class="instructor-note">
        <h4>Instructor Demonstrates First</h4>
        
        <p><strong>1. Problem Statement</strong></p>
        <p>Security architecture must ensure that customer PII and payment tokens are 
        protected against unauthorized access, tampering, and disclosure throughout the 
        transaction lifecycle, while enabling high-performance at scale.</p>
        
        <p><strong>2. Assumptions</strong></p>
        <ul>
            <li>Users access via mobile/web applications</li>
            <li>PII storage requires encryption</li>
            <li>Third-party fraud systems integrate via APIs</li>
            <li>Hybrid deployment (cloud for new services, on-prem for legacy)</li>
        </ul>
        
        <p><strong>3. Constraints</strong></p>
        <ul>
            <li>Must comply with PCI-DSS, GDPR</li>
            <li>Budget and time constraints limit custom infrastructure</li>
            <li>Must use the enterprise identity platform</li>
            <li>Cannot disrupt existing payment processing</li>
            <li>Legacy systems cannot be immediately retired</li>
        </ul>
        
        <p><strong>4. Non-Functional Security Requirements</strong></p>
        <ul>
            <li><strong>Confidentiality:</strong> PII & payment tokens must be encrypted in transit (TLS 1.3) and at rest (AES-256)</li>
            <li><strong>Integrity:</strong> All transactions must be authenticated, authorized, and logged with immutable audit trail</li>
            <li><strong>Availability:</strong> System must maintain 99.99% uptime, resilient to DDoS attacks</li>
            <li><strong>Accountability:</strong> All access to sensitive data must be attributable to specific user/service</li>
            <li><strong>Non-repudiation:</strong> Cryptographic proof of transaction submission and processing</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Team Exercise
    st.write("---")
    st.subheader(f"🎯 Your Turn: {st.session_state.team_name}")
    
    st.write("### 1. Write Your Problem Statement")
    problem_statement = st.text_area(
        "What security problem are you solving?",
        height=150,
        placeholder="""Template:
Security architecture must ensure that [ASSETS] are protected against [THREATS] 
throughout [LIFECYCLE/SCOPE], while [BUSINESS REQUIREMENTS].""",
        key="problem_statement_text"
    )
    
    st.write("### 2. Document Assumptions")
    assumptions = st.text_area(
        "What are you assuming to be true?",
        height=150,
        placeholder="""Example assumptions:
- Users will access via standard web browsers and mobile apps
- Cloud provider meets compliance requirements
- Network connectivity is reliable
- Third-party services have adequate security controls""",
        key="assumptions_text"
    )
    
    st.write("### 3. List Constraints")
    constraints = st.text_area(
        "What limits your solution?",
        height=150,
        placeholder="""Example constraints:
- Must comply with PCI-DSS v4.0
- Budget: $2M for security architecture
- Timeline: 18 months to production
- Must integrate with existing identity system
- Cannot require hardware tokens (user experience)""",
        key="constraints_text"
    )
    
    st.write("### 4. Define Non-Functional Security Requirements")
    
    col1, col2 = st.columns(2)
    
    with col1:
        confidentiality = st.text_area(
            "Confidentiality Requirements:",
            height=100,
            placeholder="PII encrypted at rest and in transit...",
            key="conf_req"
        )
        
        integrity = st.text_area(
            "Integrity Requirements:",
            height=100,
            placeholder="All transactions authenticated and logged...",
            key="int_req"
        )
        
        availability = st.text_area(
            "Availability Requirements:",
            height=100,
            placeholder="99.99% uptime, resilient to DDoS...",
            key="avail_req"
        )
    
    with col2:
        accountability = st.text_area(
            "Accountability Requirements:",
            height=100,
            placeholder="All access attributable to user/service...",
            key="acc_req"
        )
        
        non_repudiation = st.text_area(
            "Non-Repudiation Requirements:",
            height=100,
            placeholder="Cryptographic proof of transactions...",
            key="nonrep_req"
        )
        
        other_nfr = st.text_area(
            "Other Security Requirements:",
            height=100,
            placeholder="Privacy, compliance, data residency...",
            key="other_nfr"
        )
    
    # Save artifact
    if st.button("💾 Save Problem Definition Artifact", type="primary"):
        artifact = {
            'problem_statement': problem_statement,
            'assumptions': assumptions,
            'constraints': constraints,
            'nfr': {
                'confidentiality': confidentiality,
                'integrity': integrity,
                'availability': availability,
                'accountability': accountability,
                'non_repudiation': non_repudiation,
                'other': other_nfr
            },
            'timestamp': datetime.now().isoformat()
        }
        st.session_state.artifacts['problem_statement'] = artifact
        st.session_state.completed_tasks.append('part_a')
        st.success("✅ Problem Definition saved to artifacts!")
        st.balloons()
        
        # Show artifact summary
        st.markdown("""
        <div class="artifact-card">
        <h4>📄 Artifact Created: Security Problem Definition</h4>
        <p>This artifact documents the foundational understanding of your security architecture challenge.</p>
        <p><strong>Uses in practice:</strong></p>
        <ul>
            <li>Architecture Review Board presentations</li>
            <li>Stakeholder alignment meetings</li>
            <li>RFP security requirements</li>
            <li>Audit evidence (shows due diligence)</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

# ============================================================================
# PART B - SECURITY PATTERN APPLICATION
# ============================================================================

def render_part_b_pattern_application():
    """Part B: Security Pattern Application (50 mins)"""
    
    st.markdown("""
    <div class="workshop-header">
        <h1>PART B: Security Pattern Application</h1>
        <p>Duration: 50 minutes</p>
        <p><strong>Deliverable:</strong> Security Pattern Document</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Background
    st.markdown("""
    <div class="instructor-note">
    <h4>What is a Security Pattern?</h4>
    <p>A <strong>security pattern</strong> is a reusable solution to a recurring security problem, 
    designed around <strong>assets, threats, and controls</strong>.</p>
    
    <p><strong>Key Properties:</strong></p>
    <ul>
        <li><strong>Technology-agnostic:</strong> Abstract from specific vendors/products</li>
        <li><strong>Threat-traceable:</strong> Each control maps to specific threats</li>
        <li><strong>Reusable:</strong> Apply across multiple projects/systems</li>
        <li><strong>Documented:</strong> Clear scope, problem, solution</li>
    </ul>
    
    <p><strong>Pattern Structure (from SecurityPatterns.io):</strong></p>
    <ol>
        <li><strong>Scope:</strong> Boundaries (systems, data, users)</li>
        <li><strong>Problem:</strong> Security challenge being solved</li>
        <li><strong>Assets:</strong> What needs protection</li>
        <li><strong>Threats:</strong> STRIDE analysis</li>
        <li><strong>Controls:</strong> How threats are mitigated</li>
        <li><strong>Target State:</strong> Architecture diagram</li>
    </ol>
    </div>
    """, unsafe_allow_html=True)
    
    # Example Pattern Walkthrough
    with st.expander("📘 Instructor Example: Secure API Integration Pattern", expanded=True):
        st.markdown("""
        <div class="pattern-template">
<strong>Pattern Name:</strong> Secure API Integration Pattern

<strong>Scope:</strong>
- REST APIs exposed to third-party partners
- OAuth 2.1 token-based authentication
- JSON data payloads with PII

<strong>Problem Statement:</strong>
Prevent unauthorized access and data leakage via APIs when integrating 
with third-party partners of varying trust levels.

<strong>Assets Affected:</strong>
| Asset | Classification | Location |
|-------|---------------|----------|
| API endpoints | Internal | API Gateway |
| OAuth tokens | Secret | Token service |
| Customer PII | Confidential | Backend DB |
| Partner credentials | Secret | Key vault |

<strong>Threat Modeling (STRIDE):</strong>

<span class="stride-tag spoofing">Spoofing</span>
- Fake tokens presented by malicious partner
- Man-in-the-middle intercepts token

<span class="stride-tag tampering">Tampering</span>
- Modified API request payloads
- Replay attacks with captured requests

<span class="stride-tag repudiation">Repudiation</span>
- Partner denies making API call
- No proof of request origin

<span class="stride-tag info-disclosure">Information Disclosure</span>
- Excessive data returned in API response
- PII leaked in error messages

<span class="stride-tag dos">Denial of Service</span>
- Partner floods API with requests
- Resource exhaustion

<span class="stride-tag elevation">Elevation of Privilege</span>
- Partner accesses data outside their scope
- Horizontal privilege escalation

<strong>Target State Solution:</strong>

┌─────────────┐
│   Partner   │
└──────┬──────┘
       │ 1. Request access token
       │    (client_id + secret)
       ▼
┌──────────────────┐
│  OAuth 2.1       │
│  Token Service   │
│  - Validates     │
│  - Issues JWT    │
│  - Scopes        │
└──────┬───────────┘
       │ 2. Access token (JWT)
       │
       ▼
┌─────────────┐
│   Partner   │
└──────┬──────┘
       │ 3. API request
       │    (Bearer token)
       ▼
┌──────────────────┐
│  API Gateway     │
│  - Validate JWT  │
│  - Check scopes  │
│  - Rate limit    │
└──────┬───────────┘
       │ 4. Authorized request
       ▼
┌──────────────────┐
│  Backend API     │
│  - Process       │
│  - Filter fields │
│  - Log access    │
└──────────────────┘

<strong>Control Mapping:</strong>

| Threat | Control | Implementation | Effectiveness |
|--------|---------|----------------|---------------|
| Fake tokens | JWT signature validation | API Gateway | 99% |
| Modified inputs | JSON schema validation | Input pipeline | 95% |
| Info disclosure | Field filtering by scope | Backend service | 90% |
| DoS | Rate limiting (100 req/min) | API Gateway | 85% |
| Privilege escalation | Scope-based authorization | OAuth service | 95% |

<strong>Residual Risks:</strong>
- Compromised partner credentials: 5% (mitigate with rotation policy)
- Zero-day in OAuth library: 1% (mitigate with regular updates)
- Social engineering of partner: 10% (mitigate with partner security requirements)
        </div>
        """, unsafe_allow_html=True)
    
    st.write("---")
    st.subheader("🎯 Your Turn: Create a Security Pattern")
    
    # Pattern selection
    pattern_focus = st.selectbox(
        "Choose your pattern focus:",
        [
            "Partner API Protection Pattern",
            "Data Protection Pattern (PII/Payment Tokens)",
            "Identity & Access Management Pattern",
            "Logging & Audit Pattern",
            "Custom Pattern"
        ]
    )
    
    # Template option
    if st.checkbox("📋 Show Full Pattern Template"):
        st.markdown(f'<div class="pattern-template">{PATTERN_TEMPLATE}</div>', unsafe_allow_html=True)
        
        if st.button("📥 Download Pattern Template"):
            st.download_button(
                "Download Markdown Template",
                PATTERN_TEMPLATE,
                "security_pattern_template.md",
                "text/markdown"
            )
    
    # Guided pattern creation
    st.write("### Build Your Security Pattern")
    
    tabs = st.tabs([
        "1️⃣ Metadata", 
        "2️⃣ Scope & Problem", 
        "3️⃣ Assets & Threats", 
        "4️⃣ Solution Design", 
        "5️⃣ Control Mapping"
    ])
    
    with tabs[0]:
        st.write("#### Pattern Metadata")
        pattern_name = st.text_input("Pattern Name:", key="pattern_name")
        pattern_category = st.selectbox(
            "Category:",
            ["Identity & Access", "Data Protection", "Network Security", 
             "Application Security", "Infrastructure Security"]
        )
        pattern_author = st.text_input("Author:", st.session_state.team_name)
    
    with tabs[1]:
        st.write("#### Scope & Problem Statement")
        
        scope_systems = st.text_area(
            "Which systems/components:",
            placeholder="Example: REST APIs, mobile apps, backend services",
            key="scope_systems"
        )
        
        scope_data = st.text_area(
            "Which data classifications:",
            placeholder="Example: Customer PII, Payment tokens, Transaction logs",
            key="scope_data"
        )
        
        problem_statement_pattern = st.text_area(
            "Problem Statement:",
            height=150,
            placeholder="What security problem does this pattern solve? Why do existing approaches fail?",
            key="pattern_problem"
        )
    
    with tabs[2]:
        st.write("#### Assets & STRIDE Threat Modeling")
        
        # Assets table
        st.write("**Assets Affected:**")
        
        num_assets = st.number_input("Number of assets:", 1, 10, 3)
        
        assets_data = []
        for i in range(num_assets):
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                asset = st.text_input(f"Asset {i+1}:", key=f"asset_{i}")
            with col2:
                classification = st.selectbox(
                    "Classification:",
                    ["Public", "Internal", "Confidential", "Restricted", "Secret"],
                    key=f"class_{i}"
                )
            with col3:
                criticality = st.selectbox(
                    "Criticality:",
                    ["Low", "Medium", "High", "Critical"],
                    key=f"crit_{i}"
                )
            with col4:
                location = st.text_input("Location:", key=f"loc_{i}")
            
            if asset:
                assets_data.append({
                    'Asset': asset,
                    'Classification': classification,
                    'Criticality': criticality,
                    'Location': location
                })
        
        if assets_data:
            st.dataframe(pd.DataFrame(assets_data), use_container_width=True)
        
        # STRIDE threats
        st.write("**STRIDE Threat Modeling:**")
        
        threats = {}
        
        col1, col2 = st.columns(2)
        
        with col1:
            threats['spoofing'] = st.text_area(
                "Spoofing Threats:",
                placeholder="Identity/authentication threats...",
                key="threat_spoof"
            )
            
            threats['tampering'] = st.text_area(
                "Tampering Threats:",
                placeholder="Data integrity threats...",
                key="threat_tamp"
            )
            
            threats['repudiation'] = st.text_area(
                "Repudiation Threats:",
                placeholder="Non-repudiation threats...",
                key="threat_repud"
            )
        
        with col2:
            threats['info_disclosure'] = st.text_area(
                "Information Disclosure:",
                placeholder="Confidentiality threats...",
                key="threat_info"
            )
            
            threats['dos'] = st.text_area(
                "Denial of Service:",
                placeholder="Availability threats...",
                key="threat_dos"
            )
            
            threats['elevation'] = st.text_area(
                "Elevation of Privilege:",
                placeholder="Authorization threats...",
                key="threat_elev"
            )
    
    with tabs[3]:
        st.write("#### Target State Solution Design")
        
        st.write("**Architecture Diagram:**")
        solution_diagram = st.text_area(
            "Describe or draw ASCII architecture:",
            height=200,
            placeholder="""Example:
┌─────────────┐
│   Client    │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Component  │
└─────────────┘""",
            key="solution_diagram"
        )
        
        st.write("**Key Components:**")
        num_components = st.number_input("Number of components:", 1, 10, 3, key="num_comp")
        
        components = []
        for i in range(num_components):
            with st.expander(f"Component {i+1}"):
                comp_name = st.text_input("Component name:", key=f"comp_name_{i}")
                comp_purpose = st.text_area("Purpose:", key=f"comp_purp_{i}")
                comp_tech = st.text_input("Technology:", key=f"comp_tech_{i}")
                comp_security = st.text_area("Security properties:", key=f"comp_sec_{i}")
                
                if comp_name:
                    components.append({
                        'name': comp_name,
                        'purpose': comp_purpose,
                        'technology': comp_tech,
                        'security': comp_security
                    })
    
    with tabs[4]:
        st.write("#### Threat-to-Control Traceability Matrix")
        
        st.info("This is the most critical artifact - it shows HOW each control mitigates WHICH threat")
        
        st.write("**Add Control Mappings:**")
        
        if 'control_mappings' not in st.session_state:
            st.session_state.control_mappings = []
        
        # Add new mapping
        with st.form("add_control_mapping"):
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                threat_id = st.text_input("Threat ID:", placeholder="T-01")
                threat_stride = st.selectbox(
                    "STRIDE Category:",
                    ["Spoofing", "Tampering", "Repudiation", 
                     "Information Disclosure", "Denial of Service", 
                     "Elevation of Privilege"]
                )
            
            with col2:
                threat_desc = st.text_area("Threat Description:", height=100)
            
            with col3:
                control = st.text_area("Control:", height=100)
                implementation = st.text_input("Implementation:")
            
            with col4:
                effectiveness = st.slider("Effectiveness %:", 0, 100, 90)
                residual_risk = st.text_area("Residual Risk:", height=100)
            
            if st.form_submit_button("➕ Add Mapping"):
                st.session_state.control_mappings.append({
                    'threat_id': threat_id,
                    'stride': threat_stride,
                    'threat': threat_desc,
                    'control': control,
                    'implementation': implementation,
                    'effectiveness': f"{effectiveness}%",
                    'residual_risk': residual_risk
                })
                st.success("Mapping added!")
        
        # Display current mappings
        if st.session_state.control_mappings:
            st.write("**Current Threat-Control Mappings:**")
            df = pd.DataFrame(st.session_state.control_mappings)
            st.dataframe(df, use_container_width=True)
    
    # Save pattern artifact
    if st.button("💾 Save Security Pattern Artifact", type="primary"):
        pattern_artifact = {
            'metadata': {
                'name': pattern_name,
                'category': pattern_category,
                'author': pattern_author,
                'date': datetime.now().isoformat()
            },
            'scope': {
                'systems': scope_systems,
                'data': scope_data
            },
            'problem': problem_statement_pattern,
            'assets': assets_data,
            'threats': threats,
            'solution': {
                'diagram': solution_diagram,
                'components': components
            },
            'control_mappings': st.session_state.control_mappings
        }
        
        st.session_state.artifacts['patterns'].append(pattern_artifact)
        st.session_state.completed_tasks.append('part_b')
        st.success("✅ Security Pattern saved to artifacts!")
        st.balloons()

# ============================================================================
# PART C - THREAT & CONTROL MAPPING
# ============================================================================

def render_part_c_threat_control_mapping():
    """Part C: Advanced Threat & Control Mapping (60 mins)"""
    
    st.markdown("""
    <div class="workshop-header">
        <h1>PART C: Advanced Threat & Control Mapping</h1>
        <p>Duration: 60 minutes</p>
        <p><strong>Deliverable:</strong> Threat-to-Control Traceability Matrix</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Instructor guidance
    st.markdown("""
    <div class="instructor-note">
    <h4>Instructor-Led Threat Modeling Approach</h4>
    
    <p><strong>STRIDE + PATTERN Methodology:</strong></p>
    <ol>
        <li><strong>Identify assets</strong> (payment tokens, PII database)</li>
        <li><strong>Identify threats per asset</strong> (STRIDE categories)</li>
        <li><strong>Map controls to threats</strong> (specific mitigations)</li>
        <li><strong>Evaluate residual risk</strong> (what's left after controls)</li>
    </ol>
    
    <p><strong>Enterprise Context Considerations:</strong></p>
    <ul>
        <li>PCI-DSS compliance requirements</li>
        <li>Hybrid deployment complexity</li>
        <li>Third-party trust boundaries</li>
        <li>Legacy system integration</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Example mapping
    with st.expander("📘 Instructor Example: Payment Platform Threat-Control Matrix"):
        example_data = {
            'Asset': [
                'Payment Token Storage',
                'Payment Token Storage',
                'REST APIs',
                'REST APIs',
                'Customer PII Database',
                'Customer PII Database',
                'Third-party Integration'
            ],
            'Threat (STRIDE)': [
                'Information Disclosure: Token theft via database breach',
                'Tampering: Unauthorized token modification',
                'Spoofing: Fake API credentials',
                'DoS: API flooding attack',
                'Information Disclosure: PII exfiltration',
                'Elevation of Privilege: SQL injection',
                'Tampering: Modified fraud check results'
            ],
            'Control': [
                'Encryption at rest + key rotation',
                'Immutable audit log + integrity checks',
                'Mutual TLS + OAuth token validation',
                'Rate limiting + DDoS mitigation',
                'Field-level encryption + access logging',
                'Parameterized queries + input validation',
                'Request signing + response verification'
            ],
            'Traceability': [
                'PCI-DSS 3.4, Enterprise Encryption Pattern',
                'PCI-DSS 10.2, Audit Pattern',
                'Enterprise Identity Pattern, OAuth 2.1',
                'Availability Pattern, Infrastructure',
                'GDPR Art. 32, Data Protection Pattern',
                'OWASP Top 10, Secure Coding Standard',
                'Partner Integration Pattern'
            ],
            'Effectiveness': [
                '99%',
                '95%',
                '98%',
                '90%',
                '99%',
                '95%',
                '85%'
            ],
            'Residual Risk': [
                '1% - Key compromise',
                '5% - Insider threat',
                '2% - Token theft',
                '10% - Advanced DDoS',
                '1% - Key compromise',
                '5% - Zero-day',
                '15% - Partner compromise'
            ]
        }
        
        df = pd.DataFrame(example_data)
        st.dataframe(df, use_container_width=True)
        
        # Visualization
        fig = go.Figure(data=[
            go.Bar(
                name='Effectiveness',
                x=example_data['Asset'],
                y=[int(e.replace('%', '')) for e in example_data['Effectiveness']],
                marker_color='#10b981'
            )
        ])
        
        fig.update_layout(
            title="Control Effectiveness by Asset",
            xaxis_title="Asset",
            yaxis_title="Effectiveness %",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    st.write("---")
    st.subheader("🎯 Your Turn: Create Threat-Control Matrix")
    
    st.write("### Step 1: Identify Key Assets")
    
    # Asset inventory
    if 'matrix_assets' not in st.session_state:
        st.session_state.matrix_assets = []
    
    with st.form("add_asset"):
        asset_name = st.text_input("Asset Name:")
        asset_type = st.selectbox(
            "Asset Type:",
            ["Data Store", "API/Service", "Network Component", 
             "Identity System", "Third-party Integration"]
        )
        asset_criticality = st.select_slider(
            "Criticality:",
            options=["Low", "Medium", "High", "Critical"]
        )
        
        if st.form_submit_button("➕ Add Asset"):
            st.session_state.matrix_assets.append({
                'name': asset_name,
                'type': asset_type,
                'criticality': asset_criticality
            })
            st.success(f"Asset '{asset_name}' added!")
    
    if st.session_state.matrix_assets:
        st.write("**Current Assets:**")
        for asset in st.session_state.matrix_assets:
            st.write(f"- {asset['name']} ({asset['type']}) - {asset['criticality']}")
    
    st.write("### Step 2: Build Threat-Control Traceability Matrix")
    
    if 'threat_control_matrix' not in st.session_state:
        st.session_state.threat_control_matrix = []
    
    with st.form("add_threat_control"):
        col1, col2 = st.columns(2)
        
        with col1:
            tc_asset = st.selectbox(
                "Asset:",
                [a['name'] for a in st.session_state.matrix_assets] if st.session_state.matrix_assets else ["Define assets first"]
            )
            tc_stride = st.selectbox(
                "Threat (STRIDE):",
                ["Spoofing", "Tampering", "Repudiation", 
                 "Information Disclosure", "Denial of Service", "Elevation of Privilege"]
            )
            tc_threat_desc = st.text_area("Threat Description:")
            
        with col2:
            tc_control = st.text_area("Control Description:")
            tc_trace = st.text_input("Traceability (Standard/Pattern):")
            tc_effectiveness = st.slider("Effectiveness %:", 0, 100, 90)
            tc_residual = st.text_input("Residual Risk:")
        
        if st.form_submit_button("➕ Add to Matrix"):
            st.session_state.threat_control_matrix.append({
                'Asset': tc_asset,
                'Threat (STRIDE)': f"{tc_stride}: {tc_threat_desc}",
                'Control': tc_control,
                'Traceability': tc_trace,
                'Effectiveness': f"{tc_effectiveness}%",
                'Residual Risk': tc_residual
            })
            st.success("Added to matrix!")
    
    # Display matrix
    if st.session_state.threat_control_matrix:
        st.write("### Your Threat-Control Traceability Matrix")
        
        df = pd.DataFrame(st.session_state.threat_control_matrix)
        st.dataframe(df, use_container_width=True)
        
        # Save artifact
        if st.button("💾 Save Threat-Control Matrix Artifact"):
            st.session_state.artifacts['threat_control_matrix'] = st.session_state.threat_control_matrix
            st.session_state.completed_tasks.append('part_c')
            st.success("✅ Matrix saved to artifacts!")
            st.balloons()

# ============================================================================
# PART D - ENTERPRISE DEFENSE & REVIEW
# ============================================================================

def render_part_d_defense_review():
    """Part D: Enterprise Defense & Review (35 mins)"""
    
    st.markdown("""
    <div class="workshop-header">
        <h1>PART D: Enterprise Defense & Architecture Review Board</h1>
        <p>Duration: 35 minutes</p>
        <p><strong>Deliverable:</strong> Architecture Review Board (ARB) Summary</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="instructor-note">
    <h4>Architecture Review Board Simulation</h4>
    
    <p><strong>Teams will present (10 minutes each):</strong></p>
    <ol>
        <li>Problem definition</li>
        <li>Security patterns chosen (and why)</li>
        <li>Threat-control mapping</li>
        <li>Residual risk assessment</li>
    </ol>
    
    <p><strong>Instructor & Peers Challenge:</strong></p>
    <ul>
        <li>"Why did you choose this pattern over alternatives?"</li>
        <li>"How do you KNOW this control actually mitigates the threat?"</li>
        <li>"Where is residual risk acceptable? Who approved it?"</li>
        <li>"What happens when this control fails?"</li>
        <li>"How does this scale enterprise-wide?"</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("### Prepare Your ARB Presentation")
    
    # Summary builder
    st.write("#### 1. Executive Summary")
    exec_summary = st.text_area(
        "Summarize your architecture in 3-4 sentences:",
        height=150,
        placeholder="""Example:
We propose a layered security architecture for the global payment platform using 
reusable security patterns. The architecture implements defense-in-depth through 
API gateway authentication, field-level encryption, and comprehensive audit logging.
Key risks are mitigated to 95%+ effectiveness with documented residual risks.""",
        key="arb_exec_summary"
    )
    
    st.write("#### 2. Pattern Justification")
    pattern_justification = st.text_area(
        "Why did you select your patterns?",
        height=150,
        placeholder="""Example:
- Partner API Protection Pattern: Required for third-party fraud service integration
- Data Protection Pattern: PCI-DSS mandates encryption of payment tokens
- Audit Pattern: SOX compliance requires immutable audit trail""",
        key="arb_pattern_just"
    )
    
    st.write("#### 3. Key Risks & Mitigations")
    key_risks = st.text_area(
        "Top 3 risks and how you're addressing them:",
        height=150,
        placeholder="""Example:
1. Payment token theft (99% mitigated via encryption + key rotation)
2. API credential compromise (98% mitigated via mTLS + token validation)
3. PII disclosure (99% mitigated via field-level encryption)""",
        key="arb_risks"
    )
    
    st.write("#### 4. Residual Risk Statement")
    residual_risk = st.text_area(
        "What risks remain and why are they acceptable?",
        height=150,
        placeholder="""Example:
Residual risk of key compromise (1%) is accepted because:
- Key rotation every 90 days limits exposure window
- HSM protection makes key theft extremely difficult
- Cyber insurance covers potential losses
- CFO and CISO have approved this risk level""",
        key="arb_residual"
    )
    
    st.write("#### 5. Implementation Roadmap")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        phase1 = st.text_area(
            "Phase 1 (Months 1-3):",
            height=100,
            placeholder="Identity integration, API gateway...",
            key="arb_phase1"
        )
    with col2:
        phase2 = st.text_area(
            "Phase 2 (Months 4-6):",
            height=100,
            placeholder="Encryption deployment...",
            key="arb_phase2"
        )
    with col3:
        phase3 = st.text_area(
            "Phase 3 (Months 7-12):",
            height=100,
            placeholder="Full production rollout...",
            key="arb_phase3"
        )
    
    # ARB Questions
    st.write("---")
    st.write("### Prepare for ARB Questions")
    
    st.markdown("""
    <div class="defense-question">
    ❓ "Why did you choose OAuth 2.1 over mutual TLS for API authentication?"
    </div>
    """, unsafe_allow_html=True)
    
    q1_answer = st.text_area(
        "Your answer:",
        height=100,
        placeholder="OAuth provides scoped tokens per partner, mTLS is all-or-nothing...",
        key="arb_q1"
    )
    
    st.markdown("""
    <div class="defense-question">
    ❓ "How do you know field-level encryption actually prevents PII disclosure?"
    </div>
    """, unsafe_allow_html=True)
    
    q2_answer = st.text_area(
        "Your answer:",
        height=100,
        placeholder="Even if database is compromised, encrypted fields are unreadable without keys...",
        key="arb_q2"
    )
    
    st.markdown("""
    <div class="defense-question">
    ❓ "What happens when your encryption key management system fails?"
    </div>
    """, unsafe_allow_html=True)
    
    q3_answer = st.text_area(
        "Your answer:",
        height=100,
        placeholder="HSM has HA configuration, backup keys in cold storage...",
        key="arb_q3"
    )
    
    # Peer Review
    st.write("---")
    st.write("### Peer Review Feedback")
    
    st.markdown("""
    <div class="peer-review">
    <h4>Peer Reviewers: Provide Constructive Feedback</h4>
    <p>As a peer reviewer, evaluate:</p>
    <ul>
        <li>Is the problem clearly defined?</li>
        <li>Are pattern choices justified?</li>
        <li>Is threat-control mapping complete?</li>
        <li>Are residual risks documented?</li>
        <li>Could this scale enterprise-wide?</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
    
    peer_feedback = st.text_area(
        "Peer feedback (if reviewing another team):",
        height=150,
        placeholder="""Example feedback:
Strengths:
- Clear problem definition
- Good pattern selection

Areas for improvement:
- Missing DoS mitigation controls
- Need more detail on key rotation

Questions:
- How does this integrate with legacy systems?""",
        key="peer_feedback"
    )
    
    # Save ARB summary
    if st.button("💾 Save ARB Summary Artifact", type="primary"):
        arb_summary = {
            'exec_summary': exec_summary,
            'pattern_justification': pattern_justification,
            'key_risks': key_risks,
            'residual_risk': residual_risk,
            'roadmap': {
                'phase1': phase1,
                'phase2': phase2,
                'phase3': phase3
            },
            'prepared_answers': {
                'q1': q1_answer,
                'q2': q2_answer,
                'q3': q3_answer
            },
            'peer_feedback': peer_feedback,
            'timestamp': datetime.now().isoformat()
        }
        
        st.session_state.artifacts['arb_summary'] = arb_summary
        st.session_state.completed_tasks.append('part_d')
        st.success("✅ ARB Summary saved!")
        st.balloons()

# ============================================================================
# PORTFOLIO & EXPORT
# ============================================================================

def render_portfolio():
    """View and export complete architectural portfolio"""
    
    st.markdown("""
    <div class="workshop-header">
        <h1>Your Security Architecture Portfolio</h1>
        <p>Professional artifacts ready for enterprise use</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Progress tracking
    total_tasks = 4  # Parts A, B, C, D
    completed = len([t for t in ['part_a', 'part_b', 'part_c', 'part_d'] if t in st.session_state.completed_tasks])
    
    progress = completed / total_tasks
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Completion", f"{completed}/{total_tasks}")
    with col2:
        st.metric("Progress", f"{progress*100:.0f}%")
    with col3:
        st.metric("Artifacts", len([k for k, v in st.session_state.artifacts.items() if v]))
    
    st.progress(progress)
    
    # Show artifacts
    st.write("---")
    
    # Artifact 1: Problem Definition
    if st.session_state.artifacts['problem_statement']:
        with st.expander("📄 Artifact 1: Security Problem Definition", expanded=False):
            prob = st.session_state.artifacts['problem_statement']
            st.write("**Problem Statement:**")
            st.info(prob.get('problem_statement', 'Not defined'))
            
            col1, col2 = st.columns(2)
            with col1:
                st.write("**Assumptions:**")
                st.text(prob.get('assumptions', ''))
            with col2:
                st.write("**Constraints:**")
                st.text(prob.get('constraints', ''))
    
    # Artifact 2: Security Patterns
    if st.session_state.artifacts['patterns']:
        with st.expander(f"📘 Artifact 2: Security Patterns ({len(st.session_state.artifacts['patterns'])})", expanded=False):
            for idx, pattern in enumerate(st.session_state.artifacts['patterns'], 1):
                st.write(f"### Pattern {idx}: {pattern['metadata']['name']}")
                st.write(f"**Category:** {pattern['metadata']['category']}")
                st.write(f"**Problem:** {pattern.get('problem', 'Not defined')}")
                
                if pattern.get('control_mappings'):
                    df = pd.DataFrame(pattern['control_mappings'])
                    st.dataframe(df, use_container_width=True)
    
    # Artifact 3: Threat-Control Matrix
    if st.session_state.artifacts['threat_control_matrix']:
        with st.expander("🛡️ Artifact 3: Threat-Control Traceability Matrix", expanded=False):
            df = pd.DataFrame(st.session_state.artifacts['threat_control_matrix'])
            st.dataframe(df, use_container_width=True)
            
            # Download as CSV
            csv = df.to_csv(index=False)
            st.download_button(
                "📥 Download as CSV",
                csv,
                "threat_control_matrix.csv",
                "text/csv"
            )
    
    # Artifact 4: ARB Summary
    if st.session_state.artifacts['arb_summary']:
        with st.expander("📊 Artifact 4: Architecture Review Board Summary", expanded=False):
            arb = st.session_state.artifacts['arb_summary']
            st.write("**Executive Summary:**")
            st.info(arb.get('exec_summary', ''))
            st.write("**Pattern Justification:**")
            st.text(arb.get('pattern_justification', ''))
            st.write("**Key Risks:**")
            st.text(arb.get('key_risks', ''))
    
    # Export complete portfolio
    st.write("---")
    st.subheader("📦 Export Complete Portfolio")
    
    if st.button("📥 Generate Portfolio Package", type="primary"):
        portfolio = {
            'metadata': {
                'team': st.session_state.team_name,
                'export_date': datetime.now().isoformat(),
                'workshop': 'Enterprise Security Architecture',
                'scenario': 'Global Payment Platform'
            },
            'artifacts': st.session_state.artifacts,
            'completed_tasks': st.session_state.completed_tasks
        }
        
        portfolio_json = json.dumps(portfolio, indent=2, default=str)
        
        st.download_button(
            "💾 Download Portfolio JSON",
            portfolio_json,
            f"security_architecture_portfolio_{datetime.now().strftime('%Y%m%d')}.json",
            "application/json"
        )
        
        st.success("✅ Portfolio exported successfully!")

# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    # Sidebar navigation
    with st.sidebar:
        st.title("🏛️ Enterprise Security")
        st.caption("Architecture Workshop")
        
        st.write("---")
        st.write(f"**Team:** {st.session_state.team_name}")
        
        # Mode selector
        mode = st.radio(
            "Workshop Mode:",
            ["Live Workshop (Instructor-Led)", "Independent Challenge"],
            key="mode_selector"
        )
        
        st.write("---")
        st.write("### Navigation")
        
        if "Live Workshop" in mode:
            activity = st.selectbox(
                "Choose Part:",
                [
                    "📋 Scenario Briefing",
                    "Part A: Problem Formulation",
                    "Part B: Pattern Application",
                    "Part C: Threat-Control Mapping",
                    "Part D: ARB Defense & Review",
                    "📊 View Portfolio"
                ]
            )
        else:
            activity = st.selectbox(
                "Choose Task:",
                [
                    "Task 1: Define Security Pattern",
                    "Task 2: Apply to Design",
                    "Task 3: Risk Prioritization",
                    "Task 4: Defend Design",
                    "📊 View Portfolio"
                ]
            )
        
        st.write("---")
        st.write("### Progress")
        completed = len(st.session_state.completed_tasks)
        st.metric("Tasks Complete", completed)
        
        artifacts = len([k for k, v in st.session_state.artifacts.items() if v])
        st.metric("Artifacts Created", artifacts)
    
    # Main content routing
    if "Briefing" in activity:
        st.markdown(f"""
        <div class="workshop-header">
            <h1>{GLOBAL_PAYMENT_SCENARIO['title']}</h1>
            <p>{GLOBAL_PAYMENT_SCENARIO['organization']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(GLOBAL_PAYMENT_SCENARIO['context'])
        
        st.write("### Stakeholders")
        for stakeholder in GLOBAL_PAYMENT_SCENARIO['stakeholders']:
            st.write(f"- {stakeholder}")
    
    elif "Part A" in activity or "Task 1" in activity:
        render_part_a_problem_formulation()
    
    elif "Part B" in activity or "Task 2" in activity:
        render_part_b_pattern_application()
    
    elif "Part C" in activity or "Task 3" in activity:
        render_part_c_threat_control_mapping()
    
    elif "Part D" in activity or "Task 4" in activity:
        render_part_d_defense_review()
    
    elif "Portfolio" in activity:
        render_portfolio()

if __name__ == "__main__":
    main()
