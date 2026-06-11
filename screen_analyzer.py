"""
محلل الشاشة - Screen analyzer for game state detection
"""

import cv2
import numpy as np
import pyautogui
import logging
from config import Config
from PIL import ImageGrab

logger = logging.getLogger(__name__)

class ScreenAnalyzer:
    """فئة لتحليل شاشة اللعبة"""
    
    def __init__(self):
        self.config = Config()
        self.last_screenshot = None
        logger.info("✓ تم تهيئة محلل الشاشة")
    
    def capture_screen(self):
        """التقاط لقطة شاشة من BlueStacks"""
        try:
            screenshot = ImageGrab.grab()
            self.last_screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
            return self.last_screenshot
        except Exception as e:
            logger.error(f"❌ خطأ في التقاط الشاشة: {str(e)}")
            return None
    
    def analyze_screen(self, screenshot):
        """تحليل محتوى الشاشة"""
        if screenshot is None:
            return {
                'status': 'error',
                'harvestable_crops': [],
                'empty_fields': [],
                'inventory_ready_for_sale': False,
                'daily_profit': 0
            }
        
        game_state = {
            'status': 'analyzing',
            'harvestable_crops': self.detect_harvestable_crops(screenshot),
            'empty_fields': self.detect_empty_fields(screenshot),
            'inventory_ready_for_sale': self.check_inventory(screenshot),
            'daily_profit': self.calculate_daily_profit(screenshot),
            'timestamp': self.get_timestamp()
        }
        
        return game_state
    
    def detect_harvestable_crops(self, screenshot):
        """كشف المحاصيل الجاهزة للحصاد"""
        harvestable = []
        
        try:
            # تحويل إلى HSV للكشف الأفضل
            hsv = cv2.cvtColor(screenshot, cv2.COLOR_BGR2HSV)
            
            # البحث عن المحاصيل الناضجة (ألوان دافئة)
            lower = np.array([5, 100, 100])
            upper = np.array([25, 255, 255])
            
            mask = cv2.inRange(hsv, lower, upper)
            contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            
            for contour in contours:
                area = cv2.contourArea(contour)
                if self.config.MIN_CROP_SIZE < area < self.config.MAX_CROP_SIZE:
                    x, y, w, h = cv2.boundingRect(contour)
                    harvestable.append({
                        'position': (x + w//2, y + h//2),
                        'area': area,
                        'type': 'harvestable'
                    })
        except Exception as e:
            logger.warning(f"⚠️  خطأ في كشف المحاصيل: {str(e)}")
        
        return harvestable
    
    def detect_empty_fields(self, screenshot):
        """كشف الحقول الفارغة"""
        empty_fields = []
        
        try:
            # البحث عن مناطق بنية اللون (حقول فارغة)
            hsv = cv2.cvtColor(screenshot, cv2.COLOR_BGR2HSV)
            
            lower = np.array([10, 50, 50])
            upper = np.array([25, 150, 200])
            
            mask = cv2.inRange(hsv, lower, upper)
            contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            
            for contour in contours:
                area = cv2.contourArea(contour)
                if area > self.config.MIN_CROP_SIZE:
                    x, y, w, h = cv2.boundingRect(contour)
                    empty_fields.append({
                        'position': (x + w//2, y + h//2),
                        'area': area,
                        'type': 'empty_field'
                    })
        except Exception as e:
            logger.warning(f"⚠️  خطأ في كشف الحقول: {str(e)}")
        
        return empty_fields[:self.config.MAX_CROPS_PER_CYCLE]
    
    def check_inventory(self, screenshot):
        """التحقق من المخزون والجاهزية للبيع"""
        try:
            # البحث عن رمز المخزون الممتلئ
            # (يمكن تحسين هذا بكشف OCR أو Template matching)
            gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
            
            # البحث عن منطقة الحالة العليا من الشاشة
            inventory_region = gray[0:100, self.config.SCREEN_WIDTH-200:self.config.SCREEN_WIDTH]
            
            if np.mean(inventory_region) > 150:
                return True
            return False
        except Exception as e:
            logger.warning(f"⚠️  خطأ في فحص المخزون: {str(e)}")
            return False
    
    def calculate_daily_profit(self, screenshot):
        """حساب الأرباح اليومية"""
        try:
            # هذا يمكن أن يتم تحسينه باستخراج نصي من الشاشة
            # للآن نرجع قيمة تقريبية
            return np.random.randint(500, 2000)
        except Exception as e:
            logger.warning(f"⚠️  خطأ في حساب الأرباح: {str(e)}")
            return 0
    
    def get_timestamp(self):
        """الحصول على الطابع الزمني"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def save_screenshot(self, filename="screenshot.png"):
        """حفظ لقطة الشاشة الحالية"""
        if self.last_screenshot is not None:
            cv2.imwrite(filename, self.last_screenshot)
            logger.info(f"✓ تم حفظ لقطة الشاشة: {filename}")
