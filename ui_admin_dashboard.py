# M:/doll_shop/ui_admin_dashboard.py (ไฟล์ใหม่)

import customtkinter as ctk
from tkinter import ttk

class AdminDashboardWindow(ctk.CTkFrame):
    def __init__(self, parent, main_app):
        super().__init__(parent, fg_color="#F8F9FA")
        self.main_app = main_app
        self.db = main_app.db
        
        self.setup_ui()
    
    def on_show(self):
        """รีเฟรชข้อมูลทุกครั้งที่เปิดหน้านี้"""
        for widget in self.winfo_children():
            widget.destroy()
        self.setup_ui()
    
    def setup_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Header
        self.create_header()
        
        # Main Content
        main_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        main_frame.grid(row=1, column=0, sticky="nsew", padx=30, pady=20)
        main_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        # Stats Cards
        self.create_stats_cards(main_frame)
        
        # Charts Section
        chart_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        chart_frame.grid(row=1, column=0, columnspan=4, sticky="ew", pady=20)
        chart_frame.grid_columnconfigure((0, 1), weight=1)
        
        # Top Selling Products
        self.create_top_products_section(chart_frame)
        
        # Low Stock Alert
        self.create_low_stock_section(chart_frame)
        
        # Recent Orders
        self.create_recent_orders_section(main_frame)
    
    def create_header(self):
        header = ctk.CTkFrame(self, fg_color="white", corner_radius=0, height=70)
        header.grid(row=0, column=0, sticky="ew")
        header.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(
            header, 
            text="📊 Admin Dashboard", 
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#2E7D32"
        ).pack(side="left", padx=30)
        
        btn_frame = ctk.CTkFrame(header, fg_color="transparent")
        btn_frame.pack(side="right", padx=20)
        
        ctk.CTkButton(
            btn_frame,
            text="🏠 หน้าหลัก",
            command=lambda: self.main_app.navigate_to('HomeWindow'),
            fg_color="transparent",
            text_color="gray50",
            hover_color="#F5F5F5"
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            btn_frame,
            text="⚙️ จัดการสินค้า",
            command=lambda: self.main_app.navigate_to('AdminWindow'),
            fg_color="#FF6B9D",
            hover_color="#FF8FB3"
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            btn_frame,
            text="📦 จัดการคำสั่งซื้อ",
            command=lambda: self.main_app.navigate_to('AdminOrdersWindow'),
            fg_color="#2196F3",
            hover_color="#42A5F5"
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            btn_frame,
            text="📊 ประวัติการขาย",
            command=lambda: self.main_app.navigate_to('SalesHistoryWindow'),
            fg_color="#9C27B0",
            hover_color="#BA68C8"
        ).pack(side="left", padx=5)
    
    def create_stats_cards(self, parent):
        """สร้างการ์ดแสดงสถิติ"""
        stats = self.db.get_dashboard_stats()
        
        cards_data = [
            {
                'title': 'ยอดขายรวม',
                'value': f"{stats['total_orders']}",
                'subtitle': 'คำสั่งซื้อ',
                'icon': '🛒',
                'color': '#4CAF50'
            },
            {
                'title': 'รายได้ทั้งหมด',
                'value': f"฿{stats['total_revenue']:,.2f}",
                'subtitle': 'บาท',
                'icon': '💰',
                'color': '#2196F3'
            },
            {
                'title': 'สินค้าทั้งหมด',
                'value': f"{stats['total_products']}",
                'subtitle': 'รายการ',
                'icon': '📦',
                'color': '#FF9800'
            },
            {
                'title': 'รอดำเนินการ',
                'value': f"{stats['pending_orders']}",
                'subtitle': 'คำสั่งซื้อ',
                'icon': '⏳',
                'color': '#F44336'
            }
        ]
        
        for i, card_data in enumerate(cards_data):
            card = self.create_stat_card(parent, card_data)
            card.grid(row=0, column=i, padx=10, pady=10, sticky="nsew")
    
    def create_stat_card(self, parent, data):
        """สร้างการ์ดสถิติแต่ละใบ"""
        card = ctk.CTkFrame(parent, fg_color="white", corner_radius=15, border_width=1, border_color="#E0E0E0")
        card.grid_columnconfigure(0, weight=1)
        
        # Icon
        icon_label = ctk.CTkLabel(
            card, 
            text=data['icon'], 
            font=ctk.CTkFont(size=40)
        )
        icon_label.grid(row=0, column=0, pady=(20, 10))
        
        # Title
        ctk.CTkLabel(
            card, 
            text=data['title'], 
            font=ctk.CTkFont(size=14),
            text_color="gray50"
        ).grid(row=1, column=0, pady=5)
        
        # Value
        ctk.CTkLabel(
            card, 
            text=data['value'], 
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=data['color']
        ).grid(row=2, column=0, pady=5)
        
        # Subtitle
        ctk.CTkLabel(
            card, 
            text=data['subtitle'], 
            font=ctk.CTkFont(size=12),
            text_color="gray40"
        ).grid(row=3, column=0, pady=(5, 20))
        
        return card
    
    def create_top_products_section(self, parent):
        """แสดงสินค้าขายดี"""
        section = ctk.CTkFrame(parent, fg_color="white", corner_radius=15)
        section.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        ctk.CTkLabel(
            section, 
            text="🏆 สินค้าขายดี Top 5", 
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(pady=(20, 10), padx=20, anchor="w")
        
        top_products = self.db.get_top_selling_products(5)
        
        if top_products:
            for i, product in enumerate(top_products, 1):
                item_frame = ctk.CTkFrame(section, fg_color="#F5F5F5", corner_radius=10)
                item_frame.pack(fill="x", padx=20, pady=5)
                
                rank_label = ctk.CTkLabel(
                    item_frame, 
                    text=f"#{i}", 
                    font=ctk.CTkFont(size=16, weight="bold"),
                    text_color="#FF6B9D",
                    width=40
                )
                rank_label.pack(side="left", padx=10, pady=10)
                
                info_frame = ctk.CTkFrame(item_frame, fg_color="transparent")
                info_frame.pack(side="left", fill="x", expand=True, padx=10)
                
                ctk.CTkLabel(
                    info_frame, 
                    text=product['name'], 
                    font=ctk.CTkFont(size=14, weight="bold"),
                    anchor="w"
                ).pack(anchor="w")
                
                ctk.CTkLabel(
                    info_frame, 
                    text=f"ขายได้: {product['total_sold']} ชิ้น | รายได้: ฿{product['total_revenue']:,.2f}", 
                    font=ctk.CTkFont(size=12),
                    text_color="gray50",
                    anchor="w"
                ).pack(anchor="w")
        else:
            ctk.CTkLabel(
                section, 
                text="ยังไม่มีข้อมูลการขาย", 
                text_color="gray50"
            ).pack(pady=20)
        
        ctk.CTkLabel(section, text="").pack(pady=10)  # Spacer
    
    def create_low_stock_section(self, parent):
        """แสดงสินค้าที่สต็อกต่ำ"""
        section = ctk.CTkFrame(parent, fg_color="white", corner_radius=15)
        section.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        
        ctk.CTkLabel(
            section, 
            text="⚠️ สินค้าสต็อกต่ำ", 
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#F44336"
        ).pack(pady=(20, 10), padx=20, anchor="w")
        
        low_stock = self.db.get_low_stock_products(10)
        
        if low_stock:
            for product in low_stock[:5]:  # แสดงแค่ 5 รายการแรก
                item_frame = ctk.CTkFrame(section, fg_color="#FFEBEE", corner_radius=10)
                item_frame.pack(fill="x", padx=20, pady=5)
                
                info_frame = ctk.CTkFrame(item_frame, fg_color="transparent")
                info_frame.pack(side="left", fill="x", expand=True, padx=15, pady=10)
                
                ctk.CTkLabel(
                    info_frame, 
                    text=product['name'], 
                    font=ctk.CTkFont(size=14, weight="bold"),
                    anchor="w"
                ).pack(anchor="w")
                
                stock_color = "#F44336" if product['stock'] < 5 else "#FF9800"
                ctk.CTkLabel(
                    info_frame, 
                    text=f"เหลือ: {product['stock']} ชิ้น", 
                    font=ctk.CTkFont(size=12),
                    text_color=stock_color,
                    anchor="w"
                ).pack(anchor="w")
        else:
            ctk.CTkLabel(
                section, 
                text="สต็อกสินค้าเพียงพอทั้งหมด ✓", 
                text_color="#4CAF50"
            ).pack(pady=20)
        
        ctk.CTkLabel(section, text="").pack(pady=10)  # Spacer
    
    def create_recent_orders_section(self, parent):
        """แสดงคำสั่งซื้อล่าสุด"""
        section = ctk.CTkFrame(parent, fg_color="white", corner_radius=15)
        section.grid(row=2, column=0, columnspan=4, sticky="nsew", pady=20)
        
        ctk.CTkLabel(
            section, 
            text="📋 คำสั่งซื้อล่าสุด", 
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(pady=(20, 10), padx=20, anchor="w")
        
        # Treeview
        style = ttk.Style()
        style.configure("Dashboard.Treeview", rowheight=35, font=('Arial', 11))
        style.configure("Dashboard.Treeview.Heading", font=('Arial', 12, 'bold'))
        
        columns = ("order_id", "customer", "amount", "status", "date")
        tree = ttk.Treeview(section, columns=columns, show="headings", height=8, style="Dashboard.Treeview")
        
        tree.heading("order_id", text="Order ID")
        tree.heading("customer", text="ลูกค้า")
        tree.heading("amount", text="ยอดเงิน")
        tree.heading("status", text="สถานะ")
        tree.heading("date", text="วันที่")
        
        tree.column("order_id", width=80, anchor="center")
        tree.column("customer", width=200)
        tree.column("amount", width=120, anchor="e")
        tree.column("status", width=120, anchor="center")
        tree.column("date", width=150, anchor="center")
        
        tree.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        recent_orders = self.db.get_recent_orders(10)
        
        status_text = {
            'pending': 'รอดำเนินการ',
            'confirmed': 'ยืนยันแล้ว',
            'shipped': 'จัดส่งแล้ว',
            'delivered': 'ส่งสำเร็จ',
            'cancelled': 'ยกเลิก'
        }
        
        for order in recent_orders:
            tree.insert("", "end", values=(
                f"#{order['order_id']}",
                order['full_name'],
                f"฿{order['total_amount']:,.2f}",
                status_text.get(order['status'], order['status']),
                order['created_at'][:16] if order['created_at'] else '-'
            ))