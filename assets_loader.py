import os
from PIL import Image
import customtkinter as ctk

class Assets:
    """
    คลาสสำหรับจัดการและโหลดรูปภาพทั้งหมดของโปรแกรม (Singleton Pattern)
    โหลดเพียงครั้งเดียวตอนเปิดโปรแกรมเพื่อประสิทธิภาพสูงสุด
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load_all_assets()
        return cls._instance

    def _load_all_assets(self):
        """โหลดรูปภาพทั้งหมดที่โปรแกรมต้องใช้"""
        self.base_path = os.path.join(os.path.dirname(__file__), "assets")

        # --- Login & General UI ---
        self.logo = self._load_image("logo.png", size=(100, 100))
        self.bg_pattern = self._load_image("background_pattern.png", size=(2280, 1000))
        self.character_image = self._load_image("character_image.png", size=(350, 500))
        self.user_icon = self._load_image("user_icon.png", size=(20, 20))
        self.lock_icon = self._load_image("lock_icon.png", size=(20, 20))
        self.email_icon = self._load_image("email_icon.png", size=(20, 20))
        self.name_icon = self._load_image("name_icon.png", size=(20, 20))

        # --- Home & Product Display ---
        self.banner = self._load_image("banner.png", size=(2100, 250))
        self.search_icon = self._load_image("search_icon.png", size=(20, 20))
        self.placeholder = self._load_image("placeholder.png", size=(200, 200))
        
        # --- Cart ---
        self.cart_icon = self._load_image("cart_icon.png", size=(20, 20))
        self.trash_icon = self._load_image("trash_icon.png", size=(20, 20))

        # --- Admin ---
        self.placeholder_admin = self._load_image("placeholder.png", size=(200, 200))

        # --- Thank You Page ---
        self.thank_you_doll = self._load_image("thank_you_doll.png", size=(250, 250))

    def _load_image(self, filename, size):
        """Helper function สำหรับโหลดรูปภาพและจัดการ Error"""
        path = os.path.join(self.base_path, filename)
        try:
            return ctk.CTkImage(Image.open(path), size=size)
        except FileNotFoundError:
            print(f"Warning: Asset '{filename}' not found at '{path}'")
            # สร้างภาพว่างๆ สีเทาแทนที่ เพื่อไม่ให้โปรแกรมพัง
            placeholder = Image.new('RGB', size, color = 'lightgray')
            return ctk.CTkImage(placeholder, size=size)
        except Exception as e:
            print(f"Error loading asset '{filename}': {e}")
            return None

    def get_product_image(self, filename, size=(200, 200)):
        """
        ฟังก์ชันพิเศษสำหรับโหลดรูปสินค้าจากโฟลเดอร์ /images
        ถ้าไม่เจอ จะใช้รูป placeholder แทน
        """
        if not filename:
            return self.placeholder

        path = os.path.join(self.base_path, "images", filename)
        try:
            return ctk.CTkImage(Image.open(path), size=size)
        except:
            # หากไฟล์รูปสินค้าที่ระบุไม่มีอยู่จริง ให้ใช้ placeholder แทน
            return self.placeholder