import sqlite3
import pandas as pd

DB_NAME = "classroom_reports.db"

def init_db():
    """
    สร้างฐานข้อมูลและตารางที่จำเป็น 
    พร้อมสร้างบัญชี Admin เริ่มต้นหากยังไม่มีในระบบ
    """
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    # 1. สร้างตารางรายงานปัญหา
    c.execute('''CREATE TABLE IF NOT EXISTS reports
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  timestamp TEXT, 
                  username TEXT, 
                  classroom TEXT, 
                  category TEXT, 
                  issue TEXT, 
                  status TEXT, 
                  month_str TEXT)''')
    
    # 2. สร้างตารางผู้ใช้งาน
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT UNIQUE, 
                  password TEXT, 
                  role TEXT)''')
    
    # 3. 🛡️ ตรวจสอบและสร้าง Admin เริ่มต้น (ป้องกัน Database หายบน Cloud)
    admin_email = "karmbud@gmail.com"
    admin_password = "ggtwgialdcyooiqi" # รหัสผ่านที่คุณใช้
    
    c.execute("SELECT COUNT(*) FROM users WHERE role='admin'")
    if c.fetchone()[0] == 0:
        try:
            c.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", 
                      (admin_email, admin_password, "admin"))
            print(f"ระบบ: สร้างบัญชี Admin เริ่มต้น ({admin_email}) เรียบร้อยแล้ว")
        except sqlite3.IntegrityError:
            pass

    conn.commit()
    conn.close()

def save_report(data):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""INSERT INTO reports 
                 (timestamp, username, classroom, category, issue, status, month_str) 
                 VALUES (?,?,?,?,?,?,?)""", data)
    conn.commit()
    conn.close()

def get_all_reports():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT * FROM reports ORDER BY timestamp DESC", conn)
    conn.close()
    return df

def update_report_status(report_id, new_status):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE reports SET status = ? WHERE id = ?", (new_status, report_id))
    conn.commit()
    conn.close()

def delete_report(report_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM reports WHERE id = ?", (report_id,))
    conn.commit()
    conn.close()

def register_user(username, password, role="user"):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password, role) VALUES (?,?,?)", 
                  (username, password, role))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def check_login(username, password):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = c.fetchone()
    conn.close()
    return user

def get_all_users():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT id, username, role FROM users", conn)
    conn.close()
    return df

def delete_user(user_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()