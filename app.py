import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
from views.user_view import show_user_page
from views.admin_view import show_admin_page
from views.auth_view import show_auth_page
from service.db import init_db

init_db()
st.set_page_config(page_title="Report System", layout="wide")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    if "target_role" not in st.session_state:
        st.title("ยินดีต้อนรับสู่ระบบรายงานปัญหาห้องเรียน")
        c1, c2 = st.columns(2)
        
        # เมื่อกดเข้าสู่ระบบ User จะข้ามการ Login และล็อกอินด้วยบัญชีกลางทันที
        if c1.button("เข้าสู่ระบบ User"):
            st.session_state.logged_in = True
            st.session_state.username = "karmbud1@gmail.com" # บัญชีกลาง
            st.session_state.role = "user"
            st.rerun()
            
        if c2.button("เข้าสู่ระบบ Admin"):
            st.session_state.target_role = "admin"
            st.rerun()
    else:
        show_auth_page(st.session_state.target_role)
else:
    st.sidebar.write(f"ผู้ใช้งาน: {st.session_state.username}")
    if st.sidebar.button("ออกจากระบบ"):
        st.session_state.clear()
        st.rerun()
    
    # ปรับเงื่อนไขตรงนี้
    if st.session_state.role == "admin":
        # ถ้าเป็น Admin ให้แสดงหน้า Admin Dashboard โดยตรง
        show_admin_page()
    else:
        # ถ้าเป็น User ปกติ ให้แสดงหน้าแจ้งรายงาน
        show_user_page()