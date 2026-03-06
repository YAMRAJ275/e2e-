import sqlite3
import os
import json
from datetime import datetime

DB_FILE = "users.db"

def init_database():
    """Initialize database with required tables"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            secret_key TEXT,
            approved INTEGER DEFAULT 0,
            created_at TEXT,
            approved_at TEXT
        )
    ''')
    
    # User configurations table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_config (
            user_id INTEGER PRIMARY KEY,
            chat_id TEXT,
            name_prefix TEXT,
            delay INTEGER DEFAULT 5,
            cookies TEXT,
            messages TEXT,
            automation_running INTEGER DEFAULT 0,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Admin table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS admin (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    
    # Insert default admin if not exists
    cursor.execute("SELECT * FROM admin WHERE username = 'admin'")
    if not cursor.fetchone():
        cursor.execute(
            "INSERT INTO admin (username, password) VALUES (?, ?)",
            ('admin', 'YAMRAJ@ADMIN@2025')  # Default admin password
        )
    
    conn.commit()
    conn.close()

# Call init when module loads
init_database()

def create_user(username, password, secret_key=None):
    """Create new user account"""
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        cursor.execute('''
            INSERT INTO users (username, password, secret_key, created_at, approved)
            VALUES (?, ?, ?, ?, ?)
        ''', (username, password, secret_key, created_at, 0))
        
        user_id = cursor.lastrowid
        
        # Create default config for user
        cursor.execute('''
            INSERT INTO user_config (user_id, chat_id, name_prefix, delay, cookies, messages)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id, '', '', 5, '', "Hello!\nHi!\nHow are you?"))
        
        conn.commit()
        conn.close()
        return True, "User created successfully"
    except sqlite3.IntegrityError:
        return False, "Username already exists"
    except Exception as e:
        return False, f"Error: {str(e)}"

def verify_user(username, password):
    """Verify user credentials and return user_id if approved"""
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        # Check if user is approved
        cursor.execute('''
            SELECT id FROM users 
            WHERE username = ? AND password = ? AND approved = 1
        ''', (username, password))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return result[0]  # Return user_id
        return None
    except Exception as e:
        print(f"Error verifying user: {e}")
        return None

def verify_admin(username, password):
    """Verify admin credentials"""
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id FROM admin 
            WHERE username = ? AND password = ?
        ''', (username, password))
        
        result = cursor.fetchone()
        conn.close()
        
        return result is not None
    except Exception as e:
        print(f"Error verifying admin: {e}")
        return False

def get_user_config(user_id):
    """Get user configuration"""
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT chat_id, name_prefix, delay, cookies, messages, automation_running
            FROM user_config WHERE user_id = ?
        ''', (user_id,))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {
                'chat_id': result[0] or '',
                'name_prefix': result[1] or '',
                'delay': result[2] or 5,
                'cookies': result[3] or '',
                'messages': result[4] or "Hello!\nHi!\nHow are you?",
                'automation_running': bool(result[5])
            }
        return None
    except Exception as e:
        print(f"Error getting config: {e}")
        return None

def update_user_config(user_id, chat_id, name_prefix, delay, cookies, messages):
    """Update user configuration"""
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE user_config 
            SET chat_id = ?, name_prefix = ?, delay = ?, cookies = ?, messages = ?
            WHERE user_id = ?
        ''', (chat_id, name_prefix, delay, cookies, messages, user_id))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error updating config: {e}")
        return False

def set_automation_running(user_id, running):
    """Set automation running status"""
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE user_config 
            SET automation_running = ?
            WHERE user_id = ?
        ''', (1 if running else 0, user_id))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error setting automation status: {e}")
        return False

def get_automation_running(user_id):
    """Get automation running status"""
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT automation_running FROM user_config WHERE user_id = ?
        ''', (user_id,))
        
        result = cursor.fetchone()
        conn.close()
        
        return bool(result[0]) if result else False
    except Exception as e:
        print(f"Error getting automation status: {e}")
        return False

def get_pending_users():
    """Get list of unapproved users"""
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, username, secret_key, created_at 
            FROM users 
            WHERE approved = 0
            ORDER BY created_at DESC
        ''')
        
        results = cursor.fetchall()
        conn.close()
        
        pending = {}
        for row in results:
            pending[row[1]] = {
                'id': row[0],
                'username': row[1],
                'secret_key': row[2],
                'created_at': row[3]
            }
        return pending
    except Exception as e:
        print(f"Error getting pending users: {e}")
        return {}

def get_approved_users():
    """Get list of approved users"""
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, username, approved_at 
            FROM users 
            WHERE approved = 1
            ORDER BY approved_at DESC
        ''')
        
        results = cursor.fetchall()
        conn.close()
        
        approved = {}
        for row in results:
            approved[row[1]] = {
                'id': row[0],
                'username': row[1],
                'approved_at': row[2]
            }
        return approved
    except Exception as e:
        print(f"Error getting approved users: {e}")
        return {}

def approve_user(username):
    """Approve a user"""
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        approved_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        cursor.execute('''
            UPDATE users 
            SET approved = 1, approved_at = ?
            WHERE username = ?
        ''', (approved_at, username))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error approving user: {e}")
        return False

def reject_user(username):
    """Reject/Delete a user"""
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        # Get user_id first
        cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
        result = cursor.fetchone()
        
        if result:
            user_id = result[0]
            # Delete from user_config first (foreign key)
            cursor.execute('DELETE FROM user_config WHERE user_id = ?', (user_id,))
            # Delete from users
            cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error rejecting user: {e}")
        return False

def get_user_by_username(username):
    """Get user details by username"""
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, username, secret_key, approved, created_at, approved_at
            FROM users 
            WHERE username = ?
        ''', (username,))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {
                'id': result[0],
                'username': result[1],
                'secret_key': result[2],
                'approved': bool(result[3]),
                'created_at': result[4],
                'approved_at': result[5]
            }
        return None
    except Exception as e:
        print(f"Error getting user: {e}")
        return None

def get_username(user_id):
    """Get username by user_id"""
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        cursor.execute('SELECT username FROM users WHERE id = ?', (user_id,))
        result = cursor.fetchone()
        conn.close()
        
        return result[0] if result else None
    except Exception as e:
        print(f"Error getting username: {e}")
        return None

def update_secret_key(username, secret_key):
    """Update user's secret key"""
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE users 
            SET secret_key = ?
            WHERE username = ?
        ''', (secret_key, username))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error updating secret key: {e}")
        return False

def get_all_users():
    """Get all users (for admin)"""
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, username, approved, created_at, approved_at 
            FROM users 
            ORDER BY created_at DESC
        ''')
        
        results = cursor.fetchall()
        conn.close()
        
        users = []
        for row in results:
            users.append({
                'id': row[0],
                'username': row[1],
                'approved': bool(row[2]),
                'created_at': row[3],
                'approved_at': row[4]
            })
        return users
    except Exception as e:
        print(f"Error getting all users: {e}")
        return []

def get_stats():
    """Get database statistics"""
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        # Total users
        cursor.execute('SELECT COUNT(*) FROM users')
        total = cursor.fetchone()[0]
        
        # Approved users
        cursor.execute('SELECT COUNT(*) FROM users WHERE approved = 1')
        approved = cursor.fetchone()[0]
        
        # Pending users
        cursor.execute('SELECT COUNT(*) FROM users WHERE approved = 0')
        pending = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            'total_users': total,
            'approved_users': approved,
            'pending_users': pending
        }
    except Exception as e:
        print(f"Error getting stats: {e}")
        return {
            'total_users': 0,
            'approved_users': 0,
            'pending_users': 0
        }

# For testing
if __name__ == "__main__":
    # Test database functions
    print("Testing database...")
    
    # Create test user
    success, msg = create_user("testuser", "testpass", "TEST-KEY-123")
    print(f"Create user: {success} - {msg}")
    
    # Get stats
    stats = get_stats()
    print(f"Stats: {stats}")
    
    # Get pending users
    pending = get_pending_users()
    print(f"Pending: {pending}")