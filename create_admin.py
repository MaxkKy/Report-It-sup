# ไฟล์ D:\Report-Project\create_admin.py
from service.db import register_user, init_db

# ควรเรียก init_db() ก่อน เพื่อให้มั่นใจว่าไฟล์ .db ถูกสร้างขึ้น
init_db()

def create_first_admin():
    email = "karmbud@gmail.com" 
    password = "ggtwgialdcyooiqi"   
    # บังคับให้เป็น role admin ตามที่คุณต้องการ
    if register_user(email, password, role="admin"):
        print(f"เพิ่ม Admin {email} สำเร็จ!")
    else:
        print("ไม่สามารถเพิ่ม Admin ได้ (อาจมีอีเมลนี้ในระบบแล้ว)")

if __name__ == "__main__":
    create_first_admin()