"""
ملف الإعدادات المعدل - Configuration file for Hay Day Bot (Yusuf Edition)
"""

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """فئة الإعدادات الرئيسية"""
    
    # إعدادات BlueStacks (تأكد أن اسم النافذة في المحاكي يطابق هذا الاسم تماماً)
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
            'color_range': ((18, 140, 140), (24, 255, 255))  # تم تضييقه للون الذهبي الخالص للمحصول
        },
        'corn': {
            'name': 'الذرة',
            'growth_time': 180,
            'profit': 75,
            'color_range': ((10, 100, 100), (17, 255, 255))
        }
    }
    
    # 🔴 تم تعديل الإعدادات البصرية لتتوافق مع الكتل الكبيرة من الحقول في مزرعتك
    DETECTION_THRESHOLD = 0.85
    MIN_CROP_SIZE = 150      # تجاهل النقاط الصغيرة جداً (الضوضاء)
    MAX_CROP_SIZE = 900000   # السماح بكشف شريط القمح الطويل بالكامل في مزارع لفل 18
    
    # إعدادات الفأرة واللوحة
    MOUSE_SPEED = 0.3
    CLICK_DELAY = 0.2
    
    # إعدادات التخزين والبيع
    MIN_ITEMS_TO_SELL = 10
    SELL_PRICE_MULTIPLIER = 1.2
    
    # إعدادات السجل
    LOG_LEVEL = 'INFO'
    LOG_FILE = 'hayday_bot.log'
    
    # حدود الأداء
    MAX_CROPS_PER_CYCLE = 15
    MAX_SELLS_PER_CYCLE = 3
    
    @classmethod
    def get_crop_config(cls, crop_name):
        return cls.CROPS_CONFIG.get(crop_name, None)
    
    @classmethod
    def get_all_crops(cls):
        return list(cls.CROPS_CONFIG.keys())
