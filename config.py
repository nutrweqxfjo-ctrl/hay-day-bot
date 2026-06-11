"""
ملف الإعدادات - Configuration file for Hay Day Bot
"""

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """فئة الإعدادات الرئيسية"""
    
    # إعدادات BlueStacks
    BLUESTACKS_WINDOW_TITLE = "BlueStacks"
    SCREEN_WIDTH = 1280
    SCREEN_HEIGHT = 720
    
    # إعدادات الدورة الزمنية
    CYCLE_INTERVAL = 2  # ثانية
    HARVEST_CHECK_INTERVAL = 60  # كل دقيقة واحدة
    PLANT_CHECK_INTERVAL = 120  # كل دقيقتين
    SELL_CHECK_INTERVAL = 300  # كل 5 دقائق
    
    # إعدادات المحاصيل
    CROPS_CONFIG = {
        'wheat': {
            'name': 'القمح',
            'growth_time': 120,  # ثانية
            'profit': 50,
            'color_range': ((80, 120, 40), (120, 150, 80))  # BGR
        },
        'corn': {
            'name': 'الذرة',
            'growth_time': 180,
            'profit': 75,
            'color_range': ((100, 140, 60), (140, 170, 100))
        },
        'carrot': {
            'name': 'الجزر',
            'growth_time': 240,
            'profit': 100,
            'color_range': ((50, 100, 150), (90, 140, 190))
        },
        'tomato': {
            'name': 'الطماطم',
            'growth_time': 300,
            'profit': 125,
            'color_range': ((30, 80, 200), (70, 120, 240))
        }
    }
    
    # إعدادات الكشف البصري
    DETECTION_THRESHOLD = 0.7
    MIN_CROP_SIZE = 20  # pixels
    MAX_CROP_SIZE = 100  # pixels
    
    # إعدادات الفأرة واللوحة
    MOUSE_SPEED = 0.5
    CLICK_DELAY = 0.3
    
    # إعدادات التخزين والبيع
    MIN_ITEMS_TO_SELL = 10
    SELL_PRICE_MULTIPLIER = 1.2
    
    # إعدادات السجل
    LOG_LEVEL = 'INFO'
    LOG_FILE = 'hayday_bot.log'
    
    # حدود الأداء
    MAX_CROPS_PER_CYCLE = 5
    MAX_SELLS_PER_CYCLE = 3
    
    @classmethod
    def get_crop_config(cls, crop_name):
        """الحصول على إعدادات محصول معين"""
        return cls.CROPS_CONFIG.get(crop_name, None)
    
    @classmethod
    def get_all_crops(cls):
        """الحصول على قائمة كل المحاصيل"""
        return list(cls.CROPS_CONFIG.keys())
