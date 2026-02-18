"""
ENTERPRISE SECURITY ARCHITECTURE WORKSHOP
Based on SecurityPatterns.io Methodology

Complete implementation of:
- SecurityPatterns.io Quick Guide
- Threat Events Taxonomy (TE-01 to TE-42)
- Security Controls Taxonomy (NIST SP 800-53 Rev 5)
- Asset-Centric Pattern Development
- Threat-to-Asset-to-Control Mapping

Produces Professional Artifacts:
✓ Asset-Centric Security Patterns
✓ Threat Event Mapping (42 threat categories)
✓ Security Controls Mapping (NIST 800-53)
✓ Traceability Matrix (Threats → Assets → Controls)
✓ Architecture Review Board Documentation
"""

import streamlit as st
import pandas as pd
import json
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px
from typing import List, Dict, Any

st.set_page_config(
    page_title="SecurityPatterns.io Workshop",
    page_icon="🛡️",
    layout="wide"
)

# ============================================================================
# STYLING
# ============================================================================

st.markdown("""
<style>
    .methodology-header {
        background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
        color: white; padding: 2rem; border-radius: 12px;
        margin-bottom: 2rem; box-shadow: 0 8px 20px rgba(59, 130, 246, 0.4);
    }
    .step-card {
        background: white; border-left: 6px solid #10b981;
        padding: 1.5rem; margin: 1rem 0; border-radius: 10px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    .asset-card {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        border: 3px solid #f59e0b; padding: 1.5rem; margin: 1rem 0;
        border-radius: 10px;
    }
    .threat-event {
        background: #fee2e2; border-left: 5px solid #ef4444;
        padding: 1rem; margin: 0.5rem 0; border-radius: 6px;
        font-family: 'Courier New', monospace;
    }
    .control-badge {
        display: inline-block; background: #dbeafe;
        color: #1e40af; padding: 0.4rem 1rem; margin: 0.2rem;
        border-radius: 20px; font-size: 0.85rem; font-weight: 600;
    }
    .mapping-matrix {
        background: white; border: 3px solid #e5e7eb;
        padding: 2rem; margin: 1.5rem 0; border-radius: 12px;
    }
    .pattern-diagram {
        background: #f8fafc; border: 3px dashed #64748b;
        padding: 2rem; margin: 1rem 0; border-radius: 10px;
        font-family: 'Courier New', monospace; font-size: 0.9rem;
    }
    .securitypatterns-io {
        background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
        border: 3px solid #3b82f6; padding: 2rem; margin: 1rem 0;
        border-radius: 12px;
    }
    .four-steps {
        background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
        border: 3px solid #10b981; padding: 1.5rem; margin: 1rem 0;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# THREAT EVENTS TAXONOMY (SecurityPatterns.io)
# ============================================================================

THREAT_EVENTS_TAXONOMY = {
    "Physical & Environmental": {
        "TE-01": "Disaster or major events in the environment",
        "TE-02": "Unfavourable climatic conditions",
        "TE-05": "Physical theft",
        "TE-06": "Unauthorized physical access or entry to premises",
        "TE-08": "Warfare or terrorists attack"
    },
    "Human Error & Process": {
        "TE-09": "Accidental leaks or sharing of information due to human error",
        "TE-11": "Disruption due to misconfiguration or maintenance errors",
        "TE-12": "Unintentional change of data within information system",
        "TE-13": "Inadequate design and planning leading to improper deployment",
        "TE-14": "Inadequate workflows or processes leading to flaws",
        "TE-15": "Unintentional damages through security testing",
        "TE-16": "Unintentional destruction of records"
    },
    "Malicious Insider": {
        "TE-03": "Fraud",
        "TE-04": "Sabotage",
        "TE-07": "Coercion, extortion or blackmail"
    },
    "System & Infrastructure Failure": {
        "TE-17": "System failure or corruption of information systems",
        "TE-18": "Failure of network infrastructure or connectivity",
        "TE-19": "Failure due to disruption of external supply chains"
    },
    "Information Disclosure": {
        "TE-10": "Leaks through application flaws or misconfigured services",
        "TE-37": "Compromise of confidential information or data breach"
    },
    "Network Attacks": {
        "TE-20": "Interception via insecure remote access points",
        "TE-21": "Network reconnaissance and information gathering",
        "TE-22": "Session hijacking",
        "TE-23": "Man in the middle attack or traffic modification",
        "TE-39": "Distributed Denial of Service (DDoS) - network layers",
        "TE-40": "Distributed Denial of Service (DDoS) - application layers"
    },
    "Identity & Access": {
        "TE-24": "Identity theft",
        "TE-25": "Generation of false identities",
        "TE-32": "Social engineering or phishing attacks",
        "TE-41": "Brute force attempts on user or system accounts"
    },
    "Application & Code": {
        "TE-27": "Exploit hardware or platform vulnerabilities",
        "TE-28": "Infection from malware, worms or trojans",
        "TE-29": "Web application attacks or code injection",
        "TE-30": "Rogue software masquerading as trusted application",
        "TE-31": "Unauthorized changes or manipulation of application code"
    },
    "Data Integrity": {
        "TE-35": "Manipulation of audit log integrity",
        "TE-36": "Unauthorized changes or manipulation of data records",
        "TE-38": "Destruction of records through malicious user or malware"
    },
    "Resource Abuse": {
        "TE-26": "Abuse of resources through misconfiguration",
        "TE-34": "Violate isolation in multi-tenant environment",
        "TE-42": "Denial of service on hosting platform"
    },
    "Communication & Email": {
        "TE-33": "Receive of unsolicited e-mail"
    }
}

# ============================================================================
# NIST 800-53 CONTROL FAMILIES
# ============================================================================

NIST_CONTROL_FAMILIES = {
    "AC": "Access Control",
    "AT": "Awareness and Training",
    "AU": "Audit and Accountability",
    "CA": "Assessment, Authorization, and Monitoring",
    "CM": "Configuration Management",
    "CP": "Contingency Planning",
    "IA": "Identification and Authentication",
    "IR": "Incident Response",
    "MA": "Maintenance",
    "MP": "Media Protection",
    "PE": "Physical and Environmental Protection",
    "PL": "Planning",
    "PM": "Program Management",
    "PS": "Personnel Security",
    "PT": "PII Processing and Transparency",
    "RA": "Risk Assessment",
    "SA": "System and Services Acquisition",
    "SC": "System and Communications Protection",
    "SI": "System and Information Integrity",
    "SR": "Supply Chain Risk Management"
}

# ============================================================================
# SESSION STATE
# ============================================================================

def init_state():
    defaults = {
        'current_step': 1,
        'team_name': 'Security Architecture Team',
        'pattern_name': '',
        'scope_defined': False,
        'assets_identified': [],
        'threats_mapped': [],
        'solution_designed': False,
        'controls_mapped': [],
        'pattern_complete': False,
        'artifacts': {
            'scope_problem': {},
            'assets': [],
            'threat_mapping': [],
            'solution_design': {},
            'threat_asset_mapping': [],
            'control_threat_mapping': [],
            'asset_pattern': {}
        }
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# ============================================================================
# SECURITYPATTERNS.IO METHODOLOGY OVERVIEW
# ============================================================================

def render_methodology_overview():
    """Explain the SecurityPatterns.io methodology"""
    
    st.markdown("""
    <div class="methodology-header">
        <h1>🛡️ SecurityPatterns.io Methodology</h1>
        <p>Asset-Centric Security Pattern Development</p>
        <p style="opacity: 0.9; margin-top: 1rem;">
        Security patterns are design artifacts that represent defined and re-usable 
        solutions to recurring security problems. Patterns focus on describing security 
        controls in the context of assets.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("### 🎯 Why Use Security Patterns?")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="step-card">
        <h4>✅ Benefits</h4>
        <ul>
            <li><strong>Reusable Solutions:</strong> Apply across multiple projects</li>
            <li><strong>Asset-Centric:</strong> Focus on what needs protection</li>
            <li><strong>Threat-Driven:</strong> Controls based on threat modeling</li>
            <li><strong>Technology-Agnostic:</strong> Abstract from vendor specifics</li>
            <li><strong>Traceable:</strong> Clear path from threats to controls</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="step-card">
        <h4>📋 4 Key Characteristics</h4>
        <ol>
            <li><strong>Context:</strong> Security problem and how it affects assets</li>
            <li><strong>Abstracted:</strong> Not vendor or technology specific</li>
            <li><strong>Standards:</strong> Uses threat and control taxonomies</li>
            <li><strong>Traceable:</strong> Controls traced to threats mitigated</li>
        </ol>
        </div>
        """, unsafe_allow_html=True)
    
    st.write("### 📊 The SecurityPatterns.io Process")
    
    st.markdown("""
    <div class="securitypatterns-io">
    <h3 style="color: #1e40af; margin-top: 0;">4-Step Pattern Development Process</h3>
    
    <div style="margin: 2rem 0;">
        <div style="background: white; padding: 1.5rem; border-radius: 8px; margin: 1rem 0; border-left: 6px solid #10b981;">
            <h4 style="color: #059669; margin-top: 0;">Step 1: Identify Scope & Problem</h4>
            <p>Define the scope of the security pattern to a single problem space and typical challenges.
            Describe the problem in context of the assets affected.</p>
            <p><strong>Output:</strong> Problem statement with scope boundaries</p>
        </div>
        
        <div style="background: white; padding: 1.5rem; border-radius: 8px; margin: 1rem 0; border-left: 6px solid #3b82f6;">
            <h4 style="color: #1e40af; margin-top: 0;">Step 2: Identify Assets</h4>
            <p>Identify and categorize assets affected by the problem statement. Assets are discrete 
            sets of technology capabilities or components (devices, applications, platforms, data, networks).</p>
            <p><strong>Output:</strong> Asset inventory with categorization</p>
        </div>
        
        <div style="background: white; padding: 1.5rem; border-radius: 8px; margin: 1rem 0; border-left: 6px solid #f59e0b;">
            <h4 style="color: #d97706; margin-top: 0;">Step 3: Establish Threat Modeling</h4>
            <p>Identify Threat Events that affect the assets. Categorize each threat against the 
            Threat Events Taxonomy (TE-01 to TE-42).</p>
            <p><strong>Output:</strong> Threat inventory mapped to assets</p>
        </div>
        
        <div style="background: white; padding: 1.5rem; border-radius: 8px; margin: 1rem 0; border-left: 6px solid #8b5cf6;">
            <h4 style="color: #7c3aed; margin-top: 0;">Step 4: Describe Solution & Map Controls</h4>
            <p>Describe target state solution. Map threats to assets, then map controls to threats.
            Build asset-centric pattern combining Threats → Assets → Controls.</p>
            <p><strong>Output:</strong> Complete security pattern with traceability</p>
        </div>
    </div>
    
    <div class="four-steps">
        <h4>The 4-Step Control Mapping Process:</h4>
        <pre style="background: white; padding: 1rem; border-radius: 6px; overflow-x: auto;">
1. Decompose threats and map to each asset
   └─▶ For each threat: Which assets are vulnerable?

2. Map controls to threats  
   └─▶ For each threat: Which controls mitigate it?

3. Build asset-centric pattern
   └─▶ Combine mappings: Threat → Asset → Control

4. Categorize controls using taxonomy
   └─▶ NIST SP 800-53 (Rev 5) control families
        </pre>
    </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Visual workflow
    st.write("### 🔄 Pattern Development Workflow")
    
    fig = go.Figure()
    
    # Add nodes
    fig.add_trace(go.Scatter(
        x=[1, 2, 3, 4],
        y=[1, 1, 1, 1],
        mode='markers+text',
        marker=dict(size=80, color=['#10b981', '#3b82f6', '#f59e0b', '#8b5cf6']),
        text=['Step 1<br>Scope', 'Step 2<br>Assets', 'Step 3<br>Threats', 'Step 4<br>Controls'],
        textposition='middle center',
        textfont=dict(color='white', size=12, family='Arial Black'),
        hoverinfo='skip'
    ))
    
    # Add arrows
    for i in range(3):
        fig.add_annotation(
            x=i+1.5, y=1,
            ax=i+1, ay=1,
            xref='x', yref='y',
            axref='x', ayref='y',
            showarrow=True,
            arrowhead=2,
            arrowsize=2,
            arrowwidth=3,
            arrowcolor='#64748b'
        )
    
    fig.update_layout(
        showlegend=False,
        xaxis=dict(showgrid=False, showticklabels=False, zeroline=False, range=[0.5, 4.5]),
        yaxis=dict(showgrid=False, showticklabels=False, zeroline=False, range=[0.5, 1.5]),
        height=200,
        margin=dict(l=20, r=20, t=20, b=20),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    ))
    
    st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# STEP 1: SCOPE & PROBLEM
