# M:/doll_shop/ui_admin.py (วางทับไฟล์เดิมทั้งหมด)

import customtkinter as ctk
from tkinter import ttk, messagebox, filedialog
from PIL import Image
import os
import shutil

class AdminWindow(ctk.CTkFrame):
    def __init__(self, parent, main_app):
        """
        แก้ไข Constructor ให้รับ main_app และดึงส่วนประกอบหลักที่จำเป็น
        """
        super().__init__(parent, fg_color="#F8F9FA")
        self.main_app = main_app
        self.db = main_app.db
        self.assets = main_app.assets # ดึง assets ที่โหลดไว้แล้ว

        self.selected_product_id = None
        self.image_path = None # เก็บชื่อไฟล์ของรูปภาพที่อัปโหลด
        self.image_filename = None # ใช้สำหรับแสดงผล

        self.setup_ui()
        self.load_products_to_treeview()

    def on_show(self):
        """
        ฟังก์ชันนี้จะถูกเรียกโดย main.py ทุกครั้งที่หน้านี้ถูกแสดง
        เพื่อให้รายการสินค้าอัปเดตเสมอ
        """
        self.clear_form()
        self.load_products_to_treeview()

    def setup_ui(self):
        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(1, weight=1)

        # --- Header ---
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, columnspan=2, padx=30, pady=20, sticky="ew")
        ctk.CTkLabel(header_frame, text="⚙️ จัดการสินค้าในร้าน", font=ctk.CTkFont(size=28, weight="bold")).pack(side="left")
        
        # แก้ไขปุ่มกลับไปหน้าหลัก
        back_button = ctk.CTkButton(header_frame, text="< กลับไปหน้าหลัก", fg_color="transparent", text_color="gray50", hover=False,
                                    command=lambda: self.main_app.navigate_to('HomeWindow'))
        back_button.pack(side="right")

        # --- Left Panel: Product List ---
        list_frame = ctk.CTkFrame(self, fg_color="white", corner_radius=15)
        list_frame.grid(row=1, column=0, padx=(30, 10), pady=10, sticky="nsew")
        list_frame.grid_propagate(False)
        list_frame.grid_rowconfigure(1, weight=1)
        list_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(list_frame, text="รายการสินค้าทั้งหมด", font=ctk.CTkFont(size=18, weight="bold")).grid(row=0, column=0, padx=20, pady=15, sticky="w")
        self.setup_treeview(list_frame)

        # --- Right Panel: Product Form ---
        form_frame = ctk.CTkFrame(self, fg_color="white", corner_radius=15)
        form_frame.grid(row=1, column=1, padx=(10, 30), pady=10, sticky="nsew")
        form_frame.grid_columnconfigure(0, weight=1)
        
        ctk.CTkLabel(form_frame, text="เพิ่ม / แก้ไขข้อมูลสินค้า", font=ctk.CTkFont(size=18, weight="bold")).grid(row=0, column=0, padx=20, pady=15, sticky="w")
        self.setup_form(form_frame)


    def setup_treeview(self, parent):
        """สร้างตารางแสดงผล Treeview"""
        style = ttk.Style()
        style.configure("Treeview.Heading", font=('Arial', 14, 'bold'))
        style.configure("Treeview", rowheight=30, font=('Arial', 12))
        
        columns = ("id", "name", "category", "price", "stock")
        self.tree = ttk.Treeview(parent, columns=columns, show="headings", style="Treeview")

        headings = {"id": "ID", "name": "ชื่อสินค้า", "category": "หมวดหมู่", "price": "ราคา", "stock": "สต็อก"}
        widths = {"id": 50, "name": 250, "category": 120, "price": 100, "stock": 80}

        for col, heading in headings.items():
            self.tree.heading(col, text=heading)
            self.tree.column(col, width=widths[col], anchor="center")
        
        self.tree.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        self.tree.bind("<<TreeviewSelect>>", self.on_product_select)


    def setup_form(self, parent):
        """สร้างฟอร์มสำหรับกรอกข้อมูลสินค้า"""
        form_fields = ctk.CTkFrame(parent, fg_color="transparent")
        form_fields.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        form_fields.grid_columnconfigure(1, weight=1)
        
        self.entries = {}
        fields = {"name": "ชื่อสินค้า:", "category": "หมวดหมู่:", "price": "ราคา:", "stock": "จำนวน:", "description": "คำอธิบาย:"}

        for i, (key, label) in enumerate(fields.items()):
            ctk.CTkLabel(form_fields, text=label).grid(row=i, column=0, padx=5, pady=10, sticky="w")
            if key == "description":
                entry = ctk.CTkTextbox(form_fields, height=100)
            else:
                entry = ctk.CTkEntry(form_fields)
            entry.grid(row=i, column=1, padx=5, pady=10, sticky="ew")
            self.entries[key] = entry
        
        # --- Image Upload ---
        ctk.CTkLabel(form_fields, text="รูปภาพ:").grid(row=len(fields), column=0, padx=5, pady=10, sticky="w")
        self.image_label = ctk.CTkLabel(form_fields, text="ยังไม่ได้เลือกรูปภาพ", text_color="gray")
        self.image_label.grid(row=len(fields), column=1, padx=5, pady=10, sticky="w")
        upload_btn = ctk.CTkButton(form_fields, text="เลือกรูปภาพ", command=self.upload_image)
        upload_btn.grid(row=len(fields)+1, column=1, padx=5, pady=5, sticky="w")
        
        # --- Action Buttons ---
        btn_frame = ctk.CTkFrame(parent, fg_color="transparent")
        btn_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=15)
        btn_frame.grid_columnconfigure((0, 1, 2), weight=1)

        ctk.CTkButton(btn_frame, text="💾 บันทึก", command=self.save_product, height=40).grid(row=0, column=0, padx=5, sticky="ew")
        ctk.CTkButton(btn_frame, text="✨ เคลียร์ฟอร์ม", command=self.clear_form, fg_color="gray50", height=40).grid(row=0, column=1, padx=5, sticky="ew")
        ctk.CTkButton(btn_frame, text="🗑️ ลบ", command=self.delete_product, fg_color="#D22B2B", hover_color="#8B0000", height=40).grid(row=0, column=2, padx=5, sticky="ew")

    def load_products_to_treeview(self):
        """โหลดข้อมูลสินค้าทั้งหมดมาแสดงในตาราง"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        products = self.db.get_all_products()
        for p in products:
            product = p # p is already a dict
            self.tree.insert("", "end", values=(product['product_id'], product['name'], product['category'], f"{product['price']:.2f}", product['stock']))

    def on_product_select(self, event):
        """เมื่อคลิกเลือกสินค้าในตาราง ให้แสดงข้อมูลในฟอร์ม"""
        selected_items = self.tree.selection()
        if not selected_items:
            return
        
        item = self.tree.item(selected_items[0])
        self.selected_product_id = item['values'][0]
        
        product_data = self.db.get_product_by_id(self.selected_product_id)
        if not product_data:
            self.clear_form()
            return
        
        self.entries['name'].delete(0, 'end'); self.entries['name'].insert(0, product_data['name'])
        self.entries['category'].delete(0, 'end'); self.entries['category'].insert(0, product_data['category'])
        self.entries['price'].delete(0, 'end'); self.entries['price'].insert(0, product_data['price'])
        self.entries['stock'].delete(0, 'end'); self.entries['stock'].insert(0, product_data['stock'])
        self.entries['description'].delete("1.0", 'end'); self.entries['description'].insert("1.0", product_data['description'] or "")
        
        self.image_filename = product_data['image_url']
        self.image_label.configure(text=self.image_filename or "ไม่มีรูปภาพ")

    def upload_image(self):
        """เปิดหน้าต่างเพื่อเลือกไฟล์รูปภาพและคัดลอกมาเก็บในโปรเจกต์"""
        filepath = filedialog.askopenfilename(
            title="เลือกรูปภาพสินค้า", 
            filetypes=(("Image files", "*.jpg *.jpeg *.png"), ("All files", "*.*")), 
            parent=self
        )
        if not filepath:
            return

        filename = os.path.basename(filepath)
        images_dir = os.path.join(os.path.dirname(__file__), "assets", "images")
        os.makedirs(images_dir, exist_ok=True)
        
        destination_path = os.path.join(images_dir, filename)
        
        # แก้ปัญหา: เช็คว่าเป็นไฟล์เดียวกันหรือไม่ (normalize path)
        src_path = os.path.abspath(filepath).lower()
        dst_path = os.path.abspath(destination_path).lower()
        
        if src_path != dst_path:
            try:
                shutil.copy(filepath, destination_path)
                messagebox.showinfo("สำเร็จ", f"อัปโหลดรูปภาพ '{filename}' เรียบร้อย!", parent=self)
            except Exception as e:
                messagebox.showerror("ผิดพลาด", f"ไม่สามารถคัดลอกไฟล์ได้: {e}", parent=self)
                return
        else:
            messagebox.showinfo("แจ้งเตือน", "ไฟล์นี้อยู่ในโฟลเดอร์ปลายทางอยู่แล้ว", parent=self)
        
        self.image_filename = filename # เก็บแค่ชื่อไฟล์
        self.image_label.configure(text=self.image_filename)

    def save_product(self):
        """บันทึกข้อมูลสินค้า (ทั้งสร้างใหม่และอัปเดต)"""
        try:
            name = self.entries['name'].get().strip()
            category = self.entries['category'].get().strip()
            price = float(self.entries['price'].get())
            stock = int(self.entries['stock'].get())
            description = self.entries['description'].get("1.0", "end-1c").strip()

            if not all([name, category]):
                messagebox.showwarning("ข้อมูลไม่ครบ", "กรุณากรอกชื่อและหมวดหมู่สินค้า", parent=self)
                return

            # ใช้ชื่อไฟล์ที่เก็บไว้ (ถ้าไม่ได้อัปโหลดใหม่ ให้ใช้ค่าเดิม)
            image_url = self.image_filename if self.image_filename else ""

            if self.selected_product_id:
                # อัปเดตสินค้า
                self.db.update_product(
                    self.selected_product_id,
                    name=name,
                    description=description,
                    price=price,
                    stock=stock,
                    category=category,
                    image_url=image_url
                )
                messagebox.showinfo("สำเร็จ", "อัปเดตข้อมูลสินค้าเรียบร้อย!", parent=self)
            else:
                # เพิ่มสินค้าใหม่
                self.db.create_product(name, description, price, stock, category, image_url)
                messagebox.showinfo("สำเร็จ", "เพิ่มสินค้าใหม่เรียบร้อย!", parent=self)
            
            self.on_show() # รีเฟรชหน้าจอทั้งหมด
        except ValueError:
            messagebox.showerror("ผิดพลาด", "ราคาและจำนวนสต็อกต้องเป็นตัวเลขเท่านั้น", parent=self)
        except Exception as e:
            messagebox.showerror("ผิดพลาด", f"เกิดข้อผิดพลาด: {e}", parent=self)

    def delete_product(self):
        """ลบสินค้าที่เลือก"""
        if not self.selected_product_id:
            messagebox.showwarning("คำเตือน", "กรุณาเลือกสินค้าที่ต้องการลบ", parent=self)
            return
        if messagebox.askyesno("ยืนยันการลบ", "คุณแน่ใจหรือไม่ว่าต้องการลบสินค้านี้?", parent=self):
            self.db.delete_product(self.selected_product_id)
            messagebox.showinfo("สำเร็จ", "ลบสินค้าเรียบร้อยแล้ว", parent=self)
            self.on_show() # รีเฟรชหน้าจอทั้งหมด

    def clear_form(self):
        """ล้างข้อมูลในฟอร์มทั้งหมด"""
        self.selected_product_id = None
        self.image_filename = None
        self.tree.selection_remove(self.tree.selection())

        for entry in self.entries.values():
            if isinstance(entry, (ctk.CTkEntry, ctk.CTkTextbox)):
                entry.delete("1.0" if isinstance(entry, ctk.CTkTextbox) else "0", 'end')
        
        self.image_label.configure(text="ยังไม่ได้เลือกรูปภาพ")