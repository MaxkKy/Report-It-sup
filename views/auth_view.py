import streamlit as st
from service.db import check_login

def show_auth_page(role):
    st.markdown(f"### 🔐 เข้าสู่ระบบ ({role.upper()})")
    
    if st.button("← กลับหน้าเลือกประเภท"):
        del st.session_state.target_role
        st.rerun()
        
    # เหลือเฉพาะฟอร์ม Login ปกติสำหรับ Admin
    with st.form("login"):
        email = st.text_input("อีเมล")
        pw = st.text_input("รหัสผ่าน", type="password")
        if st.form_submit_button("เข้าสู่ระบบ"):
            user = check_login(email, pw)
            # ตรวจสอบว่ารหัสถูกและเป็นแอดมินเท่านั้น
            if user and user[3] == "admin":
                st.session_state.logged_in = True
                st.session_state.username = user[1]
                st.session_state.role = user[3]
                st.session_state.app_password = pw
                st.rerun()
            else:
                st.error("อีเมล/รหัสผ่านผิด หรือคุณไม่มีสิทธิ์ Admin")