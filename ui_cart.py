# M:/doll_shop/ui_cart.py (วางทับไฟล์เดิมทั้งหมด)

import customtkinter as ctk
from models import CartItem
from tkinter import messagebox

class CartWindow(ctk.CTkFrame):
    def __init__(self, parent, main_app):
        super().__init__(parent, fg_color="#FFF0F5")  # สีชมพูอ่อน
        self.main_app = main_app
        self.cart = main_app.cart
        self.assets = main_app.assets

    def on_show(self):
        """รีเฟรชข้อมูลทุกครั้งที่เปิดหน้านี้"""
        for widget in self.winfo_children():
            widget.destroy()
        self.setup_ui()

    def setup_ui(self):
        """สร้างองค์ประกอบทั้งหมดของหน้าตะกร้าสินค้า"""
        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # --- Header ---
        header_frame = ctk.CTkFrame(self, fg_color="#FFFFFF", corner_radius=0, height=70, border_width=1, border_color="#FFEBEE")
        header_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 20))
        header_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(
            header_frame, 
            text="🛒 ตะกร้าสินค้าของคุณ", 
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#FFB6C1"
        ).pack(side="left", padx=30, pady=20)
        
        back_btn = ctk.CTkButton(
            header_frame,
            text="< กลับไปช้อปต่อ",
            fg_color="transparent",
            text_color="#FFB6C1",
            hover_color="#FFE4E1",
            font=ctk.CTkFont(size=14),
            command=lambda: self.main_app.navigate_to('HomeWindow')
        )
        back_btn.pack(side="right", padx=30, pady=20)

        # --- Main Panels ---
        left_panel = ctk.CTkFrame(self, fg_color="transparent")
        left_panel.grid(row=1, column=0, sticky="nsew", padx=(30, 10), pady=10)
        self.create_cart_items_panel(left_panel)

        right_panel = ctk.CTkFrame(self, fg_color="transparent")
        right_panel.grid(row=1, column=1, sticky="nsew", padx=(10, 30), pady=10)
        self.create_summary_panel(right_panel)

    def create_cart_items_panel(self, parent):
        """สร้าง Panel แสดงรายการสินค้าในตะกร้า"""
        self.items_frame = ctk.CTkScrollableFrame(
            parent, 
            fg_color="transparent", 
            corner_radius=15,
            scrollbar_button_color="#FFB6C1"
        )
        self.items_frame.pack(expand=True, fill="both")

        cart_items = self.cart.get_items()

        if not cart_items:
            empty_frame = ctk.CTkFrame(self.items_frame, fg_color="#FFFFFF", corner_radius=20, border_width=2, border_color="#FFEBEE")
            empty_frame.pack(expand=True, fill="both", padx=10, pady=10)
            ctk.CTkLabel(
                empty_frame, 
                text="🛍️ ตะกร้าของคุณว่างเปล่า", 
                font=ctk.CTkFont(size=20, weight="bold"),
                text_color="#FFB6C1"
            ).pack(expand=True, pady=40)
            return

        for item in cart_items:
            self.create_cart_item_widget(self.items_frame, item).pack(fill="x", padx=10, pady=8)

    def create_cart_item_widget(self, parent, item: CartItem):
        """สร้าง Widget สำหรับสินค้า 1 ชิ้นในตะกร้า"""
        card = ctk.CTkFrame(
            parent, 
            fg_color="#FFFFFF", 
            corner_radius=15, 
            height=120,
            border_width=2,
            border_color="#FFEBEE"
        )

        # --- Image ---
        image = self.assets.get_product_image(item.product.image_url, size=(100,100))
        img_label = ctk.CTkLabel(card, text="", image=image)
        img_label.pack(side="left", padx=15, pady=15)

        # --- Details ---
        details_frame = ctk.CTkFrame(card, fg_color="transparent")
        details_frame.pack(side="left", fill="x", expand=True, padx=10)
        
        ctk.CTkLabel(
            details_frame, 
            text=item.product.name, 
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#6D4C41",
            anchor="w"
        ).pack(fill="x")
        
        ctk.CTkLabel(
            details_frame, 
            text=item.product.format_price(), 
            font=ctk.CTkFont(size=14), 
            text_color="#FFB6C1", 
            anchor="w"
        ).pack(fill="x", pady=(5, 0))

        # --- Quantity Control ---
        qty_frame = ctk.CTkFrame(card, fg_color="#FFF0F5", corner_radius=10)
        qty_frame.pack(side="left", padx=15)
        
        ctk.CTkButton(
            qty_frame, 
            text="-", 
            width=35,
            height=35,
            corner_radius=10,
            fg_color="#FFB6C1",
            hover_color="#FFC0CB",
            font=ctk.CTkFont(size=18, weight="bold"),
            command=lambda i=item: self.change_quantity(i, -1)
        ).pack(side="left", padx=5, pady=5)
        
        ctk.CTkLabel(
            qty_frame, 
            text=f"{item.quantity}", 
            width=40, 
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#6D4C41"
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            qty_frame, 
            text="+", 
            width=35,
            height=35,
            corner_radius=10,
            fg_color="#FFB6C1",
            hover_color="#FFC0CB",
            font=ctk.CTkFont(size=18, weight="bold"),
            command=lambda i=item: self.change_quantity(i, 1)
        ).pack(side="left", padx=5, pady=5)

        # --- Total Price & Remove Button ---
        total_frame = ctk.CTkFrame(card, fg_color="transparent", width=150)
        total_frame.pack(side="right", fill="y", padx=20, pady=15)

        ctk.CTkLabel(
            total_frame, 
            text=item.format_total_price(), 
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#FF6B9D"
        ).pack(expand=True)
        
        remove_btn = ctk.CTkButton(
            total_frame, 
            text="🗑️", 
            width=40,
            height=40,
            corner_radius=10,
            fg_color="#FFEBEE",
            hover_color="#FFB6C1",
            text_color="#F44336",
            font=ctk.CTkFont(size=18),
            command=lambda pid=item.product.product_id: self.remove_item(pid)
        )
        remove_btn.pack(expand=True, pady=(5, 0))

        return card

    def create_summary_panel(self, parent):
        """สร้าง Panel สรุปยอดและปุ่มดำเนินการต่อ"""
        summary_card = ctk.CTkFrame(
            parent, 
            fg_color="#FFFFFF", 
            corner_radius=20,
            border_width=2,
            border_color="#FFEBEE"
        )
        summary_card.pack(fill="both", expand=True)

        # Header
        header = ctk.CTkFrame(summary_card, fg_color="#FFE4E1", corner_radius=15)
        header.pack(fill="x", padx=20, pady=20)
        ctk.CTkLabel(
            header, 
            text="💰 สรุปยอด", 
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="#6D4C41"
        ).pack(pady=15)

        # Subtotal
        subtotal_frame = ctk.CTkFrame(summary_card, fg_color="transparent")
        subtotal_frame.pack(fill="x", padx=25, pady=10)
        
        ctk.CTkLabel(
            subtotal_frame, 
            text="ราคารวม (Subtotal)",
            font=ctk.CTkFont(size=14),
            text_color="#6D4C41"
        ).pack(side="left")
        
        self.subtotal_label = ctk.CTkLabel(
            subtotal_frame, 
            text=self.cart.format_total_price(), 
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#6D4C41"
        )
        self.subtotal_label.pack(side="right")

        # Separator
        ctk.CTkFrame(summary_card, height=2, fg_color="#FFEBEE").pack(fill="x", padx=25, pady=15)

        # Total
        total_frame = ctk.CTkFrame(summary_card, fg_color="transparent")
        total_frame.pack(fill="x", padx=25, pady=10)
        
        ctk.CTkLabel(
            total_frame, 
            text="ยอดสุทธิ (Total)", 
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#6D4C41"
        ).pack(side="left")
        
        self.total_label = ctk.CTkLabel(
            total_frame, 
            text=self.cart.format_total_price(), 
            font=ctk.CTkFont(size=22, weight="bold"), 
            text_color="#FF6B9D"
        )
        self.total_label.pack(side="right")

        # Spacer
        ctk.CTkLabel(summary_card, text="").pack(expand=True)

        # --- Action Buttons ---
        checkout_btn = ctk.CTkButton(
            summary_card, 
            text="💳 ดำเนินการชำระเงิน", 
            height=50, 
            corner_radius=15, 
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="#FFB6C1",
            hover_color="#FFC0CB",
            text_color="white",
            command=lambda: self.main_app.navigate_to('CheckoutWindow')
        )
        checkout_btn.pack(fill="x", padx=20, pady=(10, 10))

        continue_btn = ctk.CTkButton(
            summary_card, 
            text="< เลือกซื้อสินค้าต่อ", 
            fg_color="transparent", 
            text_color="#FFB6C1",
            hover_color="#FFE4E1",
            font=ctk.CTkFont(size=14),
            command=lambda: self.main_app.navigate_to('HomeWindow')
        )
        continue_btn.pack(pady=(0, 20))
        
        # Disable checkout if cart is empty
        if not self.cart.get_items():
            checkout_btn.configure(state="disabled")

    def change_quantity(self, item: CartItem, amount: int):
        """เพิ่ม/ลด จำนวนสินค้า"""
        new_quantity = item.quantity + amount
        if new_quantity > 0:
            self.cart.update_quantity(item.product.product_id, new_quantity)
        else:
            self.remove_item(item.product.product_id)
        self.on_show()

    def remove_item(self, product_id: int):
        """ลบสินค้าออกจากตะกร้า"""
        if messagebox.askyesno("ยืนยัน", "คุณต้องการลบสินค้านี้ออกจากตะกร้าหรือไม่?", parent=self):
            self.cart.remove_item(product_id)
            self.on_show()