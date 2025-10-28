from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List

@dataclass
class User:
    user_id: int
    username: str
    email: str
    full_name: str
    phone: Optional[str] = None
    address: Optional[str] = None
    role: str = 'customer'
    created_at: Optional[str] = None
    
    @classmethod
    def from_dict(cls, data):
        # ฟังก์ชันนี้ยังคงจำเป็นสำหรับ main.py
        return cls(
            user_id=data['user_id'],
            username=data['username'],
            email=data['email'],
            full_name=data['full_name'],
            phone=data.get('phone'),
            address=data.get('address'),
            role=data.get('role', 'customer'),
            created_at=data.get('created_at')
        )
    
    def is_admin(self) -> bool:
        return self.role == 'admin'

@dataclass
class Product:
    product_id: int
    name: str
    description: str
    price: float
    stock: int
    category: str
    image_url: Optional[str] = None
    created_at: Optional[str] = None
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            product_id=data['product_id'],
            name=data['name'],
            description=data.get('description'),
            price=data['price'],
            stock=data['stock'],
            category=data.get('category'),
            image_url=data.get('image_url'),
            created_at=data.get('created_at')
        )
    
    def is_available(self) -> bool:
        return self.stock > 0

    def format_price(self) -> str:
        return f"฿{self.price:,.2f}"
    
    def get_stock_status(self) -> tuple[str, str]:
        if self.stock > 10:
            return f"📦 คงเหลือ {self.stock}", "#32CD32" # Green
        elif self.stock > 0:
            return f"📦 เหลือเพียง {self.stock} ชิ้น", "#FFA500" # Orange
        else:
            return "❌ สินค้าหมด", "#D22B2B" # Red

@dataclass
class Order:
    order_id: int
    user_id: int
    total_amount: float
    status: str
    created_at: str
    shipping_address: str
    items: Optional[str] = None

    @classmethod
    def from_dict(cls, data):
        return cls(
            order_id=data['order_id'],
            user_id=data['user_id'],
            total_amount=data['total_amount'],
            status=data.get('status', 'pending'),
            created_at=data['created_at'],
            shipping_address=data.get('shipping_address', ''),
            items=data.get('items')
        )

    def format_date(self) -> str:
        try:
            return datetime.fromisoformat(self.created_at).strftime("%d/%m/%Y %H:%M")
        except:
            return self.created_at

    def format_total(self) -> str:
        return f"฿{self.total_amount:,.2f}"

    def get_status_text(self) -> str:
        return {"pending": "รอดำเนินการ", "shipped": "กำลังจัดส่ง", "delivered": "จัดส่งสำเร็จ", "cancelled": "ยกเลิก"}.get(self.status, "ไม่ทราบสถานะ")

    def get_status_color(self) -> str:
        return {"pending": "#FFC107", "shipped": "#17A2B8", "delivered": "#28A745", "cancelled": "#DC3545"}.get(self.status, "gray")

# --- Session Management ---
class Session:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Session, cls).__new__(cls)
            cls._instance.current_user = None
        return cls._instance

    
    def login(self, user: User):
        """
        แก้ไขให้รับ User object เข้ามาโดยตรง ไม่ต้องแปลงซ้ำ
        """
        self.current_user = user
    

    def logout(self):
        self.current_user = None
        
    def is_logged_in(self) -> bool:
        return self.current_user is not None
        
    def is_admin(self) -> bool:
        return self.is_logged_in() and self.current_user.is_admin()

# --- Cart Management ---
@dataclass
class CartItem:
    product: Product
    quantity: int

    def get_total_price(self) -> float:
        return self.product.price * self.quantity
    
    def format_total_price(self) -> str:
        return f"฿{self.get_total_price():,.2f}"

class Cart:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Cart, cls).__new__(cls)
            cls._instance.items = {}
        return cls._instance

    def add_item(self, product: Product, quantity: int = 1):
        if product.product_id in self.items:
            self.items[product.product_id].quantity += quantity
        else:
            self.items[product.product_id] = CartItem(product=product, quantity=quantity)

    def remove_item(self, product_id: int):
        if product_id in self.items:
            del self.items[product_id]

    def update_quantity(self, product_id: int, quantity: int):
        if product_id in self.items:
            if quantity > 0:
                self.items[product_id].quantity = quantity
            else:
                self.remove_item(product_id)

    def get_items(self) -> List[CartItem]:
        return list(self.items.values())

    def get_total_price(self) -> float:
        return sum(item.get_total_price() for item in self.get_items())
    
    def format_total_price(self) -> str:
        return f"฿{self.get_total_price():,.2f}"
        
    def clear(self):
        self.items = {}