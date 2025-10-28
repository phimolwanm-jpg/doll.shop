import customtkinter as ctk
from PIL import Image
import os

class AboutWindow(ctk.CTkFrame):
    def __init__(self, parent, main_app):
        super().__init__(parent, fg_color="#FFF0F5")
        self.main_app = main_app
        self.setup_ui()
    
    def on_show(self):
        pass
    
    def setup_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Header
        self.create_header()
        
        # Main Content
        main_frame = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            scrollbar_button_color="#FFB6C1"
        )
        main_frame.grid(row=1, column=0, sticky="nsew", padx=30, pady=20)
        
        self.create_content(main_frame)
    
    def create_header(self):
        header = ctk.CTkFrame(
            self,
            fg_color="#FFFFFF",
            corner_radius=0,
            height=70,
            border_width=1,
            border_color="#FFEBEE"
        )
        header.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        header.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(
            header,
            text="ℹ️ เกี่ยวกับเรา",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#FFB6C1"
        ).pack(side="left", padx=30, pady=20)
        
        ctk.CTkButton(
            header,
            text="🏠 กลับหน้าหลัก",
            fg_color="transparent",
            text_color="#FFB6C1",
            hover_color="#FFE4E1",
            font=ctk.CTkFont(size=14),
            command=lambda: self.main_app.navigate_to('HomeWindow')
        ).pack(side="right", padx=30, pady=20)
    
    def create_content(self, parent):
        content_card = ctk.CTkFrame(
            parent,
            fg_color="#FFFFFF",
            corner_radius=20,
            border_width=2,
            border_color="#FFEBEE"
        )
        content_card.pack(fill="both", expand=True, padx=50, pady=20)
        
        # Shop Info
        shop_section = ctk.CTkFrame(content_card, fg_color="#FFE4E1", corner_radius=15)
        shop_section.pack(fill="x", padx=30, pady=(30, 20))
        
        ctk.CTkLabel(shop_section, text="🎀", font=ctk.CTkFont(size=60)).pack(pady=(20, 10))
        ctk.CTkLabel(shop_section, text="Dollie Shop", font=ctk.CTkFont(size=36, weight="bold"), text_color="#FF6B9D").pack()
        ctk.CTkLabel(shop_section, text="ระบบจัดการร้านขายตุ๊กตาออนไลน์", font=ctk.CTkFont(size=16), text_color="#6D4C41").pack(pady=(5, 20))
        
        # Description
        desc_frame = ctk.CTkFrame(content_card, fg_color="transparent")
        desc_frame.pack(fill="x", padx=40, pady=20)
        
        ctk.CTkLabel(
            desc_frame,
            text="ระบบจัดการร้านค้าออนไลน์สำหรับขายตุ๊กตาและของเล่น\n"
                 "พัฒนาด้วย Python และ CustomTkinter\n"
                 "มีระบบจัดการสินค้า ตะกร้าสินค้า การชำระเงิน และระบบ Admin ที่ครบครัน",
            font=ctk.CTkFont(size=14),
            text_color="#6D4C41",
            justify="center"
        ).pack(pady=10)
        
        # Separator
        ctk.CTkFrame(content_card, height=2, fg_color="#FFEBEE").pack(fill="x", padx=40, pady=20)
        
        # Developer Section
        dev_header = ctk.CTkFrame(content_card, fg_color="#FFE4E1", corner_radius=15)
        dev_header.pack(fill="x", padx=30, pady=20)
        
        ctk.CTkLabel(dev_header, text="👩‍💻 ผู้พัฒนาโปรแกรม", font=ctk.CTkFont(size=24, weight="bold"), text_color="#6D4C41").pack(pady=15)
        
        # Developer Profile
        profile_frame = ctk.CTkFrame(content_card, fg_color="#FFF0F5", corner_radius=15)
        profile_frame.pack(fill="x", padx=40, pady=20)
        
        # Profile Image
        self.load_developer_image(profile_frame)
        
        # Developer Info
        info_container = ctk.CTkFrame(profile_frame, fg_color="transparent")
        info_container.pack(pady=20, padx=30)
        
        ctk.CTkLabel(info_container, text="นางสาว พิมลวรรณ มาตะราช", font=ctk.CTkFont(size=22, weight="bold"), text_color="#FF6B9D").pack(pady=5)
        ctk.CTkLabel(info_container, text="คณะศึกษาศาสตร์ สาขาคอมพิวเตอร์ศึกษา มหาวิทยาลัยขอนแก่น", font=ctk.CTkFont(size=22, weight="bold"), text_color="#FF6B9D").pack(pady=5)
        

        id_frame = ctk.CTkFrame(info_container, fg_color="#FFFFFF", corner_radius=10)
        id_frame.pack(pady=10)
        ctk.CTkLabel(id_frame, text="🎓 รหัสนักศึกษา: 673050139-2", font=ctk.CTkFont(size=16), text_color="#6D4C41").pack(padx=20, pady=10)
        
        # Contact Info
        contact_frame = ctk.CTkFrame(content_card, fg_color="transparent")
        contact_frame.pack(fill="x", padx=40, pady=20)
        
        ctk.CTkLabel(contact_frame, text="📞 ติดต่อสอบถาม", font=ctk.CTkFont(size=18, weight="bold"), text_color="#6D4C41").pack(pady=10)
        
        phone_frame = ctk.CTkFrame(contact_frame, fg_color="#FFFFFF", corner_radius=10, border_width=1, border_color="#FFEBEE")
        phone_frame.pack(pady=5)
        ctk.CTkLabel(phone_frame, text="📱 เบอร์โทรศัพท์: 086-379-7202", font=ctk.CTkFont(size=15), text_color="#6D4C41").pack(padx=30, pady=12)
        
        fb_frame = ctk.CTkFrame(contact_frame, fg_color="#FFFFFF", corner_radius=10, border_width=1, border_color="#FFEBEE")
        fb_frame.pack(pady=5)
        ctk.CTkLabel(fb_frame, text="📘 Facebook: Phimonwan Martarach", font=ctk.CTkFont(size=15), text_color="#6D4C41").pack(padx=30, pady=12)
        
        # Footer
        footer_frame = ctk.CTkFrame(content_card, fg_color="transparent")
        footer_frame.pack(fill="x", padx=40, pady=(20, 30))
        
        ctk.CTkLabel(footer_frame, text="💖 พัฒนาด้วยความตั้งใจ", font=ctk.CTkFont(size=16, weight="bold"), text_color="#FFB6C1").pack()
        ctk.CTkLabel(footer_frame, text="© 2025 Dollie Shop. All rights reserved.", font=ctk.CTkFont(size=12), text_color="gray50").pack(pady=(5, 0))
    
    def load_developer_image(self, parent):
        try:
            image_paths = ["assets/developer.jpg", ]
            
            for path in image_paths:
                if os.path.exists(path):
                    img = Image.open(path)
                    img = img.resize((300, 300), Image.Resampling.LANCZOS)
                    ctk_image = ctk.CTkImage(img, size=(300, 300))
                    ctk.CTkLabel(parent, text="", image=ctk_image).pack(pady=(20, 10))
                    return
            
            ctk.CTkLabel(parent, text="👩‍💻", font=ctk.CTkFont(size=80)).pack(pady=(20, 10))
        except:
            ctk.CTkLabel(parent, text="👩‍💻", font=ctk.CTkFont(size=80)).pack(pady=(20, 10))