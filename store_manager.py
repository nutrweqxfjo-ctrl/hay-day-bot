"""
مدير المتجر - Store and trading management
"""

import pyautogui
import time
import logging
from config import Config

logger = logging.getLogger(__name__)

class StoreManager:
    """فئة لإدارة المتجر والبيع والتداول"""
    
    def __init__(self):
        self.config = Config()
        self.total_sold = 0
        self.total_profit = 0
        self.sell_history = []
        logger.info("✓ تم تهيئة مدير المتجر")
    
    def sell_crops(self):
        """بيع المحاصيل في المتجر"""
        try:
            logger.info("💰 جاري فتح المتجر...")
            
            # البحث عن زر المتجر
            store_button = self.find_store_button()
            
            if store_button:
                pyautogui.click(*store_button)
                time.sleep(1)
                
                # بيع العناصر
                sold_items = self.sell_all_items()
                self.total_sold += sold_items
                
                logger.info(f"✓ تم بيع {sold_items} عنصر بنجاح")
                
                # إغلاق المتجر
                pyautogui.press('escape')
                time.sleep(0.5)
                
                return True
            else:
                logger.warning("⚠️  لم يتم العثور على زر المتجر")
                return False
                
        except Exception as e:
            logger.error(f"❌ خطأ في البيع: {str(e)}")
            return False
    
    def find_store_button(self):
        """البحث عن زر المتجر على الشاشة"""
        try:
            # الموضع التقريبي لزر المتجر
            # يمكن تحسينه باستخدام Template Matching
            store_button_position = (self.config.SCREEN_WIDTH - 100, 50)
            
            logger.info(f"🔍 البحث عن زر المتجر في الموضع {store_button_position}")
            return store_button_position
            
        except Exception as e:
            logger.error(f"❌ خطأ في البحث عن زر المتجر: {str(e)}")
            return None
    
    def sell_all_items(self):
        """بيع جميع العناصر المتاحة"""
        items_sold = 0
        
        try:
            # الضغط على "بيع الكل" أو بيع العناصر واحدة تلو الأخرى
            for _ in range(self.config.MAX_SELLS_PER_CYCLE):
                # البحث عن عنصر قابل للبيع
                item_position = self.find_sellable_item()
                
                if item_position:
                    pyautogui.click(*item_position)
                    time.sleep(0.3)
                    
                    # تأكيد البيع
                    pyautogui.press('enter')
                    time.sleep(0.3)
                    
                    items_sold += 1
                else:
                    break
            
            logger.info(f"💵 تم بيع {items_sold} عناصر")
            return items_sold
            
        except Exception as e:
            logger.error(f"❌ خطأ في بيع العناصر: {str(e)}")
            return items_sold
    
    def find_sellable_item(self):
        """البحث عن عنصر قابل للبيع"""
        try:
            # البحث في منطقة المخزون
            inventory_start_x = 100
            inventory_start_y = 200
            
            # يمكن تحسينه بكشف بصري حقيقي
            possible_positions = [
                (inventory_start_x + 50, inventory_start_y + 50),
                (inventory_start_x + 150, inventory_start_y + 50),
                (inventory_start_x + 250, inventory_start_y + 50),
            ]
            
            # إرجاع أول موضع متاح
            return possible_positions[0] if possible_positions else None
            
        except Exception as e:
            logger.error(f"❌ خطأ في البحث عن عنصر للبيع: {str(e)}")
            return None
    
    def calculate_profit(self, crop_type, quantity):
        """حساب الربح المتوقع"""
        crop_config = self.config.get_crop_config(crop_type)
        
        if crop_config:
            base_profit = crop_config['profit']
            total_profit = base_profit * quantity * self.config.SELL_PRICE_MULTIPLIER
            return int(total_profit)
        
        return 0
    
    def add_to_sell_history(self, item_type, quantity, profit):
        """إضافة عملية بيع إلى السجل"""
        self.sell_history.append({
            'item_type': item_type,
            'quantity': quantity,
            'profit': profit,
            'timestamp': time.time()
        })
        self.total_profit += profit
    
    def get_store_statistics(self):
        """الحصول على إحصائيات المتجر"""
        return {
            'total_sold': self.total_sold,
            'total_profit': self.total_profit,
            'sell_history_count': len(self.sell_history),
            'average_profit_per_sale': self.total_profit // len(self.sell_history) if self.sell_history else 0
        }
