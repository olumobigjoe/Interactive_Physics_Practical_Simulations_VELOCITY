import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import os

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Kinematics Virtual Lab & Analytics",
    page_icon="🏹",
    layout="wide"
)

# --- DIRECTORY & FILE SETUP FOR LEARNING ANALYTICS ---
LOG_FILE = "student_analytics_log.csv"

def log_user_action(student_id, action_type, details):
    """Logs student telemetry data to a CSV file for learning analytics."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_data = pd.DataFrame([{
        "Timestamp": timestamp,
        "Student_ID": student_id,
        "Action_Type": action_type,
        "Details": str(details)
    }])
    
    if not os.path.isfile(LOG_FILE):
        log_data.to_csv(LOG_FILE, index=False)
    else:
        log_data.to_csv(LOG_FILE, mode='a', header=False, index=False)

# --- INITIALIZE SESSION STATE VARIABLES ---
if 'student_id' not in st.session_state:
    st.session_state['student_id'] = "Guest_Student"
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False
if 'quiz_submitted' not in st.session_state:
    st.session_state['quiz_submitted'] = False

# --- APPLICATION HEADER ---
st.title("🏹 Interactive Kinematics Virtual Lab & Analytics Platform")
st.subheader("Department of Physics/Electronics — Advanced Classical Mechanics Lab")
st.markdown("---")

# --- USER AUTHENTICATION / LOGIN ---
if not st.session_state['authenticated']:
    st.info("👋 Welcome! Please enter your Student Matriculation Number to initialize the physics simulation bench and analytics tracking.")
    matric_no = st.text_input("Enter Student Matriculation Number (e.g., HND/PHY/2026/045):")
    if st.button("Initialize Lab Bench"):
        if matric_no.strip() != "":
            st.session_state['student_id'] = matric_no.strip()
            st.session_state['authenticated'] = True
            log_user_action(st.session_state['student_id'], "Session_Start", "Initialized kinematics lab simulator.")
            st.rerun()
        else:
            st.warning("Please enter a valid identification number.")
    st.stop()

# --- SIDEBAR: VIRTUAL INSTRUMENTATION CONTROLS ---
st.sidebar.header("🎛️ Virtual Simulation Controls")
st.sidebar.markdown("*Adjust environment parameters to model dynamic trajectories*")

# Control sliders
v0 = st.sidebar.slider("1. Initial Launch Velocity (m/s)", min_value=5.0, max_value=50.0, value=25.0, step=1.0)
angle_deg = st.sidebar.slider("2. Launch Angle (Degrees)", min_value=5, max_value=85, value=45, step=5)
cd = st.sidebar.slider("3. Drag Coefficient (C_d) [0 = Vacuum]", min_value=0.00, max_value=1.00, value=0.10, step=0.05)
gravity = st.sidebar.selectbox("4. Environmental Gravity Field", [9.81, 1.62, 3.71, 24.79], 
                               format_func=lambda x: f"Earth ({x} m/s²)" if x==9.81 else (f"Moon ({x} m/s²)" if x==1.62 else (f"Mars ({x} m/s²)" if x==3.71 else f"Jupiter ({x} m/s²)")))

st.sidebar.markdown("---")
st.sidebar.markdown(f"**Logged in as:** `{st.session_state['student_id']}`")
if st.sidebar.button("Log Out / Reset Bench"):
    log_user_action(st.session_state['student_id'], "Session_End", "Logged out of bench.")
    st.session_state['authenticated'] = False
    st.session_state['quiz_submitted'] = False
    st.rerun()

if st.sidebar.button("Log Current Trajectory State"):
    details = f"V0: {v0}, Angle: {angle_deg}, Cd: {cd}, G: {gravity}"
    log_user_action(st.session_state['student_id'], "Parameter_Calibration", details)
    st.sidebar.success("Trajectory state logged!")

# --- CORE MATHEMATICAL PHYSICS ENGINE (EULER INTEGRATION) ---
def simulate_projectile(v0, angle_deg, cd, g):
    # Constants
    dt = 0.01  # Time step (seconds)
    rho = 1.225  # Air density at sea level (kg/m³)
    area = 0.05  # Cross-sectional area (m²)
    mass = 0.5   # Mass of projectile (kg)
    
    # Initial conditions
    angle_rad = np.radians(angle_deg)
    vx = v0 * np.cos(angle_rad)
    vy = v0 * np.sin(angle_rad)
    
    x, y = 0.0, 0.0
    x_pts, y_pts = [x], [y]
    
    # Loop execution until the projectile hits the ground
    while y >= 0.0:
        v = np.sqrt(vx**2 + vy**2)
        
        # Calculate drag accelerations
        drag_force = 0.5 * rho * cd * area * v
        ax = -(drag_force * vx) / mass
        ay = -g - (drag_force * vy) / mass
        
        # Update states via Euler's method
        x += vx * dt
        y += vy * dt
        vx += ax * dt
        vy += ay * dt
        
        # Boundary guard to keep values clean
        if y < 0:
            y = 0
            
        x_pts.append(x)
        y_pts.append(y)
        
        # Safety breaker for open trajectories
        if len(x_pts) > 10000:
            break
            
    return x_pts, y_pts

# Run physics integration
x_curve, y_curve = simulate_projectile(v0, angle_deg, cd, gravity)

# --- MAIN DASHBOARD GRAPHICS LAYOUT ---
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📊 Dynamic Vector Trajectory Coordinate Plot")
    st.markdown("Hover over data paths to analyze instantaneous displacement vectors.")
    
    # Plotly Visual Layout Rendering
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_curve, y=y_curve, mode='lines', name="Trajectory", line=dict(color='#00CC96', width=3)))
    
    # Direct Layout assignment style to bypass runtime container errors
    fig.layout = go.Layout(
        xaxis=dict(title="Horizontal Distance (meters)", range=[0, max(x_curve)*1.1 if max(x_curve)>0 else 10], zeroline=True, zerolinecolor="gray"),
        yaxis=dict(title="Vertical Height (meters)", range=[0, max(y_curve)*1.2 if max(y_curve)>0 else 10], zeroline=True, zerolinecolor="gray"),
        template="plotly_dark",
        margin=dict(l=20, r=20, t=20, b=20),
        height=450
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("📋 Virtual Instrument Readout Panel")
    st.markdown("Physical milestones computed by the kinematics simulation loop:")
    
    st.metric(label="Calculated Maximum Range", value=f"{max(x_curve):.2f} meters")
    st.metric(label="Calculated Peak Vertex Height", value=f"{max(y_curve):.2f} meters")
    
    st.info("💡 **Physics Hint:** Notice how adding drag breaks the symmetry of the parabola. The projectile falls at a steeper angle at the tail end due to continuous energy loss from atmospheric resistance.")

st.markdown("---")

# --- INTERACTIVE ASSESSMENT MODULE ---
st.header("📝 Diagnostic Evaluation Module")
st.markdown("Submit your answers below based on your observation profiles above.")

with st.form("quiz_form"):
    q1 = st.radio(
        "1. How does adding a non-zero drag coefficient (C_d > 0) alter the trajectory geometry compared to a perfect vacuum?",
        ["The trajectory remains a symmetric parabola, but shrinks uniformly.", 
         "The trajectory becomes asymmetric, dropping off much more steeply at the end.", 
         "The maximum range increases due to terminal aerodynamic lift forces."]
    )
    
    q2 = st.radio(
        "2. If you launch a projectile with the same velocity and angle on Mars compared to Earth, what happens to the maximum range?",
        ["It decreases because Mars has a stronger gravitational field pull.", 
         "It increases because Mars has a weaker gravitational acceleration (3.71 m/s²).", 
         "It remains identical because initial kinematic vectors dominate the flight profile."]
    )
    
    submitted = st.form_submit_button("Submit Lab Quiz Answers")
    
    if submitted:
        st.session_state['quiz_submitted'] = True
        score = 0
        
        # Grading evaluation logic
        if q1 == "The trajectory becomes asymmetric, dropping off much more steeply at the end.":
            score += 50
        if q2 == "It increases because Mars has a weaker gravitational acceleration (3.71 m/s²).":
            score += 50
            
        st.subheader("🎯 Test Performance Results")
        st.write(f"Your calculated comprehension score: **{score}/100**")
        
        if score == 100:
            st.success("Excellent work! You have successfully interpreted your virtual instrumentation readouts.")
        else:
            st.error("Some evaluations are incorrect. Adjust the control variables on the left panel to test the curves again.")
            
        log_user_action(st.session_state['student_id'], "Quiz_Submission", f"Score: {score}%. Q1: {q1}, Q2: {q2}")

st.markdown("---")

# --- INSTRUCTOR ANALYTICS AREA ---
st.header("📊 Instructor Portal & Learning Analytics Summary")
st.markdown("*Real-time audit trails showing student interactions and learning trends.*")

if os.path.exists(LOG_FILE):
    try:
        df_logs = pd.read_csv(LOG_FILE)
        user_logs = df_logs[df_logs["Student_ID"] == st.session_state['student_id']]
        
        col_summary1, col_summary2 = st.columns(2)
        with col_summary1:
            st.subheader("Your Live Telemetry Log Profile")
            st.dataframe(user_logs, use_container_width=True)
            
        with col_summary2:
            st.subheader("Global Action Breakdown Metric")
            action_counts = df_logs["Action_Type"].value_counts().reset_index()
            action_counts.columns = ["Action", "Frequency"]
            
            fig_pie = go.Figure(data=[go.Pie(labels=action_counts["Action"], values=action_counts["Frequency"], hole=.3)])
            fig_pie.update_layout(template="plotly_dark", margin=dict(l=10, r=10, t=30, b=10), height=250)
            st.plotly_chart(fig_pie, use_container_width=True)
    except Exception as e:
        st.warning("Data repository tracking stream initializing...")
else:
    st.info("No learning analytics records have been aggregated yet. Interact with control structures above to initialize tracking pipelines.")