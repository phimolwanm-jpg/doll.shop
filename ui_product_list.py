import customtkinter as ctk
from models import Product
from tkinter import messagebox
import math

class ProductListWindow(ctk.CTkFrame):
    def __init__(self, parent, main_app):
        super().__init__(parent, fg_color="#FFF0F5")  # สีชมพูอ่อน
        self.main_app = main_app
        self.db = main_app.db
        self.cart = main_app.cart
        self.assets = main_app.assets
        
        self.category = None
        self.current_products = []
        self.search_var = ctk.StringVar()
        self.sort_var = ctk.StringVar(value="ล่าสุด")

    def on_show(self, category=None):
        """รีเฟรชข้อมูลทุกครั้งที่เปิดหน้านี้"""
        self.category = category
        self.search_var.set("")
        
        for widget in self.winfo_children():
            widget.destroy()
        
        self.setup_ui()
        self.load_products()

    def setup_ui(self):
        """สร้างองค์ประกอบทั้งหมดของหน้า"""
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.create_header(self)
        self.create_product_grid(self)

    def create_header(self, parent):
        """สร้างส่วน Header, Search, และ Filter"""
        header_frame = ctk.CTkFrame(parent, fg_color="#FFFFFF", corner_radius=0, height=90, border_width=1, border_color="#FFEBEE")
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        header_frame.grid_columnconfigure(1, weight=1)

        # Back button and Title
        left_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        left_frame.pack(side="left", padx=20, pady=20)
        
        back_btn = ctk.CTkButton(
            left_frame,
            text="<",
            width=40,
            height=40,
            corner_radius=10,
            fg_color="#FFB6C1",
            hover_color="#FFC0CB",
            font=ctk.CTkFont(size=18, weight="bold"),
            command=lambda: self.main_app.navigate_to('HomeWindow')
        )
        back_btn.pack(side="left")
        
        title_text = f"🛍️ {self.category}" if self.category else "🛍️ สินค้าทั้งหมด"
        ctk.CTkLabel(
            left_frame,
            text=title_text,
            font=ctk.CTkFont(size=26, weight="bold"),
            text_color="#FFB6C1"
        ).pack(side="left", padx=15)

        # Search and Sort
        right_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        right_frame.pack(side="right", padx=20, pady=20)

        search_entry = ctk.CTkEntry(
            right_frame,
            textvariable=self.search_var,
            placeholder_text="🔍 ค้นหาชื่อสินค้า...",
            width=250,
            height=40,
            corner_radius=15,
            border_width=1,
            border_color="#FFEBEE",
            fg_color="#FFF0F5",
            font=ctk.CTkFont(size=14)
        )
        search_entry.pack(side="left", padx=5)
        search_entry.bind("<Return>", lambda event: self.load_products())

        sort_menu = ctk.CTkOptionMenu(
            right_frame,
            variable=self.sort_var,
            values=["ล่าสุด", "ราคา: ต่ำ-สูง", "ราคา: สูง-ต่ำ", "ชื่อ: A-Z"],
            command=self.sort_products,
            width=150,
            height=40,
            corner_radius=15,
            fg_color="#FFB6C1",
            button_color="#FF6B9D",
            button_hover_color="#FF8FB3",
            font=ctk.CTkFont(size=14)
        )
        sort_menu.pack(side="left", padx=5)

    def create_product_grid(self, parent):
        """สร้าง Grid แสดงผลสินค้า"""
        container = ctk.CTkFrame(parent, fg_color="transparent")
        container.grid(row=1, column=0, sticky="nsew")
        container.grid_rowconfigure(1, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.results_label = ctk.CTkLabel(
            container,
            text="กำลังโหลด...",
            font=ctk.CTkFont(size=14),
            text_color="#6D4C41"
        )
        self.results_label.grid(row=0, column=0, sticky="w", padx=30, pady=10)
        
        self.products_frame = ctk.CTkScrollableFrame(
            container,
            fg_color="transparent",
            scrollbar_button_color="#FFB6C1"
        )
        self.products_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=5)
        for i in range(4):
            self.products_frame.grid_columnconfigure(i, weight=1, uniform="col")

    def load_products(self):
        """โหลดสินค้าจากฐานข้อมูล"""
        keyword = self.search_var.get().strip().lower()
        self.current_products = self.db.get_all_products(category=self.category, search_term=keyword)
        self.sort_products(self.sort_var.get())

    def sort_products(self, option):
        """จัดเรียงรายการสินค้า"""
        products_as_obj = [Product.from_dict(p) for p in self.current_products]
        
        if option == "ล่าสุด":
            products_as_obj.sort(key=lambda x: x.created_at or '', reverse=True)
        elif option == "ราคา: ต่ำ-สูง":
            products_as_obj.sort(key=lambda x: x.price)
        elif option == "ราคา: สูง-ต่ำ":
            products_as_obj.sort(key=lambda x: x.price, reverse=True)
        elif option == "ชื่อ: A-Z":
            products_as_obj.sort(key=lambda x: x.name)
        
        self.current_products = [p.__dict__ for p in products_as_obj]
        self.display_products()

    def display_products(self):
        """แสดงผลสินค้าลงบน Grid"""
        for widget in self.products_frame.winfo_children():
            widget.destroy()

        self.results_label.configure(text=f"📦 พบ {len(self.current_products)} รายการ")
        
        if not self.current_products:
            empty_frame = ctk.CTkFrame(self.products_frame, fg_color="#FFFFFF", corner_radius=20, border_width=2, border_color="#FFEBEE")
            empty_frame.grid(row=0, column=0, columnspan=4, pady=50, padx=20, sticky="ew")
            
            ctk.CTkLabel(
                empty_frame,
                text="😢 ไม่พบสินค้าที่ตรงกับเงื่อนไข",
                font=ctk.CTkFont(size=18, weight="bold"),
                text_color="#FFB6C1"
            ).pack(pady=40)
            return

        cols = 4
        for i, prod_dict in enumerate(self.current_products):
            product = Product.from_dict(prod_dict)
            row, col = divmod(i, cols)
            self.create_product_card(self.products_frame, product).grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

    def create_product_card(self, parent, product: Product):
        """สร้างการ์ดสำหรับสินค้า 1 ชิ้น"""
        card = ctk.CTkFrame(parent, fg_color="#FFFFFF", corner_radius=15, border_width=2, border_color="#FFEBEE")
        
        image = self.assets.get_product_image(product.image_url)
        img_label = ctk.CTkLabel(card, text="", image=image, bg_color="transparent")
        img_label.pack(pady=(15, 10))

        ctk.CTkLabel(
            card,
            text=product.name,
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#6D4C41"
        ).pack(padx=10, fill="x")
        
        # Stock status
        stock_text, stock_color = product.get_stock_status()
        stock_frame = ctk.CTkFrame(card, fg_color="#FFF0F5", corner_radius=8)
        stock_frame.pack(pady=5)
        ctk.CTkLabel(
            stock_frame,
            text=stock_text,
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=stock_color
        ).pack(padx=10, pady=3)
        
        ctk.CTkLabel(
            card,
            text=product.format_price(),
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#FF6B9D"
        ).pack(pady=5)
        
        add_to_cart_btn = ctk.CTkButton(
            card,
            text="🛒 หยิบใส่ตะกร้า",
            height=40,
            corner_radius=10,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#FFB6C1",
            hover_color="#FFC0CB",
            text_color="white",
            state="normal" if product.is_available() else "disabled",
            command=lambda p=product: self.add_to_cart(p)
        )
        add_to_cart_btn.pack(pady=10, padx=15, fill="x")
        return card

    def add_to_cart(self, product: Product):
        """เพิ่มสินค้าลงตะกร้า"""
        self.cart.add_item(product)
        messagebox.showinfo("ตะกร้าสินค้า", f"เพิ่ม '{product.name}' ลงในตะกร้าแล้ว!", parent=self)