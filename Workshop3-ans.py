"""
EXAMPLE IMPLEMENTATION: Day 1, Session 2.1 - PASTA Threat Modeling
Complete subsection showing how AWS methods are used as tools for security architecture
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

def render_1_2_1_pasta_complete_example():
    """
    Complete implementation of PASTA threat modeling subsection
    Demonstrates: AWS Discovery + Security Core + Real-world Application
    """
    
    # ========================================================================
    # PART 1: REAL-WORLD SCENARIO (THE PROBLEM)
    # ========================================================================
    
    st.markdown("""
    <div style="background-color: #fff3cd; padding: 1.5rem; border-left: 4px solid #ffc107; margin: 1rem 0;">
    <h3>🎯 Real-World Challenge: Payment API Security Assessment</h3>
    
    <p><strong>Company:</strong> FinTech SaaS processing $500M/day</p>
    <p><strong>Architecture:</strong> 50+ microservices in Kubernetes (EKS)</p>
    <p><strong>Recent Event:</strong> Pen test found 15 authorization bugs</p>
    <p><strong>Board Question:</strong> "How do we know we won't have a Capital One breach?"</p>
    
    <p><strong>Your Mission:</strong> Complete threat model using PASTA methodology</p>
    <p><strong>Timeline:</strong> 2 weeks to present findings to CISO + board</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Architecture Overview
    with st.expander("📐 Current Architecture Overview"):
        st.code("""
Internet → Cloudflare WAF → API Gateway (Kong)
                              ↓
                         EKS Cluster
                              ↓
          ┌───────────────────┴───────────────────┐
          │                                       │
    Payment Service ←→ Auth Service         Fraud Detection
          ↓                   ↓                   ↓
      Postgres            Redis             SageMaker
  (card tokens)        (sessions)          (ML model)
          │
          └──→ Stripe API (external - actual card processing)
        """)
        
        st.info("""
        **Key Security Controls:**
        - WAF (DDoS, SQLi protection)
        - API Gateway (OAuth 2.0, rate limiting)
        - mTLS between services
        - Card data is TOKENIZED (never touches your infrastructure)
        - PCI-DSS Level 1 compliance required
        """)
    
    # ========================================================================
    # PART 2: AWS METHODOLOGY AS A TOOL (DISCOVERY MINDSET)
    # ========================================================================
    
    st.markdown("---")
    st.subheader("🔍 Step 1: Apply AWS Discovery Mindset")
    
    st.info("""
    **AWS Principle:** "Diagnose the patient, don't just count the pills"
    
    **Wrong Approach:**
    - Count how many security controls you have
    - List all the tools (WAF, API Gateway, etc.)
    - Focus on what you DO have
    
    **Right Approach (Discovery):**
    - What are the business objectives? (Real impact if compromised)
    - What are the actual attack paths? (Not theoretical)
    - Where do controls FAIL? (Unhappy paths)
    """)
    
    # ========================================================================
    # PART 3: SECURITY ARCHITECTURE CORE (PASTA METHODOLOGY)
    # ========================================================================
    
    st.markdown("---")
    st.subheader("🎯 Step 2: Apply PASTA (7-Stage Threat Analysis)")
    
    st.write("""
    **PASTA = Process for Attack Simulation and Threat Analysis**
    
    AWS Discovery provides the *mindset*.
    PASTA provides the *systematic process*.
    Together: Comprehensive threat model.
    """)
    
    # Create tabs for 7 PASTA stages
    pasta_tabs = st.tabs([
        "Stage 1: Business",
        "Stage 2: Scope",
        "Stage 3: Decompose",
        "Stage 4: Threats",
        "Stage 5: Vulnerabilities",
        "Stage 6: Attack Modeling",
        "Stage 7: Risk & Impact"
    ])
    
    # Stage 1: Business Objectives
    with pasta_tabs[0]:
        st.write("### Stage 1: Define Business Objectives")
        
        st.warning("""
        **AWS Discovery Applied:**
        - NOT: "Secure the application"
        - YES: "Prevent fraud that costs $5M annually"
        """)
        
        st.write("**Exercise:** Define business objectives in $ terms")
        
        col1, col2 = st.columns(2)
        with col1:
            revenue_impact = st.number_input(
                "Daily transaction volume ($M)",
                min_value=1,
                max_value=1000,
                value=500,
                key="pasta_revenue"
            )
        with col2:
            downtime_cost = st.number_input(
                "Cost per hour downtime ($K)",
                min_value=10,
                max_value=5000,
                value=500,
                key="pasta_downtime"
            )
        
        fraud_rate = st.slider(
            "Current fraud rate (%)",
            0.0, 5.0, 0.15, 0.05,
            key="pasta_fraud"
        )
        
        # Calculate business impact
        annual_fraud_loss = revenue_impact * 365 * fraud_rate / 100
        
        st.metric(
            "Annual Fraud Loss",
            f"${annual_fraud_loss:.1f}M",
            help="This is what we're trying to prevent"
        )
        
        business_objectives = st.text_area(
            "Document business objectives:",
            value=st.session_state.pasta_analysis.get('stage1_objectives', ''),
            placeholder=f"""1. Prevent account takeover fraud (currently ${annual_fraud_loss:.1f}M/year)
2. Maintain 99.99% uptime (downtime costs ${downtime_cost}K/hour)
3. Pass PCI-DSS audit (required for Visa/MC processing)
4. Protect customer trust (breach = 20% churn based on industry data)""",
            height=150,
            key="stage1_objectives"
        )
        
        if st.button("💾 Save Stage 1", key="save_stage1"):
            st.session_state.pasta_analysis['stage1_objectives'] = business_objectives
            st.session_state.pasta_analysis['stage1_metrics'] = {
                'revenue': revenue_impact,
                'downtime_cost': downtime_cost,
                'fraud_rate': fraud_rate,
                'annual_fraud_loss': annual_fraud_loss
            }
            st.success("✅ Saved! Business objectives quantified.")
    
    # Stage 2: Technical Scope
    with pasta_tabs[1]:
        st.write("### Stage 2: Define Technical Scope")
        
        st.info("""
        **AWS Discovery Applied:**
        - Map data flows, not just servers
        - Identify trust boundaries
        - Document existing controls at each boundary
        """)
        
        st.write("**Exercise:** Map the complete technical scope")
        
        # Component checklist
        st.write("**Components in scope:**")
        components = st.multiselect(
            "Select all that apply:",
            [
                "React SPA (frontend)",
                "API Gateway (Kong)",
                "Auth Service (JWT issuer)",
                "Payment Service (core logic)",
                "Postgres DB (token storage)",
                "Redis (session store)",
                "Kafka (event streaming)",
                "Fraud Detection (ML)",
                "Stripe API (external)",
                "Cloudflare WAF",
                "AWS EKS (orchestration)",
                "Datadog (monitoring)"
            ],
            default=[
                "API Gateway (Kong)",
                "Auth Service (JWT issuer)",
                "Payment Service (core logic)",
                "Postgres DB (token storage)"
            ],
            key="pasta_components"
        )
        
        # Data flow documentation
        data_flows = st.text_area(
            "Document critical data flows:",
            value=st.session_state.pasta_analysis.get('stage2_flows', ''),
            placeholder="""Example:
1. User → React SPA → API Gateway (HTTPS/TLS 1.3)
2. API Gateway → Auth Service (mTLS, JWT validation)
3. Auth Service → Redis (session lookup)
4. Payment Service → Postgres (tokenized card data)
5. Payment Service → Stripe (via TLS, API key auth)

Trust boundaries:
- Internet → Cloudflare (DDoS protection)
- Cloudflare → API Gateway (WAF, rate limiting)
- API Gateway → Services (mTLS + JWT)
- Services → Databases (network policy + auth)""",
            height=200,
            key="stage2_flows"
        )
        
        if st.button("💾 Save Stage 2", key="save_stage2"):
            st.session_state.pasta_analysis['stage2_components'] = components
            st.session_state.pasta_analysis['stage2_flows'] = data_flows
            st.success("✅ Saved! Technical scope defined.")
    
    # Stage 3: Application Decomposition
    with pasta_tabs[2]:
        st.write("### Stage 3: Decompose the Application")
        
        st.info("""
        **Security Architecture Focus:**
        - Show security controls at EACH trust boundary
        - Identify where controls could fail (Unhappy Path)
        """)
        
        st.write("**Exercise:** Document security controls by layer")
        
        # Create control matrix
        control_layers = {
            "Perimeter (Internet → Cloudflare)": [
                "DDoS protection",
                "WAF rules (OWASP Top 10)",
                "Rate limiting",
                "TLS 1.3 enforcement"
            ],
            "API Gateway (Cloudflare → Kong)": [
                "OAuth 2.0 validation",
                "JWT signature verification",
                "API key management",
                "Request/response logging"
            ],
            "Service Mesh (Service ↔ Service)": [
                "mTLS (mutual authentication)",
                "Service-to-service authorization",
                "Network policies (Calico)",
                "Distributed tracing"
            ],
            "Data Layer (Services → Databases)": [
                "Encryption at rest (AES-256)",
                "Encryption in transit (TLS)",
                "Database auth (IAM)",
                "Query logging"
            ]
        }
        
        for layer, controls in control_layers.items():
            with st.expander(f"🔒 {layer}"):
                st.write("**Existing controls:**")
                for control in controls:
                    st.write(f"✅ {control}")
                
                # Unhappy path analysis
                unhappy_path = st.text_area(
                    "What happens if these controls FAIL?",
                    value=st.session_state.pasta_analysis.get(f'stage3_unhappy_{layer}', ''),
                    placeholder="Example: If WAF fails open, SQLi attacks reach API...",
                    height=80,
                    key=f"unhappy_{layer}"
                )
                
                if st.button(f"💾 Save", key=f"save_unhappy_{layer}"):
                    st.session_state.pasta_analysis[f'stage3_unhappy_{layer}'] = unhappy_path
                    st.success("✅")
        
        decomposition_notes = st.text_area(
            "Additional decomposition notes:",
            value=st.session_state.pasta_analysis.get('stage3_notes', ''),
            height=100,
            key="stage3_notes"
        )
        
        if st.button("💾 Save Stage 3", key="save_stage3"):
            st.session_state.pasta_analysis['stage3_notes'] = decomposition_notes
            st.success("✅ Saved! Application decomposed with unhappy paths.")
    
    # Stage 4: Threat Analysis
    with pasta_tabs[3]:
        st.write("### Stage 4: Threat Analysis (MITRE ATT&CK)")
        
        st.warning("""
        **Beyond Basic STRIDE:**
        - Map to MITRE ATT&CK tactics
        - Include full kill chain
        - Focus on REALISTIC threats (not nation-state if you're not a target)
        """)
        
        st.write("**Exercise:** Map threats to MITRE ATT&CK")
        
        # Pre-populated threat scenarios
        threat_scenarios = [
            {
                "id": "ato",
                "threat": "Account Takeover via Credential Stuffing",
                "mitre": "T1078 (Valid Accounts), T1110 (Brute Force)",
                "likelihood": "High",
                "impact": "Critical",
                "initial_access": "Credential stuffing (public breach databases)",
                "execution": "Login with valid credentials",
                "persistence": "Create API key with stolen account",
                "privilege_escalation": "N/A (already has user privileges)",
                "defense_evasion": "Use residential proxies to avoid IP blocking",
                "credential_access": "Already completed",
                "discovery": "Enumerate account permissions, linked cards",
                "lateral_movement": "N/A (single-tenant architecture)",
                "collection": "Download transaction history",
                "exfiltration": "API calls to export data",
                "impact": "Fraudulent transactions, data theft"
            },
            {
                "id": "api_key",
                "threat": "API Key Compromise (Merchant Integration)",
                "mitre": "T1552 (Unsecured Credentials), T1199 (Trusted Relationship)",
                "likelihood": "Medium",
                "impact": "High",
                "initial_access": "Merchant accidentally commits API key to GitHub",
                "execution": "Attacker uses API key to call payment API",
                "persistence": "API key doesn't expire (if no rotation)",
                "privilege_escalation": "API key has excessive permissions",
                "defense_evasion": "Normal API usage, hard to detect",
                "credential_access": "N/A (key is the credential)",
                "discovery": "API documentation reveals endpoints",
                "lateral_movement": "Access other merchant data if authz bug",
                "collection": "Query transaction data",
                "exfiltration": "Bulk data export via API",
                "impact": "Data breach, regulatory fine"
            }
        ]
        
        for scenario in threat_scenarios:
            with st.expander(f"🎯 {scenario['threat']}", expanded=True):
                st.error(f"**Likelihood:** {scenario['likelihood']} | **Impact:** {scenario['impact']}")
                
                st.write(f"**MITRE ATT&CK:** {scenario['mitre']}")
                
                # Kill chain visualization
                st.write("**Full Kill Chain:**")
                kill_chain_df = pd.DataFrame({
                    "Stage": [
                        "Initial Access",
                        "Execution",
                        "Persistence",
                        "Privilege Escalation",
                        "Defense Evasion",
                        "Credential Access",
                        "Discovery",
                        "Lateral Movement",
                        "Collection",
                        "Exfiltration",
                        "Impact"
                    ],
                    "Attacker Action": [
                        scenario['initial_access'],
                        scenario['execution'],
                        scenario['persistence'],
                        scenario['privilege_escalation'],
                        scenario['defense_evasion'],
                        scenario['credential_access'],
                        scenario['discovery'],
                        scenario['lateral_movement'],
                        scenario['collection'],
                        scenario['exfiltration'],
                        scenario['impact']
                    ]
                })
                st.dataframe(kill_chain_df, use_container_width=True)
                
                # Control analysis
                controls_stop = st.text_area(
                    "Which controls would STOP this attack?",
                    value=st.session_state.pasta_analysis.get(f'stage4_controls_{scenario["id"]}', ''),
                    placeholder="""Example:
- Rate limiting (slows credential stuffing)
- MFA (prevents takeover even with valid password)
- Anomaly detection (flags unusual login location)""",
                    height=100,
                    key=f"controls_{scenario['id']}"
                )
                
                controls_detect = st.text_area(
                    "Which controls would DETECT this attack?",
                    value=st.session_state.pasta_analysis.get(f'stage4_detect_{scenario["id"]}', ''),
                    placeholder="""Example:
- Failed login monitoring
- Velocity checks (100 logins in 1 minute = suspicious)
- SIEM alerting on multiple failed attempts""",
                    height=100,
                    key=f"detect_{scenario['id']}"
                )
                
                if st.button(f"💾 Save Analysis", key=f"save_threat_{scenario['id']}"):
                    st.session_state.pasta_analysis[f'stage4_controls_{scenario["id"]}'] = controls_stop
                    st.session_state.pasta_analysis[f'stage4_detect_{scenario["id"]}'] = controls_detect
                    st.success("✅")
        
        # Add custom threat
        st.write("---")
        st.write("**Add your own threat scenario:**")
        
        custom_threat = st.text_input("Threat name:", key="custom_threat_name")
        custom_mitre = st.text_input("MITRE ATT&CK tactics:", key="custom_threat_mitre")
        custom_killchain = st.text_area("Describe kill chain:", height=100, key="custom_threat_chain")
        
        if st.button("➕ Add Custom Threat", key="add_custom"):
            if custom_threat and custom_mitre:
                if 'custom_threats' not in st.session_state.pasta_analysis:
                    st.session_state.pasta_analysis['custom_threats'] = []
                st.session_state.pasta_analysis['custom_threats'].append({
                    'name': custom_threat,
                    'mitre': custom_mitre,
                    'killchain': custom_killchain
                })
                st.success(f"✅ Added: {custom_threat}")
    
    # Stage 5: Vulnerability Analysis
    with pasta_tabs[4]:
        st.write("### Stage 5: Vulnerability Analysis")
        
        st.info("""
        **Link threats to actual vulnerabilities:**
        - CVE/CWE mappings
        - Exploitability assessment
        - Likelihood based on attacker capability
        """)
        
        # Vulnerability scoring
        vuln_examples = [
            {
                "cwe": "CWE-285",
                "name": "Improper Authorization",
                "found_by": "Penetration test (15 instances)",
                "exploitability": "High",
                "public_exploits": "Yes",
                "threat_link": "Account Takeover, API Key Abuse"
            },
            {
                "cwe": "CWE-307",
                "name": "Improper Restriction of Excessive Authentication Attempts",
                "found_by": "Code review",
                "exploitability": "Medium",
                "public_exploits": "Yes",
                "threat_link": "Credential Stuffing"
            }
        ]
        
        st.write("**Known vulnerabilities from pen test:**")
        vuln_df = pd.DataFrame(vuln_examples)
        st.dataframe(vuln_df, use_container_width=True)
        
        vuln_analysis = st.text_area(
            "Vulnerability remediation priority:",
            value=st.session_state.pasta_analysis.get('stage5_vulns', ''),
            placeholder="""Priority 1 (Critical, fix in 7 days):
- CWE-285 in payment authorization logic
  
Priority 2 (High, fix in 30 days):
- CWE-307 (no rate limiting on login)""",
            height=150,
            key="stage5_vulns"
        )
        
        if st.button("💾 Save Stage 5", key="save_stage5"):
            st.session_state.pasta_analysis['stage5_vulns'] = vuln_analysis
            st.success("✅ Saved!")
    
    # Stage 6: Attack Modeling
    with pasta_tabs[5]:
        st.write("### Stage 6: Attack Modeling")
        
        st.warning("""
        **For each credible attack:**
        1. Enumerate full kill chain
        2. Identify which controls would detect/prevent at each stage
        3. Calculate residual risk (if Control X fails, does Control Y catch it?)
        """)
        
        st.write("**Exercise:** Defense-in-depth analysis")
        
        # Interactive attack path
        st.write("**Attack Path: Account Takeover**")
        
        attack_stages = [
            {"stage": "Initial Access", "control": "Rate limiting", "bypass": "Use distributed IPs"},
            {"stage": "Execution", "control": "MFA", "bypass": "SIM swap attack"},
            {"stage": "Persistence", "control": "Session timeout", "bypass": "Refresh tokens"},
            {"stage": "Impact", "control": "Transaction monitoring", "bypass": "Small transactions"}
        ]
        
        for idx, stage_data in enumerate(attack_stages):
            col1, col2, col3 = st.columns([2, 2, 3])
            with col1:
                st.write(f"**{stage_data['stage']}**")
            with col2:
                st.info(f"Control: {stage_data['control']}")
            with col3:
                st.error(f"Bypass: {stage_data['bypass']}")
            
            if idx < len(attack_stages) - 1:
                st.write("↓")
        
        st.write("---")
        
        defense_depth = st.text_area(
            "Document your defense-in-depth strategy:",
            value=st.session_state.pasta_analysis.get('stage6_defense', ''),
            placeholder="""Layer 1 (Prevent): Rate limiting + IP reputation
Layer 2 (Detect): Login anomaly detection
Layer 3 (Respond): Automatic account lock after 3 suspicious events
Layer 4 (Recover): Customer notification + password reset flow

Residual risk: If attacker has valid session + bypasses all controls, 
transaction monitoring is last line of defense.""",
            height=200,
            key="stage6_defense"
        )
        
        if st.button("💾 Save Stage 6", key="save_stage6"):
            st.session_state.pasta_analysis['stage6_defense'] = defense_depth
            st.success("✅ Saved!")
    
    # Stage 7: Risk & Impact Analysis (FAIR)
    with pasta_tabs[6]:
        st.write("### Stage 7: Risk & Impact Analysis")
        
        st.success("""
        **CRITICAL: Quantify in financial terms**
        
        Use FAIR model:
        - ALE (Annual Loss Expectancy) = LEF × SLE
        - LEF (Loss Event Frequency) = How often per year?
        - SLE (Single Loss Expectancy) = Cost if it happens once
        """)
        
        st.write("**Exercise:** Calculate ALE for top threat")
        
        # FAIR calculation
        st.write("**Threat: Account Takeover via Credential Stuffing**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Frequency Assessment**")
            tef = st.number_input(
                "Threat Event Frequency (attempts/year)",
                min_value=1, max_value=10000, value=500,
                help="How many times will attackers try this?",
                key="fair_tef"
            )
            vulnerability = st.slider(
                "Vulnerability (success rate %)",
                0.0, 100.0, 2.0, 0.5,
                help="What % of attempts succeed?",
                key="fair_vuln"
            )
            lef = tef * (vulnerability / 100)
            st.metric("Loss Event Frequency", f"{lef:.1f}/year")
        
        with col2:
            st.write("**Impact Assessment**")
            
            incident_response = st.number_input("Incident response ($K)", 10, 1000, 200, key="fair_ir")
            fraud_loss = st.number_input("Fraud per incident ($K)", 10, 10000, 500, key="fair_fraud")
            regulatory = st.number_input("Regulatory fines ($K)", 0, 5000, 500, key="fair_reg")
            churn = st.number_input("Customer churn cost ($K)", 0, 10000, 2000, key="fair_churn")
            
            sle = (incident_response + fraud_loss + regulatory + churn) * 1000
            st.metric("Single Loss Expectancy", f"${sle/1e6:.2f}M")
        
        # Calculate ALE
        ale = lef * sle
        
        st.write("---")
        st.write("### Final Risk Calculation")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Loss Events/Year", f"{lef:.1f}")
        with col2:
            st.metric("Cost per Event", f"${sle/1e6:.2f}M")
        with col3:
            st.metric("**Annual Loss Expectancy**", f"${ale/1e6:.1f}M", 
                     help="This is the expected annual cost")
        
        # Risk visualization
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=ale/1e6,
            title={'text': "Annual Loss Expectancy ($M)"},
            gauge={
                'axis': {'range': [None, 50]},
                'bar': {'color': "darkred" if ale/1e6 > 10 else "orange" if ale/1e6 > 5 else "green"},
                'steps': [
                    {'range': [0, 5], 'color': "lightgreen"},
                    {'range': [5, 10], 'color': "yellow"},
                    {'range': [10, 50], 'color': "lightcoral"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 10
                }
            }
        ))
        st.plotly_chart(fig, use_container_width=True)
        
        # Control cost-benefit
        st.write("---")
        st.write("**Control Cost-Benefit Analysis**")
        
        control_cost = st.number_input(
            "Proposed control investment ($K/year)",
            10, 5000, 500,
            help="Cost to implement improved controls",
            key="fair_control_cost"
        )
        
        risk_reduction = st.slider(
            "Expected risk reduction (%)",
            0, 100, 70,
            help="How much will controls reduce the risk?",
            key="fair_reduction"
        )
        
        new_ale = ale * (1 - risk_reduction/100)
        savings = ale - new_ale
        roi = ((savings - control_cost*1000) / (control_cost*1000)) * 100
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Current ALE", f"${ale/1e6:.1f}M")
        with col2:
            st.metric("New ALE", f"${new_ale/1e6:.1f}M", f"-${savings/1e6:.1f}M")
        with col3:
            st.metric("ROI", f"{roi:.0f}%", 
                     "Positive" if roi > 0 else "Negative",
                     delta_color="normal" if roi > 0 else "inverse")
        
        if roi > 0:
            st.success(f"""
            ✅ **Business Case: APPROVED**
            
            Invest ${control_cost}K to reduce risk by ${savings/1e6:.1f}M
            ROI: {roi:.0f}% in first year
            Payback period: {control_cost*1000/savings*12:.1f} months
            """)
        else:
            st.warning(f"""
            ⚠️ **Business Case: MARGINAL**
            
            Control cost (${control_cost}K) exceeds risk reduction (${savings/1e6:.1f}M)
            Consider: Alternative controls, risk acceptance, or transfer (insurance)
            """)
        
        # Save final analysis
        fair_summary = st.text_area(
            "Final risk recommendation:",
            value=st.session_state.pasta_analysis.get('stage7_recommendation', ''),
            placeholder=f"""Based on FAIR analysis:

Current risk: ${ale/1e6:.1f}M annual expected loss
Proposed controls: ${control_cost}K investment
Expected outcome: ${new_ale/1e6:.1f}M residual risk ({risk_reduction}% reduction)

Recommendation: [ACCEPT / MITIGATE / TRANSFER / AVOID]

Justification: ...""",
            height=200,
            key="stage7_recommendation"
        )
        
        if st.button("💾 Save Stage 7", key="save_stage7"):
            st.session_state.pasta_analysis['stage7_recommendation'] = fair_summary
            st.session_state.pasta_analysis['stage7_fair'] = {
                'tef': tef,
                'vulnerability': vulnerability,
                'lef': lef,
                'sle': sle,
                'ale': ale,
                'control_cost': control_cost * 1000,
                'risk_reduction': risk_reduction,
                'new_ale': new_ale,
                'roi': roi
            }
            st.success("✅ Saved!")
    
    # ========================================================================
    # PART 4: SYNTHESIS & DELIVERABLE
    # ========================================================================
    
    st.markdown("---")
    st.subheader("📊 Complete Threat Model Report")
    
    if st.button("📑 Generate PASTA Report", use_container_width=True, type="primary"):
        generate_pasta_report()
    
    # Check completion
    stages_complete = sum([
        bool(st.session_state.pasta_analysis.get('stage1_objectives')),
        bool(st.session_state.pasta_analysis.get('stage2_flows')),
        bool(st.session_state.pasta_analysis.get('stage3_notes')),
        bool(st.session_state.pasta_analysis.get('stage4_controls_ato')),
        bool(st.session_state.pasta_analysis.get('stage5_vulns')),
        bool(st.session_state.pasta_analysis.get('stage6_defense')),
        bool(st.session_state.pasta_analysis.get('stage7_recommendation'))
    ])
    
    st.progress(stages_complete / 7)
    st.caption(f"Completion: {stages_complete}/7 stages")
    
    if stages_complete == 7:
        st.success("🎉 All PASTA stages complete!")
        
        if st.button("✅ Mark Exercise Complete", use_container_width=True):
            mark_exercise_complete('pasta_payment_api')
            st.balloons()
            st.info("Proceeding to next subsection...")
            time.sleep(2)
            # Navigate to next subsection
            st.session_state.current_subsection += 1
            st.rerun()

