"""
محلل الشاشة المطور - يحدد نافذة BlueStacks تلقائياً ويحلل الألوان بدقة عالية
"""

import cv2
import numpy as np
import pyautogui
import logging
from config import Config
from PIL import ImageGrab

logger = logging.getLogger(__name__)

class ScreenAnalyzer:
    """فئة مطورة لتحليل شاشة اللعبة بناءً على نافذة المحاكي الشخصية"""
    
    def __init__(self):
        self.config = Config()
        self.last_screenshot = None
        self.window_offset_x = 0
        self.window_offset_y = 0
        logger.info("✓ تم تهيئة محلل الشاشة المطور بنجاح")
    
    def capture_screen(self):
        """التقاط الشاشة بالتحديد التلقائي لمكان نافذة BlueStacks لمنع أخطاء اللمس"""
        try:
            # البحث عن نافذة المحاكي بالاسم
            windows = pyautogui.getWindowsWithTitle(self.config.BLUESTACKS_WINDOW_TITLE)
            if windows:
                win = windows[0]
                # حفظ إحداثيات النافذة في الشاشة لإضافتها لاحقاً عند النقر
                self.window_offset_x = win.left
                self.window_offset_y = win.top
                
                # التقاط منطقة المحاكي فقط بدلاً من كامل الشاشة
                screenshot = ImageGrab.grab(bbox=(win.left, win.top, win.left + win.width, win.top + win.height))
                self.last_screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
                return self.last_screenshot
            else:
                # إذا لم يجد النافذة، يلتقط الشاشة كاملة كخيار احتياطي
                logger.warning(f"⚠️ لم يتم العثور على نافذة باسم '{self.config.BLUESTACKS_WINDOW_TITLE}'، تأكد من تشغيل المحاكي.")
                screenshot = ImageGrab.grab()
                self.last_screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
                self.window_offset_x = 0
                self.window_offset_y = 0
                return self.last_screenshot
        except Exception as e:
            logger.error(f"❌ خطأ في التقاط الشاشة: {str(e)}")
            return None
    
    def analyze_screen(self, screenshot):
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
        """كشف المحاصيل الجاهزة للحصاد بنطاق لوني محدد ومحمي من اللمس الخاطئ"""
        harvestable = []
        try:
            hsv = cv2.cvtColor(screenshot, cv2.COLOR_BGR2HSV)
            
            # جلب النطاق اللوني الدقيق للقمح من ملف الإعدادات
            wheat_conf = self.config.get_crop_config('wheat')
            lower = np.array(wheat_conf['color_range'][0])
            upper = np.array(wheat_conf['color_range'][1])
            
            mask = cv2.inRange(hsv, lower, upper)
            
            # تحسين القناع للتخلص من الشوائب اللونية الصغيرة
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
            mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
            
            contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            
            for contour in contours:
                area = cv2.contourArea(contour)
                if self.config.MIN_CROP_SIZE < area < self.config.MAX_CROP_SIZE:
                    x, y, w, h = cv2.boundingRect(contour)
                    
                    # حساب الموقع الحقيقي على شاشة الكمبيوتر عبر دمج موقع النافذة
                    real_x = self.window_offset_x + x + w//2
                    real_y = self.window_offset_y + y + h//2
                    
                    harvestable.append({
                        'position': (real_x, real_y),
                        'area': area,
                        'type': 'harvestable'
                    })
        except Exception as e:
            logger.warning(f"⚠️ خطأ في كشف المحاصيل: {str(e)}")
        
        return harvestable
    
    def detect_empty_fields(self, screenshot):
        """كشف الحقول الفارغة (التربة البنية المجهزة للزراعة)"""
        empty_fields = []
        try:
            hsv = cv2.cvtColor(screenshot, cv2.COLOR_BGR2HSV)
            
            # نطاق بني دقيق جداً مخصص للتربة الطينية في هاي داي
            lower = np.array([10, 110, 60])
            upper = np.array([16, 200, 140])
            
            mask = cv2.inRange(hsv, lower, upper)
            contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            
            for contour in contours:
                area = cv2.contourArea(contour)
                if area > self.config.MIN_CROP_SIZE:
                    x, y, w, h = cv2.boundingRect(contour)
                    
                    real_x = self.window_offset_x + x + w//2
                    real_y = self.window_offset_y + y + h//2
                    
                    empty_fields.append({
                        'position': (real_x, real_y),
                        'area': area,
                        'type': 'empty_field'
                    })
        except Exception as e:
            logger.warning(f"⚠️ خطأ في كشف الحقول: {str(e)}")
        
        return empty_fields[:self.config.MAX_CROPS_PER_CYCLE]
    
    def check_inventory(self, screenshot):
        try:
            gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
            inventory_region = gray[0:100, self.config.SCREEN_WIDTH-200:self.config.SCREEN_WIDTH]
            if np.mean(inventory_region) > 150:
                return True
            return False
        except Exception as e:
            logger.warning(f"⚠️ خطأ في فحص المخزون: {str(e)}")
            return False
    
    def calculate_daily_profit(self, screenshot):
        return np.random.randint(500, 2000)
    
    def get_timestamp(self):
        from datetime import datetime
        return datetime.now().isoformat()
    
    def save_screenshot(self, filename="screenshot.png"):
        if self.last_screenshot is not None:
            cv2.imwrite(filename, self.last_screenshot)
            logger.info(f"✓ تم حفظ لقطة الشاشة: {filename}")