# ============================================================================

def render_step1_scope_problem():
    """Step 1: Identify the scope and typical challenges"""
    
    st.markdown("""
    <div class="methodology-header">
        <h1>Step 1: Identify Scope & Problem</h1>
        <p>Define the security pattern scope and describe the problem in context of assets</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="step-card">
    <h4>📝 What You're Creating</h4>
    <p>A clear problem statement that:</p>
    <ul>
        <li>Defines the <strong>scope</strong> (boundaries of the pattern)</li>
        <li>Describes the <strong>security problem</strong> in business context</li>
        <li>References <strong>typical challenges</strong> and historic examples</li>
        <li>Explains how the problem <strong>affects assets</strong></li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Example
    with st.expander("📘 Example: Partner API Integration Pattern", expanded=True):
        st.markdown("""
        <div class="securitypatterns-io">
        <p><strong>Pattern Name:</strong> Partner API Integration Security Pattern</p>
        
        <p><strong>Scope:</strong></p>
        <ul>
            <li>REST APIs exposed to external third-party partners</li>
            <li>JSON data payloads containing customer information</li>
            <li>Partners with varying levels of trust (trusted, semi-trusted, untrusted)</li>
            <li>OAuth 2.1 token-based authentication</li>
        </ul>
        
        <p><strong>Problem Statement:</strong></p>
        <p>Organizations exposing APIs to third-party partners face challenges in ensuring 
        secure data exchange while maintaining different trust levels across partners. 
        Without proper controls, APIs are vulnerable to unauthorized access, data leakage, 
        and abuse. The pattern must address authentication, authorization, rate limiting, 
        and data protection across partners of varying trust levels.</p>
        
        <p><strong>Typical Challenges:</strong></p>
        <ul>
            <li>Partners may have weak security practices leading to credential compromise</li>
            <li>Lack of granular authorization allowing partners to access data beyond their scope</li>
            <li>No rate limiting leading to resource exhaustion or data scraping</li>
            <li>Sensitive data inadvertently exposed in API responses</li>
            <li>Insufficient audit logging making it impossible to attribute actions</li>
        </ul>
        
        <p><strong>How It Affects Assets:</strong></p>
        <ul>
            <li><strong>API Endpoints:</strong> Vulnerable to unauthorized access and abuse</li>
            <li><strong>Customer Data:</strong> Risk of disclosure to unauthorized partners</li>
            <li><strong>OAuth Tokens:</strong> If compromised, provide broad access</li>
            <li><strong>Backend Systems:</strong> Can be overwhelmed by malicious partners</li>
        </ul>
        
        <p><strong>Historic Examples:</strong></p>
        <ul>
            <li>Cambridge Analytica (2018): Facebook API allowed excessive data access to third-party apps</li>
            <li>Twitter API Abuse (2020): Scraped data from millions of accounts via API vulnerabilities</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.write("---")
    st.subheader("🎯 Your Turn: Define Your Pattern Scope & Problem")
    
    # Pattern name
    pattern_name = st.text_input(
        "Pattern Name:",
        value=st.session_state.pattern_name,
        placeholder="e.g., Zero Trust Network Access Pattern, Data Encryption at Rest Pattern",
        key="pattern_name_input"
    )
    
    if pattern_name:
        st.session_state.pattern_name = pattern_name
    
    # Scope definition
    st.write("### 1. Define the Scope")
    
    col1, col2 = st.columns(2)
    
    with col1:
        scope_systems = st.text_area(
            "Systems/Components in Scope:",
            height=120,
            placeholder="""Example:
- Web applications
- Mobile apps (iOS, Android)
- REST APIs
- Backend microservices
- Database servers""",
            key="scope_systems"
        )
    
    with col2:
        scope_boundaries = st.text_area(
            "Boundaries (What's NOT in scope):",
            height=120,
            placeholder="""Example:
- Legacy mainframe systems
- Third-party SaaS applications
- Physical security controls
- Network infrastructure (separate pattern)""",
            key="scope_boundaries"
        )
    
    scope_data = st.text_area(
        "Data Classifications in Scope:",
        height=100,
        placeholder="""Example:
- Customer PII (Personally Identifiable Information)
- Payment card data (PCI scope)
- Authentication credentials
- Business transaction records""",
        key="scope_data"
    )
    
    # Problem statement
    st.write("### 2. Problem Statement")
    
    problem_statement = st.text_area(
        "Describe the security problem in business context:",
        height=150,
        placeholder="""Template:
Organizations [CONTEXT] face challenges in [SECURITY CHALLENGE]. 
Without proper controls, [SYSTEMS] are vulnerable to [THREATS]. 
The pattern must address [KEY REQUIREMENTS].""",
        key="problem_statement"
    )
    
    # Typical challenges
    st.write("### 3. Typical Challenges")
    
    challenges = st.text_area(
        "List typical security challenges this pattern addresses:",
        height=150,
        placeholder="""Example challenges:
- Weak authentication allowing unauthorized access
- Lack of encryption exposing data in transit
- No audit logging making incident investigation impossible
- Insufficient input validation leading to injection attacks
- Missing rate limiting enabling denial of service""",
        key="challenges"
    )
    
    # Asset impact
    st.write("### 4. How Problem Affects Assets")
    
    asset_impact = st.text_area(
        "Explain how this problem affects your assets:",
        height=150,
        placeholder="""Example:
- **Web Application:** Vulnerable to SQL injection and XSS attacks
- **User Credentials:** Risk of credential stuffing and account takeover
- **Customer Database:** Unauthorized access could lead to mass data breach
- **API Gateway:** Can be overwhelmed by DDoS attacks""",
        key="asset_impact"
    )
    
    # Historic examples
    st.write("### 5. Historic Examples (Optional)")
    
    historic_examples = st.text_area(
        "Reference any relevant security incidents or case studies:",
        height=100,
        placeholder="""Example:
- Equifax breach (2017): Unpatched vulnerability in web application
- Capital One breach (2019): Misconfigured firewall rules in cloud
- SolarWinds (2020): Supply chain compromise through build system""",
        key="historic_examples"
    )
    
    # Research notes
    st.write("### 6. Research & Preparation Notes")
    
    research_notes = st.text_area(
        "Collate research notes (standards, best practices, industry guidance):",
        height=100,
        placeholder="""Example:
- OWASP Top 10 guidance
- NIST SP 800-53 AC (Access Control) family
- CIS Controls v8
- Industry-specific regulations (PCI-DSS, HIPAA, GDPR)""",
        key="research_notes"
    )
    
    # Save step 1
    if st.button("💾 Save Step 1: Scope & Problem", type="primary"):
        scope_problem = {
            'pattern_name': pattern_name,
            'scope': {
                'systems': scope_systems,
                'boundaries': scope_boundaries,
                'data': scope_data
            },
            'problem_statement': problem_statement,
            'challenges': challenges,
            'asset_impact': asset_impact,
            'historic_examples': historic_examples,
            'research_notes': research_notes,
            'timestamp': datetime.now().isoformat()
        }
        
        st.session_state.artifacts['scope_problem'] = scope_problem
        st.session_state.scope_defined = True
        st.success("✅ Step 1 Complete! Proceed to Step 2: Identify Assets")
        st.balloons()

# ============================================================================
# STEP 2: IDENTIFY ASSETS
# ============================================================================

def render_step2_identify_assets():
    """Step 2: Identify and categorize assets"""
    
    st.markdown("""
    <div class="methodology-header">
        <h1>Step 2: Identify Assets</h1>
        <p>Identify and categorize assets affected by the problem statement</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="step-card">
    <h4>🎯 What Are Assets?</h4>
    <p>Assets are considered <strong>autonomous or discrete sets of technology capabilities 
    or components</strong> within a platform or system.</p>
    
    <p><strong>Examples include:</strong></p>
    <ul>
        <li><strong>Devices:</strong> Servers, workstations, mobile devices, IoT devices</li>
        <li><strong>Applications:</strong> Web apps, mobile apps, microservices, APIs</li>
        <li><strong>Platforms:</strong> Operating systems, databases, container orchestration</li>
        <li><strong>Data Storage:</strong> Databases, file systems, object storage, data lakes</li>
        <li><strong>Networks:</strong> Network segments, VPNs, load balancers, firewalls</li>
        <li><strong>Identity Systems:</strong> Identity providers, authentication services</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Example
    with st.expander("📘 Example: Partner API Integration Assets"):
        st.markdown("""
        <div class="asset-card">
        <h4>Asset Inventory</h4>
        
        <table style="width: 100%; border-collapse: collapse; margin-top: 1rem;">
        <thead style="background: #f59e0b; color: white;">
            <tr>
                <th style="padding: 0.75rem; text-align: left;">Asset ID</th>
                <th style="padding: 0.75rem; text-align: left;">Asset Name</th>
                <th style="padding: 0.75rem; text-align: left;">Asset Type</th>
                <th style="padding: 0.75rem; text-align: left;">Classification</th>
                <th style="padding: 0.75rem; text-align: left;">Criticality</th>
            </tr>
        </thead>
        <tbody>
            <tr style="background: white;">
                <td style="padding: 0.75rem; border: 1px solid #e5e7eb;">A-01</td>
                <td style="padding: 0.75rem; border: 1px solid #e5e7eb;">Partner API Endpoints</td>
                <td style="padding: 0.75rem; border: 1px solid #e5e7eb;">Application - REST API</td>
                <td style="padding: 0.75rem; border: 1px solid #e5e7eb;">Internal</td>
                <td style="padding: 0.75rem; border: 1px solid #e5e7eb;">High</td>
            </tr>
            <tr style="background: #fef3c7;">
                <td style="padding: 0.75rem; border: 1px solid #e5e7eb;">A-02</td>
                <td style="padding: 0.75rem; border: 1px solid #e5e7eb;">OAuth Token Service</td>
                <td style="padding: 0.75rem; border: 1px solid #e5e7eb;">Identity System</td>
                <td style="padding: 0.75rem; border: 1px solid #e5e7eb;">Secret</td>
                <td style="padding: 0.75rem; border: 1px solid #e5e7eb;">Critical</td>
            </tr>
            <tr style="background: white;">
                <td style="padding: 0.75rem; border: 1px solid #e5e7eb;">A-03</td>
                <td style="padding: 0.75rem; border: 1px solid #e5e7eb;">Customer PII Database</td>
                <td style="padding: 0.75rem; border: 1px solid #e5e7eb;">Data Storage</td>
                <td style="padding: 0.75rem; border: 1px solid #e5e7eb;">Confidential</td>
                <td style="padding: 0.75rem; border: 1px solid #e5e7eb;">Critical</td>
            </tr>
            <tr style="background: #fef3c7;">
                <td style="padding: 0.75rem; border: 1px solid #e5e7eb;">A-04</td>
                <td style="padding: 0.75rem; border: 1px solid #e5e7eb;">API Gateway</td>
                <td style="padding: 0.75rem; border: 1px solid #e5e7eb;">Network - Gateway</td>
                <td style="padding: 0.75rem; border: 1px solid #e5e7eb;">Internal</td>
                <td style="padding: 0.75rem; border: 1px solid #e5e7eb;">High</td>
            </tr>
            <tr style="background: white;">
                <td style="padding: 0.75rem; border: 1px solid #e5e7eb;">A-05</td>
                <td style="padding: 0.75rem; border: 1px solid #e5e7eb;">Backend Microservices</td>
                <td style="padding: 0.75rem; border: 1px solid #e5e7eb;">Application</td>
                <td style="padding: 0.75rem; border: 1px solid #e5e7eb;">Internal</td>
                <td style="padding: 0.75rem; border: 1px solid #e5e7eb;">Medium</td>
            </tr>
        </tbody>
        </table>
        </div>
        """, unsafe_allow_html=True)
    
    st.write("---")
    st.subheader("🎯 Your Turn: Build Asset Inventory")
    
    # Asset entry form
    st.write("### Add Assets to Your Pattern")
    
    with st.form("add_asset_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            asset_id = st.text_input("Asset ID:", placeholder="A-01, A-02, etc.")
            asset_name = st.text_input("Asset Name:", placeholder="Customer Database")
            asset_type = st.selectbox(
                "Asset Type:",
                [
                    "Device - Server",
                    "Device - Workstation",
                    "Device - Mobile",
                    "Device - IoT",
                    "Application - Web App",
                    "Application - Mobile App",
                    "Application - REST API",
                    "Application - Microservice",
                    "Platform - Operating System",
                    "Platform - Database",
                    "Platform - Container Orchestration",
                    "Data Storage - Database",
                    "Data Storage - File System",
                    "Data Storage - Object Storage",
                    "Network - Segment",
                    "Network - VPN",
                    "Network - Load Balancer",
                    "Network - Firewall",
                    "Network - Gateway",
                    "Identity - IdP",
                    "Identity - Authentication Service"
                ]
            )
        
        with col2:
            asset_classification = st.selectbox(
                "Data Classification:",
                ["Public", "Internal", "Confidential", "Restricted", "Secret"]
            )
            asset_criticality = st.selectbox(
                "Criticality:",
                ["Low", "Medium", "High", "Critical"]
            )
            asset_description = st.text_area(
                "Description:",
                height=100,
                placeholder="Describe what this asset does and why it's important..."
            )
        
        if st.form_submit_button("➕ Add Asset"):
            if asset_id and asset_name:
                asset = {
                    'id': asset_id,
                    'name': asset_name,
                    'type': asset_type,
                    'classification': asset_classification,
                    'criticality': asset_criticality,
                    'description': asset_description,
                    'timestamp': datetime.now().isoformat()
                }
                
                st.session_state.assets_identified.append(asset)
                st.success(f"✅ Asset {asset_id} added!")
                st.rerun()
    
    # Display current assets
    if st.session_state.assets_identified:
        st.write("### Your Asset Inventory")
        
        df = pd.DataFrame(st.session_state.assets_identified)
        st.dataframe(df[['id', 'name', 'type', 'classification', 'criticality']], use_container_width=True)
        
        # Visualization
        criticality_counts = df['criticality'].value_counts()
        
        fig = px.bar(
            x=criticality_counts.index,
            y=criticality_counts.values,
            labels={'x': 'Criticality', 'y': 'Number of Assets'},
            title='Assets by Criticality',
            color=criticality_counts.index,
            color_discrete_map={
                'Critical': '#ef4444',
                'High': '#f59e0b',
                'Medium': '#3b82f6',
                'Low': '#10b981'
            }
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Save step 2
        if st.button("💾 Save Step 2: Asset Inventory", type="primary"):
            st.session_state.artifacts['assets'] = st.session_state.assets_identified
            st.success("✅ Step 2 Complete! Proceed to Step 3: Establish Threat Modeling")
            st.balloons()

# ============================================================================
# STEP 3: THREAT MODELING
# ============================================================================

def render_step3_threat_modeling():
    """Step 3: Establish threat modeling with TE taxonomy"""
    
    st.markdown("""
    <div class="methodology-header">
        <h1>Step 3: Establish Threat Modeling</h1>
        <p>Identify threats using SecurityPatterns.io Threat Events Taxonomy (TE-01 to TE-42)</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="step-card">
    <h4>🎯 Threat Events Taxonomy</h4>
    <p>SecurityPatterns.io provides a curated list of <strong>42 threat events (TE-01 to TE-42)</strong> 
    categorized into 11 groups. This taxonomy focuses on cyber security threats to technology.</p>
    
    <p><strong>Why use this taxonomy?</strong></p>
    <ul>
        <li>Standardized categorization for consistency across patterns</li>
        <li>Comprehensive coverage of threat landscape</li>
        <li>Facilitates reusability and pattern comparison</li>
        <li>Maintains traceability from threats to controls</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Show taxonomy
    with st.expander("📚 View Complete Threat Events Taxonomy", expanded=False):
        for category, threats in THREAT_EVENTS_TAXONOMY.items():
            st.write(f"### {category}")
            for te_id, te_desc in threats.items():
                st.markdown(f"""
                <div class="threat-event">
                <strong>{te_id}:</strong> {te_desc}
                </div>
                """, unsafe_allow_html=True)
    
    # Example
    with st.expander("📘 Example: Partner API Integration Threats"):
        st.markdown("""
        <div class="securitypatterns-io">
        <h4>Threat Mapping Example</h4>
        
        <table style="width: 100%; border-collapse: collapse; margin-top: 1rem;">
        <thead style="background: #3b82f6; color: white;">
            <tr>
                <th style="padding: 0.75rem; text-align: left;">Threat ID</th>
                <th style="padding: 0.75rem; text-align: left;">Threat Category</th>
                <th style="padding: 0.75rem; text-align: left;">Threat Description (in context)</th>
                <th style="padding: 0.75rem; text-align: left;">Affected Assets</th>
            </tr>
        </thead>
        <tbody>
            <tr style="background: white;">
                <td style="padding: 0.75rem; border: 1px solid #e5e7eb;"><strong>TE-24</strong></td>
                <td style="padding: 0.75rem; border: 1px solid #e5e7eb;">Identity theft</td>
                <td style="padding: 0.75rem; border: 1px solid #e5e7eb;">Partner credentials stolen via phishing, used to access API</td>
                <td style="padding: 0.75rem; border: 1px solid #e5e7eb;">A-01 (API), A-02 (OAuth)</td>
            </tr>
            <tr style="background: #f8fafc;">
                <td style="padding: 0.75rem; border: 1px solid #e5e7eb;"><strong>TE-29</strong></td>
                <td style="padding: 0.75rem; border: 1px solid #e5e7eb;">Web application attacks</td>
                <td style="padding: 0.75rem; border: 1px solid #e5e7eb;">SQL injection through API parameters</td>
                <td style="padding: 0.75rem; border: 1px solid #e5e7eb;">A-01 (API), A-03 (Database)</td>
            </tr>
            <tr style="background: white;">
                <td style="padding: 0.75rem; border: 1px solid #e5e7eb;"><strong>TE-37</strong></td>
                <td style="padding: 0.75rem; border: 1px solid #e5e7eb;">Data breach</td>
                <td style="padding: 0.75rem; border: 1px solid #e5e7eb;">Unauthorized partner accesses customer PII beyond their scope</td>
                <td style="padding: 0.75rem; border: 1px solid #e5e7eb;">A-03 (Database)</td>
            </tr>
            <tr style="background: #f8fafc;">
                <td style="padding: 0.75rem; border: 1px solid #e5e7eb;"><strong>TE-40</strong></td>
                <td style="padding: 0.75rem; border: 1px solid #e5e7eb;">DDoS (application)</td>
                <td style="padding: 0.75rem; border: 1px solid #e5e7eb;">Malicious partner floods API with requests</td>
                <td style="padding: 0.75rem; border: 1px solid #e5e7eb;">A-01 (API), A-04 (Gateway)</td>
            </tr>
        </tbody>
        </table>
        </div>
        """, unsafe_allow_html=True)
    
    st.write("---")
    st.subheader("🎯 Your Turn: Map Threats to Your Assets")
    
    # Threat mapping form
    if not st.session_state.assets_identified:
        st.warning("⚠️ Please complete Step 2 (Identify Assets) first!")
        return
    
    st.write("### Add Threat Events")
    
    # Category selector for easier navigation
    selected_category = st.selectbox(
        "Browse by Threat Category:",
        list(THREAT_EVENTS_TAXONOMY.keys())
    )
    
    threats_in_category = THREAT_EVENTS_TAXONOMY[selected_category]
    
    st.write(f"**Threats in {selected_category}:**")
    for te_id, te_desc in threats_in_category.items():
        st.markdown(f"""
        <div class="threat-event">
        <strong>{te_id}:</strong> {te_desc}
        </div>
        """, unsafe_allow_html=True)
    
    with st.form("add_threat_form"):
        threat_id = st.selectbox(
            "Select Threat Event ID:",
            [f"{te_id}: {te_desc[:60]}..." for te_id, te_desc in threats_in_category.items()]
        )
        
        threat_context = st.text_area(
            "Describe threat in context of YOUR assets:",
            height=100,
            placeholder="Explain how this specific threat affects your specific assets..."
        )
        
        affected_assets = st.multiselect(
            "Which assets are vulnerable to this threat?",
            [f"{a['id']}: {a['name']}" for a in st.session_state.assets_identified]
        )
        
        if st.form_submit_button("➕ Add Threat Mapping"):
            if threat_context and affected_assets:
                threat_mapping = {
                    'threat_id': threat_id.split(':')[0].strip(),
                    'threat_taxonomy': threat_id,
                    'threat_context': threat_context,
                    'affected_assets': affected_assets,
                    'category': selected_category,
                    'timestamp': datetime.now().isoformat()
                }
                
                st.session_state.threats_mapped.append(threat_mapping)
                st.success(f"✅ Threat {threat_id.split(':')[0]} mapped!")
                st.rerun()
    
    # Display current threat mappings
    if st.session_state.threats_mapped:
        st.write("### Your Threat Mappings")
        
        for threat in st.session_state.threats_mapped:
            st.markdown(f"""
            <div class="threat-event">
            <strong>{threat['threat_id']}</strong> - {threat['category']}<br>
            <em>{threat['threat_context']}</em><br>
            <strong>Affects:</strong> {', '.join(threat['affected_assets'])}
            </div>
            """, unsafe_allow_html=True)
        
        # Save step 3
        if st.button("💾 Save Step 3: Threat Modeling", type="primary"):
            st.session_state.artifacts['threat_mapping'] = st.session_state.threats_mapped
            st.success("✅ Step 3 Complete! Proceed to Step 4: Solution Design & Control Mapping")
            st.balloons()

# ============================================================================
# STEP 4: SOLUTION & CONTROLS
# ============================================================================

def render_step4_solution_controls():
    """Step 4: Describe solution and map controls"""
    
    st.markdown("""
    <div class="methodology-header">
        <h1>Step 4: Solution Design & Control Mapping</h1>
        <p>Describe target state solution and map controls to threats using NIST 800-53</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="four-steps">
    <h4>The 4-Step Control Mapping Process (SecurityPatterns.io)</h4>
    <ol>
        <li><strong>Map threats to assets:</strong> Decompose threats and identify which assets are vulnerable</li>
        <li><strong>Map controls to threats:</strong> For each threat, identify mitigating security controls</li>
        <li><strong>Build asset-centric pattern:</strong> Combine Threat → Asset → Control mappings</li>
        <li><strong>Categorize controls:</strong> Use NIST SP 800-53 (Rev 5) control families</li>
    </ol>
    </div>
    """, unsafe_allow_html=True)
    
    # Show NIST control families
    with st.expander("📚 NIST SP 800-53 (Rev 5) Control Families"):
        for code, family in NIST_CONTROL_FAMILIES.items():
            st.markdown(f"""
            <div class="control-badge">{code}: {family}</div>
            """, unsafe_allow_html=True)
    
    st.write("---")
    st.subheader("🎯 Map Controls to Threats")
    
    if not st.session_state.threats_mapped:
        st.warning("⚠️ Please complete Step 3 (Threat Modeling) first!")
        return
    
    # Control mapping form
    with st.form("add_control_form"):
        st.write("### Add Security Control")
        
        threat_to_control = st.selectbox(
            "Which threat does this control mitigate?",
            [f"{t['threat_id']}: {t['threat_context'][:60]}..." for t in st.session_state.threats_mapped]
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            control_family = st.selectbox(
                "NIST 800-53 Control Family:",
                [f"{code}: {family}" for code, family in NIST_CONTROL_FAMILIES.items()]
            )
            
            control_id = st.text_input(
                "Control ID:",
                placeholder="e.g., AC-2, IA-5, SC-8"
            )
            
            control_name = st.text_input(
                "Control Name:",
                placeholder="e.g., Account Management, MFA, Transmission Confidentiality"
            )
        
        with col2:
            control_description = st.text_area(
                "Control Description (in context):",
                height=120,
                placeholder="Describe HOW this control mitigates the threat in YOUR context..."
            )
            
            effectiveness = st.slider(
                "Effectiveness %:",
                0, 100, 90,
                help="How effective is this control at mitigating the threat?"
            )
        
        residual_risk = st.text_area(
            "Residual Risk:",
            height=80,
            placeholder="What risk remains after this control is implemented?"
        )
        
        if st.form_submit_button("➕ Add Control Mapping"):
            if control_id and control_name and control_description:
                control_mapping = {
                    'threat': threat_to_control,
                    'control_family': control_family,
                    'control_id': control_id,
                    'control_name': control_name,
                    'control_description': control_description,
                    'effectiveness': f"{effectiveness}%",
                    'residual_risk': residual_risk,
                    'timestamp': datetime.now().isoformat()
                }
                
                st.session_state.controls_mapped.append(control_mapping)
                st.success(f"✅ Control {control_id} mapped!")
                st.rerun()
    
    # Display control mappings
    if st.session_state.controls_mapped:
        st.write("### Your Control Mappings")
        
        df = pd.DataFrame(st.session_state.controls_mapped)
        st.dataframe(
            df[['control_id', 'control_name', 'control_family', 'effectiveness']], 
            use_container_width=True
        )
        
        # Complete traceability matrix
        st.write("### Complete Traceability: Threat → Asset → Control")
        
        traceability_data = []
        for control in st.session_state.controls_mapped:
            threat_id = control['threat'].split(':')[0].strip()
            
            # Find the threat
            threat_obj = next((t for t in st.session_state.threats_mapped if t['threat_id'] == threat_id), None)
            if threat_obj:
                traceability_data.append({
                    'Threat ID': threat_id,
                    'Affected Assets': ', '.join([a.split(':')[0] for a in threat_obj['affected_assets']]),
                    'Control': f"{control['control_id']}: {control['control_name']}",
                    'Control Family': control['control_family'].split(':')[0],
                    'Effectiveness': control['effectiveness']
                })
        
        if traceability_data:
            trace_df = pd.DataFrame(traceability_data)
            st.dataframe(trace_df, use_container_width=True)
            
            # Download
            csv = trace_df.to_csv(index=False)
            st.download_button(
                "📥 Download Traceability Matrix (CSV)",
                csv,
                "threat_asset_control_traceability.csv",
                "text/csv"
            )
        
        # Save step 4
        if st.button("💾 Save Step 4: Solution & Controls", type="primary"):
            st.session_state.artifacts['control_threat_mapping'] = st.session_state.controls_mapped
            st.session_state.artifacts['threat_asset_mapping'] = st.session_state.threats_mapped
            st.session_state.pattern_complete = True
            st.success("✅ Step 4 Complete! Your security pattern is ready!")
            st.balloons()

# ============================================================================
# PATTERN EXPORT
# ============================================================================

def render_pattern_export():
    """Export complete security pattern"""
    
    st.markdown("""
    <div class="methodology-header">
        <h1>📦 Your Complete Security Pattern</h1>
        <p>Export your asset-centric security pattern based on SecurityPatterns.io methodology</p>
    </div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.pattern_complete:
        st.warning("⚠️ Please complete all 4 steps before exporting your pattern!")
        return
    
    # Generate complete pattern document
    pattern_doc = f"""
# {st.session_state.pattern_name}
## Security Pattern (SecurityPatterns.io Methodology)

**Created:** {datetime.now().strftime('%Y-%m-%d %H:%M')}
**Team:** {st.session_state.team_name}

---

## 1. SCOPE & PROBLEM STATEMENT

### Scope
{st.session_state.artifacts['scope_problem']['scope']['systems']}

### Problem Statement
{st.session_state.artifacts['scope_problem']['problem_statement']}

### Typical Challenges
{st.session_state.artifacts['scope_problem']['challenges']}

---

## 2. ASSET INVENTORY

| Asset ID | Asset Name | Type | Classification | Criticality |
|----------|------------|------|----------------|-------------|
"""
    
    for asset in st.session_state.assets_identified:
        pattern_doc += f"| {asset['id']} | {asset['name']} | {asset['type']} | {asset['classification']} | {asset['criticality']} |\n"
    
    pattern_doc += """
---

## 3. THREAT MODELING (Threat Events Taxonomy)

"""
    
    for threat in st.session_state.threats_mapped:
        pattern_doc += f"""
### {threat['threat_id']} - {threat['category']}
**Context:** {threat['threat_context']}
**Affected Assets:** {', '.join(threat['affected_assets'])}

"""
    
    pattern_doc += """
---

## 4. SECURITY CONTROLS (NIST SP 800-53 Rev 5)

| Control ID | Control Name | Mitigates Threat | Effectiveness | Residual Risk |
|------------|--------------|------------------|---------------|---------------|
"""
    
    for control in st.session_state.controls_mapped:
        threat_id = control['threat'].split(':')[0].strip()
        pattern_doc += f"| {control['control_id']} | {control['control_name']} | {threat_id} | {control['effectiveness']} | {control['residual_risk'][:50]}... |\n"
    
    pattern_doc += """
---

## 5. TRACEABILITY MATRIX

**Complete Threat → Asset → Control Mapping**

"""
    
    # Show pattern
    st.markdown(pattern_doc)
    
    # Download buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.download_button(
            "📥 Download Pattern (Markdown)",
            pattern_doc,
            f"{st.session_state.pattern_name.replace(' ', '_')}.md",
            "text/markdown",
            use_container_width=True
        )
    
    with col2:
        pattern_json = json.dumps(st.session_state.artifacts, indent=2, default=str)
        st.download_button(
            "📥 Download Pattern (JSON)",
            pattern_json,
            f"{st.session_state.pattern_name.replace(' ', '_')}.json",
            "application/json",
            use_container_width=True
        )
    
    with col3:
        # CSV export of traceability
        trace_data = []
        for control in st.session_state.controls_mapped:
            threat_id = control['threat'].split(':')[0].strip()
            threat_obj = next((t for t in st.session_state.threats_mapped if t['threat_id'] == threat_id), None)
            if threat_obj:
                trace_data.append({
                    'Threat_ID': threat_id,
                    'Assets': ', '.join(threat_obj['affected_assets']),
                    'Control_ID': control['control_id'],
                    'Control_Name': control['control_name'],
                    'Effectiveness': control['effectiveness']
                })
        
        if trace_data:
            csv = pd.DataFrame(trace_data).to_csv(index=False)
            st.download_button(
                "📥 Download Traceability (CSV)",
                csv,
                "traceability_matrix.csv",
                "text/csv",
                use_container_width=True
            )

# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    # Sidebar
    with st.sidebar:
        st.title("🛡️ SecurityPatterns.io")
        st.caption("Pattern Development Workshop")
        
        st.write("---")
        st.write(f"**Team:** {st.session_state.team_name}")
        
        if st.session_state.pattern_name:
            st.write(f"**Pattern:** {st.session_state.pattern_name[:30]}...")
        
        st.write("---")
        st.write("### Progress")
        
        steps = [
            ("Step 1: Scope", st.session_state.scope_defined),
            ("Step 2: Assets", len(st.session_state.assets_identified) > 0),
            ("Step 3: Threats", len(st.session_state.threats_mapped) > 0),
            ("Step 4: Controls", len(st.session_state.controls_mapped) > 0)
        ]
        
        for step_name, completed in steps:
            icon = "✅" if completed else "⏳"
            st.write(f"{icon} {step_name}")
        
        progress = sum(1 for _, c in steps if c) / len(steps)
        st.progress(progress)
        
        st.write("---")
        st.metric("Assets", len(st.session_state.assets_identified))
        st.metric("Threats", len(st.session_state.threats_mapped))
        st.metric("Controls", len(st.session_state.controls_mapped))
    
    # Main content
    activity = st.selectbox(
        "Choose Activity:",
        [
            "📚 Methodology Overview",
            "Step 1: Scope & Problem",
            "Step 2: Identify Assets",
            "Step 3: Threat Modeling",
            "Step 4: Solution & Controls",
            "📦 Export Pattern"
        ]
    )
    
    if "Methodology" in activity:
        render_methodology_overview()
    elif "Step 1" in activity:
        render_step1_scope_problem()
    elif "Step 2" in activity:
        render_step2_identify_assets()
    elif "Step 3" in activity:
        render_step3_threat_modeling()
    elif "Step 4" in activity:
        render_step4_solution_controls()
    elif "Export" in activity:
        render_pattern_export()

if __name__ == "__main__":
    main()
