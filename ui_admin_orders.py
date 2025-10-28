# M:/doll_shop/ui_admin_orders.py (สร้างไฟล์ใหม่หรือวางทับ)

import customtkinter as ctk
from tkinter import ttk, messagebox

class AdminOrdersWindow(ctk.CTkFrame):
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
        
        # Main Content
        main_frame = ctk.CTkFrame(self, fg_color="#FFFFFF", corner_radius=20, border_width=2, border_color="#FFEBEE")
        main_frame.grid(row=1, column=0, sticky="nsew", padx=30, pady=20)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(1, weight=1)
        
        # Title
        title_frame = ctk.CTkFrame(main_frame, fg_color="#FFE4E1", corner_radius=15)
        title_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=20)
        ctk.CTkLabel(
            title_frame,
            text="📋 รายการคำสั่งซื้อทั้งหมด",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#6D4C41"
        ).pack(pady=15)
        
        # Treeview
        self.create_orders_table(main_frame)
    
    def create_header(self):
        header = ctk.CTkFrame(self, fg_color="#FFFFFF", corner_radius=0, height=70, border_width=1, border_color="#FFEBEE")
        header.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        header.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(
            header,
            text="📦 จัดการคำสั่งซื้อ",
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
    
    def create_orders_table(self, parent):
        """สร้างตารางแสดงคำสั่งซื้อ"""
        tree_frame = ctk.CTkFrame(parent, fg_color="transparent")
        tree_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
        tree_frame.grid_columnconfigure(0, weight=1)
        tree_frame.grid_rowconfigure(0, weight=1)
        
        # Style
        style = ttk.Style()
        style.configure("Orders.Treeview", rowheight=40, font=('Arial', 12))
        style.configure("Orders.Treeview.Heading", font=('Arial', 13, 'bold'))
        
        # Columns
        columns = ("order_id", "customer", "amount", "payment", "status", "date")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", style="Orders.Treeview")
        
        # Headings
        self.tree.heading("order_id", text="Order ID")
        self.tree.heading("customer", text="ลูกค้า")
        self.tree.heading("amount", text="ยอดเงิน")
        self.tree.heading("payment", text="การชำระเงิน")
        self.tree.heading("status", text="สถานะ")
        self.tree.heading("date", text="วันที่")
        
        # Column widths
        self.tree.column("order_id", width=80, anchor="center")
        self.tree.column("customer", width=200)
        self.tree.column("amount", width=120, anchor="e")
        self.tree.column("payment", width=150)
        self.tree.column("status", width=120, anchor="center")
        self.tree.column("date", width=150, anchor="center")
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        # Load data
        self.load_orders()
        
        # Action buttons
        btn_frame = ctk.CTkFrame(parent, fg_color="transparent")
        btn_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=(0, 20))
        
        ctk.CTkButton(
            btn_frame,
            text="✅ ยืนยันคำสั่งซื้อ",
            command=lambda: self.change_status("confirmed"),
            fg_color="#4CAF50",
            hover_color="#66BB6A",
            height=40,
            corner_radius=10,
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(side="left", padx=5, fill="x", expand=True)
        
        ctk.CTkButton(
            btn_frame,
            text="🚚 เริ่มจัดส่ง",
            command=lambda: self.change_status("shipped"),
            fg_color="#2196F3",
            hover_color="#42A5F5",
            height=40,
            corner_radius=10,
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(side="left", padx=5, fill="x", expand=True)
        
        ctk.CTkButton(
            btn_frame,
            text="✔️ จัดส่งสำเร็จ",
            command=lambda: self.change_status("delivered"),
            fg_color="#FF9800",
            hover_color="#FFA726",
            height=40,
            corner_radius=10,
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(side="left", padx=5, fill="x", expand=True)
        
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
    
    def load_orders(self):
        """โหลดข้อมูลคำสั่งซื้อทั้งหมด"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        orders = self.db.get_all_orders()
        
        status_text = {
            'pending': '⏳ รอดำเนินการ',
            'confirmed': '✅ ยืนยันแล้ว',
            'shipped': '🚚 กำลังจัดส่ง',
            'delivered': '✔️ จัดส่งสำเร็จ',
            'cancelled': '❌ ยกเลิก'
        }
        
        for order in orders:
            self.tree.insert("", "end", values=(
                f"#{order['order_id']}",
                order['full_name'],
                f"฿{order['total_amount']:,.2f}",
                order['payment_method'],
                status_text.get(order['status'], order['status']),
                order['created_at'][:16] if order['created_at'] else '-'
            ))
    
    def change_status(self, new_status):
        """เปลี่ยนสถานะคำสั่งซื้อที่เลือก"""
        selected_items = self.tree.selection()
        
        if not selected_items:
            messagebox.showwarning("คำเตือน", "กรุณาเลือกคำสั่งซื้อที่ต้องการเปลี่ยนสถานะ", parent=self)
            return
        
        status_names = {
            'confirmed': 'ยืนยันคำสั่งซื้อ',
            'shipped': 'เริ่มจัดส่ง',
            'delivered': 'จัดส่งสำเร็จ',
            'cancelled': 'ยกเลิก'
        }
        
        confirm_msg = f"ต้องการเปลี่ยนสถานะเป็น '{status_names.get(new_status, new_status)}' ใช่หรือไม่?"
        
        if messagebox.askyesno("ยืนยัน", confirm_msg, parent=self):
            for item in selected_items:
                values = self.tree.item(item)['values']
                order_id = int(values[0].replace('#', ''))
                
                if self.db.update_order_status(order_id, new_status):
                    messagebox.showinfo("สำเร็จ", f"เปลี่ยนสถานะคำสั่งซื้อ #{order_id} เรียบร้อย", parent=self)
                else:
                    messagebox.showerror("ผิดพลาด", f"ไม่สามารถเปลี่ยนสถานะคำสั่งซื้อ #{order_id} ได้", parent=self)
            
            self.load_orders()