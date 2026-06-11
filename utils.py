"""
دوال مساعدة - Utility functions
"""

import os
import json
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class Utils:
    """فئة دوال مساعدة"""
    
    @staticmethod
    def create_log_directory():
        """إنشاء مجلد السجلات إذا لم يكن موجوداً"""
        if not os.path.exists('logs'):
            os.makedirs('logs')
            logger.info("✓ تم إنشاء مجلد السجلات")
    
    @staticmethod
    def save_statistics(stats, filename='statistics.json'):
        """حفظ الإحصائيات إلى ملف JSON"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(stats, f, indent=4, ensure_ascii=False)
            logger.info(f"✓ تم حفظ الإحصائيات في {filename}")
            return True
        except Exception as e:
            logger.error(f"❌ خطأ في حفظ الإحصائيات: {str(e)}")
            return False
    
    @staticmethod
    def load_statistics(filename='statistics.json'):
        """تحميل الإحصائيات من ملف JSON"""
        try:
            if os.path.exists(filename):
                with open(filename, 'r', encoding='utf-8') as f:
                    stats = json.load(f)
                logger.info(f"✓ تم تحميل الإحصائيات من {filename}")
                return stats
        except Exception as e:
            logger.error(f"❌ خطأ في تحميل الإحصائيات: {str(e)}")
        
        return {}
    
    @staticmethod
    def format_time(seconds):
        """تنسيق الثواني إلى صيغة قابلة للقراءة"""
        if seconds < 60:
            return f"{int(seconds)}s"
        elif seconds < 3600:
            return f"{int(seconds // 60)}m {int(seconds % 60)}s"
        else:
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            return f"{int(hours)}h {int(minutes)}m"
    
    @staticmethod
    def format_currency(amount):
        """تنسيق المبالغ المالية"""
        if amount >= 1000000:
            return f"${amount / 1000000:.1f}M"
        elif amount >= 1000:
            return f"${amount / 1000:.1f}K"
        else:
            return f"${amount}"
    
    @staticmethod
    def get_current_time():
        """الحصول على الوقت الحالي بصيغة منسقة"""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    @staticmethod
    def create_report(crop_stats, store_stats):
        """إنشاء تقرير شامل"""
        report = {
            'timestamp': Utils.get_current_time(),
            'crops': crop_stats,
            'store': store_stats,
            'summary': {
                'total_profit': store_stats.get('total_profit', 0),
                'total_harvested': crop_stats.get('harvested_count', 0),
                'total_planted': crop_stats.get('planted_count', 0)
            }
        }
        return report
    
    @staticmethod
    def print_banner(text):
        """طباعة لافتة مزخرفة"""
        border = "═" * (len(text) + 4)
        print(f"╔{border}╗")
        print(f"║ {text} ║")
        print(f"╚{border}╝")
