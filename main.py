'''
تطبيق بوت هاي داي - Hay Day Bot Application
تم تحسينه بناءً على أفضل الممارسات
'''

import cv2
import numpy as np
import pyautogui
import time
from datetime import datetime
import logging
from config import Config
from crop_manager import CropManager
from screen_analyzer import ScreenAnalyzer
from store_manager import StoreManager
from game_analyzer import GameAnalyzer

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('hayday_bot.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class HayDayBot:
    
    def __init__(self):
        self.config = Config()
        self.crop_manager = CropManager()
        self.screen_analyzer = ScreenAnalyzer()
        self.store_manager = StoreManager()
        self.game_analyzer = GameAnalyzer()
        self.running = False
        self.cycle_count = 0
        logger.info('تم تهيئة نظام بوت هاي داي بنجاح')
        
    def start_bot(self):
        logger.info('='*60)
        logger.info('جاري بدء تشغيل بوت هاي داي')
        logger.info('='*60)
        self.running = True
        
        try:
            while self.running:
                self.cycle_count += 1
                logger.info(f'\nالدورة #{self.cycle_count}')
                
                if not self.game_analyzer.is_game_window_active():
                    logger.warning('نافذة اللعبة غير نشطة')
                    time.sleep(2)
                    continue
                
                screenshot = self.screen_analyzer.capture_screen()
                if screenshot is None:
                    time.sleep(1)
                    continue
                    
                game_state = self.screen_analyzer.analyze_screen(screenshot)
                
                self.process_game_state(game_state)
                
                time.sleep(self.config.CYCLE_INTERVAL)
                
        except KeyboardInterrupt:
            logger.info('تم إيقاف البوت من قبل المستخدم')
            self.stop_bot()
        except Exception as e:
            logger.error(f'حدث خطأ: {str(e)}')
            self.stop_bot()
    
    def process_game_state(self, game_state):
        timestamp = datetime.now().strftime('%H:%M:%S')
        logger.info(f'[{timestamp}] جاري معالجة حالة اللعبة')
        
        if game_state.get('harvestable_crops'):
            harvest_count = len(game_state['harvestable_crops'])
            logger.info(f'عدد المحاصيل الجاهزة للحصاد: {harvest_count}')
            
            for idx, crop in enumerate(game_state['harvestable_crops'][:self.config.MAX_CROPS_PER_CYCLE]):
                logger.info(f'حصاد المحصول {idx+1}/{min(len(game_state["harvestable_crops"]), self.config.MAX_CROPS_PER_CYCLE)}')
                self.crop_manager.harvest_crop(crop)
                time.sleep(1.0)
        
        if game_state.get('empty_fields'):
            empty_count = len(game_state['empty_fields'])
            logger.info(f'عدد الحقول الفارغة: {empty_count}')
            
            for idx, field in enumerate(game_state['empty_fields'][:self.config.MAX_CROPS_PER_CYCLE]):
                logger.info(f'زراعة الحقل {idx+1}/{min(len(game_state["empty_fields"]), self.config.MAX_CROPS_PER_CYCLE])}')
                crop_to_plant = self.crop_manager.get_best_crop_to_plant()
                self.crop_manager.plant_crop(field, crop_to_plant)
                time.sleep(1.0)
    
    def stop_bot(self):
        logger.info('جاري إيقاف البوت')
        self.running = False
        
        stats = self.crop_manager.get_statistics()
        logger.info('الإحصائيات النهائية:')
        logger.info(f'  المحاصيل المزروعة: {stats["planted_count"]}')
        logger.info(f'  المحاصيل المحصودة: {stats["harvested_count"]}')
        logger.info(f'  محاولات الحصاد: {stats["harvest_attempts"]}')
        logger.info(f'  المحاصيل النشطة: {stats["active_crops"]}')
        logger.info(f'  متوسط الربح: {stats["average_profit"]}')
        logger.info('تم إيقاف البوت بنجاح')

def main():
    print('\n')
    print('='*60)
    print('بوت هاي داي - نظام أتمتة زراعة وحصاد البيع')
    print('Hay Day Bot - Automated Farming System')
    print('='*60)
    print('\n')
    
    logger.info('='*60)
    logger.info('بدء تطبيق بوت هاي داي')
    logger.info('='*60)
    
    logger.info('\nتأكد من أن BlueStacks مفتوح والعبة نشطة')
    logger.info('سيتم البدء في 3 ثواني\n')
    time.sleep(3)
    
    bot = HayDayBot()
    bot.start_bot()

if __name__ == '__main__':
    main()
