"""
COMPLETE ENTERPRISE SECURITY ARCHITECTURE WORKSHOP
Professional-Grade Training Platform with Integrated Diagramming

End-to-End Journey:
Phase 1: Enterprise Architect - Requirements & High-Level Design
Phase 2: Solution Architect - Detailed Design & STRIDE
Phase 3: Security Patterns & Production

Features:
✓ Professional Diagramming Tool (draw.io equivalent)
✓ Interactive STRIDE Canvas
✓ Code-Locked Answer Keys
✓ Complete Progress Tracking
✓ Portfolio Generation
✓ Instructor-Led + Self-Learning Paths
"""

import streamlit as st
import pandas as pd
import json
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px
from streamlit_drawable_canvas import st_canvas
import base64
from io import BytesIO
from PIL import Image
import hashlib

st.set_page_config(
    page_title="Enterprise Security Architecture Workshop",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# PROFESSIONAL STYLING
# ============================================================================

st.markdown("""
<style>
    /* Main Layout */
    .main > div { padding-top: 2rem; }
    
    /* Headers */
    .phase-header {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
        color: white; padding: 2rem; border-radius: 12px;
        margin-bottom: 2rem; box-shadow: 0 10px 25px rgba(59, 130, 246, 0.3);
    }
    .module-header {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: white; padding: 1.5rem; border-radius: 10px;
        margin-bottom: 1.5rem; box-shadow: 0 8px 20px rgba(0,0,0,0.2);
    }
    
    /* Cards */
    .instructor-card {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        border: 3px solid #f59e0b; padding: 2rem; margin: 1.5rem 0;
        border-radius: 12px; box-shadow: 0 6px 15px rgba(245, 158, 11, 0.2);
    }
    .exercise-card {
        background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
        border: 3px solid #3b82f6; padding: 2rem; margin: 1.5rem 0;
        border-radius: 12px; box-shadow: 0 6px 15px rgba(59, 130, 246, 0.2);
    }
    .answer-card {
        background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
        border: 3px solid #10b981; padding: 2rem; margin: 1.5rem 0;
        border-radius: 12px; box-shadow: 0 6px 15px rgba(16, 185, 129, 0.2);
    }
    
    /* Diagram Canvas */
    .diagram-workspace {
        background: white; border: 3px solid #e5e7eb;
        border-radius: 12px; padding: 1.5rem; margin: 1rem 0;
        box-shadow: 0 8px 20px rgba(0,0,0,0.1);
    }
    .diagram-toolbar {
        background: #f8fafc; padding: 1rem; border-radius: 8px;
        margin-bottom: 1rem; display: flex; gap: 1rem; flex-wrap: wrap;
    }
    .tool-button {
        background: white; border: 2px solid #e5e7eb;
        padding: 0.75rem 1.5rem; border-radius: 8px; cursor: pointer;
        transition: all 0.3s; font-weight: 600;
    }
    .tool-button:hover {
        border-color: #3b82f6; background: #eff6ff;
        box-shadow: 0 4px 10px rgba(59, 130, 246, 0.2);
    }
    .tool-button.active {
        background: #3b82f6; color: white; border-color: #2563eb;
    }
    
    /* Component Library */
    .component-library {
        background: white; border: 2px solid #e5e7eb;
        border-radius: 10px; padding: 1rem; margin: 1rem 0;
        max-height: 600px; overflow-y: auto;
    }
    .component-item {
        background: #f8fafc; border: 2px solid #e5e7eb;
        padding: 1rem; margin: 0.5rem 0; border-radius: 8px;
        cursor: grab; transition: all 0.3s;
    }
    .component-item:hover {
        border-color: #3b82f6; box-shadow: 0 4px 10px rgba(59, 130, 246, 0.2);
        transform: translateY(-2px);
    }
    
    /* STRIDE Canvas */
    .stride-section {
        background: white; border-left: 5px solid #ef4444;
        padding: 1.5rem; margin: 1rem 0; border-radius: 8px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }
    .stride-spoofing { border-left-color: #ef4444; }
    .stride-tampering { border-left-color: #f59e0b; }
    .stride-repudiation { border-left-color: #3b82f6; }
    .stride-information { border-left-color: #ec4899; }
    .stride-dos { border-left-color: #8b5cf6; }
    .stride-elevation { border-left-color: #f97316; }
    
    /* Progress */
    .progress-bar {
        background: #e5e7eb; height: 8px; border-radius: 4px;
        overflow: hidden; margin: 0.5rem 0;
    }
    .progress-fill {
        background: linear-gradient(90deg, #3b82f6 0%, #8b5cf6 100%);
        height: 100%; transition: width 0.5s ease;
    }
    
    /* Code Lock */
    .code-lock {
        background: linear-gradient(135deg, #f5f3ff 0%, #ede9fe 100%);
        border: 3px dashed #8b5cf6; padding: 2rem; margin: 1.5rem 0;
        border-radius: 12px; text-align: center;
    }
    .code-input {
        font-size: 1.5rem; letter-spacing: 0.5rem; text-align: center;
        padding: 1rem; margin: 1rem 0; border: 3px solid #8b5cf6;
        border-radius: 8px; font-family: 'Courier New', monospace;
    }
    
    /* Trust Boundaries */
    .trust-dmz { background: #fef2f2; border: 3px solid #dc2626; }
    .trust-app { background: #fef3c7; border: 3px solid #f59e0b; }
    .trust-data { background: #dcfce7; border: 3px solid #16a34a; }
    .trust-external { background: #f3e8ff; border: 3px solid #9333ea; }
    
    /* Artifact Badge */
    .artifact-badge {
        display: inline-block; background: #3b82f6; color: white;
        padding: 0.5rem 1rem; border-radius: 20px; font-size: 0.9rem;
        font-weight: 600; margin: 0.25rem;
    }
    
    /* Export Buttons */
    .export-btn {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white; padding: 0.75rem 1.5rem; border-radius: 8px;
        border: none; font-weight: 600; cursor: pointer;
        box-shadow: 0 4px 10px rgba(16, 185, 129, 0.3);
        transition: all 0.3s;
    }
    .export-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 15px rgba(16, 185, 129, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

def init_state():
    """Initialize comprehensive session state"""
    defaults = {
        # Workshop Progress
        'current_phase': 1,
        'current_module': '1.1',
        'learning_mode': 'instructor_led',  # or 'self_learning'
        'completed_modules': [],
        'unlock_codes': {},
        
        # User Info
        'team_name': 'Security Architecture Team',
        'participant_name': '',
        
        # Phase 1: Enterprise Architect
        'business_requirements': {},
        'security_requirements': [],
        'high_level_architecture': {},
        'arb_presentation': {},
        
        # Phase 2: Solution Architect
        'component_breakdown': [],
        'stride_analysis': {},
        'detailed_diagrams': {},
        'data_flows': [],
        
        # Phase 3: Patterns
        'security_patterns': [],
        'implementation_plans': {},
        
        # Diagrams
        'diagrams_created': [],
        'current_diagram': None,
        'diagram_components': [],
        
        # Artifacts
        'artifacts': {
            'requirements_docs': [],
            'architecture_diagrams': [],
            'threat_models': [],
            'security_patterns': [],
            'presentations': []
        },
        
        # Progress Tracking
        'progress': {
            'phase1': 0,
            'phase2': 0,
            'phase3': 0,
            'overall': 0
        },
        
        # Grading
        'grades': {},
        
        # Portfolio
        'portfolio_ready': False
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_state()

# ============================================================================
# UNLOCK CODE SYSTEM
# ============================================================================

UNLOCK_CODES = {
    '1.1': 'ARCH-2024-M11',
    '1.2': 'ARCH-2024-M12',
    '1.3': 'ARCH-2024-M13',
    '1.4': 'ARCH-2024-M14',
    '2.1': 'ARCH-2024-M21',
    '2.2': 'ARCH-2024-M22',
    '2.3': 'ARCH-2024-M23',
    '3.1': 'ARCH-2024-M31',
    '3.2': 'ARCH-2024-M32'
}

def generate_code_hash(code: str) -> str:
    """Generate hash for code verification"""
    return hashlib.sha256(code.encode()).hexdigest()

def verify_unlock_code(module: str, entered_code: str) -> bool:
    """Verify if unlock code is correct"""
    correct_code = UNLOCK_CODES.get(module)
    if not correct_code:
        return False
    return entered_code.strip().upper() == correct_code

def unlock_answer_key(module: str):
    """Show unlock interface for answer key"""
    st.markdown(f"""
    <div class="code-lock">
        <h3>🔐 Answer Key Locked</h3>
        <p>Complete the instructor-led section to receive your unlock code</p>
        <p><strong>Module {module}</strong></p>
    </div>
    """, unsafe_allow_html=True)
    
    unlock_code = st.text_input(
        "Enter Unlock Code:",
        key=f"unlock_{module}",
        placeholder="ARCH-2024-XXX",
        help="Code provided after completing instructor-led section"
    ).upper()
    
    if st.button("🔓 Unlock Answer Key", key=f"btn_unlock_{module}"):
        if verify_unlock_code(module, unlock_code):
            st.session_state.unlock_codes[module] = True
            st.success("✅ Answer key unlocked!")
            st.rerun()
        else:
            st.error("❌ Invalid code. Please complete the instructor-led section first.")
    
    return st.session_state.unlock_codes.get(module, False)

# ============================================================================
# PROFESSIONAL DIAGRAMMING TOOL
# ============================================================================

# Component Library for Architecture Diagrams
COMPONENT_LIBRARY = {
    "Web & Mobile": {
        "Web Application": {"color": "#3b82f6", "icon": "🌐", "trust": "untrusted"},
        "Mobile App": {"color": "#8b5cf6", "icon": "📱", "trust": "untrusted"},
        "SPA Frontend": {"color": "#06b6d4", "icon": "⚛️", "trust": "untrusted"}
    },
    "API & Gateway": {
        "API Gateway": {"color": "#10b981", "icon": "🚪", "trust": "semi-trusted"},
        "Load Balancer": {"color": "#14b8a6", "icon": "⚖️", "trust": "semi-trusted"},
        "Service Mesh": {"color": "#22c55e", "icon": "🕸️", "trust": "trusted"}
    },
    "Services": {
        "Microservice": {"color": "#f59e0b", "icon": "⚙️", "trust": "trusted"},
        "API Service": {"color": "#f97316", "icon": "🔌", "trust": "trusted"},
        "Background Worker": {"color": "#fb923c", "icon": "⏱️", "trust": "trusted"}
    },
    "Data": {
        "Database": {"color": "#ef4444", "icon": "🗄️", "trust": "trusted"},
        "Cache": {"color": "#ec4899", "icon": "⚡", "trust": "trusted"},
        "Object Storage": {"color": "#f43f5e", "icon": "📦", "trust": "trusted"},
        "Message Queue": {"color": "#e11d48", "icon": "📨", "trust": "trusted"}
    },
    "Security": {
        "Firewall": {"color": "#dc2626", "icon": "🔥", "trust": "security"},
        "WAF": {"color": "#b91c1c", "icon": "🛡️", "trust": "security"},
        "HSM": {"color": "#991b1b", "icon": "🔐", "trust": "security"},
        "SIEM": {"color": "#7f1d1d", "icon": "👁️", "trust": "security"}
    },
    "Identity": {
        "OAuth Server": {"color": "#6366f1", "icon": "🔑", "trust": "trusted"},
        "Identity Provider": {"color": "#4f46e5", "icon": "👤", "trust": "trusted"},
        "MFA Service": {"color": "#4338ca", "icon": "🔢", "trust": "trusted"}
    },
    "External": {
        "Third-Party API": {"color": "#9333ea", "icon": "🌍", "trust": "external"},
        "Cloud Service": {"color": "#a855f7", "icon": "☁️", "trust": "external"},
        "Partner System": {"color": "#c084fc", "icon": "🤝", "trust": "external"}
    }
}

def render_professional_diagram_tool():
    """Professional-grade diagramming tool"""
    
    st.markdown('<div class="diagram-workspace">', unsafe_allow_html=True)
    
    st.subheader("🎨 Professional Architecture Diagram Designer")
    
    # Toolbar
    st.markdown('<div class="diagram-toolbar">', unsafe_allow_html=True)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        diagram_mode = st.selectbox(
            "Mode:",
            ["Select", "Draw", "Component", "Connect", "Annotate"],
            key="diagram_mode"
        )
    
    with col2:
        drawing_tool = st.selectbox(
            "Tool:",
            ["freedraw", "line", "rect", "circle", "transform"],
            key="drawing_tool"
        )
    
    with col3:
        stroke_width = st.slider("Width:", 1, 10, 3, key="stroke_width")
    
    with col4:
        stroke_color = st.color_picker("Color:", "#000000", key="stroke_color")
    
    with col5:
        bg_color = st.color_picker("Background:", "#FFFFFF", key="bg_color")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Main canvas area with component library
    col_library, col_canvas = st.columns([1, 3])
    
    with col_library:
        st.markdown('<div class="component-library">', unsafe_allow_html=True)
        st.write("**📦 Component Library**")
        
        for category, components in COMPONENT_LIBRARY.items():
            with st.expander(f"**{category}**", expanded=False):
                for comp_name, comp_info in components.items():
                    st.markdown(f"""
                    <div class="component-item">
                        <span style="font-size: 1.5rem;">{comp_info['icon']}</span>
                        <strong>{comp_name}</strong><br>
                        <small>Trust: {comp_info['trust']}</small>
                    </div>
                    """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_canvas:
        st.write("**🖼️ Drawing Canvas**")
        
        # Interactive canvas
        canvas_result = st_canvas(
            fill_color="rgba(255, 255, 255, 0)",
            stroke_width=stroke_width,
            stroke_color=stroke_color,
            background_color=bg_color,
            height=600,
            width=800,
            drawing_mode=drawing_tool,
            key="architecture_canvas"
        )
        
        # Save diagram
        col_save1, col_save2, col_save3 = st.columns(3)
        
        with col_save1:
            diagram_name = st.text_input("Diagram Name:", "Architecture Diagram")
        
        with col_save2:
            diagram_type = st.selectbox(
                "Type:",
                ["High-Level Architecture", "Component Diagram", "Data Flow",
                 "Sequence Diagram", "C4 Context", "C4 Container"]
            )
        
        with col_save3:
            if st.button("💾 Save Diagram", type="primary"):
                if canvas_result.image_data is not None:
                    # Convert to base64
                    img = Image.fromarray(canvas_result.image_data.astype('uint8'), 'RGBA')
                    buf = BytesIO()
                    img.save(buf, format='PNG')
                    
                    diagram_data = {
                        'name': diagram_name,
                        'type': diagram_type,
                        'timestamp': datetime.now().isoformat(),
                        'image': base64.b64encode(buf.getvalue()).decode(),
                        'components': st.session_state.diagram_components
                    }
                    
                    st.session_state.diagrams_created.append(diagram_data)
                    st.session_state.artifacts['architecture_diagrams'].append(diagram_data)
                    st.success(f"✅ Diagram '{diagram_name}' saved!")
                    st.balloons()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Show saved diagrams
    if st.session_state.diagrams_created:
        st.write("---")
        st.subheader("📁 Your Saved Diagrams")
        
        cols = st.columns(3)
        for idx, diagram in enumerate(st.session_state.diagrams_created):
            with cols[idx % 3]:
                st.write(f"**{diagram['name']}**")
                st.caption(f"Type: {diagram['type']}")
                
                # Show thumbnail
                img_data = base64.b64decode(diagram['image'])
                img = Image.open(BytesIO(img_data))
                st.image(img, use_container_width=True)
                
                # Download button
                st.download_button(
                    "📥 Download PNG",
                    img_data,
                    f"{diagram['name']}.png",
                    "image/png",
                    key=f"download_diagram_{idx}"
                )

# ============================================================================
# INTERACTIVE STRIDE CANVAS
# ============================================================================

def render_stride_canvas():
    """Interactive STRIDE threat modeling canvas"""
    
    st.subheader("⚔️ Interactive STRIDE Threat Modeling")
    
    # Component selector
    component = st.selectbox(
        "Select Component to Analyze:",
        ["API Gateway", "Payment Service", "Customer Database", "Custom Component"],
        key="stride_component"
    )
    
    if component == "Custom Component":
        component = st.text_input("Enter component name:", key="stride_custom_comp")
    
    # STRIDE Categories
    stride_categories = {
        "Spoofing": {
            "color": "#ef4444",
            "description": "Identity/authentication attacks",
            "examples": ["Fake credentials", "Token theft", "Man-in-the-middle"]
        },
        "Tampering": {
            "color": "#f59e0b",
            "description": "Data integrity attacks",
            "examples": ["Modified requests", "SQL injection", "Replay attacks"]
        },
        "Repudiation": {
            "color": "#3b82f6",
            "description": "Non-repudiation failures",
            "examples": ["No audit trail", "Unsigned transactions", "Deniability"]
        },
        "Information Disclosure": {
            "color": "#ec4899",
            "description": "Confidentiality breaches",
            "examples": ["Data leakage", "Excessive permissions", "Information in errors"]
        },
        "Denial of Service": {
            "color": "#8b5cf6",
            "description": "Availability attacks",
            "examples": ["Resource exhaustion", "DDoS", "Algorithmic complexity"]
        },
        "Elevation of Privilege": {
            "color": "#f97316",
            "description": "Authorization bypass",
            "examples": ["Privilege escalation", "Scope bypass", "Broken access control"]
        }
    }
    
    if 'stride_threats' not in st.session_state:
        st.session_state.stride_threats = {cat: [] for cat in stride_categories.keys()}
    
    # Tabs for each STRIDE category
    tabs = st.tabs(list(stride_categories.keys()))
    
    for idx, (category, info) in enumerate(stride_categories.items()):
        with tabs[idx]:
            st.markdown(f"""
            <div class="stride-section stride-{category.lower().replace(' ', '')}">
                <h4>{category}</h4>
                <p><em>{info['description']}</em></p>
            </div>
            """, unsafe_allow_html=True)
            
            # Add threat
            with st.form(f"add_threat_{category}"):
                st.write("**➕ Add Threat**")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    threat_desc = st.text_area(
                        "Threat Description:",
                        placeholder=f"Example: {info['examples'][0]}",
                        key=f"threat_desc_{category}"
                    )
                    
                    attack_vector = st.text_input(
                        "Attack Vector:",
                        placeholder="How could attacker exploit this?",
                        key=f"attack_vector_{category}"
                    )
                
                with col2:
                    mitigation = st.text_area(
                        "Mitigation/Control:",
                        placeholder="How do you prevent/detect this?",
                        key=f"mitigation_{category}"
                    )
                    
                    likelihood = st.select_slider(
                        "Likelihood:",
                        options=["Very Low", "Low", "Medium", "High", "Very High"],
                        value="Medium",
                        key=f"likelihood_{category}"
                    )
                    
                    impact = st.select_slider(
                        "Impact:",
                        options=["Very Low", "Low", "Medium", "High", "Critical"],
                        value="Medium",
                        key=f"impact_{category}"
                    )
                
                if st.form_submit_button("➕ Add to STRIDE Model"):
                    threat_entry = {
                        'component': component,
                        'category': category,
                        'threat': threat_desc,
                        'attack_vector': attack_vector,
                        'mitigation': mitigation,
                        'likelihood': likelihood,
                        'impact': impact,
                        'timestamp': datetime.now().isoformat()
                    }
                    
                    st.session_state.stride_threats[category].append(threat_entry)
                    st.success(f"✅ Threat added to {category}")
                    st.rerun()
            
            # Display current threats
            if st.session_state.stride_threats[category]:
                st.write("**Current Threats:**")
                for i, threat in enumerate(st.session_state.stride_threats[category]):
                    with st.expander(f"{threat['threat'][:50]}..."):
                        st.write(f"**Attack Vector:** {threat['attack_vector']}")
                        st.write(f"**Mitigation:** {threat['mitigation']}")
                        st.write(f"**Likelihood:** {threat['likelihood']} | **Impact:** {threat['impact']}")
    
    # Export STRIDE model
    st.write("---")
    if st.button("💾 Save Complete STRIDE Model", type="primary"):
        stride_model = {
            'component': component,
            'threats': st.session_state.stride_threats,
            'timestamp': datetime.now().isoformat()
        }
        
        if 'stride_analysis' not in st.session_state.artifacts:
            st.session_state.artifacts['stride_analysis'] = []
        
        st.session_state.artifacts['threat_models'].append(stride_model)
        st.success("✅ STRIDE model saved to artifacts!")
        st.balloons()

# ============================================================================
# PHASE 1: ENTERPRISE ARCHITECT MODULES
# ============================================================================

def render_module_1_1():
    """Module 1.1: Capturing Business Requirements"""
    
    st.markdown("""
    <div class="module-header">
        <h2>Module 1.1: Capturing Business Requirements</h2>
        <p>Duration: 60 minutes | Deliverable: Business Requirements Document</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Mode selector
    mode = st.radio(
        "Choose Learning Mode:",
        ["👨‍🏫 Instructor-Led Example", "📝 Student Exercise"],
        horizontal=True,
        key="mode_1_1"
    )
    
    if mode.startswith("👨‍🏫"):
        # Instructor-led example
        st.markdown("""
        <div class="instructor-card">
            <h3>📘 Instructor Example: Payment Platform Requirements</h3>
            
            <h4>Scenario</h4>
            <p><strong>Stakeholder:</strong> CFO of FinServe Global</p>
            <p><strong>Request:</strong> "We need to process payments securely and handle $500M/month"</p>
            
            <h4>Enterprise Architect Translation Process</h4>
            
            <table style="width: 100%; border-collapse: collapse; margin-top: 1rem;">
            <tr style="background: #f59e0b; color: white;">
                <th style="padding: 0.75rem; text-align: left;">Business Statement</th>
                <th style="padding: 0.75rem; text-align: left;">Architect Translation</th>
                <th style="padding: 0.75rem; text-align: left;">Security Requirement</th>
            </tr>
            <tr style="background: white;">
                <td style="padding: 0.75rem; border: 1px solid #e5e7eb;">"Secure payments"</td>
                <td style="padding: 0.75rem; border: 1px solid #e5e7eb;">PCI-DSS Level 1 compliance required</td>
                <td style="padding: 0.75rem; border: 1px solid #e5e7eb;">Never store card data, use tokenization</td>
            </tr>
            <tr style="background: #fef3c7;">
                <td style="padding: 0.75rem; border: 1px solid #e5e7eb;">"$500M/month volume"</td>
                <td style="padding: 0.75rem; border: 1px solid #e5e7eb;">High availability, scalability required</td>
                <td style="padding: 0.75rem; border: 1px solid #e5e7eb;">99.99% uptime, DDoS protection</td>
            </tr>
            <tr style="background: white;">
                <td style="padding: 0.75rem; border: 1px solid #e5e7eb;">"Customer trust"</td>
                <td style="padding: 0.75rem; border: 1px solid #e5e7eb;">Data privacy and breach protection</td>
                <td style="padding: 0.75rem; border: 1px solid #e5e7eb;">Encryption at rest & in transit, GDPR compliance</td>
            </tr>
            </table>
            
            <h4 style="margin-top: 1.5rem;">Complete Business Requirements Document</h4>
            
            <p><strong>1. Business Goals:</strong></p>
            <ul>
                <li>Process $500M/month in payment transactions</li>
                <li>Achieve PCI-DSS Level 1 certification</li>
                <li>Maintain 99.99% uptime</li>
                <li>Support international customers (GDPR compliance)</li>
            </ul>
            
            <p><strong>2. Stakeholder Requirements:</strong></p>
            <ul>
                <li><strong>CFO:</strong> Cost control, risk quantification ($5M max loss exposure)</li>
                <li><strong>CTO:</strong> Modern architecture, cloud-native, microservices</li>
                <li><strong>Legal:</strong> GDPR, PCI-DSS, SOX compliance</li>
                <li><strong>CISO:</strong> Zero-trust architecture, audit trail</li>
            </ul>
            
            <p><strong>3. Constraints:</strong></p>
            <ul>
                <li>Budget: $3M for security architecture</li>
                <li>Timeline: 18 months to production</li>
                <li>Cannot disrupt existing payment processing</li>
                <li>Must integrate with legacy on-prem identity system</li>
            </ul>
            
            <p><strong>4. Success Criteria:</strong></p>
            <ul>
                <li>PCI-DSS audit pass</li>
                <li>Zero data breaches</li>
                <li>< 100ms API latency</li>
                <li>Cost per transaction < $0.10</li>
            </ul>
            
        </div>
        """, unsafe_allow_html=True)
        
        # Show unlock code
        st.success(f"✅ Module 1.1 Instructor Section Complete! Your unlock code: **{UNLOCK_CODES['1.1']}**")
        
    else:
        # Student exercise
        st.markdown("""
        <div class="exercise-card">
            <h3>📝 Student Exercise: Healthcare Telemedicine Platform</h3>
            
            <h4>Scenario</h4>
            <p><strong>Stakeholder:</strong> CTO of HealthConnect</p>
            <p><strong>Request:</strong> "We want to build a telemedicine platform where doctors conduct video consultations 
            with patients. We need to protect patient medical records and comply with HIPAA. System should work on mobile 
            devices and allow doctors to access patient histories securely."</p>
            
            <h4>Your Task</h4>
            <p>Translate this business request into a structured Business Requirements Document.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Exercise form
        st.write("### 1. Business Goals")
        business_goals = st.text_area(
            "List 3-5 business goals:",
            height=150,
            placeholder="Example:\n- Enable remote patient consultations\n- Achieve HIPAA compliance\n- Support 10,000 concurrent video sessions",
            key="ex_business_goals_1_1"
        )
        
        st.write("### 2. Stakeholder Requirements")
        
        col1, col2 = st.columns(2)
        with col1:
            cto_req = st.text_area("CTO Requirements:", key="ex_cto_1_1")
            legal_req = st.text_area("Legal Requirements:", key="ex_legal_1_1")
        with col2:
            ciso_req = st.text_area("CISO Requirements:", key="ex_ciso_1_1")
            cmo_req = st.text_area("CMO (Medical) Requirements:", key="ex_cmo_1_1")
        
        st.write("### 3. Constraints")
        constraints = st.text_area(
            "List constraints:",
            height=100,
            placeholder="Budget, timeline, technical, regulatory...",
            key="ex_constraints_1_1"
        )
        
        st.write("### 4. Success Criteria")
        success_criteria = st.text_area(
            "Define measurable success criteria:",
            height=100,
            placeholder="HIPAA audit pass, zero PHI breaches, video latency < 200ms...",
            key="ex_success_1_1"
        )
        
        # Save and check answer
        col_save, col_answer = st.columns(2)
        
        with col_save:
            if st.button("💾 Save My Work", type="primary"):
                exercise_data = {
                    'business_goals': business_goals,
                    'stakeholder_reqs': {
                        'cto': cto_req,
                        'legal': legal_req,
                        'ciso': ciso_req,
                        'cmo': cmo_req
                    },
                    'constraints': constraints,
                    'success_criteria': success_criteria,
                    'timestamp': datetime.now().isoformat()
                }
                st.session_state.business_requirements = exercise_data
                st.session_state.artifacts['requirements_docs'].append(exercise_data)
                st.success("✅ Your work has been saved!")
        
        with col_answer:
            if st.button("🔓 View Answer Key"):
                if unlock_answer_key('1.1'):
                    show_answer_key_1_1()

def show_answer_key_1_1():
    """Show answer key for Module 1.1"""
    st.markdown("""
    <div class="answer-card">
        <h3>✅ Answer Key: Healthcare Telemedicine Platform</h3>
        
        <h4>1. Business Goals</h4>
        <ul>
            <li>Enable remote patient consultations via HIPAA-compliant video platform</li>
            <li>Achieve HIPAA compliance and pass certification audit</li>
            <li>Support 10,000 concurrent video sessions with < 200ms latency</li>
            <li>Secure access to electronic health records (EHR) for authorized clinicians</li>
            <li>Provide emergency break-glass access for life-threatening situations</li>
        </ul>
        
        <h4>2. Stakeholder Requirements</h4>
        <p><strong>CTO Requirements:</strong></p>
        <ul>
            <li>Modern microservices architecture</li>
            <li>Cloud-native deployment (AWS/Azure/GCP)</li>
            <li>Mobile-first design (iOS/Android apps)</li>
            <li>Integration with existing EHR systems (HL7/FHIR)</li>
        </ul>
        
        <p><strong>Legal Requirements:</strong></p>
        <ul>
            <li>HIPAA Title II compliance (Privacy and Security Rules)</li>
            <li>BAA (Business Associate Agreement) with vendors</li>
            <li>State medical board requirements compliance</li>
            <li>7-year audit log retention</li>
        </ul>
        
        <p><strong>CISO Requirements:</strong></p>
        <ul>
            <li>End-to-end encryption for video and data</li>
            <li>Multi-factor authentication (MFA) for all users</li>
            <li>Role-based access control (RBAC)</li>
            <li>Immutable audit trail</li>
            <li>Data loss prevention (DLP)</li>
        </ul>
        
        <p><strong>CMO (Chief Medical Officer) Requirements:</strong></p>
        <ul>
            <li>Usability: < 3 clicks to start consultation</li>
            <li>Emergency access: Break-glass for life-threatening situations</li>
            <li>Offline mode: Access recent patient notes without network</li>
            <li>Integration: Display medications, allergies, lab results</li>
        </ul>
        
        <h4>3. Constraints</h4>
        <ul>
            <li><strong>Budget:</strong> $2M for security architecture implementation</li>
            <li><strong>Timeline:</strong> 12 months to HIPAA certification</li>
            <li><strong>Technical:</strong> Must integrate with Epic EHR (HL7 v2.5)</li>
            <li><strong>Regulatory:</strong> HIPAA §164.308 (administrative safeguards)</li>
            <li><strong>Operational:</strong> 24/7 support required, cannot disrupt current operations</li>
            <li><strong>Geographic:</strong> Must support rural areas with poor connectivity</li>
        </ul>
        
        <h4>4. Success Criteria</h4>
        <ul>
            <li><strong>Compliance:</strong> Pass HIPAA certification audit with zero findings</li>
            <li><strong>Security:</strong> Zero PHI (Protected Health Information) breaches</li>
            <li><strong>Performance:</strong> Video latency < 200ms, 99.9% uptime</li>
            <li><strong>Usability:</strong> > 80% clinician satisfaction score</li>
            <li><strong>Adoption:</strong> 5,000 active clinicians within 6 months</li>
            <li><strong>Financial:</strong> Cost per consultation < $2</li>
        </ul>
        
        <h4>Grading Rubric</h4>
        <table style="width: 100%; border-collapse: collapse; margin-top: 1rem;">
        <tr style="background: #10b981; color: white;">
            <th style="padding: 0.75rem;">Criteria</th>
            <th style="padding: 0.75rem;">Points</th>
            <th style="padding: 0.75rem;">What to Include</th>
        </tr>
        <tr>
            <td style="padding: 0.75rem; border: 1px solid #e5e7eb;">Business Goals</td>
            <td style="padding: 0.75rem; border: 1px solid #e5e7eb;">25%</td>
            <td style="padding: 0.75rem; border: 1px solid #e5e7eb;">Specific, measurable, aligned with business</td>
        </tr>
        <tr>
            <td style="padding: 0.75rem; border: 1px solid #e5e7eb;">Stakeholder Reqs</td>
            <td style="padding: 0.75rem; border: 1px solid #e5e7eb;">30%</td>
            <td style="padding: 0.75rem; border: 1px solid #e5e7eb;">All key stakeholders covered, specific needs</td>
        </tr>
        <tr>
            <td style="padding: 0.75rem; border: 1px solid #e5e7eb;">Constraints</td>
            <td style="padding: 0.75rem; border: 1px solid #e5e7eb;">20%</td>
            <td style="padding: 0.75rem; border: 1px solid #e5e7eb;">Budget, timeline, technical, regulatory</td>
        </tr>
        <tr>
            <td style="padding: 0.75rem; border: 1px solid #e5e7eb;">Success Criteria</td>
            <td style="padding: 0.75rem; border: 1px solid #e5e7eb;">25%</td>
            <td style="padding: 0.75rem; border: 1px solid #e5e7eb;">Measurable, realistic, time-bound</td>
        </tr>
        </table>
        
        <h4 style="margin-top: 1.5rem;">Common Mistakes to Avoid</h4>
        <ul>
            <li>❌ Vague goals: "Be secure" → ✅ Specific: "Zero PHI breaches, HIPAA certified"</li>
            <li>❌ Missing stakeholders → ✅ Include all: CTO, Legal, CISO, Clinical</li>
            <li>❌ No measurable criteria → ✅ Define: "< 200ms latency, 99.9% uptime"</li>
            <li>❌ Ignoring constraints → ✅ Document: Budget, timeline, technical limitations</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# MODULE 1.3: HIGH-LEVEL ARCHITECTURE WITH DIAGRAMMING
# ============================================================================

def render_module_1_3():
    """Module 1.3: High-Level Architecture Design with Professional Diagramming"""
    
    st.markdown("""
    <div class="module-header">
        <h2>Module 1.3: High-Level Architecture Design</h2>
        <p>Duration: 90 minutes | Deliverable: Architecture Diagrams + Component Inventory</p>
    </div>
    """, unsafe_allow_html=True)
    
    mode = st.radio(
        "Choose Learning Mode:",
        ["👨‍🏫 Instructor-Led Example", "📝 Student Exercise"],
        horizontal=True,
        key="mode_1_3"
    )
    
    if mode.startswith("👨‍🏫"):
        st.markdown("""
        <div class="instructor-card">
            <h3>📘 Instructor Example: Payment Platform Architecture</h3>
            
            <p>We'll design a complete high-level architecture for the payment platform using 
            our professional diagramming tool.</p>
            
            <h4>Architecture Principles</h4>
            <ul>
                <li><strong>Defense in Depth:</strong> Multiple security layers</li>
                <li><strong>Zero Trust:</strong> Verify every request</li>
                <li><strong>Least Privilege:</strong> Minimum access required</li>
                <li><strong>Separation of Concerns:</strong> Clear boundaries</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # Show instructor diagram
        render_professional_diagram_tool()
        
        st.success(f"✅ Module 1.3 Instructor Section Complete! Your unlock code: **{UNLOCK_CODES['1.3']}**")
        
    else:
        st.markdown("""
        <div class="exercise-card">
            <h3>📝 Student Exercise: Design Healthcare Telemedicine Architecture</h3>
            
            <p><strong>Requirements:</strong></p>
            <ul>
                <li>Video consultation platform</li>
                <li>EHR integration</li>
                <li>Mobile apps (iOS/Android)</li>
                <li>HIPAA-compliant data storage</li>
                <li>Emergency break-glass access</li>
            </ul>
            
            <p><strong>Your Task:</strong> Create a high-level architecture diagram showing:</p>
            <ul>
                <li>All major components</li>
                <li>Trust boundaries (DMZ, Application, Data zones)</li>
                <li>Data flows between components</li>
                <li>Security controls at each boundary</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # Student uses diagram tool
        render_professional_diagram_tool()
        
        if st.button("🔓 View Answer Key"):
            if unlock_answer_key('1.3'):
                st.markdown("""
                <div class="answer-card">
                    <h3>✅ Answer Key: Healthcare Architecture</h3>
                    <p>A complete healthcare telemedicine architecture should include:</p>
                    
                    <h4>Zone 1: DMZ (Untrusted)</h4>
                    <ul>
                        <li>Web Application (React SPA)</li>
                        <li>Mobile Apps (iOS/Android native)</li>
                        <li>Load Balancer with WAF</li>
                    </ul>
                    
                    <h4>Zone 2: Application (Semi-Trusted)</h4>
                    <ul>
                        <li>API Gateway (OAuth 2.1 + MFA)</li>
                        <li>Video Service (WebRTC)</li>
                        <li>Consultation Service</li>
                        <li>EHR Integration Service</li>
                    </ul>
                    
                    <h4>Zone 3: Data (Trusted)</h4>
                    <ul>
                        <li>Patient Database (encrypted at rest)</li>
                        <li>Video Storage (E2E encrypted)</li>
                        <li>Audit Log Database (immutable)</li>
                    </ul>
                    
                    <h4>Zone 4: External</h4>
                    <ul>
                        <li>Epic EHR System (HL7 interface)</li>
                        <li>Identity Provider (SAML SSO)</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)

# ============================================================================
# MODULE 2.2: STRIDE THREAT MODELING
# ============================================================================

def render_module_2_2():
    """Module 2.2: STRIDE Threat Modeling with Interactive Canvas"""
    
    st.markdown("""
    <div class="module-header">
        <h2>Module 2.2: STRIDE Threat Modeling</h2>
        <p>Duration: 90 minutes | Deliverable: Complete STRIDE Threat Model</p>
    </div>
    """, unsafe_allow_html=True)
    
    mode = st.radio(
        "Choose Learning Mode:",
        ["👨‍🏫 Instructor-Led Example", "📝 Student Exercise"],
        horizontal=True,
        key="mode_2_2"
    )
    
    if mode.startswith("👨‍🏫"):
        st.markdown("""
        <div class="instructor-card">
            <h3>📘 Instructor Example: API Gateway STRIDE Analysis</h3>
            
            <p>We'll conduct a complete STRIDE analysis on the API Gateway component.</p>
            
            <h4>STRIDE Methodology</h4>
            <ul>
                <li><strong>S</strong>poofing: Can attacker fake identity?</li>
                <li><strong>T</strong>ampering: Can attacker modify data?</li>
                <li><strong>R</strong>epudiation: Can attacker deny actions?</li>
                <li><strong>I</strong>nformation Disclosure: Can attacker steal data?</li>
                <li><strong>D</strong>enial of Service: Can attacker disrupt service?</li>
                <li><strong>E</strong>levation of Privilege: Can attacker gain unauthorized access?</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        render_stride_canvas()
        
        st.success(f"✅ Module 2.2 Instructor Section Complete! Your unlock code: **{UNLOCK_CODES['2.2']}**")
        
    else:
        st.markdown("""
        <div class="exercise-card">
            <h3>📝 Student Exercise: Patient Data Service STRIDE Analysis</h3>
            
            <p>Conduct a complete STRIDE analysis on the Patient Data Service component.</p>
            
            <p><strong>Component Details:</strong></p>
            <ul>
                <li>Stores patient medical records (PHI)</li>
                <li>REST API with OAuth authentication</li>
                <li>PostgreSQL database with encryption at rest</li>
                <li>Accessed by clinicians and patients</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        render_stride_canvas()

# ============================================================================
# MAIN NAVIGATION
# ============================================================================

def main():
    # Sidebar
    with st.sidebar:
        st.title("🏛️ Enterprise Security")
        st.caption("Architecture Workshop")
        
        st.write("---")
        
        # Team info
        st.text_input("Team Name:", value=st.session_state.team_name, key="team_input")
        
        st.write("---")
        
        # Phase selector
        st.subheader("📚 Workshop Phases")
        
        phase = st.radio(
            "Select Phase:",
            [
                "Phase 1: Enterprise Architect",
                "Phase 2: Solution Architect",
                "Phase 3: Security Patterns"
            ],
            key="phase_selector"
        )
        
        st.write("---")
        
        # Module selector based on phase
        if "Phase 1" in phase:
            modules = [
                "1.1 - Capturing Requirements",
                "1.2 - Security Requirements",
                "1.3 - High-Level Architecture",
                "1.4 - ARB Presentation"
            ]
        elif "Phase 2" in phase:
            modules = [
                "2.1 - Component Breakdown",
                "2.2 - STRIDE Modeling",
                "2.3 - Detailed Design"
            ]
        else:
            modules = [
                "3.1 - Pattern Creation",
                "3.2 - Production Readiness"
            ]
        
        module = st.selectbox("Select Module:", modules, key="module_selector")
        
        st.write("---")
        
        # Progress
        st.subheader("📊 Your Progress")
        
        overall_progress = len(st.session_state.completed_modules) / 9 * 100
        st.progress(overall_progress / 100)
        st.caption(f"{overall_progress:.0f}% Complete")
        
        st.metric("Modules Complete", f"{len(st.session_state.completed_modules)}/9")
        st.metric("Artifacts Created", len(st.session_state.diagrams_created) + 
                 len(st.session_state.artifacts['requirements_docs']))
        
        st.write("---")
        
        # Quick actions
        if st.button("📦 View Portfolio"):
            st.session_state.current_module = "portfolio"
            st.rerun()
        
        if st.button("💾 Export All"):
            st.session_state.current_module = "export"
            st.rerun()
    
    # Main content
    st.markdown('<div class="phase-header"><h1>🏛️ Enterprise Security Architecture Workshop</h1><p>Professional Training Platform</p></div>', unsafe_allow_html=True)
    
    # Route to modules
    if "1.1" in module:
        render_module_1_1()
    elif "1.3" in module:
        render_module_1_3()
    elif "2.2" in module:
        render_module_2_2()
    else:
        st.info(f"Module {module} - Content in development")

if __name__ == "__main__":
    main()
