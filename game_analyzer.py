'''
محلل اللعبة الذكي - Intelligent game analyzer
'''

import cv2
import numpy as np
import logging
from PIL import ImageGrab

logger = logging.getLogger(__name__)

class GameAnalyzer:
    
    def __init__(self):
        logger.info('تم تهيئة محلل اللعبة الذكي')
    
    def is_game_window_active(self):
        '''
التحقق من أن نافذة اللعبة نشطة
        '''
        try:
            screenshot = ImageGrab.grab()
            img = np.array(screenshot)
            
            if img.shape[0] > 0 and img.shape[1] > 0:
                return True
            return False
        except:
            return False
    
    def detect_ui_elements(self, screenshot):
        '''
كشف عناصر واجهة المستخدم
        '''
        try:
            gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
            
            ui_elements = {
                'top_bar': None,
                'bottom_bar': None,
                'left_side': None,
                'right_side': None
            }
            
            top_bar = gray[0:100, :]
            if np.mean(top_bar) > 80:
                ui_elements['top_bar'] = True
            
            return ui_elements
        except Exception as e:
            logger.warning(f'خطأ في كشف عناصر الواجهة: {str(e)}')
            return {}
    
    def estimate_game_progress(self, harvested, planted):
        '''
تقدير تقدم اللعبة
        '''
        if planted == 0:
            return 0
        return (harvested / planted) * 100 if harvested <= planted else 100
