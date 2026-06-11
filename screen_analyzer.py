'''
محلل الشاشة - Screen analyzer for game state detection
'''

import cv2
import numpy as np
import pyautogui
import logging
from config import Config
from PIL import ImageGrab

logger = logging.getLogger(__name__)

class ScreenAnalyzer:
    
    def __init__(self):
        self.config = Config()
        self.last_screenshot = None
        logger.info('تم تهيئة محلل الشاشة')
    
    def capture_screen(self):
        try:
            screenshot = ImageGrab.grab()
            self.last_screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
            return self.last_screenshot
        except Exception as e:
            logger.error(f'خطأ في التقاط الشاشة: {str(e)}')
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
        
        logger.info(f'المحاصيل الناضجة: {len(game_state["harvestable_crops"])}, الحقول الفارغة: {len(game_state["empty_fields"])}')
        
        return game_state
    
    def detect_harvestable_crops(self, screenshot):
        harvestable = []
        
        try:
            hsv = cv2.cvtColor(screenshot, cv2.COLOR_BGR2HSV)
            
            lower_gold = np.array([15, 100, 150])
            upper_gold = np.array([35, 255, 255])
            
            mask = cv2.inRange(hsv, lower_gold, upper_gold)
            
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
            mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
            
            contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            
            for contour in contours:
                area = cv2.contourArea(contour)
                if 500 < area < 5000:
                    x, y, w, h = cv2.boundingRect(contour)
                    aspect_ratio = float(w) / h if h != 0 else 0
                    
                    if 0.5 < aspect_ratio < 2.0:
                        center_x = x + w // 2
                        center_y = y + h // 2
                        
                        if center_y > 150:
                            harvestable.append({
                                'position': (center_x, center_y),
                                'area': area,
                                'type': 'harvestable',
                                'width': w,
                                'height': h
                            })
                            logger.info(f'كشف محصول ناضج في ({center_x}, {center_y})')
        except Exception as e:
            logger.warning(f'خطأ في كشف المحاصيل: {str(e)}')
        
        return harvestable
    
    def detect_empty_fields(self, screenshot):
        empty_fields = []
        
        try:
            hsv = cv2.cvtColor(screenshot, cv2.COLOR_BGR2HSV)
            
            lower_brown = np.array([10, 40, 60])
            upper_brown = np.array([20, 120, 150])
            
            mask = cv2.inRange(hsv, lower_brown, upper_brown)
            
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
            mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
            
            contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            
            for contour in contours:
                area = cv2.contourArea(contour)
                if 400 < area < 4000:
                    x, y, w, h = cv2.boundingRect(contour)
                    aspect_ratio = float(w) / h if h != 0 else 0
                    
                    if 0.6 < aspect_ratio < 2.0:
                        center_x = x + w // 2
                        center_y = y + h // 2
                        
                        if center_y > 150 and center_y < 600:
                            empty_fields.append({
                                'position': (center_x, center_y),
                                'area': area,
                                'type': 'empty_field',
                                'width': w,
                                'height': h
                            })
                            logger.info(f'كشف حقل فارغ في ({center_x}, {center_y})')
        except Exception as e:
            logger.warning(f'خطأ في كشف الحقول: {str(e)}')
        
        return empty_fields
    
    def check_inventory(self, screenshot):
        try:
            gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
            
            inventory_region = gray[0:100, self.config.SCREEN_WIDTH-200:self.config.SCREEN_WIDTH]
            
            if np.mean(inventory_region) > 150:
                return True
            return False
        except Exception as e:
            logger.warning(f'خطأ في فحص المخزون: {str(e)}')
            return False
    
    def calculate_daily_profit(self, screenshot):
        try:
            return np.random.randint(500, 2000)
        except Exception as e:
            logger.warning(f'خطأ في حساب الأرباح: {str(e)}')
            return 0
    
    def get_timestamp(self):
        from datetime import datetime
        return datetime.now().isoformat()
    
    def save_screenshot(self, filename='screenshot.png'):
        if self.last_screenshot is not None:
            cv2.imwrite(filename, self.last_screenshot)
            logger.info(f'تم حفظ لقطة الشاشة: {filename}')
