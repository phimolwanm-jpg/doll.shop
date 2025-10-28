import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime

class ReceiptWindow(ctk.CTkFrame):
    def __init__(self, parent, main_app):
        super().__init__(parent, fg_color="#FFF0F5")
        self.main_app = main_app
        self.db = main_app.db
        self.session = main_app.session
        self.order_id = None
        
    def on_show(self, order_id=None):
        """รับ order_id และแสดงใบเสร็จ"""
        self.order_id = order_id
        
        for widget in self.winfo_children():
            widget.destroy()
        
        if not order_id:
            self.show_error()
            return
            
        self.setup_ui()
    
    def show_error(self):
        """แสดงข้อความ error เมื่อไม่มี order_id"""
        ctk.CTkLabel(
            self,
            text="❌ ไม่พบข้อมูลคำสั่งซื้อ",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#F44336"
        ).pack(expand=True)
        
        ctk.CTkButton(
            self,
            text="กลับไปหน้าหลัก",
            command=lambda: self.main_app.navigate_to('HomeWindow'),
            fg_color="#FFB6C1",
            hover_color="#FFC0CB"
        ).pack(pady=20)
    
    def setup_ui(self):
        """สร้าง UI ใบเสร็จ"""
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Header
        self.create_header()
        
        # Receipt Container
        receipt_container = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            scrollbar_button_color="#FFB6C1"
        )
        receipt_container.grid(row=1, column=0, sticky="nsew", padx=30, pady=20)
        
        # Receipt Card
        receipt_card = ctk.CTkFrame(
            receipt_container,
            fg_color="#FFFFFF",
            corner_radius=20,
            border_width=3,
            border_color="#FFB6C1"
        )
        receipt_card.pack(fill="both", expand=True, padx=50, pady=20)
        
        self.create_receipt_content(receipt_card)
    
    def create_header(self):
        """สร้าง Header"""
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
            text="🧾 ใบเสร็จการสั่งซื้อ",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#FFB6C1"
        ).pack(side="left", padx=30, pady=20)
        
        btn_frame = ctk.CTkFrame(header, fg_color="transparent")
        btn_frame.pack(side="right", padx=20)
        
        ctk.CTkButton(
            btn_frame,
            text="🖨️ พิมพ์",
            fg_color="#4CAF50",
            hover_color="#66BB6A",
            command=self.print_receipt
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            btn_frame,
            text="🏠 หน้าหลัก",
            fg_color="transparent",
            text_color="#FFB6C1",
            hover_color="#FFE4E1",
            command=lambda: self.main_app.navigate_to('HomeWindow')
        ).pack(side="left", padx=5)
    
    def create_receipt_content(self, parent):
        """สร้างเนื้อหาใบเสร็จ"""
        # โหลดข้อมูลคำสั่งซื้อ
        order = self.db.get_order_details(self.order_id)
        
        if not order:
            ctk.CTkLabel(
                parent,
                text="ไม่พบข้อมูลคำสั่งซื้อ",
                text_color="#F44336"
            ).pack(pady=50)
            return
        
        # Shop Logo & Name
        logo_frame = ctk.CTkFrame(parent, fg_color="#FFE4E1", corner_radius=15)
        logo_frame.pack(fill="x", padx=30, pady=(30, 20))
        
        ctk.CTkLabel(
            logo_frame,
            text="🎀",
            font=ctk.CTkFont(size=60)
        ).pack(pady=(20, 10))
        
        ctk.CTkLabel(
            logo_frame,
            text="Dollie Shop",
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color="#FF6B9D"
        ).pack()
        
        ctk.CTkLabel(
            logo_frame,
            text="ร้านขายตุ๊กตาน่ารัก",
            font=ctk.CTkFont(size=14),
            text_color="#6D4C41"
        ).pack(pady=(0, 20))
        
        # Receipt Title
        title_frame = ctk.CTkFrame(parent, fg_color="transparent")
        title_frame.pack(fill="x", padx=30, pady=20)
        
        ctk.CTkLabel(
            title_frame,
            text="ใบเสร็จรับเงิน / RECEIPT",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#6D4C41"
        ).pack()
        
        # Order Info
        info_frame = ctk.CTkFrame(parent, fg_color="#FFF0F5", corner_radius=15)
        info_frame.pack(fill="x", padx=30, pady=20)
        info_frame.grid_columnconfigure((0, 1), weight=1)
        
        # Left column
        left_info = ctk.CTkFrame(info_frame, fg_color="transparent")
        left_info.grid(row=0, column=0, sticky="w", padx=20, pady=20)
        
        self.add_info_row(left_info, "เลขที่ใบเสร็จ:", f"#{order['order_id']}", 0)
        self.add_info_row(left_info, "วันที่:", order['created_at'][:16] if order['created_at'] else '-', 1)
        self.add_info_row(left_info, "ลูกค้า:", order['full_name'], 2)
        
        # Right column
        right_info = ctk.CTkFrame(info_frame, fg_color="transparent")
        right_info.grid(row=0, column=1, sticky="w", padx=20, pady=20)
        
        status_colors = {
            'pending': '#FF9800',
            'confirmed': '#4CAF50',
            'shipped': '#2196F3',
            'delivered': '#4CAF50',
            'cancelled': '#F44336'
        }
        
        status_text = {
            'pending': '⏳ รอดำเนินการ',
            'confirmed': '✅ ยืนยันแล้ว',
            'shipped': '🚚 กำลังจัดส่ง',
            'delivered': '✔️ จัดส่งสำเร็จ',
            'cancelled': '❌ ยกเลิก'
        }
        
        self.add_info_row(right_info, "สถานะ:", status_text.get(order['status'], order['status']), 0)
        self.add_info_row(right_info, "การชำระเงิน:", order['payment_method'], 1)
        
        # Separator
        ctk.CTkFrame(parent, height=2, fg_color="#FFEBEE").pack(fill="x", padx=30, pady=10)
        
        # Items Table Header
        table_header = ctk.CTkFrame(parent, fg_color="#FFE4E1", corner_radius=10)
        table_header.pack(fill="x", padx=30, pady=(20, 10))
        
        header_grid = ctk.CTkFrame(table_header, fg_color="transparent")
        header_grid.pack(fill="x", padx=15, pady=10)
        header_grid.grid_columnconfigure(0, weight=2)
        header_grid.grid_columnconfigure(1, weight=1)
        header_grid.grid_columnconfigure(2, weight=1)
        
        ctk.CTkLabel(
            header_grid,
            text="รายการสินค้า",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#6D4C41",
            anchor="w"
        ).grid(row=0, column=0, sticky="w", padx=5)
        
        ctk.CTkLabel(
            header_grid,
            text="จำนวน",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#6D4C41",
            anchor="center"
        ).grid(row=0, column=1, padx=5)
        
        ctk.CTkLabel(
            header_grid,
            text="ราคา",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#6D4C41",
            anchor="e"
        ).grid(row=0, column=2, sticky="e", padx=5)
        
        # Items List
        items_container = ctk.CTkFrame(parent, fg_color="transparent")
        items_container.pack(fill="x", padx=30)
        
        # Parse items (assuming format: "item1 x2, item2 x3")
        items_str = order.get('items', '')
        if items_str:
            items = items_str.split(', ')
            for item_str in items:
                self.add_item_row(items_container, item_str)
        
        # Separator
        ctk.CTkFrame(parent, height=2, fg_color="#FFEBEE").pack(fill="x", padx=30, pady=20)
        
        # Total
        total_frame = ctk.CTkFrame(parent, fg_color="#FFE4E1", corner_radius=15)
        total_frame.pack(fill="x", padx=30, pady=20)
        
        total_grid = ctk.CTkFrame(total_frame, fg_color="transparent")
        total_grid.pack(fill="x", padx=20, pady=15)
        
        ctk.CTkLabel(
            total_grid,
            text="ยอดรวมทั้งสิ้น:",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#6D4C41"
        ).pack(side="left")
        
        ctk.CTkLabel(
            total_grid,
            text=f"฿{order['total_amount']:,.2f}",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#FF6B9D"
        ).pack(side="right")
        
        # Shipping Address
        if order.get('shipping_address'):
            address_frame = ctk.CTkFrame(parent, fg_color="#FFF0F5", corner_radius=15)
            address_frame.pack(fill="x", padx=30, pady=20)
            
            ctk.CTkLabel(
                address_frame,
                text="📍 ที่อยู่จัดส่ง",
                font=ctk.CTkFont(size=16, weight="bold"),
                text_color="#6D4C41",
                anchor="w"
            ).pack(anchor="w", padx=20, pady=(15, 5))
            
            ctk.CTkLabel(
                address_frame,
                text=order['shipping_address'],
                font=ctk.CTkFont(size=14),
                text_color="#6D4C41",
                anchor="w",
                justify="left"
            ).pack(anchor="w", padx=20, pady=(0, 15))
        
        # Footer
        footer_frame = ctk.CTkFrame(parent, fg_color="transparent")
        footer_frame.pack(fill="x", padx=30, pady=(20, 30))
        
        ctk.CTkLabel(
            footer_frame,
            text="ขอบคุณที่ใช้บริการ 💖",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#FFB6C1"
        ).pack()
        
        ctk.CTkLabel(
            footer_frame,
            text="Dollie Shop | www.dollieshop.com | โทร: 02-xxx-xxxx",
            font=ctk.CTkFont(size=12),
            text_color="gray50"
        ).pack(pady=(5, 0))
    
    def add_info_row(self, parent, label, value, row):
        """เพิ่มแถวข้อมูล"""
        ctk.CTkLabel(
            parent,
            text=label,
            font=ctk.CTkFont(size=13),
            text_color="gray50",
            anchor="w"
        ).grid(row=row, column=0, sticky="w", pady=3)
        
        ctk.CTkLabel(
            parent,
            text=value,
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#6D4C41",
            anchor="w"
        ).grid(row=row, column=1, sticky="w", padx=(10, 0), pady=3)
    
    def add_item_row(self, parent, item_str):
        """เพิ่มแถวสินค้า"""
        # Parse "Product Name x2"
        parts = item_str.rsplit(' x', 1)
        if len(parts) == 2:
            name = parts[0]
            qty = parts[1]
        else:
            name = item_str
            qty = "1"
        
        item_frame = ctk.CTkFrame(parent, fg_color="#FFF0F5", corner_radius=10)
        item_frame.pack(fill="x", pady=5)
        
        item_grid = ctk.CTkFrame(item_frame, fg_color="transparent")
        item_grid.pack(fill="x", padx=15, pady=10)
        item_grid.grid_columnconfigure(0, weight=2)
        item_grid.grid_columnconfigure(1, weight=1)
        item_grid.grid_columnconfigure(2, weight=1)
        
        ctk.CTkLabel(
            item_grid,
            text=f"• {name}",
            font=ctk.CTkFont(size=14),
            text_color="#6D4C41",
            anchor="w"
        ).grid(row=0, column=0, sticky="w", padx=5)
        
        ctk.CTkLabel(
            item_grid,
            text=f"x{qty}",
            font=ctk.CTkFont(size=14),
            text_color="#FFB6C1",
            anchor="center"
        ).grid(row=0, column=1, padx=5)
        
        ctk.CTkLabel(
            item_grid,
            text="-",
            font=ctk.CTkFont(size=14),
            text_color="#6D4C41",
            anchor="e"
        ).grid(row=0, column=2, sticky="e", padx=5)
    
    def print_receipt(self):
        """ฟังก์ชันพิมพ์ใบเสร็จ (Placeholder)"""
        messagebox.showinfo(
            "พิมพ์ใบเสร็จ",
            "ฟีเจอร์พิมพ์ใบเสร็จกำลังพัฒนา\nคุณสามารถ Screenshot หน้าจอนี้แทนได้",
            parent=self
        )