def generate_pasta_report():
    """Generate comprehensive PASTA threat model report"""
    
    st.subheader("🎯 Payment API Threat Model - Executive Summary")
    
    # Get data
    metrics = st.session_state.pasta_analysis.get('stage1_metrics', {})
    fair = st.session_state.pasta_analysis.get('stage7_fair', {})
    
    # Executive dashboard
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Daily Volume", f"${metrics.get('revenue', 0)}M")
    with col2:
        st.metric("Current ALE", f"${fair.get('ale', 0)/1e6:.1f}M")
    with col3:
        st.metric("With Controls", f"${fair.get('new_ale', 0)/1e6:.1f}M")
    with col4:
        roi = fair.get('roi', 0)
        st.metric("ROI", f"{roi:.0f}%", 
                 "Invest" if roi > 0 else "Review")
    
    # Key findings
    st.write("### 🔍 Key Findings")
    
    findings = [
        f"✅ **Stage 1:** Business impact quantified at ${fair.get('ale', 0)/1e6:.1f}M annual expected loss",
        f"✅ **Stage 2-3:** {len(st.session_state.pasta_analysis.get('stage2_components', []))} components analyzed with trust boundaries mapped",
        "✅ **Stage 4:** Top threats mapped to MITRE ATT&CK (Account Takeover, API Key Compromise)",
        "✅ **Stage 5:** 15 authorization vulnerabilities from pen test prioritized",
        "✅ **Stage 6:** Defense-in-depth strategy documented with residual risk analysis",
        f"✅ **Stage 7:** FAIR analysis shows {fair.get('roi', 0):.0f}% ROI on proposed controls"
    ]
    
    for finding in findings:
        st.write(finding)
    
    # Recommendations
    st.write("### 💡 Recommendations")
    
    st.info("""
    **Priority 1 (Immediate - 30 days):**
    1. Fix 15 authorization bugs from pen test
    2. Implement MFA for all user accounts
    3. Add rate limiting on authentication endpoints
    
    **Priority 2 (90 days):**
    1. Implement anomaly detection (login patterns)
    2. Add transaction velocity checks
    3. Improve API key management (rotation, scoping)
    
    **Priority 3 (6 months):**
    1. Migrate to Zero Trust architecture (BeyondCorp)
    2. Implement continuous authentication
    3. Add ML-based fraud detection
    """)
    
    # Download report
    report_data = {
        "metadata": {
            "date": datetime.now().isoformat(),
            "analyst": "Enterprise Security Architect",
            "system": "Payment API",
            "methodology": "PASTA 7-Stage"
        },
        "findings": st.session_state.pasta_analysis,
        "recommendations": "See report above"
    }
    
    report_json = json.dumps(report_data, indent=2, default=str)
    
    st.download_button(
        "📥 Download Complete Threat Model (JSON)",
        report_json,
        file_name=f"pasta_threat_model_{datetime.now().strftime('%Y%m%d')}.json",
        mime="application/json",
        use_container_width=True
    )

def mark_exercise_complete(exercise_id):
    """Mark exercise complete"""
    if 'completed_exercises' not in st.session_state:
        st.session_state['completed_exercises'] = []
    if exercise_id not in st.session_state.completed_exercises:
        st.session_state.completed_exercises.append(exercise_id)

# Initialize session state for this example
if 'pasta_analysis' not in st.session_state:
    st.session_state.pasta_analysis = {}

# Render the complete example
if __name__ == "__main__":
    render_1_2_1_pasta_complete_example()
