import customtkinter as ctk

class ThankYouWindow(ctk.CTkFrame):
    def __init__(self, parent, main_app):
        """
        แก้ไข Constructor ให้รับ main_app
        """
        super().__init__(parent, fg_color="#F8F9FA")
        self.main_app = main_app
        self.assets = main_app.assets
        self.order_id = None # จะถูกตั้งค่าใน on_show

    def on_show(self, order_id=None):
        """
        ฟังก์ชันนี้จะถูกเรียกโดย main.py เมื่อหน้านี้ถูกแสดง
        พร้อมรับ 'order_id' ที่ถูกส่งมาจากหน้า Checkout
        """
        self.order_id = order_id
        for widget in self.winfo_children():
            widget.destroy()
        self.setup_ui()

    def setup_ui(self):
        """สร้างองค์ประกอบ UI ทั้งหมด"""
        self.pack_propagate(False) # ป้องกันไม่ให้ frame หดตาม widget ภายใน
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.grid(row=0, column=0) # ใช้ grid แทน pack เพื่อให้อยู่ตรงกลางเสมอ

        # ดึงรูปภาพจาก assets ที่โหลดไว้แล้ว
        ctk.CTkLabel(main_frame, text="", image=self.assets.thank_you_doll).pack(pady=(0, 20))
        
        ctk.CTkLabel(main_frame, text="ขอบคุณที่อุดหนุนนะคะ!", font=ctk.CTkFont(size=32, weight="bold"), text_color="#FF69B4").pack(pady=10)
        
        order_text = f"คำสั่งซื้อของคุณหมายเลข #{self.order_id} ได้รับการยืนยันแล้ว" if self.order_id else "คำสั่งซื้อของคุณได้รับการยืนยันแล้ว"
        ctk.CTkLabel(main_frame, text=order_text, font=ctk.CTkFont(size=16), text_color="gray").pack()
        
        # --- Buttons ---
        btn_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        btn_frame.pack(pady=30)
        
        # แก้ไขการเรียก navigate_to
        home_btn = ctk.CTkButton(btn_frame, text="กลับไปหน้าหลัก", height=40, corner_radius=20,
                                 command=lambda: self.main_app.navigate_to('HomeWindow'))
        home_btn.pack(side="left", padx=10)
        
        history_btn = ctk.CTkButton(btn_frame, text="ดูประวัติการสั่งซื้อ", height=40, corner_radius=20, fg_color="transparent", border_width=1,
                                    command=lambda: self.main_app.navigate_to('OrderHistoryWindow'))
        history_btn.pack(side="left", padx=10)