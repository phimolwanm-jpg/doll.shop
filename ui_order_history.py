# M:/doll_shop/ui_order_history.py (วางทับไฟล์เดิมทั้งหมด)

import customtkinter as ctk
from models import Session, Order
from database import Database

class OrderHistoryWindow(ctk.CTkFrame):
    def __init__(self, parent, main_app):
        super().__init__(parent, fg_color="#FFF0F5")  # สีชมพูอ่อน
        self.main_app = main_app
        self.session = main_app.session
        self.db = main_app.db

    def on_show(self):
        """รีเฟรชข้อมูลทุกครั้งที่เปิดหน้านี้"""
        for widget in self.winfo_children():
            widget.destroy()
        self.setup_ui()

    def setup_ui(self):
        """สร้างองค์ประกอบ UI ทั้งหมด"""
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # --- Header ---
        header_frame = ctk.CTkFrame(self, fg_color="#FFFFFF", corner_radius=0, height=70, border_width=1, border_color="#FFEBEE")
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        header_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(
            header_frame,
            text="📜 ประวัติการสั่งซื้อ",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#FFB6C1"
        ).pack(side="left", padx=30, pady=20)
        
        back_button = ctk.CTkButton(
            header_frame,
            text="< กลับไปหน้าหลัก",
            command=lambda: self.main_app.navigate_to('HomeWindow'),
            fg_color="transparent",
            text_color="#FFB6C1",
            hover_color="#FFE4E1",
            font=ctk.CTkFont(size=14)
        )
        back_button.pack(side="right", padx=30, pady=20)

        # --- Orders List ---
        orders_frame = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            scrollbar_button_color="#FFB6C1"
        )
        orders_frame.grid(row=1, column=0, sticky="nsew", padx=30, pady=10)
        
        user_id = self.session.current_user.user_id
        orders_data = self.db.get_user_orders(user_id)

        if not orders_data:
            empty_frame = ctk.CTkFrame(orders_frame, fg_color="#FFFFFF", corner_radius=20, border_width=2, border_color="#FFEBEE")
            empty_frame.pack(expand=True, fill="both", padx=10, pady=50)
            
            ctk.CTkLabel(
                empty_frame,
                text="📦",
                font=ctk.CTkFont(size=60)
            ).pack(pady=(40, 20))
            
            ctk.CTkLabel(
                empty_frame,
                text="คุณยังไม่มีประวัติการสั่งซื้อ",
                font=ctk.CTkFont(size=20, weight="bold"),
                text_color="#FFB6C1"
            ).pack(pady=(0, 10))
            
            ctk.CTkLabel(
                empty_frame,
                text="เริ่มช้อปปิ้งเลยตอนนี้!",
                font=ctk.CTkFont(size=14),
                text_color="gray50"
            ).pack(pady=(0, 40))
            return

        for order_dict in orders_data:
            order = Order.from_dict(order_dict)
            self.create_order_card(orders_frame, order).pack(fill="x", pady=10)

    def create_order_card(self, parent, order: Order):
        """สร้างการ์ดสำหรับแสดงข้อมูล 1 คำสั่งซื้อ"""
        card = ctk.CTkFrame(
            parent,
            fg_color="#FFFFFF",
            corner_radius=20,
            border_width=2,
            border_color="#FFEBEE"
        )

        # Card Header
        header = ctk.CTkFrame(card, fg_color="#FFE4E1", corner_radius=15)
        header.pack(fill="x", padx=15, pady=15)
        
        header_content = ctk.CTkFrame(header, fg_color="transparent")
        header_content.pack(fill="x", padx=15, pady=10)
        
        ctk.CTkLabel(
            header_content,
            text=f"🛍️ หมายเลขคำสั่งซื้อ #{order.order_id}",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#6D4C41"
        ).pack(side="left")
        
        ctk.CTkLabel(
            header_content,
            text=f"📅 {order.format_date()}",
            font=ctk.CTkFont(size=14),
            text_color="#6D4C41"
        ).pack(side="right")

        # Card Body
        body_frame = ctk.CTkFrame(card, fg_color="transparent")
        body_frame.pack(fill="x", padx=20, pady=15)
        body_frame.grid_columnconfigure(0, weight=3)
        body_frame.grid_columnconfigure(1, weight=1)

        # Items list
        items_frame = ctk.CTkFrame(body_frame, fg_color="#FFF0F5", corner_radius=10)
        items_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 15))
        
        items_list = (order.items or "ไม่มีรายการ").replace(",", "\n• ")
        items_text = f"รายการสินค้า:\n• {items_list}"
        
        ctk.CTkLabel(
            items_frame,
            text=items_text,
            justify="left",
            anchor="nw",
            wraplength=500,
            font=ctk.CTkFont(size=14),
            text_color="#6D4C41"
        ).pack(padx=15, pady=15)

        # Total and Status
        summary_frame = ctk.CTkFrame(body_frame, fg_color="transparent")
        summary_frame.grid(row=0, column=1, sticky="ne")
        
        # Total Price
        total_container = ctk.CTkFrame(summary_frame, fg_color="#FFF0F5", corner_radius=10)
        total_container.pack(fill="x", pady=(0, 10))
        
        ctk.CTkLabel(
            total_container,
            text="ยอดรวม",
            font=ctk.CTkFont(size=12),
            text_color="gray50"
        ).pack(pady=(10, 0))
        
        ctk.CTkLabel(
            total_container,
            text=order.format_total(),
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="#FF6B9D"
        ).pack(pady=(5, 10))

        # Status Badge
        status_frame = ctk.CTkFrame(
            summary_frame,
            fg_color=order.get_status_color(),
            corner_radius=10
        )
        status_frame.pack(fill="x")
        
        ctk.CTkLabel(
            status_frame,
            text=order.get_status_text(),
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="white"
        ).pack(padx=20, pady=10)
        
        # View Receipt Button
        receipt_btn = ctk.CTkButton(
            summary_frame,
            text="🧾 ดูใบเสร็จ",
            fg_color="#FFB6C1",
            hover_color="#FFC0CB",
            corner_radius=10,
            height=35,
            command=lambda oid=order.order_id: self.main_app.navigate_to('ReceiptWindow', order_id=oid)
        )
        receipt_btn.pack(fill="x", pady=(10, 0))
        
        return card