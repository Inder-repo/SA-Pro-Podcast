"""
ENTERPRISE SECURITY ARCHITECTURE WORKSHOP
Professional Training Platform

COMPLETE END-TO-END WORKFLOW:

1. BUSINESS REQUIREMENTS CAPTURE
   - Gather inputs from executives (CEO, CFO, CTO)
   - Capture stakeholder concerns (CISO, business units)
   - Document business drivers and constraints

2. SECURITY REQUIREMENTS TRANSLATION
   - Transform business language to technical requirements
   - Map to compliance frameworks (GDPR, HIPAA, PCI-DSS, SOC 2)
   - Define measurable security objectives

3. HIGH-LEVEL DESIGN (HLD) PROPOSAL
   - Component architecture
   - Security zones & trust boundaries
   - Data flow diagrams
   - C4 model diagrams

4. ARCHITECTURE REVIEW & BUSINESS APPROVALS
   - Present to Architecture Review Board (ARB)
   - Defend design decisions to stakeholders
   - Address concerns from CISO, CTO, CFO
   - Obtain formal approvals

5. DETAILED SOLUTION DESIGN
   - STRIDE threat modeling
   - Attack surface analysis
   - Control selection and mapping
   - Professional diagramming (draw.io equivalent)
   - Technical specifications

6. SECURITY PATTERN CREATION
   - Document reusable patterns (SecurityPatterns.io methodology)
   - Asset-Threat-Control mapping
   - Pattern library for organization

LEARNING APPROACH:
- Instructor-Led: Complete worked example FIRST, then student exercise
- Self-Learning: Independent practice with locked answer keys
- Each phase: One example + one exercise
- Professional diagramming throughout
"""

import streamlit as st
import pandas as pd
import json
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px
from streamlit_drawable_canvas import st_canvas
from PIL import Image
from io import BytesIO
import base64

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Enterprise Security Architecture Workshop",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# ENTERPRISE-GRADE STYLING
# ============================================================================

