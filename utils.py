import re
import bcrypt

def validate_email(email):
    """ตรวจสอบรูปแบบอีเมล"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_phone(phone):
    """ตรวจสอบรูปแบบเบอร์โทร (รองรับรูปแบบไทย)"""
    pattern = r'^0\d{1,2}-?\d{3}-?\d{4}$'
    return re.match(pattern, phone) is not None

def validate_password(password):
    """ตรวจสอบความแข็งแกร่งของรหัสผ่าน (ขั้นต่ำ 6 ตัวอักษร)"""
    return len(password) >= 6

def hash_password(password):
    """เข้ารหัสรหัสผ่าน"""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

def check_password(password, hashed):
    """เช็ครหัสผ่าน"""
    return bcrypt.checkpw(password.encode(), hashed)

def format_currency(amount):
    """จัดรูปแบบเงิน"""
    return f"฿{amount:,.2f}"

def format_datetime(dt_string):
    """จัดรูปแบบวันที่-เวลา"""
    from datetime import datetime
    try:
        dt = datetime.strptime(dt_string, "%Y-%m-%d %H:%M:%S")
        return dt.strftime("%d/%m/%Y %H:%M")
    except:
        return dt_string

class Cart:
    """คลาสจัดการตะกร้าสินค้า"""
    def __init__(self):
        self.items = {}  # {product_id: {'product': product_dict, 'quantity': int}}
    
    def add_item(self, product, quantity=1):
        """เพิ่มสินค้าในตะกร้า"""
        product_id = product['product_id']
        if product_id in self.items:
            self.items[product_id]['quantity'] += quantity
        else:
            self.items[product_id] = {
                'product': product,
                'quantity': quantity
            }
    
    def remove_item(self, product_id):
        """ลบสินค้าออกจากตะกร้า"""
        if product_id in self.items:
            del self.items[product_id]
    
    def update_quantity(self, product_id, quantity):
        """อัพเดทจำนวนสินค้า"""
        if product_id in self.items:
            if quantity <= 0:
                self.remove_item(product_id)
            else:
                self.items[product_id]['quantity'] = quantity
    
    def get_total(self):
        """คำนวณราคารวม"""
        total = 0
        for item in self.items.values():
            total += item['product']['price'] * item['quantity']
        return total
    
    def get_item_count(self):
        """นับจำนวนสินค้าในตะกร้า"""
        return sum(item['quantity'] for item in self.items.values())
    
    def clear(self):
        """ล้างตะกร้า"""
        self.items = {}
    
    def get_items_for_order(self):
        """แปลงข้อมูลตะกร้าสำหรับสร้าง order"""
        order_items = []
        for item in self.items.values():
            order_items.append({
                'product_id': item['product']['product_id'],
                'quantity': item['quantity'],
                'price': item['product']['price']
            })
        return order_items

def show_message(parent, title, message, type="info"):
    """แสดงข้อความแจ้งเตือน"""
    import customtkinter as ctk
    from tkinter import messagebox
    
    if type == "info":
        messagebox.showinfo(title, message, parent=parent)
    elif type == "warning":
        messagebox.showwarning(title, message, parent=parent)
    elif type == "error":
        messagebox.showerror(title, message, parent=parent)

def confirm_dialog(parent, title, message):
    """แสดง dialog ยืนยัน"""
    from tkinter import messagebox
    return messagebox.askyesno(title, message, parent=parent)