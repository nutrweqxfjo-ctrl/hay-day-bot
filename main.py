"""
Hay Day Bot - نظام أتمتة شامل للزراعة والحصاد والبيع
Automated system for planting, harvesting, and selling crops in Hay Day
"""

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

# تكوين نظام السجلات
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('hayday_bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class HayDayBot:
    """فئة رئيسية لإدارة روبوت Hay Day"""
    
    def __init__(self):
        self.config = Config()
        self.crop_manager = CropManager()
        self.screen_analyzer = ScreenAnalyzer()
        self.store_manager = StoreManager()
        self.running = False
        logger.info("✓ تم تهيئة نظام Hay Day Bot بنجاح")
        
    def start_bot(self):
        """بدء تشغيل الروبوت"""
        logger.info("═" * 60)
        logger.info("🚀 جاري بدء تشغيل Hay Day Bot...")
        logger.info("═" * 60)
        self.running = True
        
        try:
            while self.running:
                # تحليل الشاشة الحالية
                screenshot = self.screen_analyzer.capture_screen()
                game_state = self.screen_analyzer.analyze_screen(screenshot)
                
                # إجراء العمليات بناءً على حالة اللعبة
                self.process_game_state(game_state)
                
                # انتظار قبل التحديث التالي
                time.sleep(self.config.CYCLE_INTERVAL)
                
        except KeyboardInterrupt:
            logger.info("\n⏹️  تم إيقاف الروبوت بواسطة المستخدم")
            self.stop_bot()
        except Exception as e:
            logger.error(f"❌ حدث خطأ: {str(e)}")
            self.stop_bot()
    
    def process_game_state(self, game_state):
        """معالجة حالة اللعبة"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        logger.info(f"[{timestamp}] 🎮 معالجة حالة اللعبة...")
        
        # التحقق من المحاصيل الجاهزة للحصاد
        if game_state.get('harvestable_crops'):
            harvest_count = len(game_state['harvestable_crops'])
            logger.info(f"🌾 عدد المحاصيل الجاهزة للحصاد: {harvest_count}")
            for crop in game_state['harvestable_crops']:
                self.crop_manager.harvest_crop(crop)
                time.sleep(0.5)
        
        # التحقق من الحقول الفارغة للزراعة
        if game_state.get('empty_fields'):
            empty_count = len(game_state['empty_fields'])
            logger.info(f"🌱 عدد الحقول الفارغة: {empty_count}")
            for field in game_state['empty_fields']:
                crop_to_plant = self.crop_manager.get_best_crop_to_plant()
                self.crop_manager.plant_crop(field, crop_to_plant)
                time.sleep(0.5)
        
        # بيع المحاصيل في ��لمتجر
        if game_state.get('inventory_ready_for_sale'):
            logger.info("💰 جاري بيع المحاصيل في المتجر...")
            self.store_manager.sell_crops()
            time.sleep(1)
        
        # عرض إحصائيات
        logger.info(f"📊 الأرباح اليومية: {game_state.get('daily_profit', 0)} عملة")
    
    def stop_bot(self):
        """إيقاف تشغيل الروبوت"""
        logger.info("\n⏹️  جاري إيقاف الروبوت...")
        self.running = False
        logger.info("✓ تم إيقاف الروبوت بنجاح")

def main():
    """الدالة الرئيسية"""
    print("\n")
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 58 + "║")
    print("║" + "  🌾 Hay Day Bot - نظام الأتمتة الشامل 🌾".center(58) + "║")
    print("║" + "  Automated Farming & Trading System".center(58) + "║")
    print("║" + " " * 58 + "║")
    print("╚" + "═" * 58 + "╝")
    print("\n")
    
    logger.info("═" * 60)
    logger.info("تطبيق Hay Day Bot")
    logger.info("═" * 60)
    
    # التحقق من BlueStacks
    logger.info("\n📱 تأكد من أن BlueStacks مفتوح والعبة نشطة...")
    logger.info("⏳ سيتم البدء في 3 ثوانٍ...\n")
    time.sleep(3)
    
    # إنشاء وبدء الروبوت
    bot = HayDayBot()
    bot.start_bot()

if __name__ == "__main__":
    main()