st.markdown("""
<style>
    .main { background: #f8fafc; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    
    /* Workshop Headers */
    .workshop-header {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        color: white; padding: 2.5rem; border-radius: 16px;
        margin-bottom: 2rem; box-shadow: 0 10px 25px rgba(0,0,0,0.2);
    }
    .workshop-header h1 { margin: 0; font-size: 2.2rem; font-weight: 700; }
    .workshop-header p { margin: 0.5rem 0 0 0; opacity: 0.95; font-size: 1.05rem; }
    
    /* Phase Navigation Cards */
    .phase-card {
        background: white; padding: 2rem; margin: 1.5rem 0;
        border-radius: 12px; border-left: 6px solid #3b82f6;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        transition: transform 0.2s, box-shadow 0.2s;
    }
    .phase-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.12);
    }
    
    /* Instructor Example */
    .instructor-example {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        border: 3px solid #f59e0b; padding: 2rem;
        border-radius: 12px; margin: 1.5rem 0;
    }
    .instructor-example h3 { color: #92400e; margin-top: 0; }
    
    /* Student Exercise */
    .student-exercise {
        background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
        border: 3px solid #3b82f6; padding: 2rem;
        border-radius: 12px; margin: 1.5rem 0;
    }
    .student-exercise h3 { color: #1e40af; margin-top: 0; }
    
    /* Business Requirement Card */
    .requirement-business {
        background: #fef3c7; border-left: 5px solid #f59e0b;
        padding: 1.5rem; margin: 1rem 0; border-radius: 8px;
        font-size: 1.05rem;
    }
    
    /* Security Requirement Card */
    .requirement-security {
        background: #dbeafe; border-left: 5px solid #3b82f6;
        padding: 1.5rem; margin: 1rem 0; border-radius: 8px;
    }
    
    /* Architecture Artifact */
    .architecture-artifact {
        background: #ecfdf5; border-left: 5px solid #10b981;
        padding: 1.5rem; margin: 1rem 0; border-radius: 8px;
    }
    
    /* Mapping Flow Arrow */
    .mapping-arrow {
        text-align: center; font-size: 2.5rem;
        color: #3b82f6; margin: 1.5rem 0; font-weight: 700;
    }
    
    /* Locked Content */
    .locked-content {
        background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
        border: 3px dashed #ef4444; padding: 2.5rem;
        border-radius: 12px; text-align: center; margin: 2rem 0;
    }
    .locked-content h3 { color: #991b1b; margin: 0; }
    
    /* Answer Key */
    .answer-key {
        background: #f0fdf4; border: 3px solid #10b981;
        padding: 2rem; border-radius: 12px; margin: 1.5rem 0;
    }
    
    /* Diagram Canvas Container */
    .canvas-container {
        background: white; border: 3px solid #e5e7eb;
        border-radius: 12px; padding: 1.5rem; margin: 1.5rem 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }
    
    /* STRIDE Threat Categories */
    .stride-S { background: #fee2e2; color: #991b1b; padding: 0.4rem 1rem; border-radius: 6px; display: inline-block; margin: 0.25rem; font-weight: 600; }
    .stride-T { background: #fef3c7; color: #92400e; padding: 0.4rem 1rem; border-radius: 6px; display: inline-block; margin: 0.25rem; font-weight: 600; }
    .stride-R { background: #dbeafe; color: #1e40af; padding: 0.4rem 1rem; border-radius: 6px; display: inline-block; margin: 0.25rem; font-weight: 600; }
    .stride-I { background: #fce7f3; color: #9f1239; padding: 0.4rem 1rem; border-radius: 6px; display: inline-block; margin: 0.25rem; font-weight: 600; }
    .stride-D { background: #f3e8ff; color: #6b21a8; padding: 0.4rem 1rem; border-radius: 6px; display: inline-block; margin: 0.25rem; font-weight: 600; }
    .stride-E { background: #ffedd5; color: #9a3412; padding: 0.4rem 1rem; border-radius: 6px; display: inline-block; margin: 0.25rem; font-weight: 600; }
    
    /* Stakeholder Cards */
    .stakeholder-card {
        background: white; padding: 1.5rem; margin: 0.75rem 0;
        border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    }
    .stakeholder-ceo { border-left: 5px solid #8b5cf6; }
    .stakeholder-ciso { border-left: 5px solid #ef4444; }
    .stakeholder-cto { border-left: 5px solid #3b82f6; }
    .stakeholder-cfo { border-left: 5px solid #f59e0b; }
    .stakeholder-vpe { border-left: 5px solid #10b981; }
    
    /* Security Pattern */
    .pattern-document {
        background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%);
        border: 3px solid #10b981; padding: 2rem; margin: 1.5rem 0;
        border-radius: 12px; font-family: 'Courier New', monospace;
        font-size: 0.95rem;
    }
    
    /* Progress Indicators */
    .progress-metric {
        background: white; padding: 1.5rem; border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06); margin: 1rem 0;
        text-align: center;
    }
    
    /* Table Styling */
    .dataframe { border-radius: 8px; overflow: hidden; }
    
    /* Buttons */
    .stButton>button {
        border-radius: 8px; font-weight: 600;
        transition: all 0.2s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

def init_session_state():
    """Initialize all session state variables"""
    defaults = {
        # Learning mode
        'mode': 'instructor_led',  # instructor_led or self_learning
        'current_phase': 0,  # 0 = overview, 1-6 = phases
        'completed_phases': [],
        'self_learning_unlocked': False,
        'unlock_code': 'EA-SEC-2026',  # Unlock code for self-learning
        
        # User information
        'user_name': 'Enterprise Architect',
        'organization': 'Global Enterprise',
        
        # Phase 1: Business Requirements
        'stakeholder_inputs': {},
        'business_requirements': [],
        
        # Phase 2: Security Requirements
        'security_requirements': [],
        'compliance_mapping': [],
        
        # Phase 3: High-Level Design
        'hld_components': [],
        'security_zones': [],
        'data_flows': [],
        'hld_diagrams': [],
        
        # Phase 4: ARB & Approvals
        'arb_presentation': {},
        'stakeholder_questions': [],
        'approvals': {},
        
        # Phase 5: Detailed Design
        'stride_analysis': {},
        'threat_models': [],
        'control_mappings': [],
        'detailed_diagrams': [],
        
        # Phase 6: Security Patterns
        'security_patterns': [],
        'pattern_library': [],
        
        # Progress tracking
        'artifacts_created': [],
        'answer_keys_unlocked': {},
        'exercise_submissions': {}
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session_state()

# ============================================================================
# ANSWER KEYS (EXPERT SOLUTIONS)
# ============================================================================

ANSWER_KEYS = {
    'phase1_business_req': {
        'scenario': 'Global E-Commerce Platform',
        'stakeholders': {
            'ceo': {
                'input': """We're launching a global marketplace connecting sellers and buyers across 100 countries. 
                Platform must support $5B GMV in year 1, with 10M active users. Key features: product listings, 
                payment processing, shipping integration, seller analytics. Need mobile-first experience.""",
                'priorities': ['Revenue growth', 'Market expansion', 'Customer satisfaction', 'Time to market']
            },
            'ciso': {
                'concerns': [
                    'Customer PII protection across jurisdictions (GDPR, CCPA, etc.)',
                    'Payment data security (PCI-DSS compliance)',
                    'Seller identity verification (KYC/AML)',
                    'Fraud prevention (fake listings, payment fraud)',
                    'Third-party risk (payment gateways, shipping providers)',
                    'Data residency requirements by country',
                    'Incident response capabilities'
                ],
                'risk_appetite': 'Low - financial services regulation'
            },
            'cto': {
                'requirements': [
                    'Horizontal scalability (10M → 100M users)',
                    'Multi-region deployment (latency < 200ms globally)',
                    'High availability (99.99% uptime)',
                    'Integration with 20+ payment providers',
                    'Real-time inventory synchronization'
                ],
                'constraints': ['18-month delivery timeline', 'Existing tech stack (microservices)']
            },
            'cfo': {
                'budget': '$15M capital, $5M annual operating budget',
                'roi_target': 'Security ROI: prevent $50M+ in potential breaches',
                'concerns': ['Compliance fines risk', 'Insurance premiums', 'Audit costs']
            }
        },
        'security_requirements': [
            {
                'id': 'SR-001',
                'requirement': 'All customer PII must be encrypted at rest and in transit',
                'business_driver': 'GDPR/CCPA compliance, customer trust',
                'compliance': 'GDPR Art. 32, CCPA §1798.150',
                'implementation': 'AES-256 encryption at rest, TLS 1.3 in transit, field-level encryption for sensitive data',
                'success_criteria': 'Zero plaintext PII in databases or logs, 100% encrypted connections'
            },
            {
                'id': 'SR-002',
                'requirement': 'Payment card data must never be stored; use tokenization',
                'business_driver': 'PCI-DSS compliance, reduce audit scope',
                'compliance': 'PCI-DSS Requirement 3',
                'implementation': 'Integrate payment tokenization service (Stripe, Adyen), store tokens only',
                'success_criteria': 'Zero credit card numbers in system, PCI audit scope reduced by 80%'
            },
            {
                'id': 'SR-003',
                'requirement': 'Multi-factor authentication mandatory for all users',
                'business_driver': 'Prevent account takeover, fraud reduction',
                'compliance': 'NIST 800-63B, Industry best practice',
                'implementation': 'SMS/Email OTP, Authenticator apps, biometric options for mobile',
                'success_criteria': 'Account takeover incidents < 0.01%, MFA adoption > 90%'
            },
            {
                'id': 'SR-004',
                'requirement': 'Real-time fraud detection for transactions and listings',
                'business_driver': 'Protect buyers and sellers, reduce chargebacks',
                'compliance': 'Risk management best practice',
                'implementation': 'ML-based anomaly detection, velocity checks, device fingerprinting',
                'success_criteria': 'Fraud detection rate > 95%, false positive rate < 2%'
            },
            {
                'id': 'SR-005',
                'requirement': 'Comprehensive audit logging with immutable storage',
                'business_driver': 'Forensic investigation, regulatory compliance',
                'compliance': 'SOX, GDPR Art. 33, PCI-DSS Req. 10',
                'implementation': 'Centralized SIEM, write-once storage, 7-year retention',
                'success_criteria': '100% critical events logged, audit trail never modified'
            },
            {
                'id': 'SR-006',
                'requirement': 'Zero-trust network architecture with microsegmentation',
                'business_driver': 'Limit blast radius, prevent lateral movement',
                'compliance': 'NIST 800-207',
                'implementation': 'Service mesh, identity-based access, network policies',
                'success_criteria': 'Network segments isolated, all service-to-service auth required'
            },
            {
                'id': 'SR-007',
                'requirement': 'Data residency controls for international compliance',
                'business_driver': 'Legal requirements (GDPR, China Cybersecurity Law)',
                'compliance': 'GDPR Art. 44-49, Country-specific laws',
                'implementation': 'Regional data centers, data sovereignty enforcement',
                'success_criteria': 'EU data stays in EU, China data stays in China, etc.'
            }
        ]
    },
    
    'phase3_hld': {
        'components': [
            {
                'name': 'Web Frontend (React SPA)',
                'type': 'Presentation Layer',
                'zone': 'DMZ (Public)',
                'trust_level': 'Untrusted',
                'data_classification': 'Public',
                'security_controls': [
                    'Content Security Policy (CSP)',
                    'XSS protection',
                    'CSRF tokens',
                    'Subresource Integrity (SRI)',
                    'HTTPS only (HSTS)'
                ],
                'threats': 'XSS, CSRF, clickjacking',
                'ownership': 'Frontend Team'
            },
            {
                'name': 'API Gateway',
                'type': 'Edge Service',
                'zone': 'DMZ (Public)',
                'trust_level': 'Semi-trusted',
                'data_classification': 'Internal',
                'security_controls': [
                    'OAuth 2.1 / OIDC authentication',
                    'JWT validation',
                    'Rate limiting (per user/IP)',
                    'DDoS mitigation',
                    'Request/response validation',
                    'API key management'
                ],
                'threats': 'API abuse, DDoS, broken authentication',
                'ownership': 'Platform Team'
            },
            {
                'name': 'Application Services (Microservices)',
                'type': 'Business Logic',
                'zone': 'Application (Private)',
                'trust_level': 'Trusted',
                'data_classification': 'Confidential',
                'security_controls': [
                    'Service-to-service mTLS',
                    'Authorization enforcement (RBAC/ABAC)',
                    'Input validation',
                    'Business logic controls',
                    'Secure coding practices'
                ],
                'threats': 'Authorization bypass, injection attacks, business logic flaws',
                'ownership': 'Engineering Teams'
            },
            {
                'name': 'Data Layer (Databases)',
                'type': 'Persistence',
                'zone': 'Data (Restricted)',
                'trust_level': 'Highly Trusted',
                'data_classification': 'Restricted/Secret',
                'security_controls': [
                    'Encryption at rest (AES-256)',
                    'Network isolation (private subnet)',
                    'Least privilege access',
                    'Database activity monitoring',
                    'Backup encryption',
                    'Row-level security'
                ],
                'threats': 'Data breach, SQL injection, privilege escalation',
                'ownership': 'Data Team'
            },
            {
                'name': 'Identity & Access Management (IAM)',
                'type': 'Security Service',
                'zone': 'Security (Isolated)',
                'trust_level': 'Highly Trusted',
                'data_classification': 'Secret',
                'security_controls': [
                    'MFA enforcement',
                    'SSO / Federation',
                    'Password policies',
                    'Session management',
                    'Key management service',
                    'Secrets vault'
                ],
                'threats': 'Credential theft, session hijacking, key compromise',
                'ownership': 'Security Team'
            },
            {
                'name': 'Payment Processing Service',
                'type': 'Financial Service',
                'zone': 'PCI Compliance Zone (Isolated)',
                'trust_level': 'Highly Trusted',
                'data_classification': 'Restricted (PCI)',
                'security_controls': [
                    'Tokenization',
                    'Dedicated network segment',
                    'No card data storage',
                    'PCI-DSS certified infrastructure',
                    'Hardware security module (HSM)'
                ],
                'threats': 'Payment fraud, data breach, PCI compliance failure',
                'ownership': 'Payments Team'
            },
            {
                'name': 'Logging & Monitoring (SIEM)',
                'type': 'Security Operations',
                'zone': 'Security (Isolated)',
                'trust_level': 'Highly Trusted',
                'data_classification': 'Confidential',
                'security_controls': [
                    'Centralized log aggregation',
                    'Anomaly detection',
                    'Alert correlation',
                    'Immutable log storage',
                    'SOC integration'
                ],
                'threats': 'Log tampering, blind spots, alert fatigue',
                'ownership': 'SecOps Team'
            }
        ],
        'security_zones': [
            {
                'name': 'DMZ (Public Zone)',
                'purpose': 'Internet-facing services',
                'trust': 'Untrusted',
                'components': ['Web Frontend', 'API Gateway', 'CDN'],
                'controls': 'WAF, DDoS protection, public IP filtering'
            },
            {
                'name': 'Application Zone (Private)',
                'purpose': 'Business logic execution',
                'trust': 'Trusted',
                'components': ['Microservices', 'Message queues', 'Cache'],
                'controls': 'Service mesh, network policies, private IPs only'
            },
            {
                'name': 'Data Zone (Restricted)',
                'purpose': 'Data storage and persistence',
                'trust': 'Highly Trusted',
                'components': ['Databases', 'Data warehouse', 'Backup storage'],
                'controls': 'Network isolation, encryption, access logging'
            },
            {
                'name': 'Security Zone (Isolated)',
                'purpose': 'Security services',
                'trust': 'Highly Trusted',
                'components': ['IAM', 'Key management', 'SIEM', 'Secrets vault'],
                'controls': 'Maximum isolation, audit all access, MFA required'
            },
            {
                'name': 'PCI Compliance Zone',
                'purpose': 'Payment processing',
                'trust': 'Highly Trusted',
                'components': ['Payment service', 'Tokenization', 'HSM'],
                'controls': 'PCI-DSS controls, dedicated network, no mixing'
            }
        ],
        'data_flows': [
            {
                'from': 'Web Frontend',
                'to': 'API Gateway',
                'protocol': 'HTTPS/TLS 1.3',
                'data': 'User requests + JWT token',
                'security': 'Certificate pinning, token in Authorization header',
                'encryption': 'TLS 1.3 (AES-256-GCM)'
            },
            {
                'from': 'API Gateway',
                'to': 'Application Services',
                'protocol': 'HTTPS/mTLS',
                'data': 'Validated requests',
                'security': 'Mutual TLS, service authentication',
                'encryption': 'TLS 1.3 + service mesh encryption'
            },
            {
                'from': 'Application Services',
                'to': 'Data Layer',
                'protocol': 'Database protocol (encrypted)',
                'data': 'Queries with credentials',
                'security': 'Connection encryption, least privilege',
                'encryption': 'TLS + database-native encryption'
            },
            {
                'from': 'Application Services',
                'to': 'Payment Service',
                'protocol': 'HTTPS/mTLS',
                'data': 'Payment requests (no card data)',
                'security': 'Tokenized payments only, PCI boundary',
                'encryption': 'TLS 1.3 + end-to-end encryption'
            },
            {
                'from': 'All Components',
                'to': 'SIEM',
                'protocol': 'Syslog/TLS',
                'data': 'Audit logs',
                'security': 'Tamper-proof transport, immutable storage',
                'encryption': 'TLS 1.3'
            }
        ]
    },
    
    'phase5_stride': {
        'threats': [
            {
                'id': 'T-001',
                'category': 'Spoofing',
                'threat': 'Attacker impersonates legitimate user using stolen credentials',
                'asset': 'User authentication system',
                'attack_vector': 'Phishing, credential stuffing, session hijacking',
                'likelihood': 'High',
                'impact': 'Critical',
                'current_risk': 'High',
                'controls': [
                    'Multi-factor authentication (MFA) mandatory',
                    'Risk-based authentication',
                    'Device fingerprinting',
                    'Impossible travel detection',
                    'Session timeout and revocation'
                ],
                'residual_risk': 'Low',
                'owner': 'Identity Team'
            },
            {
                'id': 'T-002',
                'category': 'Tampering',
                'threat': 'Man-in-the-middle attack modifies transaction data in transit',
                'asset': 'API communications',
                'attack_vector': 'Network interception, SSL stripping, DNS poisoning',
                'likelihood': 'Medium',
                'impact': 'Critical',
                'current_risk': 'High',
                'controls': [
                    'TLS 1.3 for all communications',
                    'Certificate pinning',
                    'Request signing',
                    'Response integrity validation',
                    'HSTS enforcement'
                ],
                'residual_risk': 'Very Low',
                'owner': 'Platform Team'
            },
            {
                'id': 'T-003',
                'category': 'Repudiation',
                'threat': 'User denies making a purchase or transaction',
                'asset': 'Transaction records',
                'attack_vector': 'Dispute/chargeback fraud',
                'likelihood': 'Medium',
                'impact': 'High',
                'current_risk': 'Medium',
                'controls': [
                    'Immutable audit logs',
                    'Digital signatures on transactions',
                    'Email/SMS confirmations',
                    'Transaction receipts',
                    'Video/photo proof of delivery'
                ],
                'residual_risk': 'Low',
                'owner': 'Payments Team'
            },
            {
                'id': 'T-004',
                'category': 'Information Disclosure',
                'threat': 'Database breach exposes customer PII and payment data',
                'asset': 'Customer database',
                'attack_vector': 'SQL injection, misconfiguration, insider threat',
                'likelihood': 'Medium',
                'impact': 'Critical',
                'current_risk': 'Critical',
                'controls': [
                    'Encryption at rest (AES-256)',
                    'Field-level encryption for sensitive data',
                    'Database activity monitoring',
                    'Least privilege access',
                    'Network isolation',
                    'Regular security audits'
                ],
                'residual_risk': 'Low',
                'owner': 'Data Team'
            },
            {
                'id': 'T-005',
                'category': 'Information Disclosure',
                'threat': 'API endpoint exposes excessive data in response',
                'asset': 'API Gateway / Backend APIs',
                'attack_vector': 'API enumeration, BOLA/IDOR vulnerabilities',
                'likelihood': 'High',
                'impact': 'High',
                'current_risk': 'High',
                'controls': [
                    'Field filtering based on user role',
                    'API response validation',
                    'Authorization checks on every endpoint',
                    'Rate limiting',
                    'API security testing (OWASP API Top 10)'
                ],
                'residual_risk': 'Medium',
                'owner': 'API Team'
            },
            {
                'id': 'T-006',
                'category': 'Denial of Service',
                'threat': 'DDoS attack makes platform unavailable',
                'asset': 'Web application and API',
                'attack_vector': 'Volumetric attack, application-layer attack',
                'likelihood': 'High',
                'impact': 'High',
                'current_risk': 'High',
                'controls': [
                    'DDoS mitigation service',
                    'CDN with DDoS protection',
                    'Rate limiting (per IP/user)',
                    'Auto-scaling',
                    'CAPTCHA for suspicious traffic',
                    'Geo-blocking high-risk countries'
                ],
                'residual_risk': 'Medium',
                'owner': 'Platform Team'
            },
            {
                'id': 'T-007',
                'category': 'Elevation of Privilege',
                'threat': 'Regular user escalates to admin privileges',
                'asset': 'Authorization system',
                'attack_vector': 'Authorization bypass, privilege escalation bugs',
                'likelihood': 'Low',
                'impact': 'Critical',
                'current_risk': 'High',
                'controls': [
                    'Principle of least privilege',
                    'Role-based access control (RBAC)',
                    'Separation of duties',
                    'Privileged access management (PAM)',
                    'Just-in-time (JIT) access',
                    'Regular privilege reviews'
                ],
                'residual_risk': 'Very Low',
                'owner': 'Security Team'
            },
            {
                'id': 'T-008',
                'category': 'Tampering',
                'threat': 'Seller uploads malicious content (XSS payload in product description)',
                'asset': 'Product listing system',
                'attack_vector': 'Stored XSS, HTML injection',
                'likelihood': 'High',
                'impact': 'High',
                'current_risk': 'High',
                'controls': [
                    'Input validation and sanitization',
                    'Content Security Policy (CSP)',
                    'HTML encoding/escaping',
                    'Automated security scanning',
                    'Content moderation'
                ],
                'residual_risk': 'Low',
                'owner': 'Marketplace Team'
            }
        ]
    }
}

def check_unlock_code(code):
    """Verify unlock code for self-learning mode"""
    return code.strip().upper() == st.session_state.unlock_code

def show_answer_key(phase_key):
    """Display answer key if unlocked"""
    if st.session_state.mode == 'instructor_led':
        # Instructor mode: always show answers
        display_answer_key_content(phase_key)
    else:
        # Self-learning mode: require unlock
        if st.session_state.answer_keys_unlocked.get(phase_key):
            display_answer_key_content(phase_key)
        else:
            st.markdown("""
            <div class="locked-content">
                <h3>🔒 Answer Key Locked</h3>
                <p>Complete your exercise first, then unlock to compare with expert solution</p>
                <p style='margin-top: 1rem;'><strong>Why?</strong> Attempting the exercise yourself builds deeper understanding</p>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                unlock_input = st.text_input(
                    "Enter unlock code:",
                    type="password",
                    key=f'unlock_{phase_key}',
                    placeholder="EA-SEC-2026"
                )
                if st.button("🔓 Unlock Expert Solution", key=f'btn_{phase_key}', use_container_width=True):
                    if check_unlock_code(unlock_input):
                        st.session_state.answer_keys_unlocked[phase_key] = True
                        st.success("✅ Expert solution unlocked!")
                        st.rerun()
                    else:
                        st.error("❌ Invalid unlock code")

def display_answer_key_content(phase_key):
    """Display the actual answer key content"""
    if phase_key not in ANSWER_KEYS:
        st.warning("Answer key not available for this exercise")
        return
    
    st.markdown('<div class="answer-key">', unsafe_allow_html=True)
    st.write("### 📖 Expert Solution")
    st.write("---")
    
    answer = ANSWER_KEYS[phase_key]
    
    if phase_key == 'phase1_business_req':
        st.write("#### Scenario: Global E-Commerce Platform")
        
        st.write("**Stakeholder Inputs:**")
        for role, data in answer['stakeholders'].items():
            st.write(f"**{role.upper()}:**")
            if 'input' in data:
                st.info(data['input'])
            if 'concerns' in data:
                for concern in data['concerns']:
                    st.write(f"• {concern}")
            if 'requirements' in data:
                for req in data['requirements']:
                    st.write(f"• {req}")
        
        st.write("---")
        st.write("**Translated Security Requirements:**")
        df_reqs = pd.DataFrame(answer['security_requirements'])
        st.dataframe(df_reqs, use_container_width=True, hide_index=True)
        
        st.write("---")
        st.write("**Key Learning Points:**")
        st.success("""
        ✅ Each stakeholder has different priorities (revenue, risk, cost, delivery)
        ✅ Business requirements are translated to measurable security objectives
        ✅ Every security requirement maps to compliance standard + implementation
        ✅ Success criteria make requirements testable and verifiable
        """)
    
    elif phase_key == 'phase3_hld':
        st.write("**Component Architecture:**")
        df_comp = pd.DataFrame(answer['components'])
        st.dataframe(df_comp, use_container_width=True, hide_index=True)
        
        st.write("---")
        st.write("**Security Zones:**")
        for zone in answer['security_zones']:
            st.write(f"**{zone['name']}** ({zone['trust']})")
            st.write(f"Purpose: {zone['purpose']}")
            st.write(f"Components: {', '.join(zone['components'])}")
            st.write(f"Controls: {zone['controls']}")
            st.write("")
        
        st.write("---")
        st.write("**Data Flows:**")
        df_flow = pd.DataFrame(answer['data_flows'])
        st.dataframe(df_flow, use_container_width=True, hide_index=True)
    
    elif phase_key == 'phase5_stride':
        st.write("**Complete STRIDE Threat Analysis:**")
        df_threats = pd.DataFrame(answer['threats'])
        st.dataframe(df_threats, use_container_width=True, hide_index=True)
        
        st.write("---")
        st.write("**Threat Summary by Category:**")
        threat_counts = {}
        for threat in answer['threats']:
            cat = threat['category']
            threat_counts[cat] = threat_counts.get(cat, 0) + 1
        
        for category, count in threat_counts.items():
            st.write(f"**{category}:** {count} threats identified")
    
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================================
# SIDEBAR NAVIGATION
# ============================================================================

def render_sidebar():
    """Enhanced sidebar navigation"""
    
    with st.sidebar:
        st.markdown("""
        <div style='text-align: center; padding: 1rem 0; border-bottom: 2px solid #e5e7eb; margin-bottom: 1rem;'>
            <h1 style='margin: 0; font-size: 3rem;'>🏛️</h1>
            <h3 style='margin: 0.5rem 0 0 0; color: #1e293b;'>Enterprise Security</h3>
            <p style='margin: 0; color: #64748b; font-size: 0.9rem;'>Architecture Workshop</p>
        </div>
        """, unsafe_allow_html=True)
        
        # User info
        st.write(f"👤 **{st.session_state.user_name}**")
        st.write(f"🏢 {st.session_state.organization}")
        
        st.markdown("---")
        
        # Mode selector
        mode_choice = st.radio(
            "🎓 Learning Mode:",
            ["👨‍🏫 Instructor-Led (with examples)",
             "📚 Self-Learning (independent practice)"],
            key='mode_selector_radio'
        )
        
        if "Instructor" in mode_choice:
            st.session_state.mode = 'instructor_led'
            st.success("✅ Instructor mode: Examples visible")
        else:
            if not st.session_state.self_learning_unlocked:
                st.warning("🔒 Unlock code required")
                unlock_code_input = st.text_input(
                    "Unlock Code:",
                    type="password",
                    key='sidebar_unlock'
                )
                if st.button("🔓 Unlock Self-Learning"):
                    if check_unlock_code(unlock_code_input):
                        st.session_state.self_learning_unlocked = True
                        st.session_state.mode = 'self_learning'
                        st.success("✅ Self-learning unlocked!")
                        st.rerun()
                    else:
                        st.error("❌ Invalid code")
            else:
                st.session_state.mode = 'self_learning'
                st.success("✅ Self-learning mode active")
        
        st.markdown("---")
        
        # Phase navigation
        st.write("### 📍 Workshop Phases")
        
        phases = [
            ("Overview", 0),
            ("Phase 1: Business Requirements", 1),
            ("Phase 2: Security Requirements", 2),
            ("Phase 3: High-Level Design", 3),
            ("Phase 4: ARB & Approvals", 4),
            ("Phase 5: Detailed Design (STRIDE)", 5),
            ("Phase 6: Security Patterns", 6)
        ]
        
        for phase_name, phase_num in phases:
            if phase_num == 0:
                icon = "🏠"
            else:
                icon = "✅" if phase_num in st.session_state.completed_phases else "⏳"
            
            if st.button(f"{icon} {phase_name}", key=f"nav_{phase_num}", use_container_width=True):
                st.session_state.current_phase = phase_num
                st.rerun()
        
        st.markdown("---")
        
        # Progress tracking
        st.write("### 📈 Your Progress")
        
        completed_count = len(st.session_state.completed_phases)
        total_phases = 6
        progress_pct = (completed_count / total_phases) * 100 if total_phases > 0 else 0
        
        st.metric("Phases Complete", f"{completed_count}/{total_phases}")
        st.progress(progress_pct / 100)
        
        artifacts_count = len(st.session_state.artifacts_created)
        st.metric("Artifacts Created", artifacts_count)
        
        st.markdown("---")
        
        # Quick actions
        if st.button("💾 Save Progress", use_container_width=True):
            save_progress()
        
        if completed_count >= 3:
            if st.button("📥 Export Portfolio", use_container_width=True):
                export_portfolio()

def save_progress():
    """Save current progress"""
    progress = {
        'user': st.session_state.user_name,
        'organization': st.session_state.organization,
        'mode': st.session_state.mode,
        'completed_phases': st.session_state.completed_phases,
        'artifacts': st.session_state.artifacts_created,
        'timestamp': datetime.now().isoformat()
    }
    
    progress_json = json.dumps(progress, indent=2)
    st.download_button(
        "📄 Download Progress JSON",
        progress_json,
        f"progress_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
        "application/json"
    )

def export_portfolio():
    """Export complete portfolio"""
    portfolio = {
        'metadata': {
            'user': st.session_state.user_name,
            'organization': st.session_state.organization,
            'export_date': datetime.now().isoformat(),
            'workshop': 'Enterprise Security Architecture'
        },
        'progress': {
            'completed_phases': st.session_state.completed_phases,
            'artifacts_created': st.session_state.artifacts_created
        },
        'artifacts': {
            'security_requirements': st.session_state.security_requirements,
            'hld_components': st.session_state.hld_components,
            'stride_analysis': st.session_state.stride_analysis,
            'security_patterns': st.session_state.security_patterns
        }
    }
    
    portfolio_json = json.dumps(portfolio, indent=2, default=str)
    st.download_button(
        "📦 Download Complete Portfolio",
        portfolio_json,
        f"security_architect_portfolio_{datetime.now().strftime('%Y%m%d')}.json",
        "application/json"
    )

# ============================================================================
# PHASE 1: BUSINESS REQUIREMENTS CAPTURE
# ============================================================================

def render_phase1():
    """Phase 1: Capture business requirements from executives"""
    
    st.markdown("""
    <div class="workshop-header">
        <h1>Phase 1: Business Requirements Capture</h1>
        <p>Learn to gather inputs from executives and stakeholders</p>
        <p style='margin-top: 0.5rem; font-size: 0.95rem;'>⏱️ 60 minutes | 📦 Deliverable: Stakeholder Input Document</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Instructor example
    if st.session_state.mode == 'instructor_led':
        with st.expander("👨‍🏫 INSTRUCTOR EXAMPLE: Financial Services Platform", expanded=True):
            st.markdown("""
            <div class="instructor-example">
            <h3>Scenario: Digital Banking Transformation</h3>
            
            <p>You are the Enterprise Security Architect hired by "GlobalBank" to design security 
            for their new digital banking platform. First step: gather requirements from stakeholders.</p>
            
            <div class="stakeholder-card stakeholder-ceo">
            <h4>👔 CEO Input:</h4>
            <p><em>"We're launching a mobile-first banking platform to compete with fintech startups. 
            Must support checking accounts, savings, instant transfers, bill pay, and personal loans. 
            Target: 2M customers in year 1, 10M in 5 years. Need to go live in 12 months."</em></p>
            <p><strong>Key Priorities:</strong> Customer acquisition, competitive differentiation, revenue growth</p>
            </div>
            
            <div class="stakeholder-card stakeholder-ciso">
            <h4>🛡️ CISO Security Concerns:</h4>
            <ul>
                <li><strong>Regulatory Compliance:</strong> Must meet banking regulations (FFIEC, GLBA, SOX)</li>
                <li><strong>Financial Fraud:</strong> Prevent account takeover, transaction fraud, identity theft</li>
                <li><strong>Data Protection:</strong> Customer PII and financial data must be protected</li>
                <li><strong>Third-Party Risk:</strong> Integrations with credit bureaus, payment networks</li>
                <li><strong>Insider Threat:</strong> Bank employees have access to sensitive customer data</li>
                <li><strong>Availability:</strong> Banking services must be available 24/7 (downtime = revenue loss)</li>
            </ul>
            </div>
            
            <div class="stakeholder-card stakeholder-cto">
            <h4>💻 CTO Technical Requirements:</h4>
            <ul>
                <li><strong>Performance:</strong> Sub-second response time for transactions</li>
                <li><strong>Scalability:</strong> Handle 10M users, 100M transactions/day</li>
                <li><strong>Availability:</strong> 99.99% uptime (52 minutes downtime per year)</li>
                <li><strong>Integration:</strong> Connect to core banking system, payment networks, credit bureaus</li>
                <li><strong>Mobile-first:</strong> iOS and Android apps as primary interface</li>
            </ul>
            </div>
            
            <div class="stakeholder-card stakeholder-cfo">
            <h4>💰 CFO Budget & Constraints:</h4>
            <ul>
                <li><strong>Capital Budget:</strong> $20M for platform development</li>
                <li><strong>Operating Budget:</strong> $5M/year for infrastructure and operations</li>
                <li><strong>ROI Target:</strong> Break even in 3 years</li>
                <li><strong>Risk Management:</strong> Cyber insurance requires specific security controls</li>
            </ul>
            </div>
            
            <div class="mapping-arrow">⬇️ DOCUMENT & SYNTHESIZE ⬇️</div>
            
            <h4>Key Takeaways from Stakeholder Interviews:</h4>
            </div>
            """, unsafe_allow_html=True)
            
            takeaways = pd.DataFrame([
                {
                    'Stakeholder': 'CEO',
                    'Primary Goal': 'Customer acquisition and growth',
                    'Key Metric': '2M customers in year 1',
                    'Timeline': '12 months to launch',
                    'Security Impact': 'Security must not hinder user experience'
                },
                {
                    'Stakeholder': 'CISO',
                    'Primary Goal': 'Regulatory compliance and risk management',
                    'Key Metric': 'Zero regulatory fines, <1% fraud rate',
                    'Timeline': 'Compliance before launch',
                    'Security Impact': 'Security is foundational requirement'
                },
                {
                    'Stakeholder': 'CTO',
                    'Primary Goal': 'Technical excellence and reliability',
                    'Key Metric': '99.99% uptime, <1s latency',
                    'Timeline': '12 months development + testing',
                    'Security Impact': 'Security must not impact performance'
                },
                {
                    'Stakeholder': 'CFO',
                    'Primary Goal': 'Cost control and ROI',
                    'Key Metric': '$20M budget, break even in 3 years',
                    'Timeline': 'Cost tracking from day 1',
                    'Security Impact': 'Security must justify ROI (prevent losses)'
                }
            ])
            
            st.dataframe(takeaways, use_container_width=True, hide_index=True)
            
            st.markdown("""
            <div class="architecture-artifact">
            <h4>📄 Artifact Created: Stakeholder Input Summary</h4>
            <p>This document captures the business context for your security architecture.</p>
            <p><strong>Next Step:</strong> Translate these business needs into security requirements (Phase 2)</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Student exercise
    st.markdown("""
    <div class="student-exercise">
    <h3>🎯 YOUR TURN: Healthcare System</h3>
    <p><strong>Scenario:</strong> You're the Enterprise Security Architect for "HealthCare Plus", 
    a large hospital system launching a patient portal and telemedicine platform.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="requirement-business">
    <h4>Your Task:</h4>
    <p>Conduct stakeholder interviews and document their inputs. Consider:</p>
    <ul>
        <li><strong>CEO:</strong> Strategic goals, growth targets, competitive pressures</li>
        <li><strong>CISO:</strong> Security and privacy concerns, regulatory requirements (HIPAA)</li>
        <li><strong>CTO:</strong> Technical requirements, integration needs, scalability</li>
        <li><strong>CFO:</strong> Budget constraints, ROI expectations, risk tolerance</li>
        <li><strong>CMO (Chief Medical Officer):</strong> Clinical workflow, patient safety, provider adoption</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Interactive stakeholder input form
    st.write("### 📝 Document Stakeholder Inputs")
    
    stakeholder_tabs = st.tabs(["CEO", "CISO", "CTO", "CFO", "CMO"])
    
    with stakeholder_tabs[0]:
        st.write("**CEO Strategic Input:**")
        ceo_input = st.text_area(
            "What are the CEO's business goals and priorities?",
            height=150,
            key='ceo_input',
            placeholder="Example: Launch patient portal to improve patient satisfaction scores and reduce call center volume by 40%..."
        )
    
    with stakeholder_tabs[1]:
        st.write("**CISO Security Concerns:**")
        ciso_concerns = st.text_area(
            "What security and compliance concerns does the CISO have?",
            height=150,
            key='ciso_input',
            placeholder="Example: HIPAA compliance, patient data protection, secure messaging with providers..."
        )
    
    with stakeholder_tabs[2]:
        st.write("**CTO Technical Requirements:**")
        cto_reqs = st.text_area(
            "What are the CTO's technical requirements and constraints?",
            height=150,
            key='cto_input',
            placeholder="Example: Must integrate with Epic EHR, support 500K patients, handle video consultations..."
        )
    
    with stakeholder_tabs[3]:
        st.write("**CFO Budget & ROI:**")
        cfo_budget = st.text_area(
            "What is the CFO's budget and ROI expectations?",
            height=150,
            key='cfo_input',
            placeholder="Example: $10M capital budget, $2M annual operating budget, expect ROI through reduced operational costs..."
        )
    
    with stakeholder_tabs[4]:
        st.write("**CMO Clinical Requirements:**")
        cmo_clinical = st.text_area(
            "What are the Chief Medical Officer's clinical and workflow requirements?",
            height=150,
            key='cmo_input',
            placeholder="Example: Secure provider-patient messaging, prescription refills, lab results access, telemedicine visits..."
        )
    
    # Summary table
    st.write("### 📊 Your Stakeholder Summary")
    
    if any([ceo_input, ciso_concerns, cto_reqs, cfo_budget, cmo_clinical]):
        summary_data = []
        
        if ceo_input:
            summary_data.append({'Stakeholder': 'CEO', 'Input Summary': ceo_input[:100] + '...' if len(ceo_input) > 100 else ceo_input})
        if ciso_concerns:
            summary_data.append({'Stakeholder': 'CISO', 'Input Summary': ciso_concerns[:100] + '...' if len(ciso_concerns) > 100 else ciso_concerns})
        if cto_reqs:
            summary_data.append({'Stakeholder': 'CTO', 'Input Summary': cto_reqs[:100] + '...' if len(cto_reqs) > 100 else cto_reqs})
        if cfo_budget:
            summary_data.append({'Stakeholder': 'CFO', 'Input Summary': cfo_budget[:100] + '...' if len(cfo_budget) > 100 else cfo_budget})
        if cmo_clinical:
            summary_data.append({'Stakeholder': 'CMO', 'Input Summary': cmo_clinical[:100] + '...' if len(cmo_clinical) > 100 else cmo_clinical})
        
        if summary_data:
            df_summary = pd.DataFrame(summary_data)
            st.dataframe(df_summary, use_container_width=True, hide_index=True)
    
    # Action buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("💾 Save Stakeholder Inputs", type="primary", use_container_width=True):
            st.session_state.stakeholder_inputs = {
                'ceo': ceo_input,
                'ciso': ciso_concerns,
                'cto': cto_reqs,
                'cfo': cfo_budget,
                'cmo': cmo_clinical
            }
            st.session_state.artifacts_created.append('Phase1_Stakeholder_Inputs')
            st.success("✅ Stakeholder inputs saved!")
    
    with col2:
        if st.button("🔍 Compare with Expert", use_container_width=True):
            show_answer_key('phase1_business_req')
    
    with col3:
        if st.button("✅ Complete Phase 1", use_container_width=True):
            if 1 not in st.session_state.completed_phases:
                st.session_state.completed_phases.append(1)
            st.balloons()
            st.success("🎉 Phase 1 Complete! Moving to Phase 2...")
            st.session_state.current_phase = 2
            st.rerun()

# ============================================================================
# PHASE 2-6 PLACEHOLDERS (Structure for continuation)
# ============================================================================

def render_phase2():
    """Phase 2: Security Requirements Translation"""
    st.markdown("""
    <div class="workshop-header">
        <h1>Phase 2: Security Requirements Translation</h1>
        <p>Transform business needs into concrete security requirements</p>
    </div>
    """, unsafe_allow_html=True)
    st.info("🚧 Phase 2: Translate business requirements to security requirements with compliance mapping...")

def render_phase3():
    """Phase 3: High-Level Design"""
    st.info("🚧 Phase 3: Component architecture, security zones, data flows, C4 diagrams...")

def render_phase4():
    """Phase 4: ARB & Approvals"""
    st.info("🚧 Phase 4: ARB presentation, stakeholder Q&A, approval workflow...")

def render_phase5():
    """Phase 5: Detailed Design (STRIDE)"""
    st.info("🚧 Phase 5: STRIDE threat modeling, professional diagramming, control mapping...")

def render_phase6():
    """Phase 6: Security Patterns"""
    st.info("🚧 Phase 6: Pattern creation using SecurityPatterns.io methodology...")

# ============================================================================
# OVERVIEW PAGE
# ============================================================================

def render_overview():
    """Workshop overview and introduction"""
    
    st.markdown("""
    <div class="workshop-header">
        <h1>Enterprise Security Architecture Workshop</h1>
        <p>Master the complete end-to-end workflow from requirements to implementation</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("### 🎯 What You'll Learn")
    
    st.write("""
    This workshop teaches you the **complete security architecture workflow** used by Fortune 500 companies:
    
    1. **Gather business requirements** from executives and stakeholders
    2. **Translate** business language to technical security requirements
    3. **Design** high-level architecture with security zones and controls
    4. **Present and defend** your design to Architecture Review Board
    5. **Perform detailed threat modeling** using STRIDE methodology
    6. **Create reusable security patterns** for your organization
    """)
    
    st.write("### 📋 Complete Workflow")
    
    workflow_phases = [
        {
            'phase': 'Phase 1: Business Requirements',
            'duration': '60 min',
            'description': 'Capture inputs from CEO, CISO, CTO, CFO and other stakeholders',
            'deliverable': 'Stakeholder Input Document',
            'skills': 'Stakeholder management, requirement elicitation, business acumen'
        },
        {
            'phase': 'Phase 2: Security Requirements',
            'duration': '60 min',
            'description': 'Translate business needs to security requirements with compliance mapping',
            'deliverable': 'Security Requirements Matrix',
            'skills': 'Requirements engineering, compliance frameworks, risk assessment'
        },
        {
            'phase': 'Phase 3: High-Level Design',
            'duration': '75 min',
            'description': 'Create component architecture with security zones, trust boundaries, data flows',
            'deliverable': 'HLD Document with C4 Diagrams',
            'skills': 'Architecture design, security zoning, data flow modeling'
        },
        {
            'phase': 'Phase 4: ARB & Approvals',
            'duration': '60 min',
            'description': 'Present to Architecture Review Board, defend decisions, obtain approvals',
            'deliverable': 'ARB Presentation & Approval Summary',
            'skills': 'Executive communication, stakeholder management, design defense'
        },
        {
            'phase': 'Phase 5: Detailed Design',
            'duration': '90 min',
            'description': 'STRIDE threat modeling, attack surface analysis, control selection, professional diagramming',
            'deliverable': 'Threat Model & Technical Specifications',
            'skills': 'Threat modeling (STRIDE), diagramming, control mapping'
        },
        {
            'phase': 'Phase 6: Security Patterns',
            'duration': '60 min',
            'description': 'Document reusable security patterns using SecurityPatterns.io methodology',
            'deliverable': 'Security Pattern Library',
            'skills': 'Pattern creation, knowledge management, asset-threat-control mapping'
        }
    ]
    
    for phase_info in workflow_phases:
        st.markdown(f"""
        <div class="phase-card">
        <h3>{phase_info['phase']} <span style='color: #64748b; font-size: 0.9rem;'>({phase_info['duration']})</span></h3>
        <p style='margin: 0.5rem 0;'>{phase_info['description']}</p>
        <p style='margin: 0.5rem 0;'><strong>📦 Deliverable:</strong> {phase_info['deliverable']}</p>
        <p style='margin: 0; color: #64748b; font-size: 0.9rem;'><strong>Skills:</strong> {phase_info['skills']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.write("### 🎓 Learning Approach")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="instructor-example">
        <h4>👨‍🏫 Instructor-Led Mode</h4>
        <ul>
            <li>Complete worked example FIRST</li>
            <li>Step-by-step walkthrough</li>
            <li>Expert commentary and tips</li>
            <li>Then: your turn with similar exercise</li>
            <li>Answer keys always available</li>
        </ul>
        <p><strong>Best for:</strong> First-time learners, classroom training</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="student-exercise">
        <h4>📚 Self-Learning Mode</h4>
        <ul>
            <li>Independent practice exercises</li>
            <li>Try it yourself first</li>
            <li>Locked answer keys (unlock with code)</li>
            <li>Compare your solution to expert</li>
            <li>Iterate and improve</li>
        </ul>
        <p><strong>Best for:</strong> Experienced architects, exam prep</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.write("### 🎯 Who Should Take This Workshop")
    
    st.write("""
    - **Security Architects** designing enterprise security solutions
    - **Enterprise Architects** responsible for security strategy
    - **Solution Architects** needing security architecture skills
    - **Security Engineers** moving into architecture roles
    - **Engineering Managers** overseeing security teams
    - **Consultants** advising clients on security architecture
    """)
    
    st.write("### 📊 What You'll Build")
    
    st.success("""
    By the end of this workshop, you'll have created a **complete security architecture portfolio**:
    
    ✅ Stakeholder input document  
    ✅ Security requirements matrix with compliance mapping  
    ✅ High-level design with C4 diagrams  
    ✅ Architecture Review Board presentation  
    ✅ Complete STRIDE threat model  
    ✅ Professional architecture diagrams  
    ✅ Reusable security pattern library  
    
    **This portfolio demonstrates real enterprise security architecture skills.**
    """)
    
    if st.button("🚀 Start Workshop", type="primary", use_container_width=True):
        st.session_state.current_phase = 1
        st.rerun()

# ============================================================================
# MAIN APPLICATION ROUTER
# ============================================================================

def main():
    """Main application entry point"""
    
    render_sidebar()
    
    # Route to appropriate phase
    phase = st.session_state.current_phase
    
    if phase == 0:
        render_overview()
    elif phase == 1:
        render_phase1()
    elif phase == 2:
        render_phase2()
    elif phase == 3:
        render_phase3()
    elif phase == 4:
        render_phase4()
    elif phase == 5:
        render_phase5()
    elif phase == 6:
        render_phase6()
    else:
        render_overview()

if __name__ == "__main__":
    main()
