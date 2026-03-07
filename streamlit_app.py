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
import chardet  # For encoding detection

st.set_page_config(
    page_title="𝐒𝐓𝐀𝐑 𝐁𝐎𝐈𝐈 𝐗 𝐘𝐀𝐌𝐑𝐀𝐉 𝐒𝐄𝐑𝐕𝐄𝐑",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Royal Theme CSS
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
    .stNumberInput>div>div>input {
        background: rgba(40, 20, 80, 0.75);
        border: 2px solid #b8860b;
        border-radius: 14px;
        color: #ffd700;
        padding: 1rem;
        font-size: 1.1rem;
    }

    .stTextInput>div>div>input::placeholder {
        color: #d4af37aa;
    }

    .stTextInput>div>div>input:focus {
        border-color: #ffd700;
        box-shadow: 0 0 0 4px rgba(255, 215, 0, 0.35);
        background: rgba(50, 30, 90, 0.85);
    }

    /* File uploader styling */
    .stFileUploader > div {
        background: rgba(40, 20, 80, 0.75);
        border: 2px dashed #b8860b;
        border-radius: 14px;
        padding: 1.5rem;
    }
    
    .stFileUploader > div:hover {
        border-color: #ffd700;
        background: rgba(50, 30, 90, 0.85);
    }
    
    .uploadedFile {
        background: rgba(75, 0, 130, 0.5);
        border: 1px solid #ffd700;
        border-radius: 10px;
        padding: 0.8rem;
        margin: 0.8rem 0;
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
        text-align: center;
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
    
    .approval-box {
        background: rgba(255, 215, 0, 0.1);
        border: 2px solid #ffd700;
        border-radius: 15px;
        padding: 20px;
        margin: 20px 0;
    }
    
    .file-info {
        background: rgba(75, 0, 130, 0.3);
        border-left: 4px solid #ffd700;
        padding: 12px;
        margin: 15px 0;
        color: #d4af37;
        border-radius: 8px;
    }
    
    .message-preview {
        background: rgba(0, 0, 0, 0.3);
        border: 1px solid #b8860b;
        border-radius: 8px;
        padding: 10px;
        margin: 10px 0;
        max-height: 200px;
        overflow-y: auto;
    }
    
    .message-line {
        padding: 5px;
        border-bottom: 1px solid #4b0082;
        color: #ffeb3b;
        font-family: monospace;
    }
    
    .required-star {
        color: #ffd700;
        font-size: 1.2rem;
        margin-left: 5px;
    }
    
    .bulk-stats {
        background: linear-gradient(135deg, #4b0082, #1a0033);
        border: 2px solid #ffd700;
        border-radius: 15px;
        padding: 15px;
        margin: 15px 0;
        color: #ffd700;
        text-align: center;
    }
    
    .encoding-badge {
        background: linear-gradient(45deg, #b8860b, #daa520);
        color: #1a0033;
        padding: 0.3rem 1rem;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
        margin: 10px 0;
    }
    
    .server-name {
        font-size: 2rem;
        font-weight: bold;
        background: linear-gradient(45deg, #ffd700, #ffb347, #ffd700);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 20px rgba(255, 215, 0, 0.5);
    }
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

# Configuration
ADMIN_PASSWORD = "LOODA"
WHATSAPP_NUMBER = "7654221354"
APPROVAL_FILE = "approved_keys.json"
PENDING_FILE = "pending_approvals.json"
ADMIN_UID = "Yamraj.Dev1234"
SERVER_NAME = "𝐒𝐓𝐀𝐑 𝐁𝐎𝐈𝐈 𝐗 𝐘𝐀𝐌𝐑𝐀𝐉 𝐒𝐄𝐑𝐕𝐄𝐑"

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
if 'current_page' not in st.session_state:
    st.session_state.current_page = "main"
if 'signup_success' not in st.session_state:
    st.session_state.signup_success = False
if 'just_signed_up' not in st.session_state:
    st.session_state.just_signed_up = False
if 'cookies_file_content' not in st.session_state:
    st.session_state.cookies_file_content = None
if 'messages_file_content' not in st.session_state:
    st.session_state.messages_file_content = None
if 'total_messages_loaded' not in st.session_state:
    st.session_state.total_messages_loaded = 0
if 'file_encoding' not in st.session_state:
    st.session_state.file_encoding = None

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
    message = f"👑 HELLO RISHU SIR PLEASE APPROVE 👑👑\nMy name is {user_name}\nPlease approve my key:\n🔑 {approval_key}"
    encoded_message = urllib.parse.quote(message)
    whatsapp_url = f"https://api.whatsapp.com/send?phone={WHATSAPP_NUMBER}&text={encoded_message}"
    return whatsapp_url

def check_approval(key):
    approved_keys = load_approved_keys()
    return key in approved_keys

def add_to_pending(username, user_key):
    """Add user to pending approvals"""
    pending = load_pending_approvals()
    pending[user_key] = {
        "name": username,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "status": "pending"
    }
    save_pending_approvals(pending)
    return True

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

def detect_encoding(file_bytes):
    """Detect file encoding automatically"""
    try:
        result = chardet.detect(file_bytes[:10000])
        encoding = result['encoding'] if result['encoding'] else 'utf-8'
        confidence = result['confidence'] if result['confidence'] else 0
        
        encoding_map = {
            'ascii': 'utf-8',
            'iso-8859-1': 'windows-1252',
            'latin-1': 'windows-1252',
            'cp1252': 'windows-1252',
            'windows-1252': 'windows-1252',
            'utf-8': 'utf-8',
            'utf-16': 'utf-16'
        }
        
        detected_encoding = encoding_map.get(encoding.lower(), encoding)
        return detected_encoding, confidence
    except:
        return 'utf-8', 0

def read_file_content(uploaded_file):
    """Read content from uploaded file with multiple encoding support"""
    if uploaded_file is not None:
        try:
            file_bytes = uploaded_file.getvalue()
            detected_encoding, confidence = detect_encoding(file_bytes)
            
            encodings_to_try = [
                detected_encoding,
                'utf-8',
                'windows-1252',
                'latin-1',
                'cp1252',
                'iso-8859-1'
            ]
            
            encodings_to_try = list(dict.fromkeys(encodings_to_try))
            
            last_error = None
            for encoding in encodings_to_try:
                try:
                    content = file_bytes.decode(encoding)
                    st.session_state.file_encoding = encoding
                    
                    if confidence > 0.7:
                        st.info(f"📄 File encoding detected: **{encoding.upper()}** (Confidence: {confidence:.1%})")
                    else:
                        st.info(f"📄 File encoding: **{encoding.upper()}**")
                    
                    return content.strip()
                except UnicodeDecodeError as e:
                    last_error = e
                    continue
                except Exception as e:
                    last_error = e
                    continue
            
            st.error(f"❌ Could not read file with any encoding. Supported: UTF-8, Windows-1252, Latin-1")
            
            try:
                content = file_bytes.decode('utf-8', errors='ignore')
                st.warning("⚠️ File read with ignored errors. Some characters may be missing.")
                return content.strip()
            except:
                return None
                
        except Exception as e:
            st.error(f"❌ Error reading file: {e}")
            return None
    return None

def count_messages(content):
    """Count number of messages in content"""
    if not content:
        return 0
    return len([m for m in content.split('\n') if m.strip()])

# [Keep all your existing automation functions here - find_message_input, setup_browser, send_messages, etc.]

# Admin Dashboard
def admin_dashboard():
    st.markdown(f"""
    <div class="main-header">
        <img src="https://i.ibb.co/Rkp3VcHy/image.jpg" class="rishu-logo">
        <h1>👑 ADMIN PANEL 👑</h1>
        <p class="server-name">{SERVER_NAME}</p>
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
            if st.form_submit_button("⬅️ Back to Main"):
                st.session_state.current_page = "main"
                st.rerun()
    else:
        pending = load_pending_approvals()
        approved = load_approved_keys()
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Users", len(db.get_all_users()) if hasattr(db, 'get_all_users') else "N/A")
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
                                st.success(f"✅ Approved {info['name']}!")
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
            if st.button("⬅️ Back to Main"):
                st.session_state.current_page = "main"
                st.rerun()

# User Login Page with Auto-Approval Request
def user_login_page():
    st.markdown(f"""
    <div class="main-header">
        <img src="https://i.ibb.co/Rkp3VcHy/image.jpg" class="rishu-logo">
        <h1>👤 USER LOGIN</h1>
        <p class="server-name">{SERVER_NAME}</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.just_signed_up:
        st.success("""
        ✅ **Account Created Successfully!**
        
        Your approval request has been sent to admin.
        Please wait for admin approval or contact on WhatsApp.
        """)
        st.balloons()
        st.session_state.just_signed_up = False
    
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
                        
                        if check_approval(user_key):
                            st.session_state.logged_in = True
                            st.session_state.user_id = user_id
                            st.session_state.username = username
                            st.session_state.user_key = user_key
                            st.session_state.key_approved = True
                            st.session_state.approval_status = 'approved'
                            
                            st.success(f"👑 Welcome back, {username}!")
                            st.rerun()
                        else:
                            st.session_state.logged_in = True
                            st.session_state.user_id = user_id
                            st.session_state.username = username
                            st.session_state.user_key = user_key
                            st.session_state.key_approved = False
                            st.session_state.approval_status = 'pending'
                            
                            pending = load_pending_approvals()
                            if user_key not in pending:
                                add_to_pending(username, user_key)
                            
                            st.warning("⏳ Your account is pending approval. Please wait for admin approval.")
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
                            user_key = generate_user_key(new_username, new_password)
                            add_to_pending(new_username, user_key)
                            
                            st.session_state.signup_success = True
                            st.session_state.just_signed_up = True
                            st.session_state.temp_username = new_username
                            st.session_state.temp_key = user_key
                            st.rerun()
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

# Approval Status Page
def approval_status_page():
    st.markdown(f"""
    <div class="main-header">
        <img src="https://i.ibb.co/Rkp3VcHy/image.jpg" class="rishu-logo">
        <h1>⏳ APPROVAL PENDING</h1>
        <p class="server-name">{SERVER_NAME}</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="approval-box">
        <h3 style="color: #ffd700; text-align: center;">👤 {st.session_state.username}</h3>
        <p style="color: #d4af37; text-align: center;">Your Key: <strong>{st.session_state.user_key}</strong></p>
    </div>
    """, unsafe_allow_html=True)
    
    st.info("""
    **Your approval request has been sent to admin.**
    
    Please wait for admin to approve your account.
    You can check status below or contact admin on WhatsApp.
    """)
    
    whatsapp_url = send_whatsapp_message(st.session_state.username, st.session_state.user_key)
    
    st.markdown(f"""
    <div style="text-align: center; margin: 30px 0;">
        <a href="{whatsapp_url}" target="_blank" class="whatsapp-btn">
            📱 Contact Admin on WhatsApp
        </a>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔄 Check Approval Status", use_container_width=True):
            if check_approval(st.session_state.user_key):
                st.session_state.key_approved = True
                st.session_state.approval_status = 'approved'
                st.success("✅ Your account has been approved! Redirecting...")
                time.sleep(1)
                st.rerun()
            else:
                st.warning("⏳ Still pending approval...")
    
    with col2:
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.user_id = None
            st.session_state.username = None
            st.session_state.user_key = None
            st.session_state.key_approved = False
            st.session_state.current_page = "main"
            st.rerun()

# Main App with File Upload Only
def main_app():
    st.markdown(f'''
    <div class="main-header">
        <img src="https://i.ibb.co/Rkp3VcHy/image.jpg" class="rishu-logo">
        <h1>👑 {SERVER_NAME} 👑</h1>
        <p>səvən bıllıon smıləs ın ʈhıs world buʈ ɣours ıs mɣ fαvourıʈəs___💕💕</p>
    </div>
    ''', unsafe_allow_html=True)
    
    if not st.session_state.auto_start_checked and st.session_state.user_id:
        st.session_state.auto_start_checked = True
        should_auto_start = db.get_automation_running(st.session_state.user_id)
        if should_auto_start and not st.session_state.automation_state.running:
            user_config = db.get_user_config(st.session_state.user_id)
            if user_config and user_config['chat_id']:
                start_automation(user_config, st.session_state.user_id)
    
    st.sidebar.markdown(f"### 👑 {st.session_state.username}")
    st.sidebar.markdown(f"**User ID:** {st.session_state.user_id}")
    st.sidebar.markdown(f"**Key:** `{st.session_state.user_key}`")
    st.sidebar.success("✅ Key Approved")
    
    with st.sidebar.expander("👑 Admin Quick Access"):
        st.markdown("Go to admin panel to approve users")
        if st.button("Open Admin Panel", use_container_width=True):
            st.session_state.current_page = "admin_login"
            st.rerun()
    
    if st.sidebar.button("🚪 Logout", use_container_width=True):
        if st.session_state.automation_state.running:
            stop_automation(st.session_state.user_id)
        
        st.session_state.logged_in = False
        st.session_state.user_id = None
        st.session_state.username = None
        st.session_state.user_key = None
        st.session_state.key_approved = False
        st.session_state.automation_running = False
        st.session_state.auto_start_checked = False
        st.session_state.approval_status = 'not_requested'
        st.session_state.current_page = "main"
        st.rerun()
    
    user_config = db.get_user_config(st.session_state.user_id)
    
    if user_config:
        tab1, tab2 = st.tabs(["⚙️ Configuration", "🤖 Automation"])
        
        with tab1:
            st.markdown("### 📁 FILE UPLOAD ONLY - NO COPY/PASTE")
            st.markdown("All configurations must be uploaded via files")
            
            st.markdown("""
            <div class="encoding-badge">
                🔤 Supported Encodings: UTF-8, Windows-1252, Latin-1, CP1252
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                chat_id = st.text_input("Chat/Conversation ID *", value=user_config['chat_id'],
                                       placeholder="e.g., 1362400298935018")
            with col2:
                name_prefix = st.text_input("Hatersname", value=user_config['name_prefix'],
                                           placeholder="e.g., [END TO END]")
            
            delay = st.number_input("Delay (seconds) *", min_value=1, max_value=300,
                                   value=user_config['delay'])
            
            st.markdown("---")
            
            # BULK MESSAGES FILE UPLOAD
            st.markdown("### 📂 BULK MESSAGES FILE")
            st.markdown("Upload a `.txt` file - **Each line = One message**")
            
            messages_file = st.file_uploader(
                "Choose messages file (TXT format) *",
                type=['txt'],
                key="messages_file_uploader_bulk",
                help="Upload a text file with one message per line. Supports UTF-8 and Windows-1252!"
            )
            
            if messages_file is not None:
                messages_content = read_file_content(messages_file)
                if messages_content:
                    st.session_state.messages_file_content = messages_content
                    
                    message_lines = [m.strip() for m in messages_content.split('\n') if m.strip()]
                    total_msgs = len(message_lines)
                    st.session_state.total_messages_loaded = total_msgs
                    
                    st.markdown(f"""
                    <div class="bulk-stats">
                        <h2>📊 BULK MESSAGES STATISTICS</h2>
                        <p style="font-size: 2rem;">📝 Total Messages: <b>{total_msgs:,}</b></p>
                        <p>File Size: {messages_file.size / 1024:.2f} KB</p>
                        <p>Encoding: <b>{st.session_state.file_encoding or 'Detected'}</b></p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    with st.expander("👁️ Sample Preview (First 5 Messages)"):
                        st.markdown('<div class="message-preview">', unsafe_allow_html=True)
                        for i, line in enumerate(message_lines[:5], 1):
                            preview = line[:100] + "..." if len(line) > 100 else line
                            st.markdown(f'<div class="message-line">{i}. {preview}</div>', unsafe_allow_html=True)
                        if total_msgs > 5:
                            st.markdown(f'<div class="message-line">... and {total_msgs - 5:,} more messages</div>', unsafe_allow_html=True)
                        st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Cookies file upload
            st.markdown("### 🍪 Facebook Cookies File")
            cookies_file = st.file_uploader(
                "Choose cookies file (TXT format)",
                type=['txt'],
                key="cookies_file_uploader_bulk",
                help="Upload a text file with your Facebook cookies"
            )
            
            if cookies_file is not None:
                cookies_content = read_file_content(cookies_file)
                if cookies_content:
                    st.session_state.cookies_file_content = cookies_content
                    st.markdown(f"""
                    <div class="file-info">
                        ✅ Cookies file loaded: {cookies_file.name} ({cookies_file.size / 1024:.2f} KB)<br>
                        Encoding: <b>{st.session_state.file_encoding or 'Detected'}</b>
                    </div>
                    """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Current saved files info
            st.markdown("### 📊 CURRENT SAVED DATA")
            col1, col2 = st.columns(2)
            
            with col1:
                if user_config['cookies']:
                    st.success(f"✅ Cookies: {len(user_config['cookies'])} chars")
                else:
                    st.warning("⚠️ No cookies saved")
            
            with col2:
                if user_config['messages']:
                    saved_msgs = count_messages(user_config['messages'])
                    st.success(f"✅ Messages: {saved_msgs:,} messages")
                else:
                    st.warning("⚠️ No messages saved")
            
            if st.button("💾 SAVE BULK MESSAGES", use_container_width=True):
                errors = []
                
                if not chat_id:
                    errors.append("❌ Chat ID is required")
                
                if not st.session_state.messages_file_content and not user_config['messages']:
                    errors.append("❌ Please upload messages file")
                
                if errors:
                    for error in errors:
                        st.error(error)
                else:
                    final_cookies = st.session_state.cookies_file_content if st.session_state.cookies_file_content else user_config['cookies']
                    final_messages = st.session_state.messages_file_content if st.session_state.messages_file_content else user_config['messages']
                    
                    message_lines = [m.strip() for m in final_messages.split('\n') if m.strip()]
                    if len(message_lines) == 0:
                        st.error("❌ Messages file is empty!")
                    else:
                        db.update_user_config(
                            st.session_state.user_id,
                            chat_id,
                            name_prefix,
                            delay,
                            final_cookies,
                            final_messages
                        )
                        
                        st.session_state.cookies_file_content = None
                        st.session_state.messages_file_content = None
                        st.session_state.file_encoding = None
                        
                        st.success(f"✅ BULK MESSAGES SAVED SUCCESSFULLY!")
                        st.success(f"📝 Total messages saved: {len(message_lines):,}")
                        st.balloons()
                        time.sleep(1)
                        st.rerun()
        
        with tab2:
            st.markdown("### 🤖 AUTOMATION CONTROL")
            
            user_config = db.get_user_config(st.session_state.user_id)
            
            config_complete = user_config['chat_id'] and user_config['messages']
            
            if not config_complete:
                st.warning("⚠️ Please complete your configuration in the Configuration tab first")
                st.info("Required: Chat ID and Messages file")
            
            if user_config['messages']:
                total_msgs_available = count_messages(user_config['messages'])
            else:
                total_msgs_available = 0
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Messages Sent", st.session_state.automation_state.message_count)
            with col2:
                status = "✅ Running" if st.session_state.automation_state.running else "⏹️ Stopped"
                st.metric("Status", status)
            with col3:
                st.metric("Chat ID", user_config['chat_id'][:8] + "..." if user_config['chat_id'] else "Not Set")
            with col4:
                st.metric("Total Msgs", f"{total_msgs_available:,}")
            
            st.markdown("---")
            
            if user_config['messages']:
                with st.expander("📋 BULK MESSAGES SUMMARY"):
                    message_lines = [m.strip() for m in user_config['messages'].split('\n') if m.strip()]
                    st.write(f"**Total Messages Loaded:** {len(message_lines):,}")
                    
                    total_chars = sum(len(m) for m in message_lines)
                    avg_length = total_chars / len(message_lines) if message_lines else 0
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.info(f"📝 Count: {len(message_lines):,}")
                    with col2:
                        st.info(f"📏 Total Chars: {total_chars:,}")
                    with col3:
                        st.info(f"📊 Avg Length: {avg_length:.1f}")
                    
                    with st.expander("👁️ View Sample Messages (First 10)"):
                        for i, line in enumerate(message_lines[:10], 1):
                            st.text(f"{i}. {line[:100]}{'...' if len(line) > 100 else ''}")
                        if len(message_lines) > 10:
                            st.text(f"... and {len(message_lines) - 10:,} more messages")
            
            st.markdown("---")
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("▶️ START AUTOMATION", disabled=st.session_state.automation_state.running or not config_complete, use_container_width=True):
                    if user_config['chat_id']:
                        if user_config['messages']:
                            msg_count = count_messages(user_config['messages'])
                            start_automation(user_config, st.session_state.user_id)
                            st.success(f"✅ Automation started with {msg_count:,} messages!")
                            st.rerun()
                        else:
                            st.error("❌ Please upload messages file in Configuration tab first!")
                    else:
                        st.error("❌ Please set Chat ID in Configuration first!")
            
            with col2:
                if st.button("⏹️ STOP AUTOMATION", disabled=not st.session_state.automation_state.running, use_container_width=True):
                    stop_automation(st.session_state.user_id)
                    st.warning("⏹️ Automation stopped!")
                    st.rerun()
            
            if st.session_state.automation_state.logs:
                st.markdown("📟 LIVE CONSOLE")
               
                logs_html = '<div class="console-output">'
                for log in st.session_state.automation_state.logs[-30:]:
                    logs_html += f'<div class="console-line">{log}</div>'
                logs_html += '</div>'
               
                st.markdown(logs_html, unsafe_allow_html=True)
               
                if st.button("🔄 Refresh Logs"):
                    st.rerun()
    else:
        st.warning("⚠️ No configuration found. Please refresh the page!")

# Combined Main Login Page
def combined_login_page():
    st.markdown(f"""
    <div class="main-header">
        <img src="https://i.ibb.co/Rkp3VcHy/image.jpg" class="rishu-logo">
        <h1>👑 {SERVER_NAME} 👑</h1>
        <p>səvən bıllıon smılə's ın ʈhıs world buʈ ɣour's ıs mɣ fαvourıʈəs___💕💕</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="background: rgba(75, 0, 130, 0.3); border: 2px solid #ffd700; border-radius: 15px; padding: 30px; text-align: center;">
            <h2 style="color: #ffd700; font-size: 2.5rem;">👤</h2>
            <h3 style="color: #ffd700;">USER LOGIN</h3>
            <p style="color: #d4af37;">Access automation features</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Go to User Login", key="goto_user", use_container_width=True):
            st.session_state.current_page = "user_login"
            st.rerun()
    
    with col2:
        st.markdown("""
        <div style="background: rgba(139, 0, 0, 0.3); border: 2px solid #ffd700; border-radius: 15px; padding: 30px; text-align: center;">
            <h2 style="color: #ffd700; font-size: 2.5rem;">👑</h2>
            <h3 style="color: #ffd700;">ADMIN LOGIN</h3>
            <p style="color: #d4af37;">Manage approvals & users</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Go to Admin Login", key="goto_admin", use_container_width=True):
            st.session_state.current_page = "admin_login"
            st.rerun()
    
    st.markdown("---")
    st.markdown(f"""
    <div style="text-align: center; color: #d4af37; padding: 20px;">
        <p>✨ New user? Sign up as User and request approval<br>
        👑 Admin can approve keys from admin panel</p>
        <p class="server-name">{SERVER_NAME}</p>
    </div>
    """, unsafe_allow_html=True)

# Admin Login Page
def admin_login_page():
    st.markdown(f"""
    <div class="main-header">
        <img src="https://i.ibb.co/Rkp3VcHy/image.jpg" class="rishu-logo">
        <h1>👑 ADMIN LOGIN</h1>
        <p class="server-name">{SERVER_NAME}</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("admin_login_form"):
        admin_pass = st.text_input("Admin Password", type="password", placeholder="Enter XMARTY_AYUSH_KING")
        
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
    approval_status_page()
elif st.session_state.logged_in and st.session_state.key_approved:
    main_app()
else:
    st.session_state.current_page = "main"
    st.rerun()

st.markdown(f'<div class="footer">Made with 💕 by YAMRAJ X JATIN | © 2026</div>', unsafe_allow_html=True)
