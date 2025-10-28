import customtkinter as ctk
from tkinter import messagebox
from models import Product

class HomeWindow(ctk.CTkFrame):
    def __init__(self, parent, main_app):
        super().__init__(parent, fg_color="#FFF0F5")
        self.main_app = main_app
        self.db = main_app.db
        self.session = main_app.session
        self.cart = main_app.cart
        self.assets = main_app.assets

    def on_show(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.setup_ui()

    def setup_ui(self):
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self.create_header(self)

        main_frame = ctk.CTkScrollableFrame(self, fg_color="transparent", scrollbar_button_color="#FFB6C1")
        main_frame.grid(row=1, column=0, sticky="nsew", padx=30, pady=0)
        main_frame.grid_columnconfigure(0, weight=1)
        
        self.create_banner(main_frame)
        self.create_categories(main_frame)
        self.create_product_display(main_frame)

    def create_header(self, parent):
        header = ctk.CTkFrame(parent, fg_color="#FFFFFF", corner_radius=0, height=70, border_width=1, border_color="#FFEBEE")
        header.grid(row=0, column=0, sticky="ew", pady=(0, 5))
        header.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(header, text="🎀 Dollie Shop", font=("IBM Plex Sans Thai", 24, "bold"), text_color="#FFB6C1").pack(side="left", padx=30)

        right_frame = ctk.CTkFrame(header, fg_color="transparent")
        right_frame.pack(side="right", padx=20, pady=10)

        welcome_text = f"สวัสดี, {self.session.current_user.full_name}"
        ctk.CTkLabel(right_frame, text=welcome_text, font=("IBM Plex Sans Thai", 14), text_color="#6D4C41").pack(side="left", padx=10)
        
        # ปุ่มสำหรับ Admin
        if self.session.is_admin():
            admin_dashboard_btn = ctk.CTkButton(
                right_frame, 
                text="📊 Dashboard", 
                fg_color="#4CAF50", 
                hover_color="#66BB6A", 
                text_color="white", 
                font=("IBM Plex Sans Thai", 14, "bold"),
                corner_radius=15,
                height=35,
                command=lambda: self.main_app.navigate_to('AdminDashboardWindow')
            )
            admin_dashboard_btn.pack(side="left", padx=5)
            
            admin_orders_btn = ctk.CTkButton(
                right_frame, 
                text="📦 คำสั่งซื้อ", 
                fg_color="#2196F3", 
                hover_color="#42A5F5", 
                text_color="white", 
                font=("IBM Plex Sans Thai", 14, "bold"),
                corner_radius=15,
                height=35,
                command=lambda: self.main_app.navigate_to('AdminOrdersWindow')
            )
            admin_orders_btn.pack(side="left", padx=5)
            
            admin_product_btn = ctk.CTkButton(
                right_frame, 
                text="⚙️ จัดการสินค้า", 
                fg_color="#FF6B9D", 
                hover_color="#FF8FB3", 
                text_color="white", 
                font=("IBM Plex Sans Thai", 14, "bold"),
                corner_radius=15,
                height=35,
                command=lambda: self.main_app.navigate_to('AdminWindow')
            )
            admin_product_btn.pack(side="left", padx=5)
        
        # ปุ่มสำหรับทุกคน
        profile_btn = ctk.CTkButton(
            right_frame, 
            text="โปรไฟล์", 
            fg_color="transparent", 
            hover_color="#FFE4E1", 
            text_color="#6D4C41", 
            font=("IBM Plex Sans Thai", 14), 
            command=lambda: self.main_app.navigate_to('ProfileWindow')
        )
        profile_btn.pack(side="left", padx=5)
        
        history_btn = ctk.CTkButton(
            right_frame, 
            text="ประวัติการซื้อ", 
            fg_color="transparent", 
            hover_color="#FFE4E1", 
            text_color="#6D4C41", 
            font=("IBM Plex Sans Thai", 14), 
            command=lambda: self.main_app.navigate_to('OrderHistoryWindow')
        )
        history_btn.pack(side="left", padx=5)
        
        cart_btn = ctk.CTkButton(
            right_frame, 
            text="", 
            image=self.assets.cart_icon, 
            width=30, 
            fg_color="transparent", 
            hover_color="#FFE4E1", 
            command=lambda: self.main_app.navigate_to('CartWindow')
        )
        cart_btn.pack(side="left", padx=5)

        logout_btn = ctk.CTkButton(
            right_frame, 
            text="ออกจากระบบ", 
            width=100, 
            corner_radius=15, 
            font=("IBM Plex Sans Thai", 14, "bold"), 
            fg_color="#FFB6C1", 
            hover_color="#FFC0CB", 
            text_color="white", 
            command=self.main_app.on_logout
        )
        logout_btn.pack(side="left", padx=10)

    def create_banner(self, parent):
        banner_label = ctk.CTkLabel(parent, text="", image=self.assets.banner, corner_radius=20)
        banner_label.grid(row=0, column=0, sticky="ew", pady=(10, 20))

    def create_categories(self, parent):
        category_frame = ctk.CTkFrame(parent, fg_color="transparent")
        category_frame.grid(row=1, column=0, sticky="ew", pady=20, padx=10)
        ctk.CTkLabel(
            category_frame, 
            text="หมวดหมู่ตุ๊กตา", 
            font=("IBM Plex Sans Thai", 20, "bold"), 
            text_color="#6D4C41"
        ).pack(anchor="w")
        
        buttons_frame = ctk.CTkFrame(category_frame, fg_color="transparent")
        buttons_frame.pack(fill="x", pady=10)

        categories = self.db.get_categories()
        icons = {
            'ตุ๊กตาหมี': '🧸', 
            'ตุ๊กตากระต่าย': '🐰', 
            'ตุ๊กตาแมว': '🐱',
            'ตุ๊กตาช้าง': '🐘',
            'ตุ๊กตายูนิคอร์น': '🦄',
            'ตุ๊กตาสุนัข': '🐶',
            'ตุ๊กตาไดโนเสาร์': '🦕'
        }
        
        for category in categories:
            icon = icons.get(category, '🎀')
            btn = ctk.CTkButton(
                buttons_frame, 
                text=f"{icon} {category}", 
                height=40, 
                corner_radius=20, 
                font=("IBM Plex Sans Thai", 14, "bold"),
                fg_color="#FFFFFF", 
                border_width=1, 
                border_color="#FFEBEE",
                text_color="#6D4C41", 
                hover_color="#FFE4E1",
                command=lambda c=category: self.main_app.navigate_to('ProductListWindow', category=c)
            )
            btn.pack(side="left", padx=5)

    def create_product_display(self, parent):
        container = ctk.CTkFrame(parent, fg_color="transparent")
        container.grid(row=2, column=0, sticky="nsew", pady=10)
        ctk.CTkLabel(
            container, 
            text="สินค้าแนะนำ ✨", 
            font=("IBM Plex Sans Thai", 20, "bold"), 
            text_color="#6D4C41"
        ).pack(anchor="w", padx=10)
        
        products_frame = ctk.CTkFrame(container, fg_color="transparent")
        products_frame.pack(fill="both", expand=True, pady=10)
        
        products_data = self.db.get_all_products(limit=8)
        
        cols = 4
        for i, prod_dict in enumerate(products_data):
            row, col = divmod(i, cols)
            products_frame.grid_columnconfigure(col, weight=1, uniform="prod")
            self.create_product_card(products_frame, Product.from_dict(prod_dict)).grid(
                row=row, column=col, padx=10, pady=10, sticky="nsew"
            )
        
        # Footer with About button
        footer_frame = ctk.CTkFrame(parent, fg_color="transparent")
        footer_frame.grid(row=3, column=0, sticky="ew", pady=20)
        
        ctk.CTkButton(
            footer_frame,
            text="ℹ️ เกี่ยวกับเรา / ผู้พัฒนา",
            fg_color="transparent",
            text_color="#FFB6C1",
            hover_color="#FFE4E1",
            border_width=1,
            border_color="#FFB6C1",
            corner_radius=15,
            height=40,
            font=("IBM Plex Sans Thai", 14),
            command=lambda: self.main_app.navigate_to('AboutWindow')
        ).pack(pady=10)

    def create_product_card(self, parent, product: Product):
        card = ctk.CTkFrame(parent, fg_color="#FFFFFF", corner_radius=15, border_width=1, border_color="#FFEBEE")
        
        image = self.assets.get_product_image(product.image_url)
        img_label = ctk.CTkLabel(card, text="", image=image, bg_color="transparent")
        img_label.pack(pady=(15, 10))

        ctk.CTkLabel(
            card, 
            text=product.name, 
            font=("IBM Plex Sans Thai", 16, "bold"), 
            text_color="#6D4C41"
        ).pack(padx=10)
        
        ctk.CTkLabel(
            card, 
            text=product.format_price(), 
            font=("IBM Plex Sans Thai", 14), 
            text_color="#FFB6C1"
        ).pack(pady=5)
        
        add_to_cart_btn = ctk.CTkButton(
            card, 
            text="หยิบใส่ตะกร้า", 
            height=35, 
            corner_radius=10, 
            font=("IBM Plex Sans Thai", 14, "bold"), 
            fg_color="#FFB6C1", 
            hover_color="#FFC0CB", 
            text_color="white",
            command=lambda p=product: self.add_to_cart(p)
        )
        add_to_cart_btn.pack(pady=10, padx=15, fill="x")
        return card

    def add_to_cart(self, product: Product):
        self.cart.add_item(product)
        messagebox.showinfo("ตะกร้าสินค้า", f"เพิ่ม '{product.name}' ลงในตะกร้าแล้ว!", parent=self)