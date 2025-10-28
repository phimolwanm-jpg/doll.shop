import customtkinter as ctk
from tkinter import ttk

class SalesHistoryWindow(ctk.CTkFrame):
    def __init__(self, parent, main_app):
        super().__init__(parent, fg_color="#FFF0F5")
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
        
        # Stats Cards
        stats_frame = ctk.CTkFrame(self, fg_color="transparent")
        stats_frame.grid(row=1, column=0, sticky="ew", padx=30, pady=(0, 10))
        stats_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        self.create_stats_cards(stats_frame)
        
        # Main Content
        main_frame = ctk.CTkFrame(
            self,
            fg_color="#FFFFFF",
            corner_radius=20,
            border_width=2,
            border_color="#FFEBEE"
        )
        main_frame.grid(row=2, column=0, sticky="nsew", padx=30, pady=(0, 20))
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(1, weight=1)
        
        # Title
        title_frame = ctk.CTkFrame(main_frame, fg_color="#FFE4E1", corner_radius=15)
        title_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=20)
        ctk.CTkLabel(
            title_frame,
            text="📋 ประวัติการขายทั้งหมด",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#6D4C41"
        ).pack(pady=15)
        
        # Treeview
        self.create_sales_table(main_frame)
    
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
            text="📊 ประวัติการขาย",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#FFB6C1"
        ).pack(side="left", padx=30, pady=20)
        
        btn_frame = ctk.CTkFrame(header, fg_color="transparent")
        btn_frame.pack(side="right", padx=20)
        
        ctk.CTkButton(
            btn_frame,
            text="🏠 หน้าหลัก",
            command=lambda: self.main_app.navigate_to('HomeWindow'),
            fg_color="transparent",
            text_color="#FFB6C1",
            hover_color="#FFE4E1",
            font=ctk.CTkFont(size=14)
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            btn_frame,
            text="📊 Dashboard",
            command=lambda: self.main_app.navigate_to('AdminDashboardWindow'),
            fg_color="#4CAF50",
            hover_color="#66BB6A",
            font=ctk.CTkFont(size=14)
        ).pack(side="left", padx=5)
    
    def create_stats_cards(self, parent):
        """สร้างการ์ดสถิติ"""
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
                'title': 'ลูกค้าทั้งหมด',
                'value': f"{stats['total_customers']}",
                'subtitle': 'คน',
                'icon': '👥',
                'color': '#FF9800'
            },
            {
                'title': 'สินค้าขายแล้ว',
                'value': f"{self.get_total_items_sold()}",
                'subtitle': 'ชิ้น',
                'icon': '📦',
                'color': '#E91E63'
            }
        ]
        
        for i, card_data in enumerate(cards_data):
            card = self.create_stat_card(parent, card_data)
            card.grid(row=0, column=i, padx=10, sticky="nsew")
    
    def create_stat_card(self, parent, data):
        """สร้างการ์ดสถิติแต่ละใบ"""
        card = ctk.CTkFrame(
            parent,
            fg_color="#FFFFFF",
            corner_radius=15,
            border_width=2,
            border_color="#FFEBEE"
        )
        
        ctk.CTkLabel(
            card,
            text=data['icon'],
            font=ctk.CTkFont(size=40)
        ).pack(pady=(15, 5))
        
        ctk.CTkLabel(
            card,
            text=data['title'],
            font=ctk.CTkFont(size=12),
            text_color="gray50"
        ).pack(pady=2)
        
        ctk.CTkLabel(
            card,
            text=data['value'],
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=data['color']
        ).pack(pady=2)
        
        ctk.CTkLabel(
            card,
            text=data['subtitle'],
            font=ctk.CTkFont(size=11),
            text_color="gray40"
        ).pack(pady=(2, 15))
        
        return card
    
    def get_total_items_sold(self):
        """คำนวณจำนวนสินค้าที่ขายไปทั้งหมด"""
        cursor = self.db.connect()
        cursor.execute("SELECT COALESCE(SUM(quantity), 0) FROM order_items")
        total = cursor.fetchone()[0]
        self.db.close()
        return total
    
    def create_sales_table(self, parent):
        """สร้างตารางแสดงประวัติการขาย"""
        tree_frame = ctk.CTkFrame(parent, fg_color="transparent")
        tree_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
        tree_frame.grid_columnconfigure(0, weight=1)
        tree_frame.grid_rowconfigure(0, weight=1)
        
        # Style
        style = ttk.Style()
        style.configure("Sales.Treeview", rowheight=40, font=('Arial', 12))
        style.configure("Sales.Treeview.Heading", font=('Arial', 13, 'bold'))
        
        # Columns
        columns = ("order_id", "date", "customer", "items", "amount", "payment", "status")
        self.tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show="headings",
            style="Sales.Treeview"
        )
        
        # Headings
        headings = {
            "order_id": "Order ID",
            "date": "วันที่",
            "customer": "ลูกค้า",
            "items": "รายการสินค้า",
            "amount": "ยอดเงิน",
            "payment": "ชำระเงิน",
            "status": "สถานะ"
        }
        
        widths = {
            "order_id": 80,
            "date": 150,
            "customer": 180,
            "items": 300,
            "amount": 120,
            "payment": 150,
            "status": 120
        }
        
        for col, heading in headings.items():
            self.tree.heading(col, text=heading)
            self.tree.column(
                col,
                width=widths[col],
                anchor="center" if col in ["order_id", "amount", "status"] else "w"
            )
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        # Load data
        self.load_sales_data()
        
        # Action buttons
        btn_frame = ctk.CTkFrame(parent, fg_color="transparent")
        btn_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=(0, 20))
        
        ctk.CTkButton(
            btn_frame,
            text="🔄 รีเฟรช",
            command=self.on_show,
            fg_color="#FFB6C1",
            hover_color="#FFC0CB",
            height=40,
            corner_radius=10,
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(side="left", padx=5, fill="x", expand=True)
        
        ctk.CTkButton(
            btn_frame,
            text="📊 ดูสถิติเพิ่มเติม",
            command=lambda: self.main_app.navigate_to('AdminDashboardWindow'),
            fg_color="#4CAF50",
            hover_color="#66BB6A",
            height=40,
            corner_radius=10,
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(side="left", padx=5, fill="x", expand=True)
        
        ctk.CTkButton(
            btn_frame,
            text="📦 จัดการคำสั่งซื้อ",
            command=lambda: self.main_app.navigate_to('AdminOrdersWindow'),
            fg_color="#2196F3",
            hover_color="#42A5F5",
            height=40,
            corner_radius=10,
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(side="left", padx=5, fill="x", expand=True)
    
    def load_sales_data(self):
        """โหลดข้อมูลประวัติการขาย"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        orders = self.db.get_all_orders()
        
        status_text = {
            'pending': '⏳ รอดำเนินการ',
            'confirmed': '✅ ยืนยันแล้ว',
            'shipped': '🚚 กำลังจัดส่ง',
            'delivered': '✔️ สำเร็จ',
            'cancelled': '❌ ยกเลิก'
        }
        
        payment_text = {
            'โอนเงินผ่านธนาคาร': '🏦 โอนเงิน',
            'เก็บเงินปลายทาง': '📦 COD',
            'Credit Card': '💳 บัตร'
        }
        
        for order in orders:
            # แปลง items ให้สั้นลง
            items = order.get('items', '')
            if len(items) > 50:
                items = items[:47] + "..."
            
            self.tree.insert("", "end", values=(
                f"#{order['order_id']}",
                order['created_at'][:16] if order['created_at'] else '-',
                order['full_name'],
                items if items else 'ไม่มีรายการ',
                f"฿{order['total_amount']:,.2f}",
                payment_text.get(order['payment_method'], order['payment_method']),
                status_text.get(order['status'], order['status'])
            ))