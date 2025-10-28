import customtkinter as ctk
from tkinter import messagebox
import re

def validate_email(email: str) -> bool:
    return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None

def show_message(parent, title, message, severity="info"):
    if severity == "error":
        messagebox.showerror(title, message, parent=parent)
    elif severity == "warning":
        messagebox.showwarning(title, message, parent=parent)
    else:
        messagebox.showinfo(title, message, parent=parent)

class LoginWindow(ctk.CTkFrame):
    def __init__(self, parent, main_app):
        super().__init__(parent, fg_color="#FFF0F5")
        self.main_app = main_app
        self.db = main_app.db
        self.assets = main_app.assets
        self.setup_ui()

    def setup_ui(self):
        main_card = ctk.CTkFrame(self, width=850, height=600, corner_radius=25,
                                 fg_color="#FFFFFF", border_width=2,
                                 border_color="#FFEBEE")
        main_card.place(relx=0.5, rely=0.5, anchor="center")
        main_card.grid_propagate(False)
        main_card.grid_columnconfigure(0, weight=5)
        main_card.grid_columnconfigure(1, weight=6)
        main_card.grid_rowconfigure(0, weight=1)

        img_frame = ctk.CTkFrame(main_card, fg_color="#FFE4E1", corner_radius=20)
        img_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        img_label = ctk.CTkLabel(img_frame, text="", image=self.assets.character_image)
        img_label.pack(expand=True)

        form_frame = ctk.CTkFrame(main_card, fg_color="transparent")
        form_frame.grid(row=0, column=1, sticky="nsew", padx=(0, 40), pady=20)

        ctk.CTkLabel(form_frame, text="", image=self.assets.logo).pack(pady=(20, 10))
        ctk.CTkLabel(form_frame, text="Welcome to Dollie Shop", font=("IBM Plex Sans Thai", 28, "bold"), text_color="#6D4C41").pack()
        ctk.CTkLabel(form_frame, text="เข้าสู่ระบบ หรือ สร้างบัญชีใหม่", font=("IBM Plex Sans Thai", 14), text_color="#BCAAA4").pack(pady=(0, 20))

        tab_view = ctk.CTkTabview(form_frame, fg_color="transparent", border_width=1, border_color="#FFEBEE",
                                  segmented_button_selected_color="#FFB6C1",
                                  segmented_button_selected_hover_color="#FFC0CB",
                                  segmented_button_unselected_color="#FFFFFF",
                                  text_color="#6D4C41")
        tab_view.pack(fill="both", expand=True)
        self.login_tab = tab_view.add("เข้าสู่ระบบ")
        self.register_tab = tab_view.add("สมัครสมาชิก")
        self.tab_view = tab_view

        self.setup_login_tab(self.login_tab)
        self.setup_register_tab(self.register_tab)

    def create_entry_with_icon(self, parent, icon, placeholder):
        entry_frame = ctk.CTkFrame(parent, fg_color="#FFF0F5", corner_radius=15,
                                   border_width=1, border_color="#FFEBEE")
        icon_label = ctk.CTkLabel(entry_frame, text="", image=icon)
        icon_label.pack(side="left", padx=(10, 5))
        entry = ctk.CTkEntry(entry_frame, placeholder_text=placeholder, height=35,
                             border_width=0, fg_color="transparent", font=("IBM Plex Sans Thai", 14))
        entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        return entry_frame, entry

    def setup_login_tab(self, tab):
        frame, self.login_username = self.create_entry_with_icon(tab, self.assets.user_icon, "ชื่อผู้ใช้")
        frame.pack(fill="x", pady=(20, 10), padx=10)

        frame, self.login_password = self.create_entry_with_icon(tab, self.assets.lock_icon, "รหัสผ่าน")
        self.login_password.configure(show="*")
        frame.pack(fill="x", pady=10, padx=10)

        ctk.CTkButton(tab, text="เข้าสู่ระบบ", height=45, corner_radius=20, font=("IBM Plex Sans Thai", 14, "bold"),
                      fg_color="#FFB6C1", hover_color="#FFC0CB", text_color="white",
                      command=self.handle_login).pack(fill="x", pady=20, padx=10)

    def setup_register_tab(self, tab):
        frame, self.reg_username = self.create_entry_with_icon(tab, self.assets.user_icon, "ตั้งชื่อผู้ใช้")
        frame.pack(fill="x", pady=(10, 8), padx=10)
        frame, self.reg_email = self.create_entry_with_icon(tab, self.assets.email_icon, "อีเมล")
        frame.pack(fill="x", pady=8, padx=10)
        frame, self.reg_fullname = self.create_entry_with_icon(tab, self.assets.name_icon, "ชื่อ-นามสกุล")
        frame.pack(fill="x", pady=8, padx=10)
        frame, self.reg_password = self.create_entry_with_icon(tab, self.assets.lock_icon, "ตั้งรหัสผ่าน (6 ตัวขึ้นไป)")
        self.reg_password.configure(show="*")
        frame.pack(fill="x", pady=8, padx=10)

        ctk.CTkButton(tab, text="สร้างบัญชี", height=45, corner_radius=20, font=("IBM Plex Sans Thai", 14, "bold"),
                      fg_color="#FFB6C1", hover_color="#FFC0CB", text_color="white",
                      command=self.handle_register).pack(fill="x", pady=15, padx=10)

    def handle_login(self):
        username = self.login_username.get().strip()
        password = self.login_password.get()
        if not username or not password:
            show_message(self, "ข้อมูลไม่ครบ", "กรุณากรอกชื่อผู้ใช้และรหัสผ่าน", "warning")
            return

        user_data = self.db.authenticate_user(username, password)
        if user_data:
            self.main_app.on_login_success(user_data)
        else:
            show_message(self, "ผิดพลาด", "ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง", "error")

    def handle_register(self):
        username = self.reg_username.get().strip()
        email = self.reg_email.get().strip()
        fullname = self.reg_fullname.get().strip()
        password = self.reg_password.get()

        if not all([username, email, fullname, password]):
            show_message(self, "ข้อมูลไม่ครบ", "กรุณากรอกข้อมูลให้ครบทุกช่อง", "warning")
            return
        if not validate_email(email):
            show_message(self, "ผิดพลาด", "รูปแบบอีเมลไม่ถูกต้อง", "error")
            return
        if len(password) < 6:
            show_message(self, "ผิดพลาด", "รหัสผ่านต้องมีอย่างน้อย 6 ตัวอักษร", "error")
            return
        if self.db.get_user(username):
             show_message(self, "ผิดพลาด", "ชื่อผู้ใช้นี้มีอยู่แล้ว", "error")
             return

        user_id = self.db.create_user(username, password, email, fullname)
        if user_id:
            show_message(self, "สำเร็จ", "สมัครสมาชิกสำเร็จ! กรุณาเข้าสู่ระบบ", "info")
            self.tab_view.set("เข้าสู่ระบบ")
            self.reg_username.delete(0, 'end')
            self.reg_email.delete(0, 'end')
            self.reg_fullname.delete(0, 'end')
            self.reg_password.delete(0, 'end')
        else:
            show_message(self, "ผิดพลาด", "การสมัครสมาชิกล้มเหลว", "error")