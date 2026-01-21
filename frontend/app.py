import streamlit as st
import requests
import json
import time

# Configuration
API_URL = "http://127.0.0.1:8000/api/medicine-info"
st.set_page_config(
    page_title="AI Medicine Assistant",
    page_icon="💊",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Load Custom CSS
def load_css():
    with open("frontend/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

try:
    load_css()
except FileNotFoundError:
    st.error("CSS file not found. Please ensure frontend/style.css exists.")

# Sidebar
with st.sidebar:
    # Logo - Restored as requested, but smaller
    try:
        col_logo_1, col_logo_2, col_logo_3 = st.columns([1, 2, 1])
        with col_logo_2:
             st.image("frontend/logo.png", use_container_width=True)
    except Exception:
        st.title("💊 AI MedAssist")
    st.markdown("---")
    st.markdown("### 🌍 Settings")
    language = st.selectbox("Select Language", ["English", "Spanish", "French", "Hindi", "German", "Japanese"])
    
    st.markdown("---")
    st.info(
        "**Taking care of you.**\n\n"
        "Enter a medicine name to get instant, easy-to-understand details.\n\n"
        "⚠️ **Note**: AI-generated content. Consult a doctor."
    )

# Main Content
st.title("AI Medicine Assistant")
st.markdown("<p style='text-align: center; font-size: 1.2rem; margin-bottom: 40px; opacity: 0.8;'>Your intelligent companion for safe medicine usage.</p>", unsafe_allow_html=True)

# Search Bar with improved layout
col1, col2, col3 = st.columns([1, 6, 1])
with col2:
    medicine_name = st.text_input("", placeholder="🔍 Enter medicine name (e.g., Paracetamol, Amoxicillin)...", label_visibility="collapsed")
    search_button = st.button("Analyze Medicine")

if search_button:
    if medicine_name:
        # Progress Bar Simulation for "Thinking" effect
        progress_text = "Analyzing medical database..."
        my_bar = st.progress(0, text=progress_text)
        
        for percent_complete in range(100):
            time.sleep(0.01)
            my_bar.progress(percent_complete + 1, text=progress_text)
        time.sleep(0.5)
        my_bar.empty()

        try:
            # Call Backend API
            payload = {"medicine_name": medicine_name, "language": language}
            response = requests.post(API_URL, json=payload)
            
            if response.status_code == 200:
                data = response.json()
                
                # Title Card
                st.markdown(f"""
                <div class="glass-card" style="text-align: center;">
                    <h2 style="font-size: 2rem; color: #00e5ff !important; margin-bottom: 5px;">💊 {data['medicine']}</h2>
                    <p style="opacity: 0.8;">Information via AI Analysis</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Main Info Grid
                col_a, col_b = st.columns(2)
                
                with col_a:
                    st.markdown(f"""
                    <div class="glass-card" style="height: 100%;">
                        <h3>📋 Usage</h3>
                        <p>{data['usage']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                with col_b:
                    st.markdown(f"""
                    <div class="glass-card" style="height: 100%;">
                        <h3>⚠️ Side Effects</h3>
                        <p>{data['side_effects']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                st.markdown(f"""
                <div class="glass-card">
                    <h3>✅ Dos & ❌ Don'ts</h3>
                    <p>{data['dos_donts']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Disclaimer
                st.warning(f"**Safety Disclaimer:** {data['disclaimer']}")
            
            elif response.status_code == 400:
                 st.error(f"Configuration Error: {response.json().get('detail', 'Unknown error')}")
            else:
                st.error(f"Server Error: Unable to fetch data. (Status: {response.status_code})")
                
        except requests.exceptions.ConnectionError:
            st.error("🚨 Connection Error: Could not connect to the backend server. Please make sure the backend is running.")
    else:
        st.warning("Please enter a medicine name to begin.")

# No Footer as requested
