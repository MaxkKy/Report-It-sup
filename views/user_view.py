import streamlit as st
from datetime import datetime
from config import ROOM_OPTIONS, ISSUE_OPTIONS
from service.db import save_report
from service.email_service import send_email_alert

def show_user_page():
    st.title("🏫 ระบบรายงานปัญหา")
    with st.form("report", clear_on_submit=True):
        room = st.selectbox("เลือกห้อง", ROOM_OPTIONS)
        cat = st.selectbox("ประเภท", ISSUE_OPTIONS)
        detail = st.text_area("รายละเอียด *")
        if st.form_submit_button("ส่งรายงาน"):
            if not detail: st.error("กรุณากรอกรายละเอียด")
            else:
                now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                save_report((now, st.session_state.username, room, cat, detail, "รอดำเนินการ", datetime.now().strftime("%Y-%m")))
                try:
                    # ไม่ต้องส่ง st.session_state.app_password แล้ว
                    send_email_alert(st.session_state.username, None, cat, detail, room)
                    st.success("✅ บันทึกและส่งเมลแจ้งเตือนแล้ว")
                except Exception as e:
                    st.error(f"ส่งเมลไม่สำเร็จ: {e}")