import streamlit as st
import qrcode
from io import BytesIO
# นำเข้าฟังก์ชันเดิมที่มีอยู่แล้ว
from service.db import get_all_users, register_user, delete_user, get_all_reports, update_report_status, delete_report

def show_admin_page():
    st.title("🔐 Admin Management")
    
    # 1. เพิ่มเมนู "สร้าง QR Code" เข้าไปใน radio
    menu = st.radio("เลือกเมนู", ["จัดการผู้ใช้งาน", "ดูรายงาน", "สร้าง QR Code"], horizontal=True)
    
    if menu == "จัดการผู้ใช้งาน":
        # ... (โค้ดส่วนเดิมของคุณ) ...
        st.subheader("👥 เพิ่ม/ลบ ผู้ใช้งาน")
        with st.form("add_user", clear_on_submit=True):
            u = st.text_input("อีเมล (Username)")
            p = st.text_input("รหัสผ่าน", type="password")
            role = st.radio("เลือกประเภทผู้ใช้งาน", ["user", "admin"], horizontal=True)
            if st.form_submit_button("เพิ่มสมาชิกใหม่"):
                if u and p:
                    if register_user(u, p, role): 
                        st.success(f"เพิ่ม {u} ในฐานะ {role} สำเร็จแล้ว!")
                        st.rerun()
                    else: 
                        st.error("อีเมลนี้มีอยู่ในระบบแล้ว กรุณาใช้ชื่ออื่น")
                else:
                    st.warning("กรุณากรอกข้อมูลให้ครบถ้วน")
        st.divider()
        st.write("### รายชื่อผู้ใช้งานทั้งหมด")
        users = get_all_users()
        st.dataframe(users, use_container_width=True)
        uid = st.number_input("ใส่ ID ที่ต้องการลบ", min_value=1, step=1)
        if st.button("ลบผู้ใช้นี้ออกจากระบบ", type="secondary"):
            delete_user(uid)
            st.success(f"ลบ ID {uid} เรียบร้อยแล้ว")
            st.rerun()
            
    elif menu == "ดูรายงาน":
        # ... (โค้ดส่วนเดิมของคุณ) ...
        st.subheader("📋 รายการแจ้งปัญหาทั้งหมด")
        reports = get_all_reports()
        if not reports.empty:
            for index, row in reports.iterrows():
                with st.container(border=True):
                    col1, col2, col3 = st.columns([3, 1, 1])
                    col1.write(f"**ID: {row['id']}** | ห้อง: {row['classroom']} | {row['category']}")
                    col1.write(f"รายละเอียด: {row['issue']}")
                    if col2.button("🗑️ ลบ", key=f"del_{row['id']}"):
                        delete_report(row['id'])
                        st.rerun()
                    with col3.form(key=f"st_form_{row['id']}"):
                        new_status = st.selectbox("สถานะ", ["รอดำเนินการ", "กำลังดำเนินการ", "เรียบร้อย"], 
                                                 index=["รอดำเนินการ", "กำลังดำเนินการ", "เรียบร้อย"].index(row['status']))
                        if st.form_submit_button("บันทึก"):
                            update_report_status(row['id'], new_status)
                            st.rerun()
        else:
            st.info("ยังไม่มีข้อมูลรายงาน")

    # 2. เพิ่มส่วนการทำงานของ "สร้าง QR Code"
    elif menu == "สร้าง QR Code":
        st.subheader("🖼️ สร้าง QR Code สำหรับเข้าใช้งานระบบ")
        
        # ช่องสำหรับใส่ URL ของเว็บแอป (เช่น URL จาก Streamlit Cloud)
        url = st.text_input("ใส่ URL ของเว็บแอปของคุณ", placeholder="https://your-app-name.streamlit.app")
        
        if st.button("สร้าง QR Code"):
            if url:
                # สร้าง QR Code Object
                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=10,
                    border=4,
                )
                qr.add_data(url)
                qr.make(fit=True)

                img = qr.make_image(fill_color="black", back_color="white")
                
                # แปลงไฟล์รูปภาพเป็น Bytes เพื่อแสดงผลและดาวน์โหลด
                buf = BytesIO()
                img.save(buf, format="PNG")
                byte_im = buf.getvalue()
                
                # แสดงรูป QR Code
                st.image(byte_im, caption="Scan เพื่อเข้าสู่ระบบรายงานปัญหา")
                
                # ปุ่มดาวน์โหลดไฟล์รูป
                st.download_button(
                    label="📥 ดาวน์โหลดไฟล์ QR Code (PNG)",
                    data=byte_im,
                    file_name="report_system_qr.png",
                    mime="image/png"
                )
            else:
                st.warning("กรุณากรอก URL ก่อนกดปุ่มสร้าง")