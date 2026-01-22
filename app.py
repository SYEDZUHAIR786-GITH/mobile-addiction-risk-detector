import streamlit as st
import joblib
import numpy as np

# -------------------------------
# 1. Page Config & Layout
# -------------------------------
st.set_page_config(
    page_title="Mobile Addiction Risk Detector",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern dark theme with gradient
st.markdown("""
    <style>
    /* Dark theme background */
    .stApp {
        background: linear-gradient(135deg, #0f1419 0%, #1a2332 50%, #1a1a2e 100%);
        color: #ffffff;
    }
    
    /* Main container */
    .main {
        padding: 2rem;
    }
    
    /* Gradient title */
    h1 {
        background: linear-gradient(90deg, #00d4ff 0%, #7b2cbf 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 2.5rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    h2 {
        color: #ffffff;
        text-align: center;
        font-size: 2rem;
        margin: 2rem 0;
    }
    
    /* Progress bar styling */
    .progress-text {
        text-align: center;
        color: #00d4ff;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    
    /* Option button styling */
    .option-btn {
        background: linear-gradient(135deg, rgba(0, 212, 255, 0.1), rgba(123, 44, 191, 0.1));
        border: 2px solid rgba(0, 212, 255, 0.3);
        color: #ffffff;
        padding: 1.5rem;
        margin: 0.5rem 0;
        border-radius: 12px;
        cursor: pointer;
        font-size: 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
        text-align: left;
        width: 100%;
    }
    
    .option-btn:hover {
        background: linear-gradient(135deg, rgba(0, 212, 255, 0.2), rgba(123, 44, 191, 0.2));
        border-color: #00d4ff;
        box-shadow: 0 0 15px rgba(0, 212, 255, 0.4);
    }
    
    .option-btn.selected {
        background: linear-gradient(135deg, #00d4ff, #7b2cbf);
        border-color: #00d4ff;
        box-shadow: 0 0 20px rgba(0, 212, 255, 0.6);
    }
    
    /* Button styling with gradient and glow */
    .stButton > button {
        width: 100%;
        background: linear-gradient(90deg, #00d4ff 0%, #7b2cbf 100%);
        color: white;
        border: none;
        padding: 12px 24px;
        font-size: 1rem;
        font-weight: 700;
        border-radius: 50px;
        cursor: pointer;
        box-shadow: 0 0 20px rgba(0, 212, 255, 0.6), 0 0 40px rgba(123, 44, 191, 0.4);
        transition: all 0.3s ease;
        margin-top: 1.5rem;
    }
    
    .stButton > button:hover {
        box-shadow: 0 0 30px rgba(0, 212, 255, 0.8), 0 0 60px rgba(123, 44, 191, 0.6);
        transform: scale(1.02);
    }
    
    /* Success/Warning/Error styling */
    .stSuccess {
        background-color: rgba(0, 200, 100, 0.1);
        border-left: 4px solid #00c864;
        color: #00ff88;
    }
    
    .stWarning {
        background-color: rgba(255, 150, 0, 0.1);
        border-left: 4px solid #ffa500;
        color: #ffbb00;
    }
    
    .stError {
        background-color: rgba(255, 0, 100, 0.1);
        border-left: 4px solid #ff0066;
        color: #ff3366;
    }
    
    /* Sidebar styling */
    .stSidebar {
        background: linear-gradient(180deg, #1a2332 0%, #0f1419 100%);
    }
    
    .stInfo {
        background-color: rgba(0, 212, 255, 0.1);
        border-left: 4px solid #00d4ff;
        color: #e0e0e0;
    }
    </style>
""", unsafe_allow_html=True)

# Load saved model
model = joblib.load("addiction_model.pkl")

# Initialize session state
if "step" not in st.session_state:
    st.session_state.step = 1
    st.session_state.screen_time_ans = None
    st.session_state.social_media_ans = None
    st.session_state.sleep_hours_ans = None
    st.session_state.pickups_ans = None

# Map answers to values
screen_time_map = {
    "All day, every day": 10,
    "A few hours in the morning & evening": 6,
    "Only for work/school": 4,
    "Mainly before sleep": 2
}

social_media_map = {
    "More than 5 hours": 8,
    "3–5 hours": 5,
    "1–3 hours": 2,
    "Less than 1 hour": 1
}

sleep_hours_map = {
    "Less than 5 hours": 3,
    "5–6 hours": 5,
    "7–8 hours": 7,
    "More than 8 hours": 9
}

pickups_map = {
    "More than 150 times": 200,
    "80–150 times": 120,
    "40–80 times": 60,
    "Less than 40 times": 20
}

# Title
st.markdown("<h1>📱 Mobile Addiction Risk Detector</h1>", unsafe_allow_html=True)

# Progress bar
progress = st.session_state.step / 4
st.markdown(f"""
    <div style="background: linear-gradient(90deg, #00d4ff 0%, #7b2cbf 100%); height: 8px; border-radius: 10px; margin: 1rem 0; width: 100%;">
        <div style="background: linear-gradient(90deg, #00d4ff 0%, #7b2cbf 100%); height: 100%; width: {progress*100}%; border-radius: 10px;"></div>
    </div>
    <p style="text-align: center; color: #00d4ff; font-weight: 600;">Step {st.session_state.step} of 4: Your Habits</p>
""", unsafe_allow_html=True)

# Step 1: Screen Time
if st.session_state.step == 1:
    st.markdown("<h2>How often do you use your phone?</h2>", unsafe_allow_html=True)
    
    options_1 = ["All day, every day", "A few hours in the morning & evening", "Only for work/school", "Mainly before sleep"]
    
    for opt in options_1:
        emoji = "📅" if opt == "All day, every day" else "☀️" if opt == "A few hours in the morning & evening" else "⏰" if opt == "Only for work/school" else "🛏️"
        if st.button(f"{emoji} {opt}", key=f"btn_1_{opt}", use_container_width=True):
            st.session_state.screen_time_ans = opt
            st.session_state.step = 2
            st.rerun()

# Step 2: Social Media
elif st.session_state.step == 2:
    st.markdown("<h2>How much time on social media?</h2>", unsafe_allow_html=True)
    
    options_2 = ["More than 5 hours", "3–5 hours", "1–3 hours", "Less than 1 hour"]
    
    for opt in options_2:
        if st.button(f"📱 {opt}", key=f"btn_2_{opt}", use_container_width=True):
            st.session_state.social_media_ans = opt
            st.session_state.step = 3
            st.rerun()
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back", use_container_width=True):
            st.session_state.step = 1
            st.rerun()

# Step 3: Sleep Hours
elif st.session_state.step == 3:
    st.markdown("<h2>How many hours do you sleep?</h2>", unsafe_allow_html=True)
    
    options_3 = ["Less than 5 hours", "5–6 hours", "7–8 hours", "More than 8 hours"]
    
    for opt in options_3:
        if st.button(f"🛌 {opt}", key=f"btn_3_{opt}", use_container_width=True):
            st.session_state.sleep_hours_ans = opt
            st.session_state.step = 4
            st.rerun()
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back", use_container_width=True):
            st.session_state.step = 2
            st.rerun()

# Step 4: Phone Pickups
elif st.session_state.step == 4:
    st.markdown("<h2>Phone pickups per day?</h2>", unsafe_allow_html=True)
    
    options_4 = ["Less than 40 times", "40–80 times", "80–150 times", "More than 150 times"]
    
    for opt in options_4:
        if st.button(f"📲 {opt}", key=f"btn_4_{opt}", use_container_width=True):
            st.session_state.pickups_ans = opt
            st.session_state.step = 5
            st.rerun()
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back", use_container_width=True):
            st.session_state.step = 3
            st.rerun()

# Step 5: Results
elif st.session_state.step == 5:
    # Calculate prediction using user's answers
    screen_time_val = screen_time_map[st.session_state.screen_time_ans]
    social_media_val = social_media_map[st.session_state.social_media_ans]
    sleep_hours_val = sleep_hours_map[st.session_state.sleep_hours_ans]
    pickups_val = pickups_map[st.session_state.pickups_ans]
    
    input_data = np.array([[
        screen_time_val,
        social_media_val,
        sleep_hours_val,
        pickups_val
    ]])
    
    result = model.predict(input_data)[0]
    
    # Display user's answers
    st.markdown("<h2>📊 Your Results</h2>", unsafe_allow_html=True)
    st.markdown(f"""
    **Your Answers:**
    - Phone Usage: {st.session_state.screen_time_ans}
    - Social Media: {st.session_state.social_media_ans}
    - Sleep Hours: {st.session_state.sleep_hours_ans}
    - Phone Pickups: {st.session_state.pickups_ans}
    """)
    
    st.markdown("---")
    
    # Display result
    if result == "Low":
        st.success("🟢 **Low Addiction Risk**")
        st.write("Your usage is well balanced. Keep it up! 👍")
        st.balloons()
    elif result == "Medium":
        st.warning("🟡 **Medium Addiction Risk**")
        st.write("Try reducing screen time and improving sleep habits.")
    else:
        st.error("🔴 **High Addiction Risk**")
        st.write("Your usage shows signs of addiction. Consider digital detox.")
    
    st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)
    
    if st.button("Take Quiz Again", use_container_width=True):
        st.session_state.step = 1
        st.session_state.screen_time_ans = None
        st.session_state.social_media_ans = None
        st.session_state.sleep_hours_ans = None
        st.session_state.pickups_ans = None
        st.rerun()

# Sidebar tips
st.sidebar.title("💡 Healthy Mobile Habits")
st.sidebar.info(
    """
    **Tips for better digital wellness:**
    
    ✅ Take breaks from your phone
    
    ✅ Sleep at least 7–8 hours
    
    ✅ Reduce social media time
    
    ✅ Track usage weekly
    
    ✅ Set phone-free times daily
    
    ✅ Keep phone away during meals
    
    ✅ Use app limiters
    
    ✅ Practice mindfulness
    """
)

st.sidebar.markdown("---")
st.sidebar.write("📊 **About this detector:** This tool uses machine learning to assess your mobile usage patterns.")

