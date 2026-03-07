import streamlit as st
import streamlit.components.v1 as components
import time
import threading
import uuid
import hashlib
import os
import subprocess
import json
import urllib.parse
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import database as db
import requests

st.set_page_config(
    page_title="E2E BY RISHU",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS (same as before)
custom_css = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel+Decorative:wght@400;700&family=Great+Vibes&family=Playfair+Display:wght@400;700&display=swap');

    * {
        font-family: 'Playfair Display', serif;
    }

    .stApp {
        background-image: linear-gradient(rgba(20, 0, 40, 0.88), rgba(40, 0, 80, 0.78)),
                          url('https://i.ibb.co/0mQfX0b/dark-royal-purple-velvet-texture.jpg');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }

    .main .block-container {
        background: rgba(30, 10, 60, 0.68);
        backdrop-filter: blur(12px);
        border-radius: 22px;
        padding: 32px;
        border: 2px solid rgba(255, 215, 0, 0.38);
        box-shadow: 0 12px 45px rgba(255, 215, 0, 0.18),
                    inset 0 0 28px rgba(255, 215, 0, 0.10);
    }

    .main-header {
        background: linear-gradient(135deg, #1a0033, #4b0082, #2a0055);
        border: 2px solid #ffd700;
        border-radius: 25px;
        padding: 2.4rem;
        text-align: center;
        margin-bottom: 2.8rem;
        box-shadow: 0 18px 55px rgba(0, 0, 0, 0.75),
                    0 0 35px rgba(255, 215, 0, 0.30);
        position: relative;
        overflow: hidden;
    }

    .main-header::before {
        content: "👑";
        position: absolute;
        top: -40px;
        left: 50%;
        transform: translateX(-50%);
        font-size: 6.5rem;
        opacity: 0.14;
        color: #ffd700;
    }

    .main-header h1 {
        background: linear-gradient(90deg, #ffd700, #ffeb3b, #ffd700);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'Cinzel Decorative', cursive;
        font-size: 3.4rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 0 0 25px rgba(255, 215, 0, 0.7);
    }

    .main-header p {
        color: #d4af37;
        font-family: 'Great Vibes', cursive;
        font-size: 1.8rem;
        margin-top: 0.7rem;
        letter-spacing: 1.8px;
    }

    .prince-logo {
        width: 120px;
        height: 120px;
        border-radius: 50%;
        margin-bottom: 22px;
        border: 4px solid #ffd700;
        box-shadow: 0 0 35px rgba(255, 215, 0, 0.8),
                    inset 0 0 18px rgba(255, 255, 255, 0.35);
    }

    .stButton>button {
        background: linear-gradient(45deg, #b8860b, #ffd700, #daa520);
        color: #1a0033;
        border: 2px solid #b8860b;
        border-radius: 16px;
        padding: 1rem 2.4rem;
        font-family: 'Cinzel Decorative', cursive;
        font-weight: 700;
        font-size: 1.2rem;
        transition: all 0.4s ease;
        box-shadow: 0 8px 25px rgba(255, 215, 0, 0.45);
        text-shadow: 1px 1px 3px rgba(0,0,0,0.5);
        width: 100%;
    }

    .stButton>button:hover {
        transform: translateY(-5px) scale(1.04);
        box-shadow: 0 15px 40px rgba(255, 215, 0, 0.75);
        background: linear-gradient(45deg, #ffd700, #ffeb3b, #ffd700);
    }

    .stTextInput>div>div>input,
    .stTextArea>div>div>textarea,
    .stNumberInput>div>div>input {
        background: rgba(40, 20, 80, 0.75);
        border: 2px solid #b8860b;
        border-radius: 14px;
        color: #ffd700;
        padding: 1rem;
        font-size: 1.1rem;
    }

    .stTextInput>div>div>input::placeholder,
    .stTextArea>div>div>textarea::placeholder {
        color: #d4af37aa;
    }

    .stTextInput>div>div>input:focus,
    .stTextArea>div>div>textarea:focus {
        border-color: #ffd700;
        box-shadow: 0 0 0 4px rgba(255, 215, 0, 0.35);
        background: rgba(50, 30, 90, 0.85);
    }

    label {
        color: #ffd700 !important;
        font-weight: 600 !important;
        font-size: 1.15rem !important;
        text-shadow: 1px 1px 4px #000;
    }

    .stTabs [data-baseweb="tab-list"] {
        background: rgba(30, 10, 60, 0.65);
        border-radius: 16px;
        padding: 10px;
        border: 1px solid #b8860b;
    }

    .stTabs [data-baseweb="tab"] {
        background: rgba(75, 0, 130, 0.55);
        color: #d4af37;
        border-radius: 12px;
        padding: 14px 26px;
        font-weight: 600;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(45deg, #b8860b, #ffd700);
        color: #1a0033;
    }

    [data-testid="stMetricValue"] {
        color: #ffd700;
        font-size: 2.6rem;
        font-weight: 700;
        text-shadow: 0 0 18px rgba(255, 215, 0, 0.7);
    }

    [data-testid="stMetricLabel"] {
        color: #d4af37;
        font-weight: 500;
    }

    .console-section {
        background: rgba(20, 0, 40, 0.75);
        border: 2px solid #b8860b;
        border-radius: 16px;
        padding: 22px;
        margin-top: 28px;
    }

    .console-header {
        color: #ffd700;
        font-family: 'Cinzel Decorative', cursive;
        text-shadow: 0 0 18px #ffd700bb;
        margin-bottom: 18px;
    }

    .console-output {
        background: #0f001a;
        border: 2px solid #4b0082;
        border-radius: 14px;
        padding: 18px;
        color: #ffeb3b;
        font-family: 'Courier New', monospace;
        font-size: 13.5px;
        max-height: 480px;
        overflow-y: auto;
    }

    .console-line {
        background: rgba(75, 0, 130, 0.25);
        border-left: 4px solid #ffd700;
        padding: 9px 14px;
        margin: 7px 0;
        color: #ffeb3b;
    }

    .success-box {
        background: linear-gradient(135deg, #b8860b, #ffd700);
        color: #1a0033;
        border: 2px solid #1a0033;
    }

    .error-box {
        background: linear-gradient(135deg, #8b0000, #c71585);
        border: 2px solid #ffd700;
    }

    .whatsapp-btn {
        background: linear-gradient(45deg, #006400, #228b22, #006400);
        border: 2px solid #ffd700;
        color: #ffd700;
        font-family: 'Playfair Display', serif;
        font-weight: 700;
        box-shadow: 0 8px 25px rgba(0, 100, 0, 0.55);
        padding: 0.8rem 1.5rem;
        border-radius: 12px;
        text-decoration: none;
        display: inline-block;
    }

    .whatsapp-btn:hover {
        background: linear-gradient(45deg, #228b22, #32cd32, #228b22);
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(50, 205, 50, 0.7);
    }

    .footer {
        background: rgba(30, 10, 60, 0.75);
        border-top: 3px solid #b8860b;
        color: #d4af37;
        font-family: 'Great Vibes', cursive;
        font-size: 1.5rem;
        padding: 2.8rem;
        text-shadow: 1px 1px 5px #000;
    }
    
    .admin-badge {
        background: linear-gradient(45deg, #ffd700, #b8860b);
        color: #1a0033;
        padding: 0.3rem 1rem;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
        margin-bottom: 1rem;
    }
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

ADMIN_PASSWORD = "YAMRAJ_KING"
WHATSAPP_NUMBER = "7654221354"
APPROVAL_FILE = "approved_keys.json"
PENDING_FILE = "pending_approvals.json"

# Session state initialization
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'username' not in st.session_state:
    st.session_state.username = None
if 'user_key' not in st.session_state:
    st.session_state.user_key = None
if 'key_approved' not in st.session_state:
    st.session_state.key_approved = False
if 'approval_status' not in st.session_state:
    st.session_state.approval_status = 'not_requested'
if 'automation_running' not in st.session_state:
    st.session_state.automation_running = False
if 'logs' not in st.session_state:
    st.session_state.logs = []
if 'message_count' not in st.session_state:
    st.session_state.message_count = 0
if 'whatsapp_opened' not in st.session_state:
    st.session_state.whatsapp_opened = False
if 'admin_authenticated' not in st.session_state:
    st.session_state.admin_authenticated = False
if 'show_admin' not in st.session_state:
    st.session_state.show_admin = False
if 'current_page' not in st.session_state:
    st.session_state.current_page = "user"

class AutomationState:
    def __init__(self):
        self.running = False
        self.message_count = 0
        self.logs = []
        self.message_rotation_index = 0

if 'automation_state' not in st.session_state:
    st.session_state.automation_state = AutomationState()

if 'auto_start_checked' not in st.session_state:
    st.session_state.auto_start_checked = False

ADMIN_UID = "YAMRAJ DEV"

# Helper functions
def generate_user_key(username, password):
    combined = f"{username}:{password}"
    key_hash = hashlib.sha256(combined.encode()).hexdigest()[:8].upper()
    return f"KEY-{key_hash}"

def load_approved_keys():
    if os.path.exists(APPROVAL_FILE):
        try:
            with open(APPROVAL_FILE, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_approved_keys(keys):
    with open(APPROVAL_FILE, 'w') as f:
        json.dump(keys, f, indent=2)

def load_pending_approvals():
    if os.path.exists(PENDING_FILE):
        try:
            with open(PENDING_FILE, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_pending_approvals(pending):
    with open(PENDING_FILE, 'w') as f:
        json.dump(pending, f, indent=2)

def send_whatsapp_message(user_name, approval_key):
    message = f"👑 HELLO YAMRAJ SIR PLEASE 👑👑\nMy name is {user_name}\nPlease approve my key:\n🔑 {approval_key}"
    encoded_message = urllib.parse.quote(message)
    whatsapp_url = f"https://api.whatsapp.com/send?phone={WHATSAPP_NUMBER}&text={encoded_message}"
    return whatsapp_url

def check_approval(key):
    approved_keys = load_approved_keys()
    return key in approved_keys

def log_message(msg, automation_state=None):
    timestamp = time.strftime("%H:%M:%S")
    formatted_msg = f"[{timestamp}] {msg}"
   
    if automation_state:
        automation_state.logs.append(formatted_msg)
    else:
        if 'logs' in st.session_state:
            st.session_state.logs.append(formatted_msg)

def get_user_by_username(username):
    """Get user data from database by username"""
    try:
        conn = db.create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, password FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        conn.close()
        
        if user:
            return {
                'id': user[0],
                'username': user[1],
                'password': user[2]
            }
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

# [All your existing automation functions remain the same]
# find_message_input, setup_browser, get_next_message, send_messages, 
# send_admin_notification, run_automation_with_notification, start_automation, stop_automation
# (I'm omitting them here for brevity, but keep all your original functions)

# Admin Dashboard Function
def admin_dashboard():
    st.markdown("""
    <div class="main-header">
        <img src="https://i.ibb.co/Rkp3VcHy/image.jpg" class="RISHU-logo">
        <h1>👑 ADMIN DASHBOARD 👑</h1>
        <p>Complete Approval Management System</p>
    </div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.admin_authenticated:
        with st.form("admin_login_form"):
            st.markdown("### 🔐 Admin Login")
            admin_pass = st.text_input("Admin Password", type="password")
            
            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                login_btn = st.form_submit_button("Login", use_container_width=True)
            
            if login_btn:
                if admin_pass == ADMIN_PASSWORD:
                    st.session_state.admin_authenticated = True
                    st.rerun()
                else:
                    st.error("❌ Invalid password!")
            
            st.markdown("---")
            if st.form_submit_button("⬅️ Back to User Login"):
                st.session_state.current_page = "user"
                st.rerun()
    else:
        # Full admin dashboard
        pending = load_pending_approvals()
        approved = load_approved_keys()
        
        # Stats
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Users", db.get_total_users() if hasattr(db, 'get_total_users') else "N/A")
        with col2:
            st.metric("Pending Approvals", len(pending))
        with col3:
            st.metric("Approved Keys", len(approved))
        with col4:
            st.metric("Active Automations", db.get_active_automations() if hasattr(db, 'get_active_automations') else "N/A")
        
        st.markdown("---")
        
        tab1, tab2, tab3 = st.tabs(["⏳ Pending Approvals", "✅ Approved Keys", "⚡ Quick Approve"])
        
        with tab1:
            if pending:
                for key, info in pending.items():
                    with st.container():
                        col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
                        with col1:
                            st.write(f"**👤 {info['name']}**")
                        with col2:
                            st.code(key)
                        with col3:
                            st.write(f"🕐 {info.get('timestamp', 'N/A')}")
                        with col4:
                            if st.button("✅ Approve", key=f"dash_{key}"):
                                approved[key] = info
                                save_approved_keys(approved)
                                del pending[key]
                                save_pending_approvals(pending)
                                st.success(f"Approved {info['name']}!")
                                st.rerun()
                        st.divider()
            else:
                st.info("No pending approvals")
        
        with tab2:
            if approved:
                search = st.text_input("🔍 Search by username", placeholder="Type username...")
                for key, info in approved.items():
                    if not search or search.lower() in info['name'].lower():
                        with st.container():
                            col1, col2, col3 = st.columns([2, 3, 2])
                            with col1:
                                st.write(f"**👤 {info['name']}**")
                            with col2:
                                st.code(key)
                            with col3:
                                st.write(f"🕐 {info.get('timestamp', 'N/A')}")
                            st.divider()
            else:
                st.info("No approved keys")
        
        with tab3:
            st.markdown("### ⚡ Quick Approve by Username")
            username = st.text_input("Enter username to approve", placeholder="e.g., john_doe")
            
            if st.button("✅ Approve User", use_container_width=True):
                if username:
                    user_data = get_user_by_username(username)
                    if user_data:
                        user_key = generate_user_key(username, user_data['password'])
                        
                        approved[user_key] = {
                            "name": username,
                            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                            "approved_by": "dashboard"
                        }
                        save_approved_keys(approved)
                        
                        if user_key in pending:
                            del pending[user_key]
                            save_pending_approvals(pending)
                        
                        st.success(f"✅ User '{username}' approved!\nKey: {user_key}")
                    else:
                        st.error(f"❌ Username '{username}' not found!")
                else:
                    st.warning("⚠️ Please enter username")
        
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("🚪 Logout Admin", use_container_width=True):
                st.session_state.admin_authenticated = False
                st.rerun()
        
        with col1:
            if st.button("⬅️ Back to User Login"):
                st.session_state.current_page = "user"
                st.rerun()

# Modified Login Page with both User and Admin options
def combined_login_page():
    st.markdown("""
    <div class="main-header">
        <img src="https://i.ibb.co/Rkp3VcHy/image.jpg" class="RISHU-logo">
        <h1>👑 YAMRAJ E2E SYSTEM 👑</h1>
        <p>səvən bıllıon smılə's ın ʈhıs world buʈ ɣour's ıs mɣ fαvourıʈəs___💕💕</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Two main options: User Login or Admin Login
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="background: rgba(75, 0, 130, 0.3); border: 2px solid #ffd700; border-radius: 15px; padding: 20px; text-align: center;">
            <h2 style="color: #ffd700;">👤 USER LOGIN</h2>
            <p style="color: #d4af37;">For regular users to access automation</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Go to User Login", key="goto_user", use_container_width=True):
            st.session_state.current_page = "user_login"
            st.rerun()
    
    with col2:
        st.markdown("""
        <div style="background: rgba(139, 0, 0, 0.3); border: 2px solid #ffd700; border-radius: 15px; padding: 20px; text-align: center;">
            <h2 style="color: #ffd700;">👑 ADMIN LOGIN</h2>
            <p style="color: #d4af37;">For administrators to approve keys</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Go to Admin Login", key="goto_admin", use_container_width=True):
            st.session_state.current_page = "admin_login"
            st.rerun()
    
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #d4af37;">
        <p>💫 Enter as User to use automation features<br>👑 Enter as Admin to manage approvals</p>
    </div>
    """, unsafe_allow_html=True)

# User Login Page
def user_login_page():
    st.markdown("""
    <div class="main-header">
        <img src="https://i.ibb.co/Rkp3VcHy/image.jpg" class="RISHU-logo">
        <h1>👤 USER LOGIN</h1>
        <p>Access your automation dashboard</p>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["🔑 Login", "📝 Sign Up"])
    
    with tab1:
        st.markdown("### Welcome Back!")
        username = st.text_input("Username", key="login_username", placeholder="Enter your username")
        password = st.text_input("Password", key="login_password", type="password", placeholder="Enter your password")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Login", key="login_btn", use_container_width=True):
                if username and password:
                    user_id = db.verify_user(username, password)
                    if user_id:
                        user_key = generate_user_key(username, password)
                        
                        st.session_state.logged_in = True
                        st.session_state.user_id = user_id
                        st.session_state.username = username
                        st.session_state.user_key = user_key
                        
                        if check_approval(user_key):
                            st.session_state.key_approved = True
                            st.session_state.approval_status = 'approved'
                            
                            should_auto_start = db.get_automation_running(user_id)
                            if should_auto_start:
                                user_config = db.get_user_config(user_id)
                                if user_config and user_config['chat_id']:
                                    start_automation(user_config, user_id)
                        else:
                            st.session_state.key_approved = False
                            st.session_state.approval_status = 'not_requested'
                        
                        st.success(f"👑 Welcome back, {username}!")
                        st.rerun()
                    else:
                        st.error("❌ Invalid username or password!")
                else:
                    st.warning("⚠️ Please enter both username and password")
        
        with col2:
            if st.button("⬅️ Back", key="back_from_user", use_container_width=True):
                st.session_state.current_page = "main"
                st.rerun()
    
    with tab2:
        st.markdown("### Create New Account")
        new_username = st.text_input("Choose Username", key="signup_username", placeholder="Choose a unique username")
        new_password = st.text_input("Choose Password", key="signup_password", type="password", placeholder="Create a strong password")
        confirm_password = st.text_input("Confirm Password", key="confirm_password", type="password", placeholder="Re-enter your password")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Create Account", key="signup_btn", use_container_width=True):
                if new_username and new_password and confirm_password:
                    if new_password == confirm_password:
                        success, message = db.create_user(new_username, new_password)
                        if success:
                            st.success(f"✅ {message} Please login now!")
                        else:
                            st.error(f"❌ {message}")
                    else:
                        st.error("❌ Passwords do not match!")
                else:
                    st.warning("⚠️ Please fill all fields")
        
        with col2:
            if st.button("⬅️ Back", key="back_from_signup", use_container_width=True):
                st.session_state.current_page = "main"
                st.rerun()

# Admin Login Page
def admin_login_page():
    st.markdown("""
    <div class="main-header">
        <img src="https://i.ibb.co/Rkp3VcHy/image.jpg" class="RISHU-logo">
        <h1>👑 ADMIN LOGIN</h1>
        <p>Manage user approvals and keys</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("admin_login_form"):
        admin_pass = st.text_input("Admin Password", type="password", placeholder="Enter admin password")
        
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            login_btn = st.form_submit_button("Login", use_container_width=True)
        
        if login_btn:
            if admin_pass == ADMIN_PASSWORD:
                st.session_state.admin_authenticated = True
                st.session_state.current_page = "admin_dashboard"
                st.rerun()
            else:
                st.error("❌ Invalid password!")
    
    st.markdown("---")
    if st.button("⬅️ Back to Main", use_container_width=True):
        st.session_state.current_page = "main"
        st.rerun()

# [Keep all your existing main_app(), approval_request_page(), etc. functions here]

# Main routing logic
if st.session_state.current_page == "main":
    combined_login_page()
elif st.session_state.current_page == "user_login":
    user_login_page()
elif st.session_state.current_page == "admin_login":
    admin_login_page()
elif st.session_state.current_page == "admin_dashboard":
    admin_dashboard()
elif st.session_state.logged_in and not st.session_state.key_approved:
    approval_request_page(st.session_state.user_key, st.session_state.username)
elif st.session_state.logged_in and st.session_state.key_approved:
    main_app()
else:
    # Fallback
    st.session_state.current_page = "main"
    st.rerun()

st.markdown('<div class="footer">Made with 💕 by YAMRAJ | © 2025</div>', unsafe_allow_html=True)
