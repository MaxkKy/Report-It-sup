# แก้ไขไฟล์ email_service.py
import smtplib
from email.mime.text import MIMEText
import streamlit as st # เพิ่มบรรทัดนี้

def send_email_alert(sender_email, app_password, cat, detail, room):
    # 1. ระบุอีเมลบัญชีกลางที่คุณต้องการใช้ส่ง
    GMAIL_USER = "karmbud1@gmail.com" 
    
    # 2. ระบุรหัสผ่านแอป 16 หลัก (App Password) ที่ได้จาก Google
    APP_PASSWORD = st.secrets["EMAIL_PASSWORD"]    
    # อีเมลปลายทางที่จะรับแจ้งเตือน
    admin_email = "karmbud@gmail.com"

    subject = f"แจ้งเตือนปัญหา: {cat} - ห้อง {room}"
    body = f"รายละเอียด: {detail}\nผู้รายงาน: {sender_email}"

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = GMAIL_USER
    msg['To'] = admin_email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(GMAIL_USER, APP_PASSWORD)
            server.sendmail(GMAIL_USER, admin_email, msg.as_string())
    except Exception as e:
        raise e