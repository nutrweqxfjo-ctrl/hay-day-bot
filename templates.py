'''
ملف القوالب - Template images for crop detection
هذا الملف يحتوي على البيانات المشفرة للصور المستخدمة في الكشف
'''

import cv2
import numpy as np
from base64 import b64decode

class Templates:
    
    @staticmethod
    def get_ripe_crop_template():
        '''
المحصول الناضج الأصفر - يتم البحث عن هذه الصورة في الشاشة
        '''
        ripe_crop = np.array([
            [0, 255, 255, 255, 0],
            [255, 255, 255, 255, 255],
            [255, 255, 255, 255, 255],
            [255, 255, 255, 255, 255],
            [0, 255, 255, 255, 0]
        ], dtype=np.uint8)
        
        hsv_crop = cv2.cvtColor(cv2.cvtColor(ripe_crop.reshape(5, 5, 1), cv2.COLOR_GRAY2BGR), cv2.COLOR_BGR2HSV)
        return hsv_crop
    
    @staticmethod
    def get_empty_field_template():
        '''
الحقل الفارغ البني - يتم البحث عن هذه الصورة في الشاشة
        '''
        empty_field = np.array([
            [150, 140, 150],
            [140, 130, 140],
            [150, 140, 150]
        ], dtype=np.uint8)
        
        return empty_field
    
    @staticmethod
    def get_harvest_tool_template():
        '''
أداة الحصاد (المعول) - يتم البحث عن هذه الصورة عند محاولة الحصاد
        '''
        harvest_tool = np.array([
            [0, 200, 200],
            [200, 200, 200],
            [200, 200, 0]
        ], dtype=np.uint8)
        
        return harvest_tool
    
    @staticmethod
    def create_yellow_crop_template(size=30):
        '''
إنشاء قالب محصول أصفر ناضج
        '''
        template = np.zeros((size, size, 3), dtype=np.uint8)
        center = size // 2
        cv2.circle(template, (center, center), center - 2, (0, 255, 255), -1)
        return template
    
    @staticmethod
    def create_brown_field_template(size=30):
        '''
إنشاء قالب حقل بني فارغ
        '''
        template = np.ones((size, size, 3), dtype=np.uint8)
        template[:, :, 0] = 165
        template[:, :, 1] = 100
        template[:, :, 2] = 50
        return template
