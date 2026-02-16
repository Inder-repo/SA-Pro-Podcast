"""
ADVANCED ENTERPRISE SECURITY ARCHITECTURE WORKSHOP
Professional Training Platform - 4-Day Intensive Masterclass

Focus: Enterprise-scale security architecture with real-world scenarios
No vendor-specific content - pure architecture principles
"""

import streamlit as st
import json
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import hashlib
from typing import Dict, List, Any, Optional
import base64
from io import BytesIO

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
# CUSTOM CSS - ENTERPRISE PROFESSIONAL THEME
# ============================================================================

st.markdown("""
<style>
    /* Professional color scheme */
    :root {
        --primary-blue: #1e3a8a;
        --secondary-blue: #3b82f6;
        --success-green: #059669;
        --warning-amber: #d97706;
        --danger-red: #dc2626;
        --neutral-gray: #6b7280;
    }
    
    /* Main containers */
    .stApp {
        background-color: #f8fafc;
    }
    
    /* Scenario boxes */
    .scenario-box {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        border-left: 5px solid #f59e0b;
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    .scenario-box h3 {
        color: #92400e;
        margin-top: 0;
    }
    
    /* Case study boxes */
    .case-study {
        background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
        border-left: 5px solid #2563eb;
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    /* Failure mode warnings */
    .failure-mode {
        background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
        border-left: 5px solid #dc2626;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    }
    
    /* Success patterns */
    .success-pattern {
        background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
        border-left: 5px solid #059669;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    }
    
    /* Exercise containers */
    .exercise-container {
        background: white;
        border: 2px solid #e5e7eb;
        border-radius: 8px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    
    /* Answer reveal */
    .answer-revealed {
        background: #f0fdf4;
        border: 2px solid #10b981;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    /* Metrics cards */
    .metric-card {
        background: white;
        border-radius: 8px;
        padding: 1rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        text-align: center;
    }
    
    /* Progress indicators */
    .progress-high {
        background: #10b981;
    }
    
    .progress-medium {
        background: #f59e0b;
    }
    
    .progress-low {
        background: #ef4444;
    }
    
    /* Buttons */
    .stButton > button {
        border-radius: 6px;
        font-weight: 600;
        transition: all 0.3s;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 6px 6px 0 0;
        padding: 10px 20px;
        background-color: #e5e7eb;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #2563eb;
        color: white;
    }
    
    /* Expanders */
    .streamlit-expanderHeader {
        font-weight: 600;
        font-size: 1.1rem;
    }
    
    /* Text areas */
    textarea {
        border-radius: 6px;
        border: 2px solid #e5e7eb;
    }
    
    textarea:focus {
        border-color: #2563eb;
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
    }
    
    /* Tables */
    .dataframe {
        border-radius: 8px;
        overflow: hidden;
    }
    
    /* Tooltips */
    .tooltip {
        position: relative;
        display: inline-block;
        border-bottom: 1px dotted #6b7280;
        cursor: help;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

def init_session_state():
    """Initialize comprehensive session state"""
    
    defaults = {
        # Navigation
        'current_day': 1,
        'current_session': 1,
        'current_subsection': 1,
        'completed_exercises': [],
        
        # Day 1: Enterprise Context
        'day1': {
            'complexity_assessment': {},
            'ma_integration': {},
            'arb_decisions': {},
            'governance_model': {},
            'toolchain_audit': {},
            'pasta_analysis': {},
            'supply_chain': {},
            'cloud_threats': {},
            'k8s_threat_model': {},
            'compliance_design': {},
            'policy_code': {},
            'audit_evidence': {}
        },
        
        # Day 2: Real-World Challenges
        'day2': {
            'pe_rollup': {},
            'integration_plan': {},
            'tech_debt_register': [],
            'multicloud_design': {},
            'zero_trust_maturity': {},
            'beyondcorp_architecture': {},
            'legacy_zt': {},
            'attack_surface': {},
            'threat_intel': {},
            'red_team': {}
        },
        
        # Day 3: Documentation & Communication
        'day3': {
            'c4_diagrams': {},
            'adr_records': [],
            'board_presentations': [],
            'fair_analyses': [],
            'breach_communications': {},
            'architect_jd': {},
            'arb_model': {},
            'kpis': {}
        },
        
        # Day 4: Capstone
        'day4': {
            'capstone_discovery': {},
            'complete_architecture': {},
            'board_pitch': {},
            'breach_response': {},
            'post_breach': {},
            'portfolio': {}
        },
        
        # Progress tracking
        'quiz_scores': {},
        'time_spent': {},
        'notes': {},
        'bookmarks': []
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session_state()

# ============================================================================
# CURRICULUM STRUCTURE - COMPLETE 4-DAY WORKSHOP
# ============================================================================

CURRICULUM = {
    "Day 1": {
        "title": "Enterprise Context & Architecture at Scale",
        "duration": "4 Hours",
        "icon": "🏛️",
        "sessions": {
            "1.1": {
                "title": "The Reality of Enterprise Architecture",
                "duration": "60 min",
                "subsections": {
                    "1.1.1": {
                        "title": "What's Different at Enterprise Scale?",
                        "duration": "20 min",
                        "exercises": ["complexity_variables", "ma_nightmare_90day"],
                        "has_answers": True
                    },
                    "1.1.2": {
                        "title": "Architecture Governance at Scale",
                        "duration": "20 min",
                        "exercises": ["arb_scope_quiz", "governance_design"],
                        "has_answers": True
                    },
                    "1.1.3": {
                        "title": "The Architect's Toolchain",
                        "duration": "20 min",
                        "exercises": ["toolchain_audit", "adr_template"],
                        "has_answers": False
                    }
                }
            },
            "1.2": {
                "title": "Advanced Threat Modeling",
                "duration": "90 min",
                "subsections": {
                    "1.2.1": {
                        "title": "Beyond STRIDE: PASTA",
                        "duration": "30 min",
                        "exercises": ["pasta_payment_api", "ale_calculation"],
                        "has_answers": True
                    },
                    "1.2.2": {
                        "title": "Supply Chain Threat Modeling",
                        "duration": "30 min",
                        "exercises": ["codecov_analysis", "cicd_redesign"],
                        "has_answers": True
                    },
                    "1.2.3": {
                        "title": "Cloud-Native Threat Modeling",
                        "duration": "30 min",
                        "exercises": ["k8s_multitenant", "isolation_analysis"],
                        "has_answers": True
                    }
                }
            },
            "1.3": {
                "title": "Regulatory Complexity & Compliance",
                "duration": "90 min",
                "subsections": {
                    "1.3.1": {
                        "title": "Multi-Jurisdiction Compliance",
                        "duration": "30 min",
                        "exercises": ["gdpr_cloudact_conflict", "data_residency"],
                        "has_answers": True
                    },
                    "1.3.2": {
                        "title": "Compliance as Code",
                        "duration": "30 min",
                        "exercises": ["opa_policies", "cicd_compliance"],
                        "has_answers": True
                    },
                    "1.3.3": {
                        "title": "Audit Readiness Architecture",
                        "duration": "30 min",
                        "exercises": ["audit_simulation", "evidence_collection"],
                        "has_answers": True
                    }
                }
            }
        }
    },
    "Day 2": {
        "title": "Real-World Architecture Challenges",
        "duration": "4 Hours",
        "icon": "🔧",
        "sessions": {
            "2.1": {
                "title": "M&A Integration Architecture",
                "duration": "90 min",
                "subsections": {
                    "2.1.1": {
                        "title": "The M&A Security Challenge",
                        "duration": "30 min",
                        "exercises": ["pe_rollup_plan", "sso_migration"],
                        "has_answers": True
                    },
                    "2.1.2": {
                        "title": "Technical Debt Remediation",
                        "duration": "30 min",
                        "exercises": ["debt_register", "remediation_roadmap"],
                        "has_answers": True
                    },
                    "2.1.3": {
                        "title": "Multi-Cloud Security",
                        "duration": "30 min",
                        "exercises": ["multicloud_iam", "cross_cloud_design"],
                        "has_answers": True
                    }
                }
            },
            "2.2": {
                "title": "Zero Trust Architecture",
                "duration": "90 min",
                "subsections": {
                    "2.2.1": {
                        "title": "Zero Trust Fundamentals",
                        "duration": "30 min",
                        "exercises": ["nist_800_207", "maturity_assessment"],
                        "has_answers": True
                    },
                    "2.2.2": {
                        "title": "BeyondCorp Implementation",
                        "duration": "30 min",
                        "exercises": ["beyondcorp_design", "policy_engine"],
                        "has_answers": True
                    },
                    "2.2.3": {
                        "title": "Zero Trust for Legacy",
                        "duration": "30 min",
                        "exercises": ["legacy_proxy", "risk_acceptance"],
                        "has_answers": True
                    }
                }
            },
            "2.3": {
                "title": "Threat Intelligence & Attack Surface",
                "duration": "90 min",
                "subsections": {
                    "2.3.1": {
                        "title": "Attack Surface Management",
                        "duration": "30 min",
                        "exercises": ["asset_discovery", "shadow_it"],
                        "has_answers": True
                    },
                    "2.3.2": {
                        "title": "Threat Intelligence Operations",
                        "duration": "30 min",
                        "exercises": ["ti_pipeline", "scattered_spider"],
                        "has_answers": True
                    },
                    "2.3.3": {
                        "title": "Red Team / Purple Team",
                        "duration": "30 min",
                        "exercises": ["red_team_scenario", "purple_debrief"],
                        "has_answers": True
                    }
                }
            }
        }
    },
    "Day 3": {
        "title": "Documentation & Communication",
        "duration": "4 Hours",
        "icon": "📊",
        "sessions": {
            "3.1": {
                "title": "Architecture Documentation",
                "duration": "60 min",
                "subsections": {
                    "3.1.1": {
                        "title": "C4 Architecture Diagrams",
                        "duration": "30 min",
                        "exercises": ["c4_diagram", "security_overlay"],
                        "has_answers": True
                    },
                    "3.1.2": {
                        "title": "Architecture Decision Records",
                        "duration": "30 min",
                        "exercises": ["advanced_adr", "tls_decision"],
                        "has_answers": True
                    }
                }
            },
            "3.2": {
                "title": "Executive Communication",
                "duration": "90 min",
                "subsections": {
                    "3.2.1": {
                        "title": "Board-Level Presentations",
                        "duration": "30 min",
                        "exercises": ["board_deck", "ransomware_response"],
                        "has_answers": True
                    },
                    "3.2.2": {
                        "title": "FAIR Risk Quantification",
                        "duration": "30 min",
                        "exercises": ["fair_analysis", "roi_calculation"],
                        "has_answers": True
                    },
                    "3.2.3": {
                        "title": "Crisis Communication",
                        "duration": "30 min",
                        "exercises": ["breach_disclosure", "72hour_timeline"],
                        "has_answers": True
                    }
                }
            },
            "3.3": {
                "title": "Building Architecture Practice",
                "duration": "90 min",
                "subsections": {
                    "3.3.1": {
                        "title": "Hiring Architects",
                        "duration": "30 min",
                        "exercises": ["architect_jd", "interview_questions"],
                        "has_answers": True
                    },
                    "3.3.2": {
                        "title": "ARB Operating Model",
                        "duration": "30 min",
                        "exercises": ["arb_design", "mock_arb"],
                        "has_answers": True
                    },
                    "3.3.3": {
                        "title": "Architecture KPIs",
                        "duration": "30 min",
                        "exercises": ["kpi_selection", "dashboard_design"],
                        "has_answers": False
                    }
                }
            }
        }
    },
    "Day 4": {
        "title": "Capstone & Crisis Scenarios",
        "duration": "4 Hours",
        "icon": "🎓",
        "sessions": {
            "4.1": {
                "title": "Capstone Exercise",
                "duration": "150 min",
                "subsections": {
                    "4.1.1": {
                        "title": "Complete Discovery",
                        "duration": "45 min",
                        "exercises": ["megasaas_discovery"],
                        "has_answers": False
                    },
                    "4.1.2": {
                        "title": "Solution Design",
                        "duration": "60 min",
                        "exercises": ["complete_architecture"],
                        "has_answers": False
                    },
                    "4.1.3": {
                        "title": "Board Defense",
                        "duration": "45 min",
                        "exercises": ["board_pitch"],
                        "has_answers": False
                    }
                }
            },
            "4.2": {
                "title": "Crisis Simulation",
                "duration": "90 min",
                "subsections": {
                    "4.2.1": {
                        "title": "Live Breach Response",
                        "duration": "45 min",
                        "exercises": ["breach_containment"],
                        "has_answers": False
                    },
                    "4.2.2": {
                        "title": "Post-Breach Redesign",
                        "duration": "45 min",
                        "exercises": ["architecture_hardening"],
                        "has_answers": False
                    }
                }
            },
            "4.3": {
                "title": "Graduation & Portfolio",
                "duration": "60 min",
                "subsections": {
                    "4.3.1": {
                        "title": "Portfolio Review",
                        "duration": "30 min",
                        "exercises": ["portfolio_compile"],
                        "has_answers": False
                    },
                    "4.3.2": {
                        "title": "Final Assessment",
                        "duration": "30 min",
                        "exercises": ["growth_plan"],
                        "has_answers": False
                    }
                }
            }
        }
    }
}

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def get_subsection_key() -> str:
    """Generate current subsection key"""
    return f"{st.session_state.current_day}.{st.session_state.current_session}.{st.session_state.current_subsection}"

def mark_exercise_complete(exercise_id: str):
    """Mark exercise as complete with timestamp"""
    if exercise_id not in st.session_state.completed_exercises:
        st.session_state.completed_exercises.append(exercise_id)
        st.success(f"✅ Exercise '{exercise_id}' completed!")
        st.balloons()

def calculate_progress() -> Dict[str, float]:
    """Calculate overall and per-day progress"""
    total_exercises = sum(
        len(subsec['exercises'])
        for day in CURRICULUM.values()
        for session in day['sessions'].values()
        for subsec in session['subsections'].values()
    )
    
    completed = len(st.session_state.completed_exercises)
    
    progress = {
        'overall': (completed / total_exercises * 100) if total_exercises > 0 else 0,
        'completed': completed,
        'total': total_exercises
    }
    
    # Per-day progress
    for day_num, day_key in enumerate(['Day 1', 'Day 2', 'Day 3', 'Day 4'], 1):
        day_exercises = [
            ex
            for session in CURRICULUM[day_key]['sessions'].values()
            for subsec in session['subsections'].values()
            for ex in subsec['exercises']
        ]
        day_completed = sum(1 for ex in day_exercises if ex in st.session_state.completed_exercises)
        progress[f'day{day_num}'] = (day_completed / len(day_exercises) * 100) if day_exercises else 0
    
    return progress

def save_work(data: Dict, category: str, subsection: str):
    """Save work with automatic timestamping"""
    day_key = f"day{st.session_state.current_day}"
    if day_key in st.session_state:
        st.session_state[day_key][category] = {
            'data': data,
            'subsection': subsection,
            'timestamp': datetime.now().isoformat(),
            'version': st.session_state[day_key].get(category, {}).get('version', 0) + 1
        }
        st.success("💾 Work saved successfully!")

# ============================================================================
# NAVIGATION & SIDEBAR
# ============================================================================

def render_sidebar():
    """Professional sidebar with navigation and progress"""
    
    st.sidebar.title("🏛️ Enterprise Security")
    st.sidebar.caption("Architecture Masterclass")
    st.sidebar.markdown("---")
    
    # Progress Overview
    progress = calculate_progress()
    
    st.sidebar.metric(
        "Overall Progress",
        f"{progress['completed']}/{progress['total']}",
        f"{progress['overall']:.1f}%"
    )
    
    # Progress bar with color
    progress_pct = progress['overall'] / 100
    color = 'success' if progress_pct > 0.7 else 'warning' if progress_pct > 0.3 else 'error'
    st.sidebar.progress(progress_pct)
    
    # Per-day progress
    with st.sidebar.expander("📊 Progress by Day", expanded=False):
        for i in range(1, 5):
            day_progress = progress.get(f'day{i}', 0)
            st.write(f"**Day {i}:** {day_progress:.0f}%")
            st.progress(day_progress / 100)
    
    st.sidebar.markdown("---")
    
    # Current location
    day_key = list(CURRICULUM.keys())[st.session_state.current_day - 1]
    session_key = list(CURRICULUM[day_key]['sessions'].keys())[st.session_state.current_session - 1]
    subsection_key = list(CURRICULUM[day_key]['sessions'][session_key]['subsections'].keys())[st.session_state.current_subsection - 1]
    current = CURRICULUM[day_key]['sessions'][session_key]['subsections'][subsection_key]
    
    st.sidebar.info(f"""
    **Current Location:**
    {day_key}
    {subsection_key}: {current['title']}
    Duration: {current['duration']}
    """)
    
    st.sidebar.markdown("---")
    
    # Quick navigation
    st.sidebar.subheader("📍 Jump To")
    
    for day_idx, (day_key, day_data) in enumerate(CURRICULUM.items(), 1):
        with st.sidebar.expander(f"{day_data['icon']} {day_key}", expanded=(day_idx == st.session_state.current_day)):
            for session_key, session_data in day_data['sessions'].items():
                # Check if session is complete
                session_exercises = [
                    ex
                    for subsec in session_data['subsections'].values()
                    for ex in subsec['exercises']
                ]
                session_complete = all(ex in st.session_state.completed_exercises for ex in session_exercises)
                icon = "✅" if session_complete else "⏳"
                
                if st.button(
                    f"{icon} {session_key}: {session_data['title']}",
                    key=f"nav_{day_idx}_{session_key}",
                    use_container_width=True
                ):
                    st.session_state.current_day = day_idx
                    st.session_state.current_session = int(session_key.split('.')[1])
                    st.session_state.current_subsection = 1
                    st.rerun()
    
    st.sidebar.markdown("---")
    
    # Actions
    col1, col2 = st.sidebar.columns(2)
    with col1:
        if st.button("📥 Export", use_container_width=True):
            export_portfolio()
    with col2:
        if st.button("📊 Report", use_container_width=True):
            st.session_state['show_report'] = True
            st.rerun()

def export_portfolio():
    """Export complete portfolio as JSON"""
    portfolio = {
        'metadata': {
            'export_date': datetime.now().isoformat(),
            'participant': 'Enterprise Security Architect',
            'progress': calculate_progress()
        },
        'completed_exercises': st.session_state.completed_exercises,
        'day1': st.session_state.day1,
        'day2': st.session_state.day2,
        'day3': st.session_state.day3,
        'day4': st.session_state.day4,
        'notes': st.session_state.notes
    }
    
    portfolio_json = json.dumps(portfolio, indent=2, default=str)
    
    st.sidebar.download_button(
        "💾 Download Portfolio",
        portfolio_json,
        file_name=f"security_architect_portfolio_{datetime.now().strftime('%Y%m%d')}.json",
        mime="application/json",
        use_container_width=True
    )

# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    """Main application router"""
    
    render_sidebar()
    
    # Get current location
    day_key = list(CURRICULUM.keys())[st.session_state.current_day - 1]
    day_data = CURRICULUM[day_key]
    session_key = list(day_data['sessions'].keys())[st.session_state.current_session - 1]
    session_data = day_data['sessions'][session_key]
    subsection_key = list(session_data['subsections'].keys())[st.session_state.current_subsection - 1]
    subsection_data = session_data['subsections'][subsection_key]
    
    # Header
    col1, col2, col3 = st.columns([5, 1, 1])
    with col1:
        st.title(f"{subsection_key}: {subsection_data['title']}")
        st.caption(f"{day_key} • {session_data['title']} • {subsection_data['duration']}")
    with col2:
        ex_done = sum(1 for ex in subsection_data['exercises'] 
                     if ex in st.session_state.completed_exercises)
        st.metric("Exercises", f"{ex_done}/{len(subsection_data['exercises'])}")
    with col3:
        if subsection_data.get('has_answers'):
            st.metric("Answers", "✅ Available")
        else:
            st.metric("Type", "📝 Open")
    
    st.markdown("---")
    
    # Route to content based on subsection
    render_subsection_content(
        st.session_state.current_day,
        st.session_state.current_session,
        st.session_state.current_subsection
    )
    
    # Navigation footer
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("⬅️ Previous", use_container_width=True):
            navigate_previous()
    with col2:
        # Bookmark feature
        if st.button("🔖 Bookmark This Section", use_container_width=True):
            bookmark = {
                'day': st.session_state.current_day,
                'session': st.session_state.current_session,
                'subsection': st.session_state.current_subsection,
                'title': subsection_data['title'],
                'timestamp': datetime.now().isoformat()
            }
            st.session_state.bookmarks.append(bookmark)
            st.success("Bookmarked!")
    with col3:
        if st.button("Next ➡️", use_container_width=True):
            navigate_next()

def navigate_previous():
    """Navigate to previous subsection"""
    day_key = list(CURRICULUM.keys())[st.session_state.current_day - 1]
    session_key = list(CURRICULUM[day_key]['sessions'].keys())[st.session_state.current_session - 1]
    session_data = CURRICULUM[day_key]['sessions'][session_key]
    
    if st.session_state.current_subsection > 1:
        st.session_state.current_subsection -= 1
    elif st.session_state.current_session > 1:
        st.session_state.current_session -= 1
        prev_session_key = list(CURRICULUM[day_key]['sessions'].keys())[st.session_state.current_session - 1]
        st.session_state.current_subsection = len(CURRICULUM[day_key]['sessions'][prev_session_key]['subsections'])
    elif st.session_state.current_day > 1:
        st.session_state.current_day -= 1
        prev_day_key = list(CURRICULUM.keys())[st.session_state.current_day - 1]
        st.session_state.current_session = len(CURRICULUM[prev_day_key]['sessions'])
        last_session_key = list(CURRICULUM[prev_day_key]['sessions'].keys())[-1]
        st.session_state.current_subsection = len(CURRICULUM[prev_day_key]['sessions'][last_session_key]['subsections'])
    st.rerun()

def navigate_next():
    """Navigate to next subsection"""
    day_key = list(CURRICULUM.keys())[st.session_state.current_day - 1]
    session_key = list(CURRICULUM[day_key]['sessions'].keys())[st.session_state.current_session - 1]
    session_data = CURRICULUM[day_key]['sessions'][session_key]
    
    if st.session_state.current_subsection < len(session_data['subsections']):
        st.session_state.current_subsection += 1
    elif st.session_state.current_session < len(CURRICULUM[day_key]['sessions']):
        st.session_state.current_session += 1
        st.session_state.current_subsection = 1
    elif st.session_state.current_day < len(CURRICULUM):
        st.session_state.current_day += 1
        st.session_state.current_session = 1
        st.session_state.current_subsection = 1
    st.rerun()

# ============================================================================
# CONTENT RENDERER - Routes to specific implementations
# ============================================================================

def render_subsection_content(day: int, session: int, subsection: int):
    """Route to appropriate subsection implementation"""
    
    # Import the subsection modules
    from subsections import day1, day2, day3, day4
    
    # Route based on day
    if day == 1:
        day1.render(session, subsection)
    elif day == 2:
        day2.render(session, subsection)
    elif day == 3:
        day3.render(session, subsection)
    elif day == 4:
        day4.render(session, subsection)

# ============================================================================
# RUN APPLICATION
# ============================================================================

if __name__ == "__main__":
    main()
