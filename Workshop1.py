"""
Security Architecture Design Studio
Hands-on tool to learn HOW to design real security architectures.

Run with:
    pip install streamlit
    streamlit run security_arch_designer.py
"""

import streamlit as st
import json
import re
from datetime import datetime

# ─────────────────────────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Security Architecture Design Studio",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────
#  GLOBAL CSS
# ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&family=Inter:wght@400;500;600;700;800&display=swap');

.stApp { background: #0b0f1a !important; font-family: 'Inter', sans-serif; }
section[data-testid="stSidebar"] { background: #0d1220 !important; border-right: 1px solid #1f2d45; }
.block-container { padding: 1.5rem 2rem !important; max-width: 1400px; }
h1, h2, h3 { font-family: 'Inter', sans-serif !important; color: #f1f5f9 !important; }
label { color: #94a3b8 !important; font-size: 0.82rem !important; font-weight: 600 !important; }

.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div { background: #1a2236 !important; border: 1px solid #1f2d45 !important; color: #f1f5f9 !important; border-radius: 8px !important; }

.stButton > button { background: linear-gradient(135deg, #1d4ed8, #2563eb) !important; color: white !important; border: none !important; border-radius: 8px !important; font-weight: 600 !important; }

.stTabs [data-baseweb="tab-list"] { background: #111827 !important; border-radius: 10px !important; padding: 4px !important; border: 1px solid #1f2d45 !important; }
.stTabs [data-baseweb="tab"] { background: transparent !important; color: #475569 !important; border-radius: 8px !important; font-weight: 600 !important; font-size: 0.82rem !important; }
.stTabs [aria-selected="true"] { background: #3b82f6 !important; color: white !important; }

[data-testid="metric-container"] { background: #111827 !important; border: 1px solid #1f2d45 !important; border-radius: 10px !important; padding: 1rem !important; }

.card { background: #111827; border: 1px solid #1f2d45; border-radius: 12px; padding: 1.25rem 1.5rem; margin-bottom: 1rem; }
.card-blue  { border-left: 3px solid #3b82f6; }
.card-green { border-left: 3px solid #10b981; }
.card-amber { border-left: 3px solid #f59e0b; }
.card-red   { border-left: 3px solid #ef4444; }
.card-purple{ border-left: 3px solid #8b5cf6; }

.badge { display:inline-block; padding:2px 10px; border-radius:20px; font-size:0.7rem; font-weight:700; text-transform:uppercase; letter-spacing:0.05em; margin-right:4px; margin-bottom:4px; }
.badge-blue   { background:rgba(59,130,246,0.15); color:#60a5fa; border:1px solid rgba(59,130,246,0.3); }
.badge-green  { background:rgba(16,185,129,0.15); color:#34d399; border:1px solid rgba(16,185,129,0.3); }
.badge-red    { background:rgba(239,68,68,0.15);  color:#f87171; border:1px solid rgba(239,68,68,0.3); }
.badge-amber  { background:rgba(245,158,11,0.15); color:#fbbf24; border:1px solid rgba(245,158,11,0.3); }
.badge-purple { background:rgba(139,92,246,0.15); color:#a78bfa; border:1px solid rgba(139,92,246,0.3); }

.slabel { font-size:0.65rem; font-weight:700; letter-spacing:0.1em; text-transform:uppercase; color:#475569; margin-bottom:0.5rem; }
.mono { font-family:'JetBrains Mono',monospace; font-size:0.78rem; line-height:1.7; color:#94a3b8; background:#0a0e1a; border:1px solid #1f2d45; border-radius:10px; padding:1.25rem; white-space:pre; overflow-x:auto; }

::-webkit-scrollbar { width:6px; } ::-webkit-scrollbar-track { background:#0b0f1a; } ::-webkit-scrollbar-thumb { background:#1f2d45; border-radius:3px; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────
#  DATA: ZONES
# ─────────────────────────────────────────────────────────────────
ZONES = {
    "Internet Zone": {
        "trust": 0, "emoji": "🔴",
        "desc": "Fully untrusted. Everything here is hostile. You have zero control over traffic originating here.",
        "controls": ["NGFW / Packet Filter", "DDoS Protection", "BGP Filtering", "Geo-blocking"],
        "assets": ["External Users", "Internet Traffic", "Public DNS", "CDN Edge"],
    },
    "DMZ (Perimeter Zone)": {
        "trust": 1, "emoji": "🟠",
        "desc": "Semi-trusted buffer. Public-facing services live here. No direct path to internal zones.",
        "controls": ["Reverse Proxy", "WAF", "IDS/IPS", "TLS Termination", "Load Balancer"],
        "assets": ["Web Servers", "API Gateway", "Email Gateway", "Jump / Bastion Host"],
    },
    "Application Zone": {
        "trust": 2, "emoji": "🟡",
        "desc": "Business logic layer. Only reachable via DMZ. No direct internet access.",
        "controls": ["Internal Firewall", "mTLS", "Service Mesh", "App-layer AuthZ"],
        "assets": ["App Servers", "Microservices", "Message Queues", "Cache Layer"],
    },
    "Data Zone": {
        "trust": 3, "emoji": "🟢",
        "desc": "Highest sensitivity. Databases and secrets. Strictly controlled, heavily monitored.",
        "controls": ["DB Firewall", "Encryption at Rest", "PAM", "Audit Logging", "DLP"],
        "assets": ["Databases", "Data Warehouses", "Key Management (KMS/HSM)", "Secrets Vault"],
    },
    "Management Zone": {
        "trust": 4, "emoji": "🔵",
        "desc": "Out-of-band admin network. Only privileged users via hardened access paths. Never reachable from app zone.",
        "controls": ["MFA", "PAM + Session Recording", "JIT Access", "Bastion Host", "Immutable Audit Logs"],
        "assets": ["Admin Consoles", "SIEM / SOAR", "Config Management", "Monitoring Tools"],
    },
}

# ─────────────────────────────────────────────────────────────────
#  DATA: CONTROL LIBRARY
# ─────────────────────────────────────────────────────────────────
CONTROLS = {
    "Identity & Access": {
        "MFA (Multi-Factor Authentication)":        {"blocks": ["Credential Theft", "Phishing", "Password Spray"],       "zones": ["All Zones"],                                     "effort": "Low"},
        "SSO (Single Sign-On)":                     {"blocks": ["Password Sprawl", "Credential Reuse"],                   "zones": ["Application Zone"],                              "effort": "Medium"},
        "PAM (Privileged Access Management)":       {"blocks": ["Privilege Escalation", "Insider Threat"],               "zones": ["Management Zone", "Data Zone"],                  "effort": "High"},
        "JIT Access (Just-in-Time)":                {"blocks": ["Standing Privilege Abuse", "Privilege Persistence"],    "zones": ["Management Zone"],                               "effort": "High"},
        "RBAC (Role-Based Access Control)":         {"blocks": ["Excessive Permissions", "Horizontal Privilege Escalation"], "zones": ["Application Zone", "Data Zone"],             "effort": "Medium"},
        "Zero Standing Privileges":                 {"blocks": ["Lateral Movement", "Insider Threat"],                   "zones": ["All Zones"],                                     "effort": "High"},
        "Certificate-Based Auth (mTLS)":            {"blocks": ["Service Impersonation", "MITM between services"],       "zones": ["Application Zone", "DMZ (Perimeter Zone)"],      "effort": "Medium"},
    },
    "Network Security": {
        "Next-Gen Firewall (NGFW)":                 {"blocks": ["Unauthorized Access", "C2 Traffic", "Port Scanning"],   "zones": ["DMZ (Perimeter Zone)", "Application Zone"],      "effort": "Medium"},
        "Micro-segmentation":                       {"blocks": ["Lateral Movement", "East-West Attack"],                 "zones": ["Application Zone", "Data Zone"],                 "effort": "High"},
        "WAF (Web Application Firewall)":           {"blocks": ["SQLi", "XSS", "OWASP Top 10", "API Abuse"],            "zones": ["DMZ (Perimeter Zone)"],                          "effort": "Low"},
        "IDS/IPS":                                  {"blocks": ["Known Exploits", "Anomalous Scanning", "C2 Traffic"],   "zones": ["DMZ (Perimeter Zone)", "Application Zone"],      "effort": "Medium"},
        "Network ACLs":                             {"blocks": ["Unauthorized Lateral Movement"],                        "zones": ["All Zones"],                                     "effort": "Low"},
        "VPN / ZTNA":                               {"blocks": ["Unauthorized Remote Access", "Exposed Services"],      "zones": ["Internet Zone"],                                 "effort": "Medium"},
        "DNS Filtering / RPZ":                      {"blocks": ["C2 over DNS", "Malware Callbacks", "Phishing Domains"], "zones": ["Internet Zone", "DMZ (Perimeter Zone)"],         "effort": "Low"},
    },
    "Data Protection": {
        "Encryption at Rest (AES-256)":             {"blocks": ["Data Theft from Storage", "Backup Theft"],              "zones": ["Data Zone"],                                     "effort": "Low"},
        "Encryption in Transit (TLS 1.3)":          {"blocks": ["Eavesdropping", "MITM", "Network Sniffing"],            "zones": ["All Zones"],                                     "effort": "Low"},
        "Tokenization":                             {"blocks": ["PAN Data Exposure", "PCI Scope Creep"],                 "zones": ["Application Zone", "Data Zone"],                 "effort": "High"},
        "DLP (Data Loss Prevention)":               {"blocks": ["Data Exfiltration", "Accidental Disclosure"],           "zones": ["Application Zone", "Internet Zone"],             "effort": "High"},
        "Database Encryption (TDE)":                {"blocks": ["Physical Theft", "Raw Disk Access"],                   "zones": ["Data Zone"],                                     "effort": "Low"},
        "Key Management (HSM/KMS)":                 {"blocks": ["Key Theft", "Crypto Weakness"],                        "zones": ["Data Zone", "Management Zone"],                  "effort": "Medium"},
        "Data Masking":                             {"blocks": ["Dev/Test Data Exposure", "Insider View of PII"],       "zones": ["Application Zone", "Data Zone"],                 "effort": "Medium"},
    },
    "Detection & Response": {
        "SIEM":                                     {"blocks": ["Undetected Breaches", "Slow Response"],                 "zones": ["Management Zone"],                               "effort": "High"},
        "EDR (Endpoint Detection & Response)":      {"blocks": ["Malware", "Ransomware", "Fileless Attack"],             "zones": ["Application Zone"],                              "effort": "Medium"},
        "SOAR (Security Orchestration)":            {"blocks": ["Slow Manual Response"],                                 "zones": ["Management Zone"],                               "effort": "High"},
        "Log Aggregation & UEBA":                   {"blocks": ["Insider Threat", "Anomalous Behavior"],                 "zones": ["Management Zone"],                               "effort": "Medium"},
        "Honeypots / Deception":                    {"blocks": ["Internal Recon", "Lateral Movement"],                  "zones": ["Application Zone", "Data Zone"],                 "effort": "Medium"},
        "Threat Intelligence Feed":                 {"blocks": ["Known IOCs", "Emerging Threat Actors"],                 "zones": ["Management Zone"],                               "effort": "Low"},
        "Cloud Security Posture Mgmt (CSPM)":       {"blocks": ["Cloud Misconfigurations", "Exposed Storage Buckets"],  "zones": ["Management Zone"],                               "effort": "Low"},
    },
    "Application Security": {
        "API Gateway with Rate Limiting":           {"blocks": ["API Abuse", "DDoS on APIs", "Credential Stuffing"],    "zones": ["DMZ (Perimeter Zone)"],                          "effort": "Low"},
        "Input Validation & Sanitization":          {"blocks": ["SQLi", "XSS", "Command Injection"],                    "zones": ["Application Zone"],                              "effort": "Low"},
        "Secrets Management (Vault)":               {"blocks": ["Hardcoded Credentials", "Secret Sprawl"],              "zones": ["Application Zone", "Data Zone"],                 "effort": "Medium"},
        "SBOM & Dependency Scanning":               {"blocks": ["Supply Chain Attack", "Known Vulnerable Libraries"],   "zones": ["Application Zone"],                              "effort": "Low"},
        "Container Security (Runtime)":             {"blocks": ["Container Escape", "Privilege Escalation in Pods"],    "zones": ["Application Zone"],                              "effort": "Medium"},
        "CSP (Content Security Policy)":            {"blocks": ["XSS", "Clickjacking", "Data Injection"],               "zones": ["DMZ (Perimeter Zone)"],                          "effort": "Low"},
        "RASP (Runtime App Self-Protection)":       {"blocks": ["Zero-Day Exploits", "Unknown Attack Patterns"],        "zones": ["Application Zone"],                              "effort": "High"},
    },
}

# ─────────────────────────────────────────────────────────────────
#  DATA: ATTACK SCENARIOS
# ─────────────────────────────────────────────────────────────────
ATTACKS = {
    "External Attacker — Web App Breach": {
        "goal": "Exfiltrate customer database",
        "stages": [
            ("Internet Zone",        "Recon",               "Scan public assets, identify web tech stack via HTTP headers, scrape for employee emails"),
            ("DMZ (Perimeter Zone)", "Initial Access",      "SQLi via vulnerable login form; WAF bypass using double-encoding technique"),
            ("Application Zone",     "Lateral Movement",    "Pivot from web server to app server via unprotected internal API call"),
            ("Data Zone",            "Exfiltration",        "Dump customer table via app-layer DB connection. Exfil via HTTPS to attacker-controlled server"),
        ],
        "blocking_controls": {"WAF (Web Application Firewall)": ["DMZ (Perimeter Zone)"], "Input Validation & Sanitization": ["Application Zone"],
                              "Micro-segmentation": ["Application Zone"], "DLP (Data Loss Prevention)": ["Application Zone"],
                              "Encryption in Transit (TLS 1.3)": ["All Zones"]},
    },
    "Phishing → Ransomware": {
        "goal": "Encrypt all data, demand ransom",
        "stages": [
            ("Internet Zone",        "Delivery",            "Spear phishing email with malicious Office macro attachment sent to finance team"),
            ("Application Zone",     "Execution",           "User opens attachment; macro executes PowerShell, downloads loader from C2 via HTTPS"),
            ("Application Zone",     "Lateral Movement",    "Credential dumping via LSASS; Pass-the-Hash to pivot to other workstations and file servers"),
            ("Data Zone",            "Impact",              "Encrypt file shares, databases, and detected backup systems. Delete VSS shadow copies"),
        ],
        "blocking_controls": {"MFA (Multi-Factor Authentication)": ["All Zones"], "EDR (Endpoint Detection & Response)": ["Application Zone"],
                              "SIEM": ["Management Zone"], "Micro-segmentation": ["Application Zone"],
                              "DNS Filtering / RPZ": ["Internet Zone"]},
    },
    "Insider Threat — Privileged User Data Theft": {
        "goal": "Exfiltrate IP to sell to competitor",
        "stages": [
            ("Management Zone",      "Internal Recon",      "Admin uses existing PAM session to browse database schemas and identify high-value tables"),
            ("Data Zone",            "Collection",          "Bulk export of customer and IP data using standing DB admin privileges to local CSV"),
            ("Application Zone",     "Staging",             "Copy files to personal laptop via USB / unapproved cloud sync tool"),
            ("Internet Zone",        "Exfiltration",        "Upload staged files to personal Google Drive over corporate network during lunch"),
        ],
        "blocking_controls": {"PAM (Privileged Access Management)": ["Management Zone", "Data Zone"], "JIT Access (Just-in-Time)": ["Management Zone"],
                              "Log Aggregation & UEBA": ["Management Zone"], "DLP (Data Loss Prevention)": ["Application Zone", "Internet Zone"],
                              "Zero Standing Privileges": ["All Zones"]},
    },
    "Supply Chain Compromise (SolarWinds-style)": {
        "goal": "Persistent silent espionage across multiple organizations",
        "stages": [
            ("Application Zone",     "Initial Compromise",  "Trojanized build of a trusted software update deployed to production (signed, legitimate-looking)"),
            ("Application Zone",     "Persistence",         "Backdoor beacons to C2 over HTTPS with randomized delays to evade detection"),
            ("Management Zone",      "Privilege Escalation","Use initial foothold to harvest service account credentials with high privileges"),
            ("Data Zone",            "Collection/Exfil",    "Exfiltrate sensitive data via encrypted DNS tunneling or slow HTTPS upload to appear as normal traffic"),
        ],
        "blocking_controls": {"SBOM & Dependency Scanning": ["Application Zone"], "SIEM": ["Management Zone"],
                              "DNS Filtering / RPZ": ["Internet Zone"], "EDR (Endpoint Detection & Response)": ["Application Zone"],
                              "Secrets Management (Vault)": ["Application Zone", "Data Zone"]},
    },
}

# ─────────────────────────────────────────────────────────────────
#  DATA: DESIGN SCENARIOS
# ─────────────────────────────────────────────────────────────────
SCENARIOS = {
    "Healthcare SaaS (PHI / HIPAA)": {
        "desc": "Cloud-based EHR platform storing patient health records for 200 hospitals. Used by 50,000 clinicians daily.",
        "data": "PHI (Protected Health Information) — medical records, lab results, prescriptions, diagnoses",
        "users": "Clinicians, Nurses, Patients (portal), Admins — via web browser and mobile app",
        "platform": "AWS Multi-region (us-east-1, eu-west-1)",
        "compliance": ["HIPAA", "HITRUST CSF", "SOC 2 Type II"],
        "key_risks": ["Unauthorised access to PHI", "Data breach / mass exfiltration", "Ransomware disrupting care", "Insider data theft by clinicians"],
        "crown_jewel": "Patient health records database — PHI is the most sensitive asset. Breach = regulatory fines + patient harm.",
    },
    "Fintech Payment Platform (PCI-DSS)": {
        "desc": "Payment processing API handling card transactions for 5,000 merchants. 10M transactions/day.",
        "data": "PAN (card numbers), CVV, transaction records — must be tokenised. Never store raw card data.",
        "users": "Merchants via API keys, internal ops team, compliance team",
        "platform": "GCP + On-prem HSM for key storage",
        "compliance": ["PCI-DSS Level 1", "SOX", "GDPR"],
        "key_risks": ["Card data theft", "Transaction fraud / replay", "API key compromise", "Audit failure / PCI de-certification"],
        "crown_jewel": "Cardholder data environment (CDE) — card numbers in any unencrypted form. Compromise = immediate PCI de-cert.",
    },
    "Enterprise B2B SaaS (ISO 27001)": {
        "desc": "CRM platform storing confidential sales data for 50 Fortune 500 enterprise customers.",
        "data": "Customer PII, deal pipeline data, revenue forecasts — customer-classified as Confidential/Restricted",
        "users": "Sales teams across 50 enterprise customers — SSO via SAML 2.0 federated to customer IdPs",
        "platform": "Azure (multi-tenant, single deployment)",
        "compliance": ["SOC 2 Type II", "ISO 27001", "GDPR", "Customer contractual obligations"],
        "key_risks": ["Cross-tenant data isolation failure", "Account takeover via SSO misconfiguration", "API key/token theft", "Bulk exfiltration via reporting features"],
        "crown_jewel": "Tenant data isolation — if Customer A can see Customer B's data, the product is finished.",
    },
    "Custom Scenario (Build Your Own)": {
        "desc": "", "data": "", "users": "", "platform": "",
        "compliance": [], "key_risks": [], "crown_jewel": "",
    },
}

# ─────────────────────────────────────────────────────────────────
#  DATA: ARCHITECTURE PATTERNS
# ─────────────────────────────────────────────────────────────────
PATTERNS = {
    "Zero Trust Network Architecture": {
        "problem": "Traditional perimeter security trusts anything inside the network. Once an attacker breaches the perimeter via phishing or VPN exploit, they move freely to any internal system.",
        "solution": "Every access request — regardless of network location — is fully authenticated, authorised, and continuously re-validated. There is no implicit trust anywhere.",
        "when": "Remote workforce, cloud-first architectures, when internal network trust is no longer meaningful (it rarely is).",
        "components": [
            ("Identity Provider (IdP)", "Authenticates every user and device. No anonymous connections permitted."),
            ("Policy Engine", "Evaluates every access request: user identity + device health + location + time + behaviour."),
            ("Policy Enforcement Point (PEP)", "Gateway that enforces the policy engine's allow/deny decision."),
            ("Micro-segmentation", "Workloads can only reach explicitly permitted destinations — limits blast radius."),
            ("Continuous Validation", "Sessions re-evaluated continuously. Anomalous behaviour triggers step-up auth."),
        ],
        "diagram": """\
 ┌───────────────────────────────────────────────────────┐
 │              ZERO TRUST ARCHITECTURE                  │
 └───────────────────────────────────────────────────────┘

   User / Device            Trust Broker              Resource
   ─────────────        ─────────────────────        ──────────
   [Browser]  ──────►  │ 1. Authenticate (IdP) │ ──► [App A]
   [Mobile ]           │ 2. Check device health│     [App B]
   [Service]           │ 3. Evaluate policy    │     [DB   ]
                       │ 4. Enforce (PEP)      │     [API  ]
                       │ 5. Log every access   │
                       └──────────────────────┘
          │                      │                     │
          └──── Continuous validation ◄── re-check ───┘
                 on every request / behaviour change

   PRINCIPLE: "Never trust, always verify"
   No network location grants implicit access — ever.""",
    },
    "Defense in Depth (Layered Security)": {
        "problem": "No single control is perfect. Controls fail via misconfiguration, zero-days, or human error. One failed control = total compromise in a flat model.",
        "solution": "Independent security controls at every layer. An attacker must defeat ALL layers in sequence. Each layer buys detection time.",
        "when": "Always. This is a universal principle applied to every architecture, not a specific technology choice.",
        "components": [
            ("Perimeter Controls", "NGFW, WAF, DDoS — outermost layer blocking known-bad traffic."),
            ("Network Controls", "Segmentation, IDS/IPS, ACLs — limit movement once perimeter is breached."),
            ("Endpoint Controls", "EDR, disk encryption — protect the device even if network controls fail."),
            ("Application Controls", "Input validation, RBAC, API gateway — block app-layer attacks."),
            ("Data Controls", "Encryption, DLP, tokenisation — last line; data useless even if everything else fails."),
        ],
        "diagram": """\
 ┌───────────────────────────────────────────────────────┐
 │              DEFENSE IN DEPTH                         │
 └───────────────────────────────────────────────────────┘

   INTERNET
       │
   ╔══════════════════╗  L1 PERIMETER  → Blocks: DDoS, known attacks
   ║  NGFW + WAF      ║
   ╚══════════════════╝
       │
   ╔══════════════════╗  L2 NETWORK    → Blocks: Lateral movement
   ║  Segmentation    ║
   ║  IDS / IPS       ║
   ╚══════════════════╝
       │
   ╔══════════════════╗  L3 APPLICATION → Blocks: Injection, AuthZ
   ║  AuthN + AuthZ   ║
   ║  Input Validation║
   ╚══════════════════╝
       │
   ╔══════════════════╗  L4 DATA        → Blocks: Theft even if above fails
   ║  Encryption      ║
   ║  DLP / Tokens    ║
   ╚══════════════════╝

   Attacker must defeat EVERY layer — each layer = detection opportunity.""",
    },
    "Secure API Gateway Pattern": {
        "problem": "APIs are the primary modern attack surface. Each microservice implementing its own security creates inconsistency and coverage gaps.",
        "solution": "All API traffic routes through a centralised gateway that handles auth, authorisation, rate limiting, and input validation before reaching any backend.",
        "when": "Any microservices architecture, public-facing APIs, mobile backends, B2B integrations — essentially all modern applications.",
        "components": [
            ("API Gateway", "Single entry point. Handles all cross-cutting security centrally — consistency guaranteed."),
            ("OAuth 2.0 / JWT", "Token-based, stateless auth — works for users, services, and machine-to-machine."),
            ("Rate Limiting", "Per-client limits prevent brute force, credential stuffing, and API DDoS."),
            ("Request Schema Validation", "Reject malformed/unexpected inputs at the gateway — never reach the app."),
            ("Mutual TLS (mTLS) to backends", "Gateway-to-service communication is authenticated — no service can be called directly."),
        ],
        "diagram": """\
 ┌───────────────────────────────────────────────────────┐
 │              SECURE API GATEWAY PATTERN               │
 └───────────────────────────────────────────────────────┘

   Clients                API Gateway              Services
   ────────              ─────────────────        ──────────
   Mobile  ─┐
   Web     ─┤──► ┌──────────────────────┐ ──mTLS──► Svc A
   Partner ─┤    │ 1. Authenticate      │           Svc B
   3rd Party┘    │    (OAuth2 / OIDC)   │ ──mTLS──► Svc C
                 │ 2. Authorise (RBAC)  │           Svc D
                 │ 3. Rate Limit        │
                 │ 4. Validate Schema   │
                 │ 5. Audit Log         │
                 └──────────────────────┘
                         │
                   [No direct access
                    to services from
                    outside gateway]""",
    },
    "Identity-Centric Security Architecture": {
        "problem": "Network perimeter is dissolving — cloud, remote work, BYOD. Network location no longer determines trust. Credentials are the new attack target.",
        "solution": "Identity is the primary control plane. Every access decision is based on verified identity, device health, and behavioural context — not network location.",
        "when": "Cloud-first architectures, remote workforce, SaaS-heavy environments. Especially critical with sensitive data or compliance requirements.",
        "components": [
            ("Identity Provider (IdP)", "Central source of truth for all identities — users, devices, services."),
            ("MFA / Passwordless", "Eliminates ~99% of credential-based compromise. Second factor or hardware key."),
            ("SSO (Single Sign-On)", "One identity across all apps — enables centralised policy enforcement and visibility."),
            ("PAM (Privileged Access Management)", "Separate, hardened pathway for admin access. Recorded sessions, time-limited."),
            ("UEBA", "Baseline normal behaviour. Alert on: bulk downloads, off-hours access, unusual source locations."),
        ],
        "diagram": """\
 ┌───────────────────────────────────────────────────────┐
 │            IDENTITY-CENTRIC ARCHITECTURE              │
 └───────────────────────────────────────────────────────┘

   Standard User            Privileged Admin
        │                          │
   [MFA + SSO]             [MFA + PAM]
        │                  [JIT — time-limited]
        │                  [Full session recording]
        ▼                          ▼
   ┌───────────────────────────────────┐
   │       IDENTITY PROVIDER (IdP)     │
   │  ┌──────────┐  ┌───────────────┐  │
   │  │  AuthN   │  │     AuthZ     │  │
   │  │ (Who?)   │  │  (What can?)  │  │
   │  └──────────┘  └───────────────┘  │
   │  ┌──────────────────────────────┐  │
   │  │    UEBA — Is this normal?   │  │
   │  └──────────────────────────────┘  │
   └───────────────┬───────────────────┘
                   │  Token / session
              ┌────▼────┐
              │Resources│
              └─────────┘""",
    },
}


# ─────────────────────────────────────────────────────────────────
#  SESSION STATE
# ─────────────────────────────────────────────────────────────────
def init():
    defaults = {
        "scenario": "Healthcare SaaS (PHI / HIPAA)",
        "selected_zones": ["Internet Zone", "DMZ (Perimeter Zone)", "Application Zone", "Data Zone"],
        "controls_by_zone": {},
        "data_flows": [],
        "arch_notes": "",
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v
    # Ensure each zone has a list in controls_by_zone
    for z in st.session_state["selected_zones"]:
        if z not in st.session_state["controls_by_zone"]:
            st.session_state["controls_by_zone"][z] = []

init()


# ─────────────────────────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────────────────────────
def all_controls_flat():
    result = []
    for cl in st.session_state["controls_by_zone"].values():
        result.extend(cl)
    return result

def coverage_score():
    flat = set(all_controls_flat())
    cats_hit = 0
    for cat, items in CONTROLS.items():
        if any(c in items for c in flat):
            cats_hit += 1
    cat_score  = (cats_hit / len(CONTROLS)) * 50
    count_score = min(len(flat) / 15 * 50, 50)
    return round(cat_score + count_score)

def render_diagram():
    zones_sel = st.session_state["selected_zones"]
    cbz = st.session_state["controls_by_zone"]
    if not zones_sel:
        return "No zones defined yet."
    lines = ["┌───────────────────────────────────────────────────────┐",
             "│         SECURITY ARCHITECTURE  —  ZONE DIAGRAM        │",
             "└───────────────────────────────────────────────────────┘", ""]
    for i, z in enumerate(zones_sel):
        info = ZONES[z]
        ctrls = cbz.get(z, [])
        ctrl_str = " | ".join(ctrls[:3])
        if len(ctrls) > 3:
            ctrl_str += f"  +{len(ctrls)-3} more"
        if not ctrls:
            ctrl_str = "⚠ NO CONTROLS ASSIGNED"
        trust_bar = "█" * (info["trust"] + 1) + "░" * (4 - info["trust"])
        lines += [
            "╔══════════════════════════════════════════════════════╗",
            f"║  {info['emoji']}  {z:<46} ║",
            f"║     Trust [{trust_bar}]                                  ║",
            f"║     {ctrl_str[:52]:<52} ║",
            "╚══════════════════════════════════════════════════════╝",
        ]
        if i < len(zones_sel) - 1:
            lines += ["                │   ▼  (firewall / boundary control)"]
    return "\n".join(lines)

def gap_analysis():
    flat = set(all_controls_flat())
    zones = st.session_state["selected_zones"]
    gaps = []
    if "MFA (Multi-Factor Authentication)" not in flat:
        gaps.append(("🔴 CRITICAL", "No MFA anywhere. All accounts are one stolen password from compromise.",
                     "Add MFA to every user-facing auth point. Start with privileged accounts."))
    if "Encryption at Rest (AES-256)" not in flat and "Data Zone" in zones:
        gaps.append(("🔴 CRITICAL", "Data Zone present but no encryption at rest. Stolen disk = stolen data.",
                     "Enable AES-256 encryption at rest on all Data Zone storage. Use KMS/HSM for keys."))
    if "SIEM" not in flat:
        gaps.append(("🔴 CRITICAL", "No SIEM. You're architecturally blind — breaches go undetected for months.",
                     "Deploy SIEM. Aggregate logs from every zone boundary and critical system."))
    if "WAF (Web Application Firewall)" not in flat and "DMZ (Perimeter Zone)" in zones:
        gaps.append(("🟡 HIGH", "DMZ without WAF. OWASP Top 10 web attacks (SQLi, XSS) are completely unmitigated.",
                     "Place WAF at DMZ ingress, in front of all public-facing services."))
    if "PAM (Privileged Access Management)" not in flat and "Management Zone" in zones:
        gaps.append(("🟡 HIGH", "Management Zone without PAM. Privileged access is unrecorded and uncontrolled.",
                     "Implement PAM with session recording for all admin access to management-zone systems."))
    if "Micro-segmentation" not in flat and "Application Zone" in zones:
        gaps.append(("🟠 MEDIUM", "Application Zone without micro-segmentation. Compromised app server reaches all peers.",
                     "Implement micro-segmentation to limit east-west movement within the Application Zone."))
    if "Encryption in Transit (TLS 1.3)" not in flat:
        gaps.append(("🟠 MEDIUM", "No TLS in transit. Traffic between zones can be intercepted.",
                     "Enforce TLS 1.3 on all inter-zone connections. Use mTLS for service-to-service."))
    if not st.session_state["data_flows"]:
        gaps.append(("🔵 INFO", "No data flows documented. Unknown flows = unknown attack paths.",
                     "Document all data flows, especially those crossing zone boundaries."))
    return gaps

def generate_doc():
    scenario = st.session_state["scenario"]
    sinfo    = SCENARIOS.get(scenario, {})
    zones    = st.session_state["selected_zones"]
    cbz      = st.session_state["controls_by_zone"]
    flows    = st.session_state["data_flows"]
    notes    = st.session_state["arch_notes"]
    score    = coverage_score()
    now      = datetime.now().strftime("%Y-%m-%d %H:%M")
    flat     = list(set(all_controls_flat()))

    doc = f"""# SECURITY ARCHITECTURE DESIGN DOCUMENT
**Scenario:** {scenario}
**Generated:** {now}
**Coverage Score:** {score}/100

---

## 1. SYSTEM OVERVIEW
{sinfo.get('desc','—')}

| Field | Detail |
|-------|--------|
| Data in Scope | {sinfo.get('data','—')} |
| Users | {sinfo.get('users','—')} |
| Platform | {sinfo.get('platform','—')} |
| Compliance | {', '.join(sinfo.get('compliance',[])) or '—'} |
| Crown Jewel | {sinfo.get('crown_jewel','—')} |

---

## 2. ARCHITECTURE DIAGRAM
```
{render_diagram()}
```

---

## 3. SECURITY ZONES
"""
    for z in zones:
        zinfo = ZONES[z]
        ctrls = cbz.get(z, [])
        doc += f"""
### {zinfo['emoji']} {z}
- **Trust Level:** {zinfo['trust']}/4
- **Purpose:** {zinfo['desc']}
- **Controls Applied:** {', '.join(ctrls) if ctrls else '⚠️ None assigned'}
"""

    doc += "\n---\n\n## 4. SECURITY CONTROLS\n"
    for cat, items in CONTROLS.items():
        cat_ctrls = [c for c in flat if c in items]
        if cat_ctrls:
            doc += f"\n**{cat}**\n"
            for c in cat_ctrls:
                info = items[c]
                doc += f"- **{c}** — Blocks: {', '.join(info['blocks'])}\n"

    doc += "\n---\n\n## 5. DATA FLOWS\n"
    if flows:
        for i, f in enumerate(flows, 1):
            doc += f"{i}. {f}\n"
    else:
        doc += "_No data flows documented._\n"

    doc += "\n---\n\n## 6. GAP ANALYSIS\n"
    gaps = gap_analysis()
    if not gaps:
        doc += "No critical gaps detected.\n"
    else:
        for sev, issue, fix in gaps:
            doc += f"\n**{sev}** — {issue}\n→ Fix: {fix}\n"

    if notes:
        doc += f"\n---\n\n## 7. ARCHITECT'S NOTES\n{notes}\n"

    doc += f"\n---\n*Generated by Security Architecture Design Studio*\n"
    return doc


# ─────────────────────────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding:1rem 0 0.25rem'>
      <div style='font-size:0.6rem;font-weight:700;letter-spacing:0.15em;color:#475569;text-transform:uppercase;margin-bottom:0.35rem'>
        Hands-On Tool
      </div>
      <div style='font-size:1.3rem;font-weight:800;color:#f1f5f9;line-height:1.2'>
        🏛️ Arch Designer
      </div>
      <div style='font-size:0.75rem;color:#64748b;margin-top:0.2rem'>
        Design real security architectures
      </div>
    </div>
    <hr style='border-color:#1f2d45;margin:0.75rem 0'>
    """, unsafe_allow_html=True)

    page = st.radio("Go to", [
        "🎯  Design Workbench",
        "🔐  Zone & Control Library",
        "⚔️  Attack Path Simulator",
        "📐  Architecture Patterns",
        "📋  Export My Design",
    ], label_visibility="collapsed")

    st.markdown("<hr style='border-color:#1f2d45;margin:0.75rem 0'>", unsafe_allow_html=True)

    sc = coverage_score()
    z_count = len(st.session_state["selected_zones"])
    c_count = len(set(all_controls_flat()))
    color = "#10b981" if sc >= 70 else "#f59e0b" if sc >= 40 else "#ef4444"

    c1, c2 = st.columns(2)
    c1.metric("Zones", z_count)
    c2.metric("Controls", c_count)

    st.markdown(f"""
    <div style='margin-top:0.5rem'>
      <div style='display:flex;justify-content:space-between;font-size:0.7rem;color:#64748b;margin-bottom:3px'>
        <span>Coverage Score</span>
        <span style='color:{color};font-weight:700'>{sc}/100</span>
      </div>
      <div style='background:#1a2236;border-radius:4px;height:6px;overflow:hidden'>
        <div style='width:{sc}%;height:100%;background:linear-gradient(90deg,{color},#3b82f6);border-radius:4px'></div>
      </div>
      <div style='font-size:0.65rem;color:#475569;margin-top:3px'>
        {"🟢 Good coverage" if sc>=70 else "🟡 Needs more controls" if sc>=40 else "🔴 Critical gaps present"}
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr style='border-color:#1f2d45;margin:0.75rem 0'>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:0.62rem;color:#374151;text-align:center'>Build real architectures. Understand every decision.</div>", unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════════
#  PAGE: DESIGN WORKBENCH
# ═════════════════════════════════════════════════════════════════
if page == "🎯  Design Workbench":
    st.markdown("""
    <div style='margin-bottom:1.5rem'>
      <div style='font-size:0.62rem;font-weight:700;letter-spacing:0.12em;color:#3b82f6;text-transform:uppercase;margin-bottom:0.2rem'>Step-by-Step Hands-On Design</div>
      <h1 style='font-size:1.9rem;font-weight:800;margin:0'>Design Workbench</h1>
      <p style='color:#64748b;margin-top:0.35rem;font-size:0.88rem'>Design a complete security architecture step-by-step. Every field teaches a real decision an architect makes.</p>
    </div>
    """, unsafe_allow_html=True)

    t1, t2, t3, t4, t5 = st.tabs(["① Scenario", "② Zones", "③ Controls", "④ Data Flows", "⑤ Review"])

    # ── TAB 1: SCENARIO ──────────────────────────────────────────
    with t1:
        st.markdown("""
        <div class='card card-blue'>
          <div style='font-size:0.7rem;font-weight:700;color:#60a5fa;margin-bottom:0.4rem'>WHY THIS STEP MATTERS</div>
          <p style='margin:0;color:#94a3b8;font-size:0.85rem;line-height:1.7'>
          Every architecture starts with a business context — <strong style='color:#e2e8f0'>what are we protecting, for whom, and under what constraints?</strong>
          Security architects don't design in the abstract. They design for specific data classifications, user populations, compliance obligations, and adversary profiles.
          Getting this wrong means you'll over-engineer some controls and miss critical ones entirely.
          </p>
        </div>
        """, unsafe_allow_html=True)

        choice = st.selectbox("Select a design scenario", list(SCENARIOS.keys()),
                              index=list(SCENARIOS.keys()).index(st.session_state["scenario"]))
        st.session_state["scenario"] = choice
        sinfo = SCENARIOS[choice]

        if choice != "Custom Scenario (Build Your Own)":
            c1, c2 = st.columns(2)
            with c1:
                st.markdown(f"""
                <div class='card card-blue'>
                  <div class='slabel'>System</div>
                  <p style='color:#e2e8f0;font-size:0.88rem;margin:0 0 0.75rem;line-height:1.6'>{sinfo['desc']}</p>
                  <div class='slabel'>Data in Scope</div>
                  <p style='color:#fbbf24;font-size:0.83rem;margin:0 0 0.75rem'>{sinfo['data']}</p>
                  <div class='slabel'>Users</div>
                  <p style='color:#a5f3fc;font-size:0.83rem;margin:0'>{sinfo['users']}</p>
                </div>
                """, unsafe_allow_html=True)
            with c2:
                comp_html = " ".join([f'<span class="badge badge-purple">{c}</span>' for c in sinfo["compliance"]])
                risk_html = " ".join([f'<div style="font-size:0.78rem;color:#f87171;margin-bottom:3px">⚠ {r}</div>' for r in sinfo["key_risks"]])
                st.markdown(f"""
                <div class='card card-amber'>
                  <div class='slabel'>Platform</div>
                  <p style='color:#e2e8f0;font-size:0.88rem;margin:0 0 0.75rem'>{sinfo['platform']}</p>
                  <div class='slabel'>Compliance Obligations</div>
                  <div style='margin-bottom:0.75rem'>{comp_html}</div>
                  <div class='slabel'>Crown Jewel</div>
                  <p style='color:#34d399;font-size:0.8rem;margin:0 0 0.75rem;font-weight:600'>{sinfo['crown_jewel']}</p>
                  <div class='slabel'>Key Risks</div>
                  {risk_html}
                </div>
                """, unsafe_allow_html=True)
        else:
            col1, col2 = st.columns(2)
            with col1:
                d  = st.text_area("System Description", height=80, placeholder="What does the system do?")
                dt = st.text_input("Data in Scope",     placeholder="What sensitive data does it handle?")
                u  = st.text_input("Users",              placeholder="Who accesses it and how?")
            with col2:
                pl = st.text_input("Platform",           placeholder="AWS, Azure, GCP, On-prem...")
                co = st.text_input("Compliance",         placeholder="SOC2, PCI-DSS, HIPAA...")
                rk = st.text_area("Key Risks",           height=80, placeholder="Top risks, one per line")
                cj = st.text_input("Crown Jewel",        placeholder="Most critical asset to protect?")
            if d:
                SCENARIOS["Custom Scenario (Build Your Own)"].update({
                    "desc": d, "data": dt, "users": u, "platform": pl,
                    "compliance": [x.strip() for x in co.split(",") if x.strip()],
                    "key_risks": [x.strip() for x in rk.split("\n") if x.strip()],
                    "crown_jewel": cj,
                })

        st.markdown("""
        <div style='padding:0.9rem 1.1rem;background:#0a0e1a;border:1px solid #1f2d45;border-radius:8px;margin-top:1.25rem'>
          <div style='font-size:0.65rem;font-weight:700;color:#8b5cf6;margin-bottom:0.35rem'>🎓 ARCHITECT'S THINKING</div>
          <p style='color:#64748b;font-size:0.78rem;margin:0;line-height:1.6'>
          Before drawing a single box, real architects answer three questions:<br>
          <strong style='color:#94a3b8'>1. What is the crown jewel?</strong> The one thing whose compromise ends the business.<br>
          <strong style='color:#94a3b8'>2. Who is the realistic adversary?</strong> Nation-state? Ransomware gang? Malicious insider? The adversary shapes the threat model.<br>
          <strong style='color:#94a3b8'>3. What are the hard constraints?</strong> Compliance is a floor not a ceiling. What are the latency, cost, and operational constraints?
          </p>
        </div>
        """, unsafe_allow_html=True)

    # ── TAB 2: ZONES ──────────────────────────────────────────────
    with t2:
        st.markdown("""
        <div class='card card-green'>
          <div style='font-size:0.7rem;font-weight:700;color:#34d399;margin-bottom:0.4rem'>WHY THIS STEP MATTERS</div>
          <p style='margin:0;color:#94a3b8;font-size:0.85rem;line-height:1.7'>
          <strong style='color:#e2e8f0'>Security zones are the foundation of every architecture.</strong>
          They create trust levels, define traffic flow rules, and — most importantly — limit blast radius.
          Without zones, a compromised web server has a direct database connection. With zones, it can't even reach the data tier.
          Each zone boundary must be <em>enforced</em> by a control. A zone without an enforced boundary is just a label on a diagram.
          </p>
        </div>
        """, unsafe_allow_html=True)

        selected = st.multiselect(
            "Choose the security zones for this architecture",
            list(ZONES.keys()),
            default=st.session_state["selected_zones"],
            help="Minimum viable architecture: Internet Zone + DMZ + Application Zone + Data Zone."
        )
        st.session_state["selected_zones"] = selected

        # Sync controls dict
        for z in selected:
            if z not in st.session_state["controls_by_zone"]:
                st.session_state["controls_by_zone"][z] = []
        for z in list(st.session_state["controls_by_zone"]):
            if z not in selected:
                del st.session_state["controls_by_zone"][z]

        if selected:
            st.markdown("---")
            st.markdown("### Zone Detail — Design Rules & Typical Assets")
            cols = st.columns(min(len(selected), 3))
            for i, z in enumerate(selected):
                info = ZONES[z]
                bar_color = ["#ef4444","#f97316","#f59e0b","#10b981","#3b82f6"][info["trust"]]
                bar = "█" * (info["trust"]+1) + "░" * (4-info["trust"])
                ctrl_html = "".join([f'<div style="font-size:0.73rem;color:#64748b;margin-bottom:2px">→ {c}</div>' for c in info["controls"]])
                asset_html = "".join([f'<div style="font-size:0.73rem;color:#94a3b8;margin-bottom:2px">· {a}</div>' for a in info["assets"]])
                with cols[i % 3]:
                    st.markdown(f"""
                    <div class='card' style='border-left:3px solid {bar_color};min-height:220px'>
                      <div style='font-size:1rem;margin-bottom:0.3rem'>{info['emoji']} <strong>{z}</strong></div>
                      <div style='margin-bottom:0.6rem'>
                        <span style='font-size:0.68rem;color:#64748b'>Trust: </span>
                        <span style='font-family:JetBrains Mono,monospace;color:{bar_color}'>{bar} {info["trust"]}/4</span>
                      </div>
                      <p style='color:#94a3b8;font-size:0.78rem;line-height:1.5;margin-bottom:0.6rem'>{info['desc']}</p>
                      <div class='slabel'>Typical Controls</div>{ctrl_html}
                      <div class='slabel' style='margin-top:0.5rem'>Example Assets</div>{asset_html}
                    </div>
                    """, unsafe_allow_html=True)

        st.markdown("""
        <div style='padding:0.9rem 1.1rem;background:#0a0e1a;border:1px solid #1f2d45;border-radius:8px;margin-top:1rem'>
          <div style='font-size:0.65rem;font-weight:700;color:#8b5cf6;margin-bottom:0.35rem'>🎓 ARCHITECT'S THINKING</div>
          <p style='color:#64748b;font-size:0.78rem;margin:0;line-height:1.6'>
          <strong style='color:#94a3b8'>Zone design principle: data should only flow to higher-trust zones through explicit, controlled chokepoints.</strong><br>
          A DMZ web server can call an Application Zone API — but the Application Zone should never be directly reachable from the Internet Zone.
          The Management Zone should be completely isolated — app servers don't need admin console access.<br>
          Ask: "What is the minimum trust level required to perform this operation?" Design to enforce exactly that — nothing more.
          </p>
        </div>
        """, unsafe_allow_html=True)

    # ── TAB 3: CONTROLS ───────────────────────────────────────────
    with t3:
        st.markdown("""
        <div class='card card-amber'>
          <div style='font-size:0.7rem;font-weight:700;color:#fbbf24;margin-bottom:0.4rem'>WHY THIS STEP MATTERS</div>
          <p style='margin:0;color:#94a3b8;font-size:0.85rem;line-height:1.7'>
          Controls are the mechanisms that enforce your security policy. <strong style='color:#e2e8f0'>Each control must be mapped to a specific zone</strong> — a floating control that isn't tied to a layer creates gaps.
          For every control, a good architect can answer two questions instantly: <em>"What specific attack technique does this block?"</em> and <em>"What happens if this single control fails?"</em>
          Defense-in-depth means an attacker must defeat several controls in sequence — no single failure means total compromise.
          </p>
        </div>
        """, unsafe_allow_html=True)

        if not st.session_state["selected_zones"]:
            st.warning("⚠️ Define security zones in Step ② first.")
        else:
            for zone in st.session_state["selected_zones"]:
                zinfo = ZONES[zone]
                with st.expander(f"{zinfo['emoji']}  {zone}  —  assign controls", expanded=True):
                    ca, cb = st.columns([3, 2])
                    with ca:
                        all_opts = []
                        for cat, items in CONTROLS.items():
                            for cname, cinfo in items.items():
                                if "All Zones" in cinfo["zones"] or zone in cinfo["zones"]:
                                    all_opts.append(f"[{cat}] {cname}")
                                else:
                                    all_opts.append(f"[{cat}] {cname}  ⚠ non-standard for this zone")

                        current_labels = []
                        for cat, items in CONTROLS.items():
                            for c in st.session_state["controls_by_zone"].get(zone, []):
                                if c in items:
                                    current_labels.append(f"[{cat}] {c}")

                        chosen = st.multiselect(
                            f"Controls for {zone}",
                            all_opts,
                            default=[l for l in current_labels if l in all_opts],
                            key=f"ms_{zone}",
                            label_visibility="collapsed",
                        )
                        parsed = []
                        for s in chosen:
                            m = re.match(r'\[(.+?)\] (.+?)(\s+⚠.*)?$', s)
                            if m:
                                parsed.append(m.group(2))
                        st.session_state["controls_by_zone"][zone] = parsed

                    with cb:
                        rec_html = "".join([f'<div style="font-size:0.73rem;color:#64748b;margin-bottom:3px">→ {c}</div>' for c in zinfo["controls"]])
                        st.markdown(f"""
                        <div style='background:#0a0e1a;border:1px solid #1f2d45;border-radius:8px;padding:0.85rem'>
                          <div class='slabel'>Recommended for this zone</div>{rec_html}
                        </div>
                        """, unsafe_allow_html=True)

            # ── Control detail lookup ──────────────────────────────
            st.markdown("---")
            st.markdown("### 🔍 Understand Any Control")
            all_ctrl_names = [c for cat in CONTROLS.values() for c in cat]
            pick = st.selectbox("Select a control to understand what it does and why", ["— select —"] + all_ctrl_names)
            if pick != "— select —":
                for cat, items in CONTROLS.items():
                    if pick in items:
                        info = items[pick]
                        ec = "#10b981" if info["effort"]=="Low" else "#f59e0b" if info["effort"]=="Medium" else "#ef4444"
                        bc = " ".join([f'<span class="badge badge-red">{b}</span>' for b in info["blocks"]])
                        zc = " ".join([f'<span class="badge badge-green">{z}</span>' for z in info["zones"]])
                        st.markdown(f"""
                        <div class='card card-blue'>
                          <div style='font-size:0.95rem;font-weight:700;color:#f1f5f9;margin-bottom:0.75rem'>{pick}
                            <span style='font-size:0.7rem;font-weight:700;color:{ec};background:{ec}22;padding:2px 10px;border-radius:20px;border:1px solid {ec}44;margin-left:8px'>{info["effort"]} Effort</span>
                          </div>
                          <div class='slabel'>Category</div>
                          <div style='color:#60a5fa;font-size:0.82rem;margin-bottom:0.75rem;font-weight:600'>{cat}</div>
                          <div class='slabel'>Attack Techniques This Blocks</div>
                          <div style='margin-bottom:0.75rem'>{bc}</div>
                          <div class='slabel'>Natural Zone Placement</div>
                          <div>{zc}</div>
                        </div>
                        """, unsafe_allow_html=True)
                        break

        st.markdown("""
        <div style='padding:0.9rem 1.1rem;background:#0a0e1a;border:1px solid #1f2d45;border-radius:8px;margin-top:1rem'>
          <div style='font-size:0.65rem;font-weight:700;color:#8b5cf6;margin-bottom:0.35rem'>🎓 ARCHITECT'S THINKING</div>
          <p style='color:#64748b;font-size:0.78rem;margin:0;line-height:1.6'>
          <strong style='color:#94a3b8'>The "⚠ non-standard" flag is intentional.</strong>
          You CAN place any control in any zone — but it needs a documented reason.
          A WAF in the Application Zone (not DMZ) might protect internal APIs — valid, but unusual. Document it in an ADR.<br>
          <strong style='color:#94a3b8'>The golden rule: if you can't explain what attack a control prevents, it shouldn't be in your architecture.</strong>
          Every control costs money, adds complexity, and can fail. Every control must earn its place.
          </p>
        </div>
        """, unsafe_allow_html=True)

    # ── TAB 4: DATA FLOWS ─────────────────────────────────────────
    with t4:
        st.markdown("""
        <div class='card card-purple'>
          <div style='font-size:0.7rem;font-weight:700;color:#a78bfa;margin-bottom:0.4rem'>WHY THIS STEP MATTERS</div>
          <p style='margin:0;color:#94a3b8;font-size:0.85rem;line-height:1.7'>
          <strong style='color:#e2e8f0'>Data flow diagrams reveal where sensitive data travels, what systems touch it, and where it crosses trust boundaries.</strong>
          Most breaches exploit undocumented data flows — pathways nobody on the security team knew existed.
          Every flow that crosses a zone boundary is a potential attack path. Document all of them.
          Then ask: Does this flow need to exist? Is it encrypted? Is it authenticated and authorised? Is it monitored?
          </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### Add a Data Flow")
        zones_list = st.session_state["selected_zones"] or list(ZONES.keys())

        col1, col2, col3 = st.columns([2,1,2])
        with col1:
            src = st.selectbox("Source Zone", zones_list, key="flow_src")
        with col2:
            proto = st.selectbox("Protocol", ["HTTPS/TLS 1.3","mTLS","JDBC+SSL","gRPC/TLS","REST/HTTPS",
                                              "SSH","SFTP","Kafka+TLS","Internal gRPC","LDAPS"], key="flow_proto")
        with col3:
            dst = st.selectbox("Destination Zone", zones_list, key="flow_dst")

        col4, col5 = st.columns([4,1])
        with col4:
            desc = st.text_input("Describe the data flowing", placeholder="e.g. Encrypted user session token from web browser to API gateway", key="flow_desc")
        with col5:
            st.markdown("<div style='height:1.75rem'></div>", unsafe_allow_html=True)
            if st.button("➕ Add", use_container_width=True):
                if desc and src != dst:
                    st.session_state["data_flows"].append(f"{src}  →[{proto}]→  {dst}  |  {desc}")
                    st.rerun()
                elif src == dst:
                    st.error("Source and destination must differ.")
                else:
                    st.error("Describe the data flow.")

        # Trust-level jump warning
        if src and dst and src != dst:
            st_trust = ZONES.get(src, {}).get("trust", 0)
            dt_trust = ZONES.get(dst, {}).get("trust", 0)
            jump = abs(st_trust - dt_trust)
            if jump > 1:
                st.markdown(f"""
                <div style='padding:0.55rem 0.9rem;background:rgba(239,68,68,0.08);border:1px solid rgba(239,68,68,0.3);border-radius:8px;margin-top:0.4rem'>
                  <strong style='color:#f87171;font-size:0.78rem'>⚠ HIGH TRUST JUMP ({jump} levels)</strong>
                  <span style='color:#94a3b8;font-size:0.78rem'> — Skipping intermediate zone(s). Ensure a proxy/gateway sits between these zones and this flow has explicit logging and MFA-backed authorisation.</span>
                </div>
                """, unsafe_allow_html=True)

        # Existing flows
        if st.session_state["data_flows"]:
            st.markdown("---")
            st.markdown("### Documented Data Flows")
            for i, flow in enumerate(st.session_state["data_flows"]):
                parts = flow.split(" | ")
                path = parts[0].strip()
                fdesc = parts[1].strip() if len(parts) > 1 else ""
                fc, fd = st.columns([10, 1])
                with fc:
                    st.markdown(f"""
                    <div style='padding:0.6rem 1rem;background:#111827;border:1px solid #1f2d45;border-radius:8px;margin-bottom:5px;display:flex;align-items:center;gap:12px'>
                      <div style='font-family:JetBrains Mono,monospace;font-size:0.75rem;color:#60a5fa;white-space:nowrap'>{path}</div>
                      <div style='color:#1f2d45;font-size:0.78rem'>|</div>
                      <div style='font-size:0.78rem;color:#94a3b8'>{fdesc}</div>
                    </div>
                    """, unsafe_allow_html=True)
                with fd:
                    if st.button("✕", key=f"df_{i}"):
                        st.session_state["data_flows"].pop(i)
                        st.rerun()
        else:
            st.markdown("""
            <div style='padding:2rem;text-align:center;color:#475569;border:1px dashed #1f2d45;border-radius:8px;margin-top:0.75rem'>
              No data flows documented yet.
            </div>
            """, unsafe_allow_html=True)

        st.markdown("""
        <div style='padding:0.9rem 1.1rem;background:#0a0e1a;border:1px solid #1f2d45;border-radius:8px;margin-top:1rem'>
          <div style='font-size:0.65rem;font-weight:700;color:#8b5cf6;margin-bottom:0.35rem'>🎓 ARCHITECT'S THINKING</div>
          <p style='color:#64748b;font-size:0.78rem;margin:0;line-height:1.6'>
          For <em>every</em> cross-zone flow, an architect must confirm four things:<br>
          <strong style='color:#94a3b8'>1. Is it encrypted in transit?</strong> Protocol must enforce this — no plaintext across zone boundaries, ever.<br>
          <strong style='color:#94a3b8'>2. Is it authenticated?</strong> Who/what is authorised to make this call? Service identity, not just user identity.<br>
          <strong style='color:#94a3b8'>3. Is it authorised at the data level?</strong> Can the caller access this specific data, not just the endpoint?<br>
          <strong style='color:#94a3b8'>4. Is it logged?</strong> You can't detect abuse of an unlogged data path. Undocumented flows become silent attack paths.
          </p>
        </div>
        """, unsafe_allow_html=True)

    # ── TAB 5: REVIEW ─────────────────────────────────────────────
    with t5:
        st.markdown("### Architecture Review & Coverage Analysis")

        sc = coverage_score()
        flat = set(all_controls_flat())
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Coverage Score", f"{sc}/100",
                  delta="Good" if sc >= 70 else "Needs Work",
                  delta_color="normal" if sc >= 70 else "inverse")
        m2.metric("Zones Defined", len(st.session_state["selected_zones"]),
                  delta="✓" if len(st.session_state["selected_zones"]) >= 3 else "Add more")
        m3.metric("Unique Controls", len(flat),
                  delta="✓" if len(flat) >= 8 else "Add more")
        m4.metric("Data Flows", len(st.session_state["data_flows"]),
                  delta="✓" if st.session_state["data_flows"] else "Document flows")

        st.markdown("---")
        st.markdown("### Zone Diagram")
        st.code(render_diagram(), language=None)

        st.markdown("---")
        st.markdown("### Gap Analysis")

        gaps = gap_analysis()
        if not gaps:
            st.success("✅ No critical gaps detected in your current design.")
        else:
            for sev, issue, fix in gaps:
                vc = "red" if "CRITICAL" in sev else "amber" if "HIGH" in sev or "MEDIUM" in sev else "blue"
                st.markdown(f"""
                <div class='card card-{vc}' style='margin-bottom:0.6rem'>
                  <div style='display:flex;align-items:flex-start;gap:12px'>
                    <div>
                      <span class='badge badge-{vc}'>{sev}</span>
                      <p style='color:#e2e8f0;font-size:0.85rem;margin:0.4rem 0 0.25rem;font-weight:500'>{issue}</p>
                      <p style='color:#64748b;font-size:0.78rem;margin:0'>→ <strong style='color:#94a3b8'>Fix:</strong> {fix}</p>
                    </div>
                  </div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("---")
        notes = st.text_area(
            "Architect's Notes & Design Decisions",
            value=st.session_state.get("arch_notes", ""),
            placeholder="Document your key architectural choices here. E.g. 'We chose to terminate TLS at the load balancer rather than the app server because...'",
            height=120,
        )
        st.session_state["arch_notes"] = notes


# ═════════════════════════════════════════════════════════════════
#  PAGE: ZONE & CONTROL LIBRARY
# ═════════════════════════════════════════════════════════════════
elif page == "🔐  Zone & Control Library":
    st.markdown("""
    <div style='margin-bottom:1.5rem'>
      <div style='font-size:0.62rem;font-weight:700;letter-spacing:0.12em;color:#10b981;text-transform:uppercase;margin-bottom:0.2rem'>Reference</div>
      <h1 style='font-size:1.9rem;font-weight:800;margin:0'>Zone & Control Library</h1>
      <p style='color:#64748b;margin-top:0.35rem;font-size:0.88rem'>Understand what each zone and control does, when to use it, and what attack it defeats.</p>
    </div>
    """, unsafe_allow_html=True)

    lt1, lt2 = st.tabs(["🏛️  Security Zones", "🛡️  Security Controls"])

    with lt1:
        for zone, info in ZONES.items():
            trust = info["trust"]
            pct = trust / 4 * 100
            bc  = ["#ef4444","#f97316","#f59e0b","#10b981","#3b82f6"][trust]
            trust_name = ["Untrusted","Low Trust","Partial Trust","High Trust","Restricted"][trust]
            ctrl_html  = "".join([f'<div style="font-size:0.75rem;color:#60a5fa;margin-bottom:3px">🔒 {c}</div>' for c in info["controls"]])
            asset_html = "".join([f'<div style="font-size:0.75rem;color:#64748b;margin-bottom:3px">· {a}</div>' for a in info["assets"]])
            with st.expander(f"{info['emoji']}  {zone}  —  Trust Level {trust}/4  ({trust_name})"):
                c1, c2 = st.columns([3,2])
                with c1:
                    st.markdown(f"""
                    <p style='color:#94a3b8;font-size:0.88rem;line-height:1.7;margin-bottom:1rem'>{info['desc']}</p>
                    <div style='background:#0a0e1a;padding:0.75rem;border-radius:8px'>
                      <div class='slabel'>Trust Level</div>
                      <div style='background:#1a2236;border-radius:4px;height:8px;overflow:hidden;margin-bottom:0.3rem'>
                        <div style='width:{pct}%;height:100%;background:{bc};border-radius:4px'></div>
                      </div>
                      <div style='font-size:0.72rem;color:{bc};font-weight:600'>{trust_name} ({trust}/4)</div>
                    </div>
                    """, unsafe_allow_html=True)
                with c2:
                    st.markdown(f"""
                    <div style='background:#0a0e1a;border:1px solid #1f2d45;border-radius:8px;padding:0.85rem'>
                      <div class='slabel'>Typical Controls</div>{ctrl_html}
                      <div class='slabel' style='margin-top:0.6rem'>Example Assets</div>{asset_html}
                    </div>
                    """, unsafe_allow_html=True)

    with lt2:
        search = st.text_input("🔍 Search by control name or what it blocks", placeholder="e.g. lateral movement, encryption, phishing")
        for cat, items in CONTROLS.items():
            filtered = {k: v for k, v in items.items()
                        if not search
                        or search.lower() in k.lower()
                        or any(search.lower() in b.lower() for b in v["blocks"])}
            if not filtered:
                continue
            st.markdown(f"""
            <div style='margin:1.25rem 0 0.6rem'>
              <span style='font-size:0.73rem;font-weight:700;color:#3b82f6;text-transform:uppercase;letter-spacing:0.1em'>{cat}</span>
            </div>
            """, unsafe_allow_html=True)
            cols = st.columns(3)
            for i, (cname, cinfo) in enumerate(filtered.items()):
                ec = "#10b981" if cinfo["effort"]=="Low" else "#f59e0b" if cinfo["effort"]=="Medium" else "#ef4444"
                block_html = "".join([f'<div style="font-size:0.72rem;color:#f87171;margin-bottom:2px">✗ {b}</div>' for b in cinfo["blocks"]])
                zone_str   = ", ".join(cinfo["zones"][:2])
                with cols[i % 3]:
                    st.markdown(f"""
                    <div class='card card-blue' style='min-height:160px'>
                      <div style='font-size:0.83rem;font-weight:700;color:#f1f5f9;margin-bottom:0.4rem'>{cname}</div>
                      <div class='slabel'>Blocks</div>{block_html}
                      <div class='slabel' style='margin-top:0.4rem'>Natural Zone</div>
                      <div style='font-size:0.72rem;color:#34d399;margin-bottom:0.4rem'>{zone_str}</div>
                      <span style='font-size:0.65rem;font-weight:700;color:{ec};background:{ec}22;padding:2px 8px;border-radius:20px;border:1px solid {ec}44'>{cinfo["effort"]} Effort</span>
                    </div>
                    """, unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════════
#  PAGE: ATTACK PATH SIMULATOR
# ═════════════════════════════════════════════════════════════════
elif page == "⚔️  Attack Path Simulator":
    st.markdown("""
    <div style='margin-bottom:1.5rem'>
      <div style='font-size:0.62rem;font-weight:700;letter-spacing:0.12em;color:#ef4444;text-transform:uppercase;margin-bottom:0.2rem'>Adversarial Thinking</div>
      <h1 style='font-size:1.9rem;font-weight:800;margin:0'>Attack Path Simulator</h1>
      <p style='color:#64748b;margin-top:0.35rem;font-size:0.88rem'>The best architects think like attackers. See how real breaches happen, then check if your design stops them.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class='card card-red'>
      <div style='font-size:0.7rem;font-weight:700;color:#f87171;margin-bottom:0.4rem'>THE ARCHITECT'S IMPERATIVE</div>
      <p style='margin:0;color:#94a3b8;font-size:0.85rem;line-height:1.7'>
      Security architecture is not about building walls — it's about designing systems that remain secure <strong style='color:#e2e8f0'>even when individual controls fail.</strong>
      Every control in your design should break a specific step in a real attack chain.
      If you can't map a control to an attack technique, question whether it earns its place in the architecture.
      </p>
    </div>
    """, unsafe_allow_html=True)

    attack_choice = st.selectbox("Select an attack scenario to simulate", list(ATTACKS.keys()))
    attack = ATTACKS[attack_choice]

    col_left, col_right = st.columns([3, 2])

    with col_left:
        st.markdown("### Attack Progression")
        for i, (zone, stage, technique) in enumerate(attack["stages"]):
            zinfo = ZONES.get(zone, {})
            user_ctrls_here = st.session_state["controls_by_zone"].get(zone, [])

            # Check which user controls block this stage
            blocking = []
            rec_blocking = attack.get("blocking_controls", {})
            for ctrl, ctrl_zones in rec_blocking.items():
                if ctrl in user_ctrls_here and (zone in ctrl_zones or "All Zones" in ctrl_zones):
                    blocking.append(ctrl)

            is_blocked   = len(blocking) > 0
            box_bg       = "rgba(16,185,129,0.07)" if is_blocked else "rgba(239,68,68,0.06)"
            box_border   = "rgba(16,185,129,0.35)" if is_blocked else "rgba(239,68,68,0.3)"
            status_color = "#10b981" if is_blocked else "#ef4444"
            status_label = "BLOCKED ✓" if is_blocked else "VULNERABLE ✗"
            block_text   = f"Blocked by: {', '.join(blocking)}" if is_blocked else "No blocking control in your current design for this zone"
            block_color  = "#34d399" if is_blocked else "#f87171"

            st.markdown(f"""
            <div style='padding:0.9rem 1.1rem;background:{box_bg};border:1px solid {box_border};border-radius:10px;margin-bottom:0.4rem'>
              <div style='display:flex;justify-content:space-between;align-items:flex-start'>
                <div style='flex:1'>
                  <div style='font-size:0.62rem;font-weight:700;color:#475569;text-transform:uppercase;margin-bottom:0.2rem'>
                    Stage {i+1} — {zinfo.get("emoji","⬜")} {zone} — {stage}
                  </div>
                  <div style='font-size:0.85rem;color:#e2e8f0;font-weight:600;margin-bottom:0.3rem'>{technique}</div>
                  <div style='font-size:0.75rem;color:{block_color}'>{block_text}</div>
                </div>
                <div style='font-size:0.7rem;font-weight:700;color:{status_color};background:{status_color}18;padding:3px 10px;border-radius:20px;border:1px solid {status_color}44;white-space:nowrap;margin-left:12px'>
                  {status_label}
                </div>
              </div>
            </div>
            """, unsafe_allow_html=True)

            if i < len(attack["stages"]) - 1:
                st.markdown("<div style='text-align:center;color:#ef4444;font-size:1.1rem;margin:2px 0'>↓</div>", unsafe_allow_html=True)

    with col_right:
        st.markdown("### Attack Intel")
        st.markdown(f"""
        <div class='card card-red'>
          <div class='slabel'>Attacker Goal</div>
          <div style='color:#f87171;font-size:0.9rem;font-weight:600;margin-bottom:0.75rem'>{attack['goal']}</div>
          <div class='slabel'>Recommended Controls to Break This Chain</div>
        """, unsafe_allow_html=True)
        for ctrl, ctrl_zones in attack.get("blocking_controls", {}).items():
            in_design = ctrl in all_controls_flat()
            sc = "#10b981" if in_design else "#ef4444"
            si = "✓" if in_design else "✗"
            st = "In your design" if in_design else "Missing"
            st.markdown(f"""
              <div style='padding:0.5rem 0.8rem;background:#0a0e1a;border:1px solid {"rgba(16,185,129,0.3)" if in_design else "#1f2d45"};border-radius:7px;margin-bottom:4px;display:flex;justify-content:space-between;align-items:center'>
                <div style='font-size:0.78rem;color:#e2e8f0'>{ctrl}</div>
                <div style='font-size:0.7rem;color:{sc};font-weight:700'>{si} {st}</div>
              </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        total  = len(attack["blocking_controls"])
        have   = sum(1 for c in attack["blocking_controls"] if c in all_controls_flat())
        pct_bl = round(have / total * 100) if total else 0
        col_m  = "#10b981" if pct_bl >= 70 else "#f59e0b" if pct_bl >= 40 else "#ef4444"
        st.markdown(f"""
        <div style='padding:0.9rem;background:#111827;border:1px solid #1f2d45;border-radius:8px;margin-top:0.6rem;text-align:center'>
          <div style='font-size:0.65rem;color:#475569;text-transform:uppercase;font-weight:700;margin-bottom:0.3rem'>Your protection against this attack</div>
          <div style='font-size:2rem;font-weight:800;color:{col_m}'>{pct_bl}%</div>
          <div style='font-size:0.72rem;color:#64748b'>{have}/{total} recommended controls in place</div>
        </div>
        """, unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════════
#  PAGE: ARCHITECTURE PATTERNS
# ═════════════════════════════════════════════════════════════════
elif page == "📐  Architecture Patterns":
    st.markdown("""
    <div style='margin-bottom:1.5rem'>
      <div style='font-size:0.62rem;font-weight:700;letter-spacing:0.12em;color:#8b5cf6;text-transform:uppercase;margin-bottom:0.2rem'>Proven Design Patterns</div>
      <h1 style='font-size:1.9rem;font-weight:800;margin:0'>Architecture Patterns</h1>
      <p style='color:#64748b;margin-top:0.35rem;font-size:0.88rem'>Study how real security architectures solve specific problems. Each pattern addresses a concrete failure mode.</p>
    </div>
    """, unsafe_allow_html=True)

    for pname, pinfo in PATTERNS.items():
        with st.expander(f"📐  {pname}"):
            c1, c2 = st.columns([5, 4])
            with c1:
                st.markdown(f"""
                <div class='card card-red' style='margin-bottom:0.75rem'>
                  <div class='slabel'>The Problem This Solves</div>
                  <p style='color:#94a3b8;font-size:0.85rem;margin:0;line-height:1.7'>{pinfo['problem']}</p>
                </div>
                <div class='card card-green' style='margin-bottom:0.75rem'>
                  <div class='slabel'>The Architecture Solution</div>
                  <p style='color:#94a3b8;font-size:0.85rem;margin:0;line-height:1.7'>{pinfo['solution']}</p>
                </div>
                <div class='card card-blue'>
                  <div class='slabel'>When to Use This Pattern</div>
                  <p style='color:#94a3b8;font-size:0.85rem;margin:0;line-height:1.7'>{pinfo['when']}</p>
                </div>
                """, unsafe_allow_html=True)
            with c2:
                st.code(pinfo["diagram"], language=None)

            st.markdown("**Key Components:**")
            comp_cols = st.columns(len(pinfo["components"]) if len(pinfo["components"]) <= 3 else 3)
            for i, (comp_name, comp_desc) in enumerate(pinfo["components"]):
                with comp_cols[i % 3]:
                    st.markdown(f"""
                    <div style='padding:0.7rem 0.9rem;background:#111827;border:1px solid #1f2d45;border-left:2px solid #3b82f6;border-radius:8px;margin-bottom:6px;min-height:80px'>
                      <div style='font-size:0.78rem;font-weight:700;color:#60a5fa;margin-bottom:0.25rem'>{comp_name}</div>
                      <div style='font-size:0.75rem;color:#94a3b8;line-height:1.5'>{comp_desc}</div>
                    </div>
                    """, unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════════
#  PAGE: EXPORT
# ═════════════════════════════════════════════════════════════════
elif page == "📋  Export My Design":
    st.markdown("""
    <div style='margin-bottom:1.5rem'>
      <div style='font-size:0.62rem;font-weight:700;letter-spacing:0.12em;color:#f59e0b;text-transform:uppercase;margin-bottom:0.2rem'>Your Design Output</div>
      <h1 style='font-size:1.9rem;font-weight:800;margin:0'>Export My Design</h1>
      <p style='color:#64748b;margin-top:0.35rem;font-size:0.88rem'>Your completed architecture — ready to present, document, or export as a portfolio piece.</p>
    </div>
    """, unsafe_allow_html=True)

    if not st.session_state["selected_zones"]:
        st.info("👈 Complete the Design Workbench (Steps ①–⑤) to generate your output.")
    else:
        sc   = coverage_score()
        flat = set(all_controls_flat())
        doc  = generate_doc()

        col_doc, col_stats = st.columns([3, 1])

        with col_doc:
            st.markdown("### Architecture Document")
            st.markdown(doc)

        with col_stats:
            st.markdown("### Stats")
            col_m = "#10b981" if sc >= 70 else "#f59e0b" if sc >= 40 else "#ef4444"
            st.markdown(f"""
            <div style='padding:1.25rem;background:#111827;border:1px solid #1f2d45;border-radius:10px;text-align:center;margin-bottom:0.75rem'>
              <div style='font-size:0.65rem;color:#475569;text-transform:uppercase;font-weight:700;margin-bottom:0.3rem'>Coverage Score</div>
              <div style='font-size:2.5rem;font-weight:800;color:{col_m}'>{sc}</div>
              <div style='font-size:0.72rem;color:#64748b'>out of 100</div>
            </div>
            """, unsafe_allow_html=True)
            st.metric("Zones", len(st.session_state["selected_zones"]))
            st.metric("Controls", len(flat))
            st.metric("Data Flows", len(st.session_state["data_flows"]))

            st.markdown("---")
            st.markdown("### Export")
            st.download_button(
                "📥 Download as Markdown",
                data=doc,
                file_name=f"security_arch_{datetime.now().strftime('%Y%m%d_%H%M')}.md",
                mime="text/markdown",
                use_container_width=True,
            )

            export_json = json.dumps({
                "scenario":   st.session_state["scenario"],
                "generated":  datetime.now().isoformat(),
                "score":      sc,
                "zones":      st.session_state["selected_zones"],
                "controls":   {k: list(v) for k, v in st.session_state["controls_by_zone"].items()},
                "data_flows": st.session_state["data_flows"],
                "notes":      st.session_state.get("arch_notes", ""),
            }, indent=2)
            st.download_button(
                "📥 Download as JSON",
                data=export_json,
                file_name=f"arch_design_{datetime.now().strftime('%Y%m%d')}.json",
                mime="application/json",
                use_container_width=True,
            )

            st.markdown("""
            <div style='padding:0.85rem;background:#0a0e1a;border:1px solid #1f2d45;border-radius:8px;margin-top:0.75rem'>
              <div style='font-size:0.65rem;font-weight:700;color:#8b5cf6;margin-bottom:0.3rem'>🎓 WHAT TO DO WITH THIS</div>
              <p style='color:#64748b;font-size:0.75rem;margin:0;line-height:1.5'>
              This document is your architecture portfolio piece. Present it to stakeholders. Bring it to a review board. Iterate as threats evolve. Every revision is experience.
              </p>
            </div>
            """, unsafe_allow_html=True)
