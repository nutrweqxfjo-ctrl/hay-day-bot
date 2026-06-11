"""
إعدادات متقدمة - Advanced settings for power users
"""

class AdvancedSettings:
    """إعدادات متقدمة وتكوينات اختيارية"""
    
    # معايرة الشاشة
    SCREEN_CALIBRATION = {
        'store_button': (1230, 50),
        'field_offset': (150, 200),
        'field_spacing': (100, 100)
    }
    
    # خوارزميات التحسين
    OPTIMIZATION = {
        'enable_ocr': False,  # استخراج نصي
        'enable_template_matching': True,  # مطابقة القوالب
        'enable_neural_detection': False,  # كشف عصبي
    }
    
    # وضع اختبار
    TEST_MODE = {
        'enabled': False,
        'simulate_clicks': False,
        'save_screenshots': True,
        'verbose_logging': True
    }
    
    # استراتيجيات متقدمة
    STRATEGIES = {
        'max_profit_first': True,  # أكثر ربحية أولاً
        'time_efficient': False,   # كفاءة وقتية
        'balanced': False          # متوازن
    }
    
    # حدود الأمان
    SAFETY_LIMITS = {
        'max_clicks_per_minute': 30,
        'max_crops_per_cycle': 5,
        'min_cycle_interval': 1,
        'max_consecutive_runs': 3600  # ساعة واحدة
    }
    
    # تكوين التنبيهات
    NOTIFICATIONS = {
        'enable_sound': True,
        'enable_desktop_notifications': False,
        'log_to_file': True
    }
    
    # أوقات مخصصة
    CUSTOM_SCHEDULES = {
        'enable_scheduling': False,
        'start_time': '09:00',
        'end_time': '22:00',
        'pause_on_evening': True
    }
    
    @classmethod
    def get_setting(cls, category, key):
        """الحصول على إعداد محدد"""
        settings = getattr(cls, category, {})
        return settings.get(key, None)
    
    @classmethod
    def update_setting(cls, category, key, value):
        """تحديث إعداد محدد"""
        if hasattr(cls, category):
            settings = getattr(cls, category)
            settings[key] = value
            return True
        return False
