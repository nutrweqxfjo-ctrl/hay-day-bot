'''
إعدادات متقدمة - Advanced settings for power users
'''

class AdvancedSettings:
    
    SCREEN_CALIBRATION = {
        'store_button': (1230, 50),
        'field_offset': (150, 200),
        'field_spacing': (100, 100)
    }
    
    OPTIMIZATION = {
        'enable_ocr': False,
        'enable_template_matching': True,
        'enable_neural_detection': False,
    }
    
    TEST_MODE = {
        'enabled': False,
        'simulate_clicks': False,
        'save_screenshots': True,
        'verbose_logging': True
    }
    
    STRATEGIES = {
        'max_profit_first': True,
        'time_efficient': False,
        'balanced': False
    }
    
    SAFETY_LIMITS = {
        'max_clicks_per_minute': 30,
        'max_crops_per_cycle': 5,
        'min_cycle_interval': 1,
        'max_consecutive_runs': 3600
    }
    
    NOTIFICATIONS = {
        'enable_sound': True,
        'enable_desktop_notifications': False,
        'log_to_file': True
    }
    
    CUSTOM_SCHEDULES = {
        'enable_scheduling': False,
        'start_time': '09:00',
        'end_time': '22:00',
        'pause_on_evening': True
    }
    
    @classmethod
    def get_setting(cls, category, key):
        settings = getattr(cls, category, {})
        return settings.get(key, None)
    
    @classmethod
    def update_setting(cls, category, key, value):
        if hasattr(cls, category):
            settings = getattr(cls, category)
            settings[key] = value
            return True
        return False
