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
import gc
import tempfile
from datetime import datetime

st.set_page_config(
    page_title="E2E YAMRAJ APPROVAL SYSTEM",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 👑 SIMPLE CLEAN CSS
custom_css = """
<style>
    /* Simple clean font for everyone */
    * {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }

    .main .block-container {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 30px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.1);
    }

    /* Admin Panel Header */
    .admin-header {
        background: linear-gradient(135deg, #ff6b6b, #ee5253);
        color: white;
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 20px;
        text-align: center;
    }
    
    .admin-header h1 {
        margin: 0;
        font-size: 2.2rem;
    }

    /* User Panel Header */
    .user-header {
        background: linear-gradient(135deg, #4834d4, #686de0);
        color: white;
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 20px;
        text-align: center;
    }
    
    .user-header h1 {
        margin: 0;
        font-size: 2.2rem;
    }

    /* Category Badges */
    .admin-badge {
        background: #ff6b6b;
        color: white;
        padding: 5px 15px;
        border-radius: 20px;
        font-size: 0.9rem;
        display: inline-block;
        margin: 5px;
    }
    
    .user-badge {
        background: #4834d4;
        color: white;
        padding: 5px 15px;
        border-radius: 20px;
        font-size: 0.9rem;
        display: inline-block;
        margin: 5px;
    }
    
    .pending-badge {
        background: #f39c12;
        color: white;
        padding: 5px 15px;
        border-radius: 20px;
        font-size: 0.9rem;
        display: inline-block;
        margin: 5px;
    }

    /* Buttons */
    .stButton>button {
        border-radius: 10px;
        font-weight: 600;
        transition: all 0.3s;
        border: none;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }

    /* Admin Button */
    div[data-testid="column"]:nth-of-type(1) .stButton>button {
        background: linear-gradient(135deg, #4834d4, #686de0);
        color: white;
    }
    
    /* User Button */
    div[data-testid="column"]:nth-of-type(2) .stButton>button {
        background: linear-gradient(135deg, #ff6b6b, #ee5253);
        color: white;
    }
    
    /* Danger Button */
    div[data-testid="column"]:nth-of-type(3) .stButton>button {
        background: linear-gradient(135deg, #ff6b6b, #ee5253);
        color: white;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.8; }
        100% { opacity: 1; }
    }

    /* Input Fields */
    .stTextInput>div>div>input,
    .stTextArea>div>div>textarea,
    .stNumberInput>div>div>input {
        border-radius: 10px;
        border: 2px solid #e0e0e0;
        padding: 12px;
        font-size: 1rem;
    }
    
    .stTextInput>div>div>input:focus,
    .stTextArea>div>div>textarea:focus,
    .stNumberInput>div>div>input:focus {
        border-color: #4834d4;
        box-shadow: 0 0 0 3px rgba(72, 52, 212, 0.1);
    }

    /* Metrics */
    [data-testid="stMetricValue"] {
        color: #4834d4;
        font-size: 2rem;
        font-weight: 700;
    }
    
    [data-testid="stMetricLabel"] {
        color: #666;
        font-weight: 500;
    }

    /* Console Output */
    .console-output {
        background: #1e1e2f;
        border-radius: 10px;
        padding: 15px;
        color: #00ff00;
        font-family: 'Courier New', monospace;
        font-size: 13px;
        max-height: 400px;
        overflow-y: auto;
    }

    .console-line {
        border-bottom: 1px solid #333;
        padding: 5px 10px;
        margin: 3px 0;
        font-family: 'Courier New', monospace;
    }
    
    .console-line-success { color: #00ff00; }
    .console-line-error { color: #ff4444; }
    .console-line-info { color: #ffffaa; }
    .console-line-send { color: #00ffff; }

    /* Status Box */
    .status-box {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        margin: 10px 0;
    }
    
    .status-box h3 {
        margin: 0;
        font-size: 1.5rem;
    }

    /* Secret Key Display */
    .secret-key {
        background: #f0f0f0;
        padding: 15px;
        border-radius: 10px;
        font-family: 'Courier New', monospace;
        font-size: 1.2rem;
        text-align: center;
        border: 2px dashed #4834d4;
        margin: 10px 0;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #666;
        padding: 20px;
        font-size: 0.9rem;
    }
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

# ==================== CONSTANTS ====================
WHATSAPP_NUMBER = "7654221354"  # Admin ka WhatsApp number
ADMIN_SECRET_PASSWORD = "YAMRAJ@ADMIN@2025"  # Admin direct login password
APPROVAL_FILE = "approved_users.json"
PENDING_FILE = "pending_users.json"
USERS_FILE = "registered_users.json"

# ==================== HELPER FUNCTIONS ====================
def generate_secret_key(username, password):
    """Generate unique secret key for user"""
    combined = f"{username}:{password}:{time.time()}"
    key_hash = hashlib.sha256(combined.encode()).hexdigest()[:12].upper()
    return f"KEY-{key_hash}"

def load_json_file(filename, default={}):
    """Load JSON file safely"""
    if os.path.exists(filename):
        try:
            with open(filename, 'r') as f:
                return json.load(f)
        except:
            return default
    return default

def save_json_file(filename, data):
    """Save JSON file safely"""
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

def load_approved_users():
    return load_json_file(APPROVAL_FILE, {})

def save_approved_users(users):
    save_json_file(APPROVAL_FILE, users)

def load_pending_users():
    return load_json_file(PENDING_FILE, {})

def save_pending_users(users):
    save_json_file(PENDING_FILE, users)

def load_registered_users():
    return load_json_file(USERS_FILE, {})

def save_registered_users(users):
    save_json_file(USERS_FILE, users)

def send_whatsapp_notification(username, secret_key):
    """Send secret key to admin WhatsApp"""
    message = f"""👑 NEW USER REGISTRATION - YAMRAJ SYSTEM 👑

👤 Username: {username}
🔑 Secret Key: {secret_key}
⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Please approve this user in Admin Panel!"""
    
    encoded_message = urllib.parse.quote(message)
    whatsapp_url = f"https://api.whatsapp.com/send?phone={WHATSAPP_NUMBER}&text={encoded_message}"
    return whatsapp_url

def check_user_approval(username):
    """Check if user is approved"""
    approved = load_approved_users()
    return username in approved

def register_new_user(username, password):
    """Register new user and add to pending"""
    # Check if user already exists
    registered = load_registered_users()
    if username in registered:
        return False, "Username already exists!"
    
    # Generate secret key
    secret_key = generate_secret_key(username, password)
    
    # Save registered user
    registered[username] = {
        "username": username,
        "password": password,  # In production, hash this!
        "secret_key": secret_key,
        "registered_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "status": "pending"
    }
    save_registered_users(registered)
    
    # Add to pending approvals
    pending = load_pending_users()
    pending[username] = {
        "username": username,
        "secret_key": secret_key,
        "requested_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    save_pending_users(pending)
    
    return True, secret_key

# ==================== SESSION STATE ====================
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_type' not in st.session_state:  # 'admin' or 'user'
    st.session_state.user_type = None
if 'username' not in st.session_state:
    st.session_state.username = None
if 'secret_key' not in st.session_state:
    st.session_state.secret_key = None
if 'user_approved' not in st.session_state:
    st.session_state.user_approved = False
if 'pending_status' not in st.session_state:
    st.session_state.pending_status = None
if 'automation_running' not in st.session_state:
    st.session_state.automation_running = False
if 'logs' not in st.session_state:
    st.session_state.logs = []
if 'message_count' not in st.session_state:
    st.session_state.message_count = 0
if 'show_close_confirmation' not in st.session_state:
    st.session_state.show_close_confirmation = False
if 'last_refresh' not in st.session_state:
    st.session_state.last_refresh = time.time()
if 'messages_content' not in st.session_state:
    st.session_state.messages_content = ""

class AutomationState:
    def __init__(self):
        self.running = False
        self.message_count = 0
        self.logs = []
        self.message_rotation_index = 0
        self.driver = None
        self.current_chat_id = None
        self.speed = 0
        self.total_messages = 0
        self.start_time = None

if 'automation_state' not in st.session_state:
    st.session_state.automation_state = AutomationState()

# ==================== LOGGING FUNCTION ====================
def log_message(msg, msg_type="info", automation_state=None):
    now = datetime.now()
    timestamp = now.strftime("%I:%M:%S %p")
    
    emoji_map = {
        "success": "✅",
        "error": "❌",
        "warning": "⚠️",
        "send": "📤",
        "load": "📥",
        "info": "ℹ️"
    }
    emoji = emoji_map.get(msg_type, "ℹ️")
    
    formatted_msg = f"[{timestamp}] {emoji} {msg}"
   
    if automation_state:
        automation_state.logs.append(formatted_msg)
        if len(automation_state.logs) > 100:
            automation_state.logs = automation_state.logs[-100:]
    else:
        st.session_state.logs.append(formatted_msg)
        if len(st.session_state.logs) > 100:
            st.session_state.logs = st.session_state.logs[-100:]
    
    return formatted_msg

# ==================== AUTOMATION FUNCTIONS ====================
def find_message_input(driver, process_id, automation_state=None):
    log_message(f'{process_id}: Finding message input...', "info", automation_state)
    # ... (rest of the function remains same)
    # For brevity, keeping the function signature but you can keep your existing implementation
    return None

def setup_browser(automation_state=None):
    log_message('Setting up Chrome browser...', "info", automation_state)
    # ... (rest of the function remains same)
    return None

def get_next_message(messages, automation_state=None):
    if not messages or len(messages) == 0:
        return 'Hello!'
   
    if automation_state:
        message = messages[automation_state.message_rotation_index % len(messages)]
        automation_state.message_rotation_index += 1
    else:
        message = messages[0]
   
    return message

def send_messages(config, automation_state, user_id, process_id='AUTO-1'):
    # ... (your existing implementation)
    pass

def start_automation(user_config, user_id):
    automation_state = st.session_state.automation_state
   
    if automation_state.running:
        return
   
    automation_state.running = True
    automation_state.message_count = 0
    automation_state.logs = []
    automation_state.current_chat_id = user_config['chat_id']
    automation_state.start_time = datetime.now()
   
    db.set_automation_running(user_id, True)
   
    thread = threading.Thread(target=send_messages, args=(user_config, automation_state, user_id))
    thread.daemon = True
    thread.start()

def stop_automation(user_id):
    st.session_state.automation_state.running = False
    db.set_automation_running(user_id, False)
    log_message("Automation stopped by user", "warning", st.session_state.automation_state)

# ==================== PAGE FUNCTIONS ====================
def admin_page():
    """Admin Panel - User Approval Management"""
    st.markdown("""
    <div class="admin-header">
        <h1>👑 ADMIN PANEL 👑</h1>
        <p>User Approval Management System</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Load data
    pending = load_pending_users()
    approved = load_approved_users()
    registered = load_registered_users()
    
    # Statistics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Registered", len(registered))
    with col2:
        st.metric("Pending Approval", len(pending))
    with col3:
        st.metric("Approved Users", len(approved))
    
    st.markdown("---")
    
    # Pending Approvals Section
    if pending:
        st.markdown("### ⏳ PENDING APPROVALS")
        
        for username, data in pending.items():
            with st.expander(f"👤 {username} - Requested: {data['requested_at']}"):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.markdown(f"**Username:** {username}")
                    st.markdown(f"**Secret Key:** `{data['secret_key']}`")
                    st.markdown(f"**Request Time:** {data['requested_at']}")
                
                with col2:
                    if st.button("✅ APPROVE", key=f"approve_{username}"):
                        # Add to approved
                        approved[username] = {
                            "username": username,
                            "secret_key": data['secret_key'],
                            "approved_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        }
                        save_approved_users(approved)
                        
                        # Update registered user status
                        if username in registered:
                            registered[username]['status'] = 'approved'
                            registered[username]['approved_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            save_registered_users(registered)
                        
                        # Remove from pending
                        del pending[username]
                        save_pending_users(pending)
                        
                        st.success(f"✅ User {username} approved!")
                        st.rerun()
                    
                    if st.button("❌ REJECT", key=f"reject_{username}"):
                        # Update registered user status
                        if username in registered:
                            registered[username]['status'] = 'rejected'
                            save_registered_users(registered)
                        
                        # Remove from pending
                        del pending[username]
                        save_pending_users(pending)
                        
                        st.error(f"❌ User {username} rejected!")
                        st.rerun()
    else:
        st.info("No pending approvals")
    
    st.markdown("---")
    
    # Approved Users Section
    if approved:
        st.markdown("### ✅ APPROVED USERS")
        for username in approved.keys():
            st.markdown(f"👤 **{username}**")
    
    # Logout button
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.user_type = None
        st.rerun()

def user_pending_page(username, secret_key):
    """Page shown to user while waiting for approval"""
    st.markdown("""
    <div class="user-header">
        <h1>⏳ APPROVAL PENDING</h1>
        <p>Your account is waiting for admin approval</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 👤 Your Details")
        st.markdown(f"**Username:** {username}")
        st.markdown(f"**Secret Key:** `{secret_key}`")
        st.markdown(f"**Status:** ⏳ Pending Approval")
    
    with col2:
        st.markdown("### 📱 Contact Admin")
        whatsapp_url = send_whatsapp_notification(username, secret_key)
        
        st.markdown(f"""
        <a href="{whatsapp_url}" target="_blank" style="text-decoration: none;">
            <div style="background: #25D366; color: white; padding: 15px; border-radius: 10px; text-align: center;">
                📱 Contact Admin on WhatsApp
            </div>
        </a>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background: #f0f0f0; padding: 15px; border-radius: 10px; margin-top: 10px;">
            <p style="margin:0; color: #666;">Admin will approve your account soon. Check back after approval.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Check approval status button
    if st.button("🔄 Check Approval Status", use_container_width=True):
        if check_user_approval(username):
            st.session_state.user_approved = True
            st.session_state.pending_status = None
            st.success("✅ Your account is approved! Redirecting...")
            time.sleep(2)
            st.rerun()
        else:
            st.warning("⏳ Still pending approval")
    
    # Logout
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.rerun()

def user_page():
    """Main User Dashboard"""
    st.markdown("""
    <div class="user-header">
        <h1>👤 USER DASHBOARD</h1>
        <p>Facebook Message Automation</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar user info
    with st.sidebar:
        st.markdown(f"### 👤 {st.session_state.username}")
        st.markdown(f"**Secret Key:** `{st.session_state.secret_key}`")
        st.markdown("**Status:** ✅ Approved")
        st.markdown("---")
        
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.user_type = None
            st.rerun()
    
    # Main content - Your existing automation UI
    user_config = db.get_user_config(st.session_state.user_id) if st.session_state.user_id else None
    
    if user_config:
        tab1, tab2 = st.tabs(["⚙️ Configuration", "🤖 Automation"])
        
        with tab1:
            st.markdown("### Your Configuration")
            
            chat_id = st.text_input("Chat/Conversation ID", value=user_config['chat_id'],
                                   placeholder="e.g., 1362400298935018")
            
            name_prefix = st.text_input("Hatersname", value=user_config['name_prefix'],
                                       placeholder="e.g., [END TO END]")
            
            delay = st.number_input("Delay (seconds)", min_value=1, max_value=300,
                                   value=user_config['delay'])
            
            cookies = st.text_area("Facebook Cookies", value=user_config['cookies'],
                                  placeholder="Paste your cookies here...", height=150)
            
            messages = st.text_area("Messages (one per line)", value=user_config['messages'],
                                   placeholder="Enter messages...", height=200)
            
            if st.button("💾 Save Configuration", use_container_width=True):
                db.update_user_config(st.session_state.user_id, chat_id, name_prefix, delay, cookies, messages)
                st.success("✅ Configuration saved!")
                st.rerun()
        
        with tab2:
            st.markdown("### Automation Control")
            
            # Status
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Messages Sent", st.session_state.automation_state.message_count)
            with col2:
                status = "🟢 Running" if st.session_state.automation_state.running else "🔴 Stopped"
                st.metric("Status", status)
            with col3:
                st.metric("Chat ID", user_config['chat_id'][:8] + "..." if user_config['chat_id'] else "Not Set")
            
            # Control buttons
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("▶️ START", disabled=st.session_state.automation_state.running, use_container_width=True):
                    if user_config['chat_id'] and user_config['cookies']:
                        start_automation(user_config, st.session_state.user_id)
                        st.success("✅ Started!")
                        st.rerun()
                    else:
                        st.error("❌ Set Chat ID and Cookies first!")
            
            with col2:
                if st.button("⏹️ STOP", disabled=not st.session_state.automation_state.running, use_container_width=True):
                    stop_automation(st.session_state.user_id)
                    st.rerun()
            
            with col3:
                if st.button("🗑️ CLOSE ALL", use_container_width=True):
                    st.session_state.show_close_confirmation = True
            
            # Auto-refresh when running
            if st.session_state.automation_state.running:
                if time.time() - st.session_state.last_refresh > 2:
                    st.session_state.last_refresh = time.time()
                    st.rerun()
            
            # Logs
            if st.session_state.automation_state.logs:
                st.markdown("### 📟 Live Logs")
                logs_html = '<div class="console-output">'
                for log in st.session_state.automation_state.logs[-20:]:
                    logs_html += f'<div class="console-line">{log}</div>'
                logs_html += '</div>'
                st.markdown(logs_html, unsafe_allow_html=True)
    else:
        st.warning("⚠️ No configuration found. Please contact admin.")

def login_page():
    """Main Login/Registration Page"""
    st.markdown("""
    <div style="text-align: center; margin-bottom: 30px;">
        <h1 style="color: #4834d4;">👑 E2E YAMRAJ SYSTEM</h1>
        <p style="color: #666;">Facebook Message Automation Platform</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="background: #f8f9fa; padding: 30px; border-radius: 15px; text-align: center;">
            <h2 style="color: #4834d4;">👤 USER LOGIN</h2>
            <p>For approved users only</p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("user_login_form"):
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            submitted = st.form_submit_button("🔑 Login as User", use_container_width=True)
            
            if submitted:
                if username and password:
                    # Check registered users
                    registered = load_registered_users()
                    if username in registered and registered[username]['password'] == password:
                        # Check if approved
                        if check_user_approval(username):
                            # Get user_id from database
                            user_id = db.verify_user(username, password)
                            if not user_id:
                                # Create in database if not exists
                                success, msg = db.create_user(username, password)
                                if success:
                                    user_id = db.verify_user(username, password)
                            
                            if user_id:
                                st.session_state.logged_in = True
                                st.session_state.user_type = 'user'
                                st.session_state.username = username
                                st.session_state.user_id = user_id
                                st.session_state.secret_key = registered[username]['secret_key']
                                st.session_state.user_approved = True
                                st.success("✅ Login successful!")
                                st.rerun()
                            else:
                                st.error("❌ Database error!")
                        else:
                            # Show pending page
                            st.session_state.logged_in = True
                            st.session_state.user_type = 'pending'
                            st.session_state.username = username
                            st.session_state.secret_key = registered[username]['secret_key']
                            st.session_state.pending_status = 'pending'
                            st.rerun()
                    else:
                        st.error("❌ Invalid username or password!")
                else:
                    st.warning("⚠️ Fill all fields!")
    
    with col2:
        st.markdown("""
        <div style="background: #f8f9fa; padding: 30px; border-radius: 15px; text-align: center;">
            <h2 style="color: #ff6b6b;">👑 ADMIN LOGIN</h2>
            <p>System administrators only</p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("admin_login_form"):
            admin_password = st.text_input("Admin Password", type="password", placeholder="Enter admin password")
            admin_submitted = st.form_submit_button("🔑 Login as Admin", use_container_width=True)
            
            if admin_submitted:
                if admin_password == ADMIN_SECRET_PASSWORD:
                    st.session_state.logged_in = True
                    st.session_state.user_type = 'admin'
                    st.session_state.username = "Admin"
                    st.success("✅ Admin login successful!")
                    st.rerun()
                else:
                    st.error("❌ Invalid admin password!")
    
    st.markdown("---")
    
    # Registration Section
    st.markdown("### 📝 New User Registration")
    st.markdown("Create an account and wait for admin approval")
    
    with st.form("registration_form"):
        reg_username = st.text_input("Choose Username", placeholder="Enter username")
        reg_password = st.text_input("Choose Password", type="password", placeholder="Enter password")
        reg_confirm = st.text_input("Confirm Password", type="password", placeholder="Confirm password")
        reg_submitted = st.form_submit_button("📝 Register", use_container_width=True)
        
        if reg_submitted:
            if reg_username and reg_password and reg_confirm:
                if reg_password == reg_confirm:
                    success, result = register_new_user(reg_username, reg_password)
                    if success:
                        secret_key = result
                        whatsapp_url = send_whatsapp_notification(reg_username, secret_key)
                        
                        st.success("✅ Registration successful! Please wait for admin approval.")
                        
                        # Show WhatsApp link
                        st.markdown(f"""
                        <div style="background: #25D366; padding: 15px; border-radius: 10px; text-align: center; margin: 10px 0;">
                            <a href="{whatsapp_url}" target="_blank" style="color: white; text-decoration: none; font-weight: bold;">
                                📱 Admin ko WhatsApp bhejein (Click Here)
                            </a>
                        </div>
                        <div class="secret-key">
                            Your Secret Key: {secret_key}
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.info("Login with your credentials after admin approval!")
                    else:
                        st.error(f"❌ {result}")
                else:
                    st.error("❌ Passwords don't match!")
            else:
                st.warning("⚠️ Fill all fields!")

# ==================== MAIN APP FLOW ====================
def main():
    if not st.session_state.logged_in:
        login_page()
    elif st.session_state.user_type == 'admin':
        admin_page()
    elif st.session_state.user_type == 'pending':
        user_pending_page(st.session_state.username, st.session_state.secret_key)
    elif st.session_state.user_type == 'user':
        user_page()
    
    st.markdown('<div class="footer">Made with ❤️ by YAMRAJ | © 2025</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()