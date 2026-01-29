import streamlit as st
import pandas as pd
import numpy as np
import time
import random
from datetime import datetime, timedelta

# ==========================================
# 1. CONFIGURATION & STATE MANAGEMENT
# ==========================================
st.set_page_config(
    page_title="Predictraforge | AI Maintenance",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Session State
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = [
        {"role": "assistant", "content": "👋 Hi! I'm Forge, your AI maintenance assistant. I can help you analyze data, schedule maintenance, or answer questions about the platform."}
    ]
if 'analysis_complete' not in st.session_state:
    st.session_state.analysis_complete = False
if 'uploaded_data' not in st.session_state:
    st.session_state.uploaded_data = None

# ==========================================
# 2. CYBERPUNK STYLING (CSS)
# ==========================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

    /* Global Theme */
    .stApp {
        background-color: #020617;
        color: #ffffff;
        font-family: 'Outfit', sans-serif;
    }
    
    /* Typography */
    h1, h2, h3 {
        font-family: 'Outfit', sans-serif;
        font-weight: 800 !important;
        letter-spacing: -0.5px;
    }
    .mono { font-family: 'JetBrains Mono', monospace; }
    
    /* Neon Effects */
    .gradient-text {
        background: linear-gradient(135deg, #00ffff 0%, #00ff88 50%, #0088ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
    }
    
    .neon-box {
        border: 1px solid rgba(0, 255, 255, 0.3);
        box-shadow: 0 0 10px rgba(0, 255, 255, 0.1);
        background: rgba(15, 23, 42, 0.6);
        border-radius: 12px;
        padding: 20px;
        backdrop-filter: blur(10px);
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(90deg, #06b6d4 0%, #2563eb 100%);
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 8px;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 1px;
        transition: all 0.3s ease;
        width: 100%;
    }
    .stButton > button:hover {
        box-shadow: 0 0 20px rgba(6, 182, 212, 0.6);
        transform: translateY(-2px);
    }
    
    /* Inputs */
    .stTextInput > div > div > input, .stTextArea > div > div > textarea, .stSelectbox > div > div > div {
        background-color: #0f172a;
        color: white;
        border: 1px solid #334155;
        border-radius: 8px;
    }
    
    /* Dataframes */
    [data-testid="stDataFrame"] {
        border: 1px solid #334155;
        border-radius: 8px;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #0b1121;
        border-right: 1px solid #1e293b;
    }
    
    /* Chat bubbles */
    .user-msg {
        background: rgba(6, 182, 212, 0.2);
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 10px;
        border-left: 3px solid #06b6d4;
    }
    .bot-msg {
        background: rgba(30, 41, 59, 0.5);
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 10px;
        border-left: 3px solid #8b5cf6;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. SIDEBAR (Navigation & Forge)
# ==========================================
with st.sidebar:
    st.markdown('<div class="gradient-text" style="font-size: 2rem;">⚡ PREDICTRAFORGE</div>', unsafe_allow_html=True)
    st.markdown('<div class="mono" style="color: #94a3b8; font-size: 0.8rem; margin-bottom: 2rem;">V 2.0.4 | SYSTEM ONLINE</div>', unsafe_allow_html=True)
    
    page = st.radio("NAVIGATION", [
        "Home",
        "Input Data",
        "Real-Time Monitoring",
        "Anomaly Detection",
        "Smart Scheduling",
        "Instant Alerts",
        "Digital Twin",
        "Custom Reports",
        "Watch Demo",
        "Get Demo",
        "Free Trial"
    ], label_visibility="collapsed")
    
    st.markdown("---")
    
    # --- FORGE CHATBOT ---
    st.markdown("### 🤖 Forge Assistant")
    
    # Display simplified chat history (last 3 messages)
    chat_container = st.container()
    with chat_container:
        for msg in st.session_state.chat_history[-3:]:
            css_class = "user-msg" if msg["role"] == "user" else "bot-msg"
            icon = "👤" if msg["role"] == "user" else "🤖"
            st.markdown(f'<div class="{css_class}">{icon} {msg["content"]}</div>', unsafe_allow_html=True)
            
    # Chat Input
    with st.form(key='chat_form', clear_on_submit=True):
        user_input = st.text_input("Ask Forge...", key="user_input")
        submit_chat = st.form_submit_button("Send")
        
    if submit_chat and user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        
        # Simple AI Logic
        response = "I'm processing that request. For detailed analysis, please visit the Input Data page."
        u_in = user_input.lower()
        if "hello" in u_in or "hi" in u_in:
            response = "Hello! I'm ready to optimize your maintenance schedules. Where should we start?"
        elif "pricing" in u_in or "cost" in u_in:
            response = "Our prediction models typically save clients 45% in maintenance costs. Plans start at $499/mo."
        elif "upload" in u_in or "data" in u_in:
            response = "You can upload CSV files in the 'Input Data' section. I'll scan them for anomalies automatically."
        elif "alert" in u_in:
            response = "I monitor sensors 24/7. You can configure SMS, Email, or Slack notifications in the 'Instant Alerts' page."
            
        st.session_state.chat_history.append({"role": "assistant", "content": response})
        st.rerun()

# ==========================================
# 4. PAGE ROUTING & LOGIC
# ==========================================

# --- HOME PAGE ---
if page == "Home":
    col1, col2 = st.columns([1.5, 1])
    with col1:
        st.markdown('<div style="height: 50px;"></div>', unsafe_allow_html=True)
        st.markdown('<div class="mono" style="color:#22d3ee; margin-bottom:10px;">AI-POWERED SYSTEM</div>', unsafe_allow_html=True)
        st.markdown('<h1 style="font-size: 4.5rem; line-height: 1.1;">Predict Failures<br><span class="gradient-text">Before They Happen</span></h1>', unsafe_allow_html=True)
        st.markdown('<p style="font-size: 1.2rem; color: #94a3b8; margin: 20px 0;">Transform your factory operations with AI-driven predictive maintenance. Reduce downtime by up to 70% and extend equipment lifespan.</p>', unsafe_allow_html=True)
        
        c1, c2 = st.columns([1, 1])
        with c1:
            if st.button("START FREE TRIAL ➔"):
                # Ideally this would switch pages, but Streamlit nav is state-based
                st.info("Please select 'Free Trial' from the sidebar!")
        with c2:
            st.button("WATCH DEMO ▶")

    with col2:
        # Dashboard Preview
        st.markdown("""
        <div class="neon-box" style="margin-top: 50px;">
            <div style="display:flex; justify-content:space-between; margin-bottom:10px;">
                <span class="mono" style="color:#ef4444;">● LIVE</span>
                <span class="mono" style="color:#22d3ee;">SYSTEM HEALTH: 98%</span>
            </div>
            <svg height="200" width="100%" xmlns="http://www.w3.org/2000/svg">
                <path d="M0,100 Q50,50 100,100 T200,100 T300,50 T400,120" fill="none" stroke="#22d3ee" stroke-width="3"/>
                <path d="M0,100 Q50,50 100,100 T200,100 T300,50 T400,120 V200 H0 Z" fill="rgba(34, 211, 238, 0.1)"/>
            </svg>
            <div style="display:grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: 10px;">
                <div style="background:#1e293b; padding:10px; border-radius:5px; text-align:center;">
                    <div style="font-size:0.8rem; color:#94a3b8;">VIBRATION</div>
                    <div style="color:#22d3ee; font-weight:bold;">2.4 mm/s</div>
                </div>
                <div style="background:#1e293b; padding:10px; border-radius:5px; text-align:center;">
                    <div style="font-size:0.8rem; color:#94a3b8;">TEMP</div>
                    <div style="color:#22d3ee; font-weight:bold;">68°C</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("<h2 style='text-align: center;'>Intelligent Maintenance Features</h2>", unsafe_allow_html=True)
    
    fc1, fc2, fc3 = st.columns(3)
    with fc1:
        st.markdown('<div class="neon-box"><h3>📊 Real-Time Monitoring</h3><p>Continuous monitoring of vibration, temperature, and acoustic patterns with sub-millisecond precision.</p></div>', unsafe_allow_html=True)
    with fc2:
        st.markdown('<div class="neon-box"><h3>🧠 Anomaly Detection</h3><p>Deep learning algorithms identify subtle patterns that precede equipment failures weeks in advance.</p></div>', unsafe_allow_html=True)
    with fc3:
        st.markdown('<div class="neon-box"><h3>📅 Smart Scheduling</h3><p>AI-optimized maintenance windows that minimize production impact and maximize uptime.</p></div>', unsafe_allow_html=True)

# --- INPUT DATA PAGE ---
elif page == "Input Data":
    st.markdown('<h1 style="text-align:center;">Upload Data <span class="gradient-text">For Analysis</span></h1>', unsafe_allow_html=True)
    
    if not st.session_state.analysis_complete:
        st.markdown("""
        <div style="text-align:center; max-width: 600px; margin: 0 auto;">
            <p style="color:#94a3b8;">Securely upload your historical equipment logs in CSV format. Our AI engine will analyze patterns and generate predictive models instantly.</p>
        </div>
        """, unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader("Drag & Drop CSV Files", type=['csv'])
        
        if uploaded_file is not None:
            # Simulate reading data
            try:
                df = pd.read_csv(uploaded_file)
                st.session_state.uploaded_data = df
                st.success(f"Successfully uploaded: {uploaded_file.name}")
                
                with st.expander("Preview Data"):
                    st.dataframe(df.head())
                
                if st.button("ANALYZE DATA 🚀"):
                    with st.spinner("Forge AI is processing neural networks..."):
                        time.sleep(2.5) # Simulate delay
                        st.session_state.analysis_complete = True
                        st.rerun()
            except Exception as e:
                st.error("Error reading file. Please ensure it is a valid CSV.")
                
    else:
        # RESULTS DASHBOARD
        st.markdown('<div class="neon-box" style="text-align:center; border-color:#34d399;"><h2 style="color:#34d399; margin:0;">✅ ANALYSIS COMPLETE</h2><p>Processing finished successfully.</p></div>', unsafe_allow_html=True)
        
        m1, m2, m3 = st.columns(3)
        with m1:
            st.metric("Health Score", "85/100", "-2.5%")
        with m2:
            st.metric("Anomalies Found", "3", "High Priority")
        with m3:
            st.metric("Records Processed", "14,205")
            
        st.markdown("### ⚠️ Critical Predictions")
        
        # Fake Prediction Data
        predictions = pd.DataFrame({
            "Machine ID": ["CNC-01", "Press-04", "Pump-02", "Conveyor-A"],
            "Detected Issue": ["Bearing Wear", "Overheating", "Vibration", "Belt Tension"],
            "Probability": ["92%", "78%", "65%", "45%"],
            "Est. Time to Failure": ["2 weeks", "5 days", "1 month", "3 months"],
            "Action Required": ["Urgent", "High", "Medium", "Low"]
        })
        
        # Styling the table
        st.dataframe(predictions, use_container_width=True)
        
        st.markdown("### Next Steps")
        ns1, ns2 = st.columns(2)
        with ns1:
            if st.button("Simulate in Digital Twin"):
                st.info("Redirecting to Digital Twin simulation with detected parameters...")
        with ns2:
            if st.button("Download PDF Report"):
                st.success("Report generated! (mock download)")
                
        if st.button("Start New Analysis", type="secondary"):
            st.session_state.analysis_complete = False
            st.session_state.uploaded_data = None
            st.rerun()

# --- REAL TIME MONITORING ---
elif page == "Real-Time Monitoring":
    st.title("Real-Time Monitoring")
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("### Vibration Sensor Feed (CNC-01)")
        # Simulate live chart
        chart_data = pd.DataFrame(np.random.randn(50, 3) + [0, 2, 0], columns=['Axis X', 'Axis Y', 'Axis Z'])
        st.line_chart(chart_data)
        
    with col2:
        st.markdown("### Live Stats")
        st.metric("RPM", "3,240", "+12")
        st.metric("Temperature", "68.5°C", "0.4°C")
        st.metric("Power Load", "82%", "Stable")
        st.markdown("---")
        st.markdown('<div class="mono" style="color:#34d399;">● MACHINE ONLINE</div>', unsafe_allow_html=True)

# --- ANOMALY DETECTION ---
elif page == "Anomaly Detection":
    st.title("Anomaly Detection")
    st.markdown("Deep learning analysis of sensor fusion data.")
    
    # Generate fake anomaly data
    dates = pd.date_range(start=datetime.now()-timedelta(days=30), periods=30)
    scores = np.random.uniform(0, 50, 30)
    scores[25] = 95 # Spike
    scores[26] = 88
    
    df_anomaly = pd.DataFrame({"Date": dates, "Anomaly Score": scores})
    
    st.bar_chart(df_anomaly.set_index("Date"))
    
    st.warning("⚠️ Critical anomaly detected on **2024-02-25**. Pattern matches 'Bearing Failure Mode A'.")

# --- SMART SCHEDULING ---
elif page == "Smart Scheduling":
    st.title("Smart Maintenance Scheduling")
    
    schedule_data = pd.DataFrame({
        "Date": [datetime.now().date() + timedelta(days=i) for i in [2, 5, 12, 14]],
        "Machine": ["CNC-01", "Press-04", "Robot-02", "Pump-09"],
        "Task": ["Bearing Replacement", "Lubrication", "Calibration", "Seal Check"],
        "Duration": ["4h", "1h", "2h", "3h"],
        "Production Impact": ["Low", "None", "Low", "Medium"]
    })
    
    st.table(schedule_data)
    st.button("Optimize Schedule with AI")

# --- INSTANT ALERTS ---
elif page == "Instant Alerts":
    st.title("Configuration & Alerts")
    
    st.markdown("### Alert Rules")
    
    with st.expander("🔥 Temperature Thresholds", expanded=True):
        st.slider("Critical Temp (°C)", 0, 120, 90)
        st.multiselect("Notify Channels", ["Email", "SMS", "Slack", "Webhook"], default=["SMS", "Slack"])
        
    with st.expander("〰️ Vibration Thresholds"):
        st.slider("Max Vibration (mm/s)", 0.0, 10.0, 4.5)
        
    st.markdown("### Recent Alert Log")
    st.markdown("""
    - **10:42 AM** - Warning: Press-04 Temp > 85°C
    - **09:15 AM** - Info: Weekly Report Generated
    - **Yesterday** - Critical: Pump-02 Vibration Exceeded Limit
    """)

# --- DIGITAL TWIN ---
elif page == "Digital Twin":
    st.title("Digital Twin Simulation")
    st.markdown("Simulate operating conditions on the virtual replica.")
    
    c1, c2 = st.columns(2)
    with c1:
        # Placeholder for 3D model or image
        st.markdown("""
        <div style="width:100%; height:300px; background: radial-gradient(circle, rgba(6,182,212,0.2) 0%, rgba(2,6,23,1) 100%); border: 1px solid #334155; border-radius: 12px; display:flex; align-items:center; justify-content:center;">
            <div style="text-align:center;">
                <div style="font-size:3rem;">⚙️</div>
                <div class="mono">TWIN: CNC-01-V2</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with c2:
        st.markdown("### Simulation Parameters")
        rpm = st.slider("Motor Speed (RPM)", 0, 5000, 3200)
        load = st.slider("Load Factor (%)", 0, 100, 75)
        temp = st.slider("Ambient Temp (°C)", 10, 50, 22)
        
        # Simple simulation logic
        stress = (rpm * load) / 10000 + (temp / 10)
        r_col = "green"
        if stress > 25: r_col = "orange"
        if stress > 30: r_col = "red"
        
        st.markdown("### Predicted Outcomes")
        st.markdown(f"Mechanical Stress: <span style='color:{r_col}; font-weight:bold; font-size:1.5rem;'>{stress:.2f} Units</span>", unsafe_allow_html=True)
        st.progress(min(stress/40, 1.0))

# --- REPORTS ---
elif page == "Custom Reports":
    st.title("Analytics & Reports")
    
    col1, col2 = st.columns(2)
    with col1:
        st.selectbox("Report Type", ["ROI Analysis", "Equipment Health", "Maintenance Log", "Incident History"])
        st.date_input("Start Date")
        st.date_input("End Date")
        st.button("Generate Report")
    
    with col2:
        st.markdown('<div class="neon-box"><h4>Last Generated</h4><p>ROI_Q3_2024.pdf</p><p>Health_Check_Oct.csv</p></div>', unsafe_allow_html=True)

# --- WATCH DEMO ---
elif page == "Watch Demo":
    st.markdown('<h1 style="text-align:center;">See Predictraforge in Action</h1>', unsafe_allow_html=True)
    
    # Placeholder video container
    st.markdown("""
    <div style="background-color: #0f172a; padding: 20px; border-radius: 12px; border: 1px solid #334155;">
        <div style="aspect-ratio: 16/9; background-color: #000; display: flex; align-items: center; justify-content: center;">
             <span style="font-size: 3rem; color: #334155;">▶ VIDEO PLAYER</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### Key Takeaways")
    st.markdown("- How to connect IoT sensors")
    st.markdown("- Setting up your first AI model")
    st.markdown("- Interpreting anomaly alerts")

# --- FORMS (TRIAL / DEMO) ---
elif page in ["Get Demo", "Free Trial"]:
    title = "Start Your 14-Day Free Trial" if page == "Free Trial" else "Schedule a Personalized Demo"
    st.title(title)
    
    with st.form("lead_form"):
        c1, c2 = st.columns(2)
        c1.text_input("First Name")
        c2.text_input("Last Name")
        st.text_input("Work Email")
        st.text_input("Company Name")
        st.selectbox("Industry", ["Manufacturing", "Automotive", "Energy", "Aerospace"])
        
        if page == "Get Demo":
            st.date_input("Preferred Date")
            st.text_area("What specific challenges are you facing?")
            
        submitted = st.form_submit_button("Submit Request")
        
        if submitted:
            st.balloons()
            st.success("Request received successfully! Check your email for next steps.")