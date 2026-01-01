import os
import sys
import subprocess

# Try to install plotly if it's missing
try:
    import plotly.express as px
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "plotly"])
    import plotly.express as px





import streamlit as st
import pickle
import pandas as pd

# --- Load trained model and mappings ---
model = pickle.load(open("gb_model.pkl", "rb"))
mp = pickle.load(open("alert_mapping.pkl", "rb"))
INT_TO_COLOR = mp["INT_TO_COLOR"]
FEATURES = mp["FEATURES"]

# --- Page setup ---
st.set_page_config(page_title="Earthquake Impact Prediction", layout="wide")

# --- Initialize session state ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# --- Sign-in page ---
def login_page():
    login_bg = """
    <style>
    [data-testid="stAppViewContainer"] {
        background-image: url("https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=1600&auto=format&fit=crop&q=80");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    html, body, .stApp { color: white !important; }
    .login-box {
        background: rgba(0,0,0,0.6);
        border-radius: 12px;
        padding: 24px;
        margin: 100px auto;
        width: 420px;
        text-align: center;
        box-shadow: 0 8px 24px rgba(0,0,0,0.35);
        animation: fadeIn 0.6s ease;
    }
    .stTextInput input {
        color: white !important;
        background: rgba(0,0,0,0.5) !important;
        border: 1px solid rgba(255,255,255,0.35) !important;
    }
    .stButton button {
        color: white !important;
        background: rgba(0,0,0,0.7) !important;
        border: 1px solid rgba(255,255,255,0.4) !important;
    }
    @keyframes fadeIn { from { opacity: 0; transform: translateY(8px); } to { opacity: 1; transform: translateY(0); } }
    </style>
    """
    st.markdown(login_bg, unsafe_allow_html=True)

    st.markdown("<div class='login-box'><h2>🔑 Sign In</h2>", unsafe_allow_html=True)
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        # Demo credentials — replace with your own logic
        if username == "admin" and password == "1234":
            st.session_state.logged_in = True
            st.success("Login successful! Redirecting...")
        else:
            st.error("Invalid username or password")
    st.markdown("</div>", unsafe_allow_html=True)

