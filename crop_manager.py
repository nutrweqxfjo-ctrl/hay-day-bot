'''
مدير المحاصيل المحسّن - Crop manager with proper harvesting
'''

import pyautogui
import time
import logging
from config import Config

logger = logging.getLogger(__name__)

class CropManager:
    
    def __init__(self):
        self.config = Config()
        self.planted_crops = {}
        self.harvested_count = 0
        self.planted_count = 0
        logger.info('تم تهيئة مدير المحاصيل')
    
    def plant_crop(self, field, crop_type):
        try:
            x, y = field['position']
            
            logger.info(f'جاري زراعة {crop_type} في الموضع ({x}, {y})')
            
            pyautogui.moveTo(x, y, duration=0.3)
            time.sleep(0.2)
            pyautogui.click(x, y)
            time.sleep(self.config.CLICK_DELAY)
            
            self.select_crop_from_menu(crop_type)
            time.sleep(0.5)
            
            pyautogui.press('enter')
            time.sleep(self.config.CLICK_DELAY)
            
            self.planted_crops[field['position']] = {
                'type': crop_type,
                'planted_time': time.time(),
                'growth_time': self.config.CROPS_CONFIG[crop_type]['growth_time']
            }
            self.planted_count += 1
            
            logger.info(f'تم زراعة {crop_type} بنجاح (الإجمالي: {self.planted_count})')
            return True
            
        except Exception as e:
            logger.error(f'خطأ في زراعة المحصول: {str(e)}')
            return False
    
    def harvest_crop(self, crop):
        try:
            x, y = crop['position']
            
            logger.info(f'جاري حصاد المحصول من الموضع ({x}, {y})')
            
            pyautogui.moveTo(x, y, duration=0.2)
            time.sleep(0.3)
            
            pyautogui.click(x, y)
            time.sleep(0.3)
            
            logger.info('جاري سحب المعول على المحصول للحصاد')
            
            offset_x = 20
            offset_y = 20
            
            pyautogui.drag(offset_x, offset_y, duration=0.5)
            
            time.sleep(0.3)
            
            self.harvested_count += 1
            logger.info(f'تم الحصاد بنجاح (الإجمالي: {self.harvested_count})')
            
            if crop['position'] in self.planted_crops:
                del self.planted_crops[crop['position']]
            
            return True
            
        except Exception as e:
            logger.error(f'خطأ في الحصاد: {str(e)}')
            return False
    
    def select_crop_from_menu(self, crop_type):
        try:
            crop_positions = {
                'wheat': (300, 400),
                'corn': (400, 400),
                'carrot': (500, 400),
                'tomato': (600, 400)
            }
            
            if crop_type in crop_positions:
                x, y = crop_positions[crop_type]
                pyautogui.moveTo(x, y, duration=0.2)
                time.sleep(0.1)
                pyautogui.click(x, y)
                time.sleep(self.config.CLICK_DELAY)
                logger.info(f'تم اختيار {crop_type} من القائمة')
                return True
            else:
                logger.warning(f'نوع المحصول غير معروف: {crop_type}')
                return False
                
        except Exception as e:
            logger.error(f'خطأ في اختيار المحصول: {str(e)}')
            return False
    
    def get_best_crop_to_plant(self):
        best_crop = 'wheat'
        best_ratio = 0
        
        for crop_name, crop_info in self.config.CROPS_CONFIG.items():
            ratio = crop_info['profit'] / crop_info['growth_time']
            
            if ratio > best_ratio:
                best_ratio = ratio
                best_crop = crop_name
        
        logger.info(f'تم اختيار {best_crop} كأفضل محصول للزراعة')
        return best_crop
    
    def get_crop_status(self, position):
        if position in self.planted_crops:
            crop_data = self.planted_crops[position]
            elapsed_time = time.time() - crop_data['planted_time']
            remaining_time = crop_data['growth_time'] - elapsed_time
            
            return {
                'type': crop_data['type'],
                'elapsed_time': elapsed_time,
                'remaining_time': max(0, remaining_time),
                'is_ready': remaining_time <= 0
            }
        return None
    
    def get_statistics(self):
        return {
            'planted_count': self.planted_count,
            'harvested_count': self.harvested_count,
            'active_crops': len(self.planted_crops),
            'average_profit': (self.harvested_count * 75)
        }