# --- Dashboard page ---
def dashboard_page():
    page_bg_img = """
    <style>
    [data-testid="stAppViewContainer"] {
        background-image: url("https://images.unsplash.com/photo-1439405326854-014607f694d7?w=1400&auto=format&fit=crop&q=80");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    /* Default text black */
html, body, .stApp, [data-testid="stAppViewContainer"],
p, div, span, label {
    color: black !important;
}

/* Headings stay white */
h1, h2, h3, h4, h5, h6 {
    color: white !important;
}

/* Sidebar text stays white */
[data-testid="stSidebar"] {
    color: white !important;
}
    
    .stNumberInput input, .stTextInput input, .stSelectbox [role="combobox"] { color: white !important; }
    .stButton button {
        color: white !important; background: rgba(0,0,0,0.6) !important;
        border: 1px solid rgba(255,255,255,0.4) !important;
    }
    .section {
        background: rgba(0,0,0,0.6); border-radius: 12px; padding: 18px; margin: 12px 0;
        box-shadow: 0 6px 18px rgba(0,0,0,0.35);
    }
    .navbar {
        position: sticky; top: 0; z-index: 1000; background: rgba(0,0,0,0.7);
        padding: 10px; text-align: center;
    }
    .navbar a {
        color: white !important; text-decoration: none; font-weight: 600;
        margin: 0 16px; padding: 8px 10px; border-radius: 6px;
    }
    .navbar a:hover { background: rgba(255,255,255,0.2); }
    .footer {
        position: fixed; bottom: 0; width: 100%; background: rgba(0,0,0,0.7);
        text-align: center; padding: 8px; z-index: 1000; color: white !important;
    }
    </style>
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)

    # Header
    st.markdown("<h1 style='text-align:center;'>🌍 Earthquake Impact Prediction</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align:center;'>Estimate potential impact with seismic parameters</h4>", unsafe_allow_html=True)

    # Navbar
    st.markdown("""
    <div class="navbar">
      <a href="#predictor">Predictor</a>
      <a href="#info">Info</a>
      <a href="#gallery">Gallery</a>
      <a href="#about">About</a>
    </div>
    """, unsafe_allow_html=True)

    # Sidebar
    st.sidebar.title("📌 Sidebar")
    st.sidebar.write("Quick navigation and notes")
    st.sidebar.markdown("- Predictor\n- Info\n- Gallery\n- About")
    st.sidebar.write("---")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.experimental_rerun()

    # Predictor
    st.markdown("<div id='predictor' class='section'><h2>🚨 Predictor</h2>", unsafe_allow_html=True)
    st.write("Enter earthquake parameters to predict the alert color (all values allowed: negative, zero, positive):")

    col1, col2 = st.columns(2)
    with col1:
        magnitude = st.number_input("Magnitude (Mw)", value=5.5, step=0.1, help="Any number allowed.")
        depth = st.number_input("Depth (km)", value=10.0, step=0.5, help="Any number allowed.")
        cdi = st.number_input("CDI (Community Internet Intensity)", value=3.0, step=0.1, help="Any number allowed.")
    with col2:
        mmi = st.number_input("MMI (Modified Mercalli Intensity)", value=4.0, step=0.1, help="Any number allowed.")
        sig = st.number_input("SIG (Significance)", value=100.0, step=1.0, help="Any number allowed.")

    if st.button("Predict Impact"):
        X_new = pd.DataFrame([[magnitude, depth, cdi, mmi, sig]], columns=FEATURES)
        try:
            prediction = model.predict(X_new)[0]
        except Exception as e:
            st.error(f"Prediction error: {e}")
            prediction = None

        alert_color = INT_TO_COLOR.get(prediction, "Unknown")

        color_map = {
            "green": ("background-color:rgba(0,255,0,0.6);", "✅ Safe"),
            "red": ("background-color:rgba(255,0,0,0.6);", "⚠️ Danger"),
            "yellow": ("background-color:rgba(255,255,0,0.6); color:black;", "⚠️ Moderate"),
            "orange": ("background-color:rgba(255,165,0,0.6);", "⚠️ Moderate")
        }
        box_style, status_msg = color_map.get(str(alert_color).lower(), ("background-color:rgba(0,0,0,0.6);", "Unknown"))

        st.markdown(f"""
        <div style='{box_style} border-radius:12px; padding:18px; margin:12px 0;'>
          <h3>Prediction result</h3>
          <p><b>Predicted Alert Color:</b> {alert_color}</p>
          <p><b>Status:</b> {status_msg}</p>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Info
    st.markdown("<div id='info' class='section'><h2>ℹ️ Earthquake Parameters Explained</h2>", unsafe_allow_html=True)
    st.write("""
    **Magnitude (Mw):** Measures the size of an earthquake based on seismic wave energy.  
    **Depth (km):** Distance below the surface where the quake originates.  
    **CDI:** Crowdsourced shaking reports from communities.  
    **MMI:** Observed shaking intensity scale (I–XII).  
    **SIG:** Composite measure of an earthquake’s overall significance.  
    """)
    st.markdown("</div>", unsafe_allow_html=True)

    # Gallery
    st.markdown("<div id='gallery' class='section'><h2>📸 Earthquake Gallery</h2>", unsafe_allow_html=True)
    g1, g2 = st.columns(2)
    with g1:
        st.image(
            "https://images.unsplash.com/photo-1641213131995-06e2cf0790d8?w=1000&auto=format&fit=crop&q=80",
            caption="after earthquake effect",
            use_column_width=True
        )
    with g2:
        st.image(
            "https://plus.unsplash.com/premium_photo-1716985683568-b05f58cc5c87?w=1000&auto=format&fit=crop&q=80",
            caption="damage caused by earthquake",
            use_column_width=True
        )

    g3, g4 = st.columns(2)
    with g3:
        st.image(
            "https://images.unsplash.com/photo-1508624217470-5ef0f947d8be?w=1000&auto=format&fit=crop&q=80",
            caption="ocean",
            use_column_width=True
        )
    with g4:
        st.image(
            "https://media.istockphoto.com/id/2007470156/photo/seismic-waves-analysis.webp?a=1&b=1&s=612x612&w=0&k=20&c=zERyp5DzbFx87xfu5cq6MZDCeh9E7ua6CF-1w1pbYro=",
            caption="richter scale",
            use_column_width=True
        )
    st.markdown("</div>", unsafe_allow_html=True)

    # About
    st.markdown("<div id='about' class='section'><h2>👩‍💻 About</h2>", unsafe_allow_html=True)
    st.write("Designed by Tanushri — an artistic, educational dashboard for exploring earthquake impact.")
    st.markdown("</div>", unsafe_allow_html=True)

    # Footer
    st.markdown("""
    <div class="footer">
      © 2025 Earthquake Dashboard | Built with Streamlit
    </div>
    """, unsafe_allow_html=True)

# --- Routing ---
if not st.session_state.logged_in:
    login_page()
else:
    dashboard_page